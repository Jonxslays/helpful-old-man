import logging
import typing as t

import hikari
import miru
from hikari import PermissionOverwriteType
from hikari import Permissions

from hom import client as _client
from hom.config import Config
from hom.injector import Injector
from hom.models import Ticket
from .embeds import EmbedService

__all__ = ("TicketService",)
logger = logging.getLogger(__name__)


class TicketService:
    __slots__ = ()

    async def create(
        self, ctx: miru.ViewContext, embed: hikari.Embed, view: miru.View, topic: str
    ) -> Ticket:
        """Creates a support ticket for the interaction user or returns
        the existing ticket if one already exists.

        Args:
            ctx: The miru view context.
            embed: The embed to send to the created ticket channel.
            view: The view to send to the created ticket channel.
            topic: The type of ticket (will be added to the channel topic).

        Returns:
            The new or existing ticket.
        """
        client = Injector.get(_client.Client)
        assert ctx.guild_id

        if ticket := await self._get_ticket_for_user(ctx.guild_id, ctx.author.id):
            # Already has an open ticket
            message = f":envelope: View your existing ticket: <#{ticket.channel}>"
            await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)
            return ticket

        # Create the ticket channel
        channel = await client.rest.create_guild_text_channel(
            ctx.guild_id,
            f"{ctx.author.username[:15]}",
            topic=f"{topic}-{ctx.author.id}",
            category=Config.TICKET_CATEGORY,
            reason=f"{ctx.author.username} ({ctx.author.id}) has opened a ticket: {topic}.",
            permission_overwrites=self._create_ticket_overwrites(
                client.application, ctx.author.id, ctx.guild_id
            ),
        )

        # Send the initial message to the ticket
        await ctx.client.rest.create_message(
            channel.id,
            f"Welcome to your support ticket <@{ctx.author.id}>",
            embed=embed,
            components=view,
            user_mentions=True,
        )

        # Give the user a link to the ticket
        await ctx.respond(
            ":envelope: We have created a support ticket for you.\n"
            f"View your new ticket: <#{channel.id}>",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

        return Ticket(ctx.author.id, channel.id, topic, True)

    async def close(self, ctx: miru.ViewContext, view: miru.View) -> None:
        """Closes the ticket channel by removing the owners permissions
        to view it.

        Args:
            ctx: The miru view context.
            view: The view to send when the ticket is successfully closed.
        """
        embeds = Injector.get(EmbedService)
        assert ctx.guild_id

        if not (ticket := await self._get_ticket_for_channel(ctx.guild_id, ctx.channel_id)):
            # The channel topic doesnt have the correct format
            # Expecting: <ticket type>-<user id>
            # Example:   Other-123456789
            embed = embeds.error("Can't determine the original ticket owner.")
            await ctx.respond(embed)
            return None

        if ticket.is_closed():
            await ctx.respond(
                embeds.error("Ticket is already closed."),
                flags=hikari.MessageFlag.EPHEMERAL,
            )

            return None  # No need to close if its already closed

        # Remove the users permissions to the channel
        await self._remove_user_from_ticket(ticket)

        # Send the ticket closed message
        await ctx.respond(embeds.ticket_closed(ctx.author.id), components=view)

    async def archive(self, ctx: miru.ViewContext) -> None:
        print("Archiving tickets is not yet implemented.")

    async def _get_ticket_for_user(
        self, guild_id: hikari.Snowflakeish, user_id: hikari.Snowflake
    ) -> Ticket | None:
        """Gets the ticket for the user, if one exists.

        Args:
            guild_id: The guild id to look in.
            user_id: The user to look for.

        Returns:
            The ticket or none if one was not found.
        """
        async for channel in self._get_ticket_channels(guild_id):
            # If they have user specific permissions on the channel
            if overwrites := channel.permission_overwrites.get(user_id):
                # And those permissions allow them to view it
                if Permissions.VIEW_CHANNEL in overwrites.allow:
                    # This user is the owner of the ticket
                    return Ticket(user_id, channel.id, channel.topic, False)

        return None

    async def _get_ticket_for_channel(
        self, guild_id: hikari.Snowflakeish, channel_id: hikari.Snowflakeish
    ) -> Ticket | None:
        """Gets the ticket for the channel, if one exists.

        Args:
            guild_id: The guild id to look in.
            channel_id: The channel id to look in.

        Returns:
            The ticket or none if one was not found.
        """
        try:
            # Without the channel topic we dont know who the original
            # owner was. We used to fetch message history and find who
            # was mentioned in the first message in the channel but
            # I felt like we were more likely to delete that message on
            # accident than to edit the channel topic on accident.

            async for channel in self._get_ticket_channels(guild_id):
                if channel.id == channel_id:
                    if not channel.topic:
                        raise Exception("Ticket channel topic is missing")

                    # Expecting: <ticket type>-<user id>
                    # Example:   Other-123456789
                    owner_id = channel.topic.split("-")[-1].rstrip("_CLOSED")
                    return Ticket(int(owner_id), channel.id, channel.topic, False)
        except Exception as e:
            logger.error(f"Failed to find ticket owner for channel {channel_id}: {e}")

        return None

    async def _get_ticket_channels(
        self, guild_id: hikari.Snowflakeish
    ) -> t.AsyncIterable[hikari.GuildTextChannel]:
        """Gets the currently active ticket channels.

        Args:
            guild_id: The guild to get channels for.

        Returns:
            An async iterable over the active ticket channels.
        """
        client = Injector.get(_client.Client)
        channels = client.cache.get_guild_channels_view_for_guild(guild_id)
        filtered = self._filter_valid_channels(channels.values())

        # TODO: This caching mechanism is broken
        # but we dont want to always fetch
        # the ratelimit is 10 / minute.
        # someone could spam a support button and ratelimit us

        if not any(filtered):
            logger.info("Fetching ticket channels from the API")
            channels = await client.rest.fetch_guild_channels(guild_id)
            filtered = self._filter_valid_channels(channels)

        for channel in filtered:
            # We are manually caching here to prevent having to fetch
            # a bunch of times in a row
            if not client.app._cache.get_guild_channel(channel):  # type: ignore
                client.app._cache.set_guild_channel(channel)  # type: ignore

            yield channel

    def _filter_valid_channels(
        self, channels: t.Iterable[hikari.GuildChannel]
    ) -> t.Iterable[hikari.GuildTextChannel]:
        for channel in channels:
            if channel.parent_id != Config.TICKET_CATEGORY:
                # Not in the correct category
                continue

            if not isinstance(channel, hikari.GuildTextChannel):
                # Not a text channel
                continue

            yield channel

    async def _remove_user_from_ticket(self, ticket: Ticket) -> None:
        """Removes the users permissions on the ticket channel.

        Args:
            ticket: The ticket to remove the user from.
        """
        client = Injector.get(_client.Client)
        perms = self._create_member_overwrite(ticket.user, deny=Permissions.VIEW_CHANNEL)

        await client.rest.edit_channel(
            ticket.channel,
            reason=f"Ticket closed for user: {ticket.description}",
            topic=f"{ticket.description}_CLOSED",
            permission_overwrites=(perms,),
        )

    def _create_ticket_overwrites(
        self,
        application: hikari.Application | None,
        user_id: hikari.Snowflakeish,
        guild_id: hikari.Snowflakeish,
    ) -> tuple[hikari.PermissionOverwrite, ...]:
        """Creates permissions overwrites for a new support ticket.

        Args:
            application: The hikari application for giving the bot perms.
            user_id : The user owning the ticket.
            guild_id : The guild the ticket is in.

        Returns:
            A tuple containing the necessary overwrites.
        """
        assert application

        mod_perms = self._create_role_overwrite(Config.MOD_ROLE, allow=Permissions.VIEW_CHANNEL)
        hom_perms = self._create_member_overwrite(application.id, allow=Permissions.VIEW_CHANNEL)
        author_perms = self._create_member_overwrite(user_id, allow=Permissions.VIEW_CHANNEL)
        everyone_perms = self._create_role_overwrite(
            guild_id,
            deny=Permissions.VIEW_CHANNEL,
            allow=Permissions.READ_MESSAGE_HISTORY
            | Permissions.ATTACH_FILES
            | Permissions.ADD_REACTIONS
            | Permissions.EMBED_LINKS,
        )

        return (mod_perms, hom_perms, author_perms, everyone_perms)

    def _create_role_overwrite(
        self,
        role_id: hikari.Snowflakeish,
        *,
        allow: hikari.Permissions | None = None,
        deny: hikari.Permissions | None = None,
    ) -> hikari.PermissionOverwrite:
        """Creates a new permission overwrite for a role.

        Args:
            role_id: The ID of the role for the overwrite.
            allow : Permissions to allow. Defaults to None.
            deny : Permissions to deny. Defaults to None.

        Returns:
            The requested permission overwrite.
        """
        return self._create_overwrite(
            role_id, PermissionOverwriteType.ROLE, allow=allow, deny=deny
        )

    def _create_member_overwrite(
        self,
        member_id: hikari.Snowflakeish,
        *,
        allow: hikari.Permissions | None = None,
        deny: hikari.Permissions | None = None,
    ) -> hikari.PermissionOverwrite:
        """Creates a new permission overwrite for a member.

        Args:
            member_id: The ID of the member for the overwrite.
            allow : Permissions to allow. Defaults to None.
            deny : Permissions to deny. Defaults to None.

        Returns:
            The requested permission overwrite.
        """
        return self._create_overwrite(
            member_id, PermissionOverwriteType.MEMBER, allow=allow, deny=deny
        )

    def _create_overwrite(
        self,
        id_: hikari.Snowflakeish,
        type_: PermissionOverwriteType,
        *,
        allow: hikari.Permissions | None = None,
        deny: hikari.Permissions | None = None,
    ) -> hikari.PermissionOverwrite:
        """Creates a new permission overwrite.

        Args:
            id_: The ID of the entity for the overwrite.
            type_: The type of permission overwrite.
            allow : Permissions to allow. Defaults to None.
            deny : Permissions to deny. Defaults to None.

        Returns:
            The requested permission overwrite.
        """
        overwrite = hikari.PermissionOverwrite(id=id_, type=type_)

        if allow:
            overwrite.allow = allow

        if deny:
            overwrite.deny = deny

        return overwrite
