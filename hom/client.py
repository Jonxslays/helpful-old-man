import logging
import sys
import typing as t
from logging import handlers

import arc
import hikari
import miru

from hom import services
from hom import views
from hom.config import Config
from hom.injector import Injector

__all__ = ("Context", "Client", "Plugin")

Context = arc.Context["Client"]
Plugin = arc.GatewayPluginBase["Client"]
T = t.TypeVar("T")


class Client(arc.GatewayClientBase[hikari.GatewayBot]):
    """A helpful wrapper around the arc gateway client."""

    __slots__ = ("create_message", "start_view")

    def __init__(self) -> None:
        bot = hikari.GatewayBot(
            Config.DISCORD_TOKEN,
            intents=hikari.Intents.GUILD_MESSAGES | hikari.Intents.GUILDS,
        )

        super().__init__(bot, is_dm_enabled=False)
        self._initialize(bot, miru.Client(bot))

    @classmethod
    def run(cls) -> None:
        """Runs the client. **NOTE**: This is a blocking method."""
        name = f"<#{Config.SUPPORT_CHANNEL}>"
        activity_type = hikari.ActivityType.WATCHING
        activity = hikari.Activity(name=name, type=activity_type)
        cls().get_type_dependency(hikari.GatewayBot).run(
            status=hikari.Status.IDLE, activity=activity
        )

    async def _startup_handler(self) -> None:
        """Runs after the bot has started up and commands are synced."""
        self.start_view(views.Archive(), bind_to=None)
        self.start_view(views.Names(), bind_to=None)
        self.start_view(views.Groups(), bind_to=None)
        self.start_view(views.Support(), bind_to=None)
        self.start_view(views.Ticket(), bind_to=None)

    def _initialize(self, bot: hikari.GatewayBot, miru_client: miru.Client) -> None:
        """Initialize all required client attributes and configuration."""

        # Ensure all environment variables exist
        if not Config.validate():
            sys.exit(1)

        # Configure logging
        self._configure_logging()

        # Set up dependency injection
        self._set_type_dependencies(bot, miru_client)

        # Load the client extensions and set startup hook
        self.load_extensions_from("hom/extensions")
        self.set_startup_hook(Client._startup_handler)

        # Shortcut methods
        self.create_message = self.rest.create_message
        self.start_view = miru_client.start_view

    def _set_type_dependencies(self, bot: hikari.GatewayBot, miru_client: miru.Client) -> None:
        """Sets the instances associated with the given types for use in
        dependency injection.

        Args:
            bot: The gateway bot instance.
            miru_client: The miru client instance.
        """
        (
            Injector.initialize(self.get_type_dependency, self.set_type_dependency)
            .set(hikari.GatewayBot, bot)
            .set(miru.Client, miru_client)
            .set(services.ArchiveService, services.ArchiveService())
            .set(services.EmbedService, services.EmbedService())
            .set(services.ModLogService, services.ModLogService())
            .set(services.TemplateService, services.TemplateService())
            .set(services.TicketService, services.TicketService())
        )

    def _configure_logging(self) -> None:
        """Configures logging for the client."""
        logger = logging.getLogger("root")
        logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)

        handler = handlers.RotatingFileHandler(
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
