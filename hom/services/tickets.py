import hikari
import miru
from hikari import PermissionOverwriteType
from hikari import Permissions

from hom import client as _client
from hom.config import Config
from hom.injector import Injector
from hom.models import Ticket

__all__ = ("TicketService",)


class TicketService:
    __slots__ = ()

    async def create(
        self, ctx: miru.ViewContext, embed: hikari.Embed, view: miru.View, topic: str
    ) -> Ticket:
        """Creates a support ticket for the interaction user or returns
        the existing ticket if one already exists.

        Returns:
            The new or existing ticket.
        """
        client = Injector.get(_client.Client)
        assert ctx.guild_id

        if ticket := self.get_ticket(ctx.guild_id, ctx.author.id):
            # Already has an open ticket
            message = f":envelope: View your existing ticket: <#{ticket.channel}>"
            await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)
            return ticket

        channel = await client.rest.create_guild_text_channel(
            ctx.guild_id,
            f"{ctx.author.username[:15]}",
            topic=topic,
            category=Config.TICKET_CATEGORY,
            reason=f"{ctx.author.username} ({ctx.author.id}) has opened a ticket: {topic}.",
            permission_overwrites=self._create_ticket_overwrites(
                client.application, ctx.author.id, ctx.guild_id
            ),
        )

        await ctx.client.rest.create_message(
            channel.id,
            f"Welcome to your support ticket <@{ctx.author.id}>",
            embed=embed,
            components=view,
            user_mentions=True,
        )

        await ctx.respond(
            ":envelope: We have created a support ticket for you.\n"
            f"View your new ticket: <#{channel.id}>",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

        return Ticket(ctx.author.id, channel.id, topic, True)

    async def close(self, ctx: miru.ViewContext) -> None:
        client = Injector.get(_client.Client)

        message = await client.rest.fetch_messages(ctx.channel_id).last()
        channel = await client.rest.fetch_channel(message.channel_id)
        assert isinstance(channel, hikari.GuildTextChannel)

        if message.user_mentions_ids:
            reason = f"Ticket closed for user {ctx.author.username} ({ctx.author.id})"
            await client.rest.edit_channel(
                channel.id,
                reason=f"{reason}: {channel.topic}",
                permission_overwrites=(
                    hikari.PermissionOverwrite(
                        id=message.user_mentions_ids[0],
                        type=PermissionOverwriteType.MEMBER,
                        deny=Permissions.VIEW_CHANNEL,
                    ),
                ),
            )

        # TODO: Respond in the ticket channel here with the delete ticket button

    def get_ticket(
        self, guild_id: hikari.Snowflakeish, user_id: hikari.Snowflake
    ) -> Ticket | None:
        client = Injector.get(_client.Client)
        channels = client.cache.get_guild_channels_view_for_guild(guild_id)
        tickets = [c for c in channels.values() if c.parent_id == Config.TICKET_CATEGORY]

        for ticket in tickets:
            if not isinstance(ticket, hikari.GuildTextChannel):
                continue

            if overwrites := ticket.permission_overwrites.get(user_id):
                if Permissions.VIEW_CHANNEL in overwrites.allow:
                    return Ticket(user_id, ticket.id, ticket.topic, False)

        return None

    def _create_ticket_overwrites(
        self,
        application: hikari.Application | None,
        user_id: hikari.Snowflakeish,
        guild_id: hikari.Snowflakeish,
    ) -> tuple[hikari.PermissionOverwrite, ...]:
        assert application

        return (
            hikari.PermissionOverwrite(
                id=Config.MOD_ROLE,
                type=PermissionOverwriteType.ROLE,
                allow=Permissions.VIEW_CHANNEL,
            ),
            hikari.PermissionOverwrite(
                id=application.id,
                type=PermissionOverwriteType.MEMBER,
                allow=Permissions.VIEW_CHANNEL,
            ),
            hikari.PermissionOverwrite(
                id=user_id,
                type=PermissionOverwriteType.MEMBER,
                allow=Permissions.VIEW_CHANNEL,
            ),
            hikari.PermissionOverwrite(
                id=guild_id,
                type=PermissionOverwriteType.ROLE,
                deny=Permissions.VIEW_CHANNEL,
                allow=Permissions.READ_MESSAGE_HISTORY
                | Permissions.ATTACH_FILES
                | Permissions.ADD_REACTIONS
                | Permissions.EMBED_LINKS,
            ),
        )
