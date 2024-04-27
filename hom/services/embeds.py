import typing as t

import arc
import hikari

from hom.injector import Injector
from hom.models import TemplateSection
from .templates import TemplateService

__all__ = ("EmbedService",)

INFO = 0x206694
ERROR = 0xFF2B1C
SUCCESS = 0x27E65A


class EmbedService:
    __slots__ = ()

    def create(
        self,
        title: str,
        message: str,
        color: hikari.Colorish | None = None,
        footer: str | None = None,
    ) -> hikari.Embed:
        embed = hikari.Embed(title=title, description=message, color=color)

        if footer:
            embed.set_footer(footer)

        return embed

    def error(self, message: str) -> hikari.Embed:
        return self.create("Error", message, ERROR)

    def info(self, message: str) -> hikari.Embed:
        return self.create("Info", message, INFO)

    def success(self, message: str) -> hikari.Embed:
        return self.create("Success", message, SUCCESS)

    def support(self) -> hikari.Embed:
        """Gets the embed for use with the Support view.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)

        title = "Need help from one of our moderators?"
        body = templates.get_support_template()
        footer = templates.get_template(TemplateSection.Reminder)

        return self.create(title, body.content, INFO, footer.content)

    def other(self) -> hikari.Embed:
        """Gets the embed for use with the Other view.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)

        title = "Other"
        body = templates.get_other_template()
        footer = templates.get_template(TemplateSection.Private)

        return self.create(title, body.content, INFO, footer.content)

    def api_key(self) -> hikari.Embed:
        """Gets the embed for use with the ApiKey view.

        Returns:
            The embed with the template populated.
        """
        templates = Injector.get(TemplateService)

        title = "API Key"
        body = templates.get_api_key_template()
        footer = templates.get_template(TemplateSection.Private)

        return self.create(title, body.content, INFO, footer.content)

    async def send(
        self,
        ctx: arc.Context[t.Any],
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
        ctx: arc.Context[t.Any],
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
            reference: The optional reference string to place in the footer.
        """
        await self.send(ctx, "Error", message, ERROR, ephemeral, footer)

    async def send_info(
        self, ctx: arc.Context[t.Any], message: str, ephemeral: bool = False
    ) -> None:
        """Sends an info embed to the contexts channel.

        Args:
            ctx: The context to respond to.
            message: The message to send.
            ephemeral: Whether the message should be ephemeral. Defaults to False.
        """
        await self.send(ctx, "Info", message, INFO, ephemeral)
