import arc
import hikari

from hom.client import Client
from hom.models import TemplateSection

__all__ = ("Embeds",)


class Embeds:
    @classmethod
    def create(cls, title: str, message: str, color: hikari.Colorish) -> hikari.Embed:
        return hikari.Embed(title=title, description=message, color=color)

    @classmethod
    def error(cls, message: str) -> hikari.Embed:
        return cls.create("Error", message, 0xFF2B1C)

    @classmethod
    def info(cls, message: str) -> hikari.Embed:
        return cls.create("Info", message, 0x206694)

    @classmethod
    def success(cls, message: str) -> hikari.Embed:
        return cls.create("Success", message, 0x27E65A)

    @classmethod
    def support(cls, client: Client, title: str, message: str) -> hikari.Embed:
        embed = hikari.Embed(title=title, description=message, color=0x206694)
        embed.set_footer(client.get_support_template(TemplateSection.Footer))
        return embed

    @classmethod
    async def send(
        cls,
        ctx: arc.Context[Client],
        title: str,
        message: str,
        color: hikari.Colorish,
        ephemeral: bool = False,
    ) -> None:
        """Sends an embed to the contexts channel.

        Args:
            ctx: The context to respond to.
            title: The title of the embed.
            message: The message to send.
            color: The color for the embed sidebar.
            ephemeral: Whether the message should be ephemeral. Defaults to False.
        """
        await ctx.respond(
            cls.create(title, message, color),
            flags=hikari.MessageFlag.EPHEMERAL if ephemeral else hikari.UNDEFINED,
        )

    @classmethod
    async def send_error(
        cls, ctx: arc.Context[Client], message: str, ephemeral: bool = False
    ) -> None:
        """Sends an error embed to the contexts channel.

        Args:
            ctx: The context to respond to.
            message: The message to send.
            ephemeral: Whether the message should be ephemeral. Defaults to False.
        """
        await cls.send(ctx, "Error", message, 0xFF2B1C, ephemeral)

    @classmethod
    async def send_info(
        cls, ctx: arc.Context[Client], message: str, ephemeral: bool = False
    ) -> None:
        """Sends an info embed to the contexts channel.

        Args:
            ctx: The context to respond to.
            message: The message to send.
            ephemeral: Whether the message should be ephemeral. Defaults to False.
        """
        await cls.send(ctx, "Info", message, 0x0E6FED, ephemeral)
