# import typing as t
import datetime
import io

# import arc
import hikari
import miru

from hom.config import Config
from hom.injector import Injector

# from hom.models import TemplateSection
from .templates import TemplateService

__all__ = ("ArchiveService",)


class ArchiveService:
    """Handles the archival of support tickets."""

    __slots__ = ()

    async def archive_ticket(self, ctx: miru.ViewContext) -> None:
        data = io.BytesIO()

        ## Accumulate the contents of each message (including embeds) as bytes
        async for message in ctx.client.rest.fetch_messages(ctx.channel_id).reversed():
            data.write(self._get_message_bytes(message))

        # Convert the bytes to a file and send it to the mod log channel
        await ctx.client.rest.create_message(
            Config.MOD_LOG_CHANNEL,
            attachment=self._get_attachment(ctx.author, data),
        )

    def _get_embed_summary(self, embed: hikari.Embed) -> str:
        return f"\nEmbed title: {embed.title}\nEmbed description:\n{embed.description}"

    def _get_message_bytes(self, message: hikari.Message) -> bytes:
        templates = Injector.get(TemplateService)

        author = f"{message.author.username} ({message.author.id})"
        timestamp = f"{message.created_at.strftime('%Y-%m-%d %I:%M %p')}"
        content = f"{message.content or ''}\n"

        if message.embeds:
            content += "Embeds:\n"

            for embed in message.embeds:
                content += self._get_embed_summary(embed)

        template = templates.get_log_message_template(author, timestamp, content)
        return template.content.encode()

    def _get_attachment(self, author: hikari.User, data: io.BytesIO) -> hikari.Bytes:
        data.seek(0)

        username = author.username.replace(" ", "-")
        timestamp = (
            datetime.datetime.now(tz=datetime.timezone.utc)
            .isoformat()
            .replace(":", "-")
            .split(".")[0]
        )

        return hikari.Bytes(data.read(), f"{username}-{timestamp}.txt")
