import logging
import typing as t
from logging.handlers import RotatingFileHandler

import arc
import hikari

from hom.config import Config

T = t.TypeVar("T", bound="Hom")
Context = arc.Context[T]
Plugin = arc.GatewayPluginBase[T]


class Hom(arc.GatewayClient):
    def __init__(self) -> None:
        self.__bot = hikari.GatewayBot(
            Config.DISCORD_TOKEN, intents=hikari.Intents.MESSAGE_CONTENT
        )

        super().__init__(self.__bot, is_dm_enabled=False)

        # Configure logging
        self.configure_logging()

        # Load the bots extensions
        self.load_extensions_from("hom/extensions")

    def run(self) -> None:
        activity = hikari.Activity(name="#support", type=hikari.ActivityType.WATCHING)
        self.__bot.run(status=hikari.Status.IDLE, activity=activity)

    def get_bot(self) -> hikari.GatewayBot:
        return self.__bot

    def configure_logging(self) -> None:
        logger = logging.getLogger("root")
        logger.setLevel(logging.INFO)

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
