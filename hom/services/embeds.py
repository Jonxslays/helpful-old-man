import typing as t

import arc
import hikari
import miru

from hom.config import Images
from hom.injector import Injector
from hom.models import Template
from hom.models import TemplateSection
from .templates import TemplateService

__all__ = ("EmbedService",)

INFO = 0x206694
ERROR = 0xFF2B1C
SUCCESS = 0x27E65A


class EmbedService:
    """Useful methods for working with discord embeds."""

    __slots__ = ()

    def create(
        self,
        title: str,
        message: str,
        color: hikari.Colorish | None = None,
        footer: str | None = None,
    ) -> hikari.Embed:
        """Creates a new embed.

        Args:
            title: The embed title.
            message: The message for the description.
            color: The embed color. Defaults to `None`.
            footer: The embed footer. Defaults to `None`.

        Returns:
            The requested embed.
        """
        embed = hikari.Embed(title=title, description=message, color=color)

        if footer:
            embed.set_footer(footer)

        return embed

    def ticket_opened(
        self,
        title: str,
        body: Template,
        footer_section: TemplateSection = TemplateSection.Private,
    ) -> hikari.Embed:
        """Gets an embed for a newly opened ticket.

        Args:
            title: The title of of the ticket.
            body: The template to be used in the body of the embed.
            footer_section: The section to display in the footer.
                Defaults to `TemplateSection.Private`.

        Returns:
            hikari.Embed: _description_
        """
        templates = Injector.get(TemplateService)
        footer = templates.get_template(footer_section)
        return self.create(title, body.content, INFO, footer.content)

    def error(self, message: str) -> hikari.Embed:
        """Gets an error embed (red border).

        Args:
            message: The message to include in the description.

        Returns:
            The requested embed.
        """
        return self.create("Error", message, ERROR)

    def info(self, message: str) -> hikari.Embed:
        """Gets an info embed (blue border).

        Args:
            message: The message to include in the description.

        Returns:
            The requested embed.
        """
        return self.create("Info", message, INFO)

    def success(self, message: str) -> hikari.Embed:
        """Gets a success embed (green border).

        Args:
            message: The message to include in the description.

        Returns:
            The requested embed.
        """
        return self.create("Success", message, SUCCESS)

    def ticket_closed(self, user_id: hikari.Snowflakeish) -> hikari.Embed:
        """Gets the embed for use when a ticket is closed.

        Args:
            user_id: The ID of the user who closed the ticket.

        Returns:
            The requested embed.
        """
        body = f"<@{user_id}> ({user_id}) has closed the ticket."
        return self.create("Ticket closed", body, ERROR)

    def support(self) -> hikari.Embed:
        """Gets the embed for use in the support channel.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_support_template()
        title = "Need help from one of our moderators?"
        return self.ticket_opened(title, template, TemplateSection.Reminder)

    def other(self) -> hikari.Embed:
        """Gets the embed for use with the "Other" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_other_template()
        return self.ticket_opened("Other", template)

    def api_key(self) -> hikari.Embed:
        """Gets the embed for use with the "API key" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_api_key_template()
        return self.ticket_opened("API key", template)

    def patreon(self) -> hikari.Embed:
        """Gets the embed for use with the "Patreon" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_patreon_template()
        return self.ticket_opened("Patreon", template)

    def verify_group(self) -> hikari.Embed:
        """Gets the embed for use with the "Verify group" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_verify_group_template()
        title = "Groups → Verify my group"
        return self.ticket_opened(title, template).set_image(Images.GROUP)

    def reset_group_code(self) -> hikari.Embed:
        """Gets the embed for use with the "Reset group verification" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_reset_group_verification_template()
        title = "Groups → Reset my group verification code"
        return self.ticket_opened(title, template).set_image(Images.GROUP)

    def remove_from_group(self) -> hikari.Embed:
        """Gets the embed for use with the "Remove from group" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_remove_from_group_template()
        title = "Groups → Remove me from a group"
        return self.ticket_opened(title, template).set_image(Images.PLAYER)

    def approve_name_change(self) -> hikari.Embed:
        """Gets the embed for use with the "Approve name change" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_approve_name_change_template()
        title = "Names → Approve a pending name change"
        return self.ticket_opened(title, template)

    def delete_name_changes(self) -> hikari.Embed:
        """Gets the embed for use with the "Delete name changes" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_delete_name_changes_template()
        title = "Names → Delete my name change history"
        return self.ticket_opened(title, template).set_image(Images.PLAYER)

    def review_name_change(self) -> hikari.Embed:
        """Gets the embed for use with the "Review name change" ticket.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)
        template = templates.get_review_name_change_template()
        title = "Names → Review a denied name change"
        return self.ticket_opened(title, template)

    async def send(
        self,
        ctx: arc.Context[t.Any] | miru.ViewContext,
        title: str,
        message: str,
        color: hikari.Colorish,
        ephemeral: bool = False,
        footer: str | None = None,
    ) -> None:
        """Sends an embed to the contexts channel.

        Args:
            ctx: The context to respond to.
            title: The title of the embed.
            message: The message to send.
            color: The color for the embed sidebar.
            ephemeral: Whether the message should be ephemeral. Defaults to False.
            footer: The optional footer message.
        """
        await ctx.respond(
            self.create(title, message, color, footer),
            flags=hikari.MessageFlag.EPHEMERAL if ephemeral else hikari.UNDEFINED,
        )

    async def send_error(
        self,
        ctx: arc.Context[t.Any] | miru.ViewContext,
        message: str,
        *,
        ephemeral: bool = False,
        footer: str | None = None,
    ) -> None:
        """Sends an error embed to the contexts channel.

        Args:
            ctx: The context to respond to.
            message: The message to send.
            ephemeral: Whether the message should be ephemeral. Defaults to False.
            footer: The optional footer.
        """
        await self.send(ctx, "Error", message, ERROR, ephemeral, footer)

    async def send_info(
        self, ctx: arc.Context[t.Any] | miru.ViewContext, message: str, ephemeral: bool = False
    ) -> None:
        """Sends an info embed to the contexts channel.

        Args:
            ctx: The context to respond to.
            message: The message to send.
            ephemeral: Whether the message should be ephemeral. Defaults to False.
        """
        await self.send(ctx, "Info", message, INFO, ephemeral)
