import typing as t

import arc
import hikari

from hom.models import Template

__all__ = ("EmbedService",)


class EmbedService:
    def create(
        self, title: str, message: str, color: hikari.Colorish, footer: str | None = None
    ) -> hikari.Embed:
        embed = hikari.Embed(title=title, description=message, color=color)

        if footer:
            embed.set_footer(footer)

        return embed

    def error(self, message: str) -> hikari.Embed:
        return self.create("Error", message, 0xFF2B1C)

    def info(self, message: str) -> hikari.Embed:
        return self.create("Info", message, 0x206694)

    def success(self, message: str) -> hikari.Embed:
        return self.create("Success", message, 0x27E65A)

    def support(self, body: Template, footer: Template) -> hikari.Embed:
        title = "Need help from one of our moderators?"
        return self.create(title, body.content, 0x206694, footer.content)

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
        await self.send(ctx, "Error", message, 0xFF2B1C, ephemeral, footer)

    async def send_info(
        self, ctx: arc.Context[t.Any], message: str, ephemeral: bool = False
    ) -> None:
        """Sends an info embed to the contexts channel.

        Args:
            ctx: The context to respond to.
            message: The message to send.
            ephemeral: Whether the message should be ephemeral. Defaults to False.
        """
        await self.send(ctx, "Info", message, 0x0E6FED, ephemeral)
