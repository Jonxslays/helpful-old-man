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

        # Only mods can run commands
        self.add_hook(self.mods_only)

        # Load the bots extensions
        self.load_extensions_from("hom/extensions")

        # Set the global error handler
        self.subscribe(arc.CommandErrorEvent, self.on_command_error)

    def run(self) -> None:
        activity = hikari.Activity(name="#support", type=hikari.ActivityType.WATCHING)
        self.__bot.run(status=hikari.Status.IDLE, activity=activity)

    def get_bot(self) -> hikari.GatewayBot:
        return self.__bot

    async def on_command_error(self, event: arc.CommandErrorEvent[t.Self]) -> None:
        if isinstance(event.exception, (arc.UnderCooldownError, arc.MaxConcurrencyReachedError)):
            await event.context.respond(
                "Someone just used this command, wait a couple seconds.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )

            return None

        await event.context.respond(
            "An unhandled exception occurred during the command, check the logs."
        )

        raise event.exception

    async def mods_only(self, ctx: Context[t.Self]) -> arc.HookResult:
        assert ctx.member  # Safe because dm commands are disabled.

        if Config.MOD_ROLE in ctx.member.role_ids:
            return arc.HookResult()

        await ctx.respond(
            "You are not allowed to do that.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

        return arc.HookResult(abort=True)

    def configure_logging(self) -> None:
        log = logging.getLogger("root")
        log.setLevel(logging.INFO)

        rfh = RotatingFileHandler(
            "./hom/logs/main.log",
            maxBytes=521288,  # 512KB
            encoding="utf-8",
            backupCount=10,
        )

        ff = logging.Formatter(
            "%(levelname)-1.1s "  # Logging level
            "%(asctime)23.23s "  # Date and time
            "%(name)s: "  # Logger name
            "%(message)s"  # Message
        )

        rfh.setFormatter(ff)
        log.addHandler(rfh)
