import logging
import sys
import typing as t
from logging.handlers import RotatingFileHandler

import arc
import hikari

from hom.config import Config

# from hom.config import Config2
from hom import models

__all__ = ("Context", "Client", "Plugin")

T = t.TypeVar("T", bound="Client")
Context = arc.Context[T]
Plugin = arc.GatewayPluginBase[T]


class Client(arc.GatewayClient):
    """A helpful wrapper around the arc gateway client."""

    __slots__ = ("_bot", "_support_messages")

    def __init__(self) -> None:
        self._support_messages: dict[str, str] = {}

        # Instantiate the gateway bot
        self._bot = hikari.GatewayBot(
            Config.DISCORD_TOKEN,
            intents=hikari.Intents.MESSAGE_CONTENT,
        )

        # Instantiate the gateway client
        super().__init__(self._bot, is_dm_enabled=False)

        # Ensure all environment variables exist
        if not Config.validate():
            sys.exit(1)

        # Configure logging
        self.configure_logging()

        # Load the client extensions
        self.load_extensions_from("hom/extensions")

    @property
    def bot(self) -> hikari.GatewayBot:
        """The gateway bot instance this client is using."""
        return self._bot

    @classmethod
    def run(cls) -> None:
        """Runs the client. **NOTE**: This is a blocking function."""
        name = f"<#{Config.SUPPORT_CHANNEL}>"
        activity_type = hikari.ActivityType.WATCHING
        activity = hikari.Activity(name=name, type=activity_type)
        cls()._bot.run(status=hikari.Status.IDLE, activity=activity)

    def configure_logging(self) -> None:
        """Configures logging for the client."""
        logger = logging.getLogger("root")
        print(Config.DEBUG)
        logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)

        handler = RotatingFileHandler(
            "./hom/logs/main.log",
            maxBytes=521288,  # 512KB
            encoding="utf-8",
            backupCount=10,
        )

        formatter = logging.Formatter(
            "%(levelname)-1.1s "  # Logging level
            "%(asctime)23.23s "  # Date and time
            "%(name)s: "  # Logger name
            "%(message)s"  # Message
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def add_support_message(self, name: str, content: str) -> None:
        """Adds a support message to the client.

        Args:
            name (`str`): The name of the message.
            content (`str`): The message content.
        """
        self._support_messages[name] = content

    def get_support_message(
        self, message_type: models.SupportCategory | models.SupportType | None = None
    ) -> str:
        name = message_type.name.lower() if message_type else "support"
        return self._support_messages[name]
