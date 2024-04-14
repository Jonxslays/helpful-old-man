import logging
import sys

# import typing as t
from logging.handlers import RotatingFileHandler

import arc
import hikari
import miru

from hom.config import Config
from hom import services
from hom import views

__all__ = ("Context", "Client", "Plugin")

# ClientT = t.TypeVar("ClientT", bound="Client")
Context = arc.Context["Client"]
Plugin = arc.GatewayPluginBase["Client"]


class Client(arc.GatewayClient):
    """A helpful wrapper around the arc gateway client."""

    __slots__ = (
        "_bot",
        "_views",
        "_dependencies_injected",
        "create_message",
        "start_view",
    )

    def __init__(self) -> None:
        self._dependencies_injected = False

        # Instantiate the gateway bot
        self._bot = hikari.GatewayBot(
            Config.DISCORD_TOKEN,
            intents=hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILD_MESSAGES,
        )

        # Instantiate the gateway client
        super().__init__(self._bot, is_dm_enabled=False)

        # Instantiate the miru client
        self._views = miru.Client(self._bot)

        # Initialize remaining dependencies
        self._initialize()

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
        """Runs the client. **NOTE**: This is a blocking method."""
        name = f"<#{Config.SUPPORT_CHANNEL}>"
        activity_type = hikari.ActivityType.WATCHING
        activity = hikari.Activity(name=name, type=activity_type)
        cls()._bot.run(status=hikari.Status.IDLE, activity=activity)

    def _initialize(self) -> None:
        """Initialize all required client attributes and configuration."""

        # Ensure all environment variables exist
        if not Config.validate():
            sys.exit(1)

        # Configure logging
        self._configure_logging()

        # Set up dependency injection
        self._set_type_dependencies()

        # Load the client extensions and set startup hook
        self.load_extensions_from("hom/extensions")
        self.set_startup_hook(Client._startup_handler)

        # Shortcut methods
        self.create_message = self.rest.create_message
        self.start_view = self.views.start_view

    def _set_type_dependencies(self) -> None:
        templates = services.TemplateService()
        embeds = services.EmbedService()

        self.set_type_dependency(services.EmbedService, embeds)
        self.set_type_dependency(services.TemplateService, templates)

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

    async def _startup_handler(self) -> None:
        """Runs after the bot has started up and commands are synced."""
        self.start_view(views.Support(), bind_to=None)
