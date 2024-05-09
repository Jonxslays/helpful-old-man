# import typing as t
import datetime
import io
import zipfile

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
        """Archives the ticket channel this context originated from.

        Args:
            ctx: The view context.
        """
        attachments: list[hikari.Attachment] = []
        data = io.BytesIO()

        ## Accumulate the contents/embed contents of each message
        async for message in ctx.client.rest.fetch_messages(ctx.channel_id).reversed():
            # Get the bytes for the message content
            data.write(self._get_message_bytes(message))

            # Store this messages attachments for use later
            attachments.extend(message.attachments)

        await self._send_initial_attachment(ctx, data)
        await self._send_additional_attachments(ctx, attachments, data)

    def _get_embed_summary(self, embed: hikari.Embed) -> str:
        """Gets a simple summary for the embed.

        Args:
            embed: The embed to summarize.

        Returns:
            The summary.
        """
        return f"\nEmbed title: {embed.title}\nEmbed description:\n{embed.description}"

    async def _send_initial_attachment(self, ctx: miru.ViewContext, data: io.BytesIO) -> None:
        """Sends the attachment with info about the message content and
        embeds to the mod log channel.

        Args:
            ctx: The view context.
            data: The buffer to send.
        """

        # Clear the buffer
        data.flush()
        data.seek(0)

        # Send it
        await ctx.client.rest.create_message(
            Config.MOD_LOG_CHANNEL, attachment=self._get_attachment(ctx.author, data)
        )

    async def _send_additional_attachments(
        self, ctx: miru.ViewContext, attachments: list[hikari.Attachment], data: io.BytesIO
    ) -> None:
        """Compresses and sends the additional attachments that were
        attached to messages in the ticket channel to the mod log
        channel.

        WARNING: This method mutates the data buffer.

        Args:
            ctx: The view context.
            attachments: The attachments to send.
            data: The buffer to clear and fill with attachment data.
        """
        if not attachments:
            return None

        # Clear the buffer
        data.flush()
        data.seek(0)

        # Compress the attachments into a single zip
        with zipfile.ZipFile(data, mode="w") as f:
            for i, attachment in enumerate(attachments):
                buffer = io.BytesIO(await attachment.read())
                f.writestr(f"{i}-{attachment.filename}", buffer.getvalue())

        # Send it
        await ctx.client.rest.create_message(
            Config.MOD_LOG_CHANNEL,
            attachment=self._get_attachment(ctx.author, data, "zip", "attachments"),
        )

    def _get_message_bytes(self, message: hikari.Message) -> bytes:
        """Gets the contents of the message as bytes.

        Args:
            message: The message.

        Returns:
            The contents as bytes.
        """
        templates = Injector.get(TemplateService)

        author = f"{message.author.username} ({message.author.id})"
        timestamp = f"{message.created_at.strftime('%Y-%m-%d %I:%M %p')}"
        content = f"{message.content or ''}\n"

        if message.attachments:
            content += "\nAttachments:\n"
            content += "\n".join(a.filename for a in message.attachments)

        if message.embeds:
            content += "\nEmbeds:\n"

            for embed in message.embeds:
                content += self._get_embed_summary(embed)

        template = templates.get_log_message_template(author, timestamp, content.strip())
        return template.content.encode()

    def _get_attachment(
        self, author: hikari.User, data: io.BytesIO, ext: str = "txt", prefix: str = ""
    ) -> hikari.Bytes:
        """Gets a hikari bytes object for uploading as an attachment.

        Args:
            author: The author who uploaded the attachment.
            data: The buffer containing the attachments bytes.
            ext: The file extension. Defaults to "txt".
            prefix: The file prefix. Defaults to "".

        Returns:
            The bytes for the attachment.
        """
        data.seek(0)

        username = author.username.replace(" ", "-")
        timestamp = (
            datetime.datetime.now(tz=datetime.timezone.utc)
            .isoformat()
            .replace(":", "-")
            .split(".")[0]
        )

        prefix = f"{prefix + '-' if prefix else prefix}"
        filename = f"{prefix}{username}-{timestamp}.{ext}"
        return hikari.Bytes(data, filename)
