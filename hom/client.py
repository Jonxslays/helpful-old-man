import logging
import sys
import typing as t
from logging.handlers import RotatingFileHandler

import arc
import hikari
import miru

from hom.config import Config
from hom import models

__all__ = ("Context", "Client", "ClientT", "Plugin")

ClientT = t.TypeVar("ClientT", bound="Client")
Context = arc.Context[ClientT]
Plugin = arc.GatewayPluginBase[ClientT]


class Client(arc.GatewayClient):
    """A helpful wrapper around the arc gateway client."""

    __slots__ = ("_bot", "_support_messages", "_views", "create_message", "start_view")

    def __init__(self) -> None:
        self._support_messages: dict[str, str] = {}

        # Instantiate the gateway bot
        self._bot = hikari.GatewayBot(
            Config.DISCORD_TOKEN,
            intents=hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILD_MESSAGES,
        )

        # Instantiate the gateway client
        super().__init__(self._bot, is_dm_enabled=False)

        # Instantiate the miru client
        self._views = miru.Client(self._bot)

        # Ensure all environment variables exist
        if not Config.validate():
            sys.exit(1)

        # Configure logging
        self._configure_logging()

        # Load the client extensions
        self.load_extensions_from("hom/extensions")

        # Shortcut methods
        self.create_message = self.rest.create_message
        self.start_view = self.views.start_view

    @property
    def bot(self) -> hikari.GatewayBot:
        """The gateway bot instance this client is using."""
        return self._bot

    @property
    def views(self) -> miru.Client:
        """The miru client instance being used for component handling."""
        return self._views

    @classmethod
    def run(cls) -> None:
        """Runs the client. **NOTE**: This is a blocking function."""
        name = f"<#{Config.SUPPORT_CHANNEL}>"
        activity_type = hikari.ActivityType.WATCHING
        activity = hikari.Activity(name=name, type=activity_type)
        cls()._bot.run(status=hikari.Status.IDLE, activity=activity)

    def _configure_logging(self) -> None:
        """Configures logging for the client."""
        logger = logging.getLogger("root")
        logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)

        handler = RotatingFileHandler(
            "./hom/logs/main.log",
            maxBytes=524288,  # 512KB
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

    def add_support_template(self, name: str, content: str) -> None:
        """Adds a support template to the client.

        Args:
            name: The name of the template.
            content: The template content.
        """
        self._support_messages[name] = content

    def get_support_template(self, message_type: models.BaseStrEnum | None = None) -> str:
        """Gets the support template for the given message type.

        Args:
            message_type: The template type to get, or the main support template if `None`.

        Returns:
            The support template content.
        """
        name = message_type.name.lower() if message_type else "support"
        return self._support_messages[name]
