import logging
import typing as t
from os import environ

from dotenv import load_dotenv

__all__ = ("Config", "Constants")

load_dotenv()
logger = logging.getLogger(__name__)


class Configuration(type):
    """Metaclass for parsing config values from the environment.

    Environment variables should be in the form of `<type>:<value>`.

    Where `<type>` is the type of the variable, and `<value>` is the
    value itself.
    """

    @classmethod
    def _retrieve(cls, key: str) -> t.Any:
        """Retrieves the key from the environment.

        Args:
            key: The name of the key to retrieve.

        Returns:
            The environment variable converted to the appropriate type.
        """
        t, value = environ[f"HOM_{key}"].split(":", maxsplit=1)

        if t == "bool":
            return bool(int(value))

        return __builtins__[t](value)

    @classmethod
    def __getattr__(cls, key: str) -> t.Any:
        return cls._retrieve(key)

    @classmethod
    def __getitem__(cls, key: str) -> t.Any:
        return cls._retrieve(key)


@t.final
class Config(metaclass=Configuration):
    """Configuration for HOM."""

    DISCORD_TOKEN: str
    """The discord login token."""

    MOD_LOG_CHANNEL: int
    """The channel ID for the mod log channel."""

    MOD_ROLE: int
    """The role ID for the mod role."""

    PATREON_CHANNEL: int
    """The channel ID for the patreon channel."""

    QUESTIONS_CHANNEL: int
    """The channel ID for the general questions channel."""

    SUPPORT_CHANNEL: int
    """The channel ID for the support channel."""

    TICKET_CATEGORY: int
    """The category ID for the support ticket category."""

    DEBUG: bool
    """Whether or not to enable debug logging."""

    def __init__(self) -> None:
        raise RuntimeError("Config should not be instantiated")

    @classmethod
    def validate(cls) -> bool:
        valid = True

        for key in cls.__dict__["__annotations__"].keys():
            if key == "DEBUG":
                # Set debug if it doesnt exist
                if not environ.get("HOM_DEBUG"):
                    environ["HOM_DEBUG"] = "bool:0"
                    continue

            try:
                cls[key]
            except Exception:
                valid = False
                logger.error(f"Required environment variable {key} is missing")

        return valid


@t.final
class Constants:
    __slots__ = ()

    ARROW: t.Final[str] = "→"

    PREFIX: t.Final[str] = "!"

    DENIED: t.Final[str] = "❌"

    COMPLETE: t.Final[str] = "✅"

    FOOTER: t.Final[str] = (
        "As a reminder, all moderators and admins in this "
        "server volunteer to assist in their free time. "
        "We appreciate your patience.\u200b\n\u200b"
    )

    def __init__(self) -> None:
        raise RuntimeError("Constants should not be instantiated")
