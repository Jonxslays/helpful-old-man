import logging
import typing as t
from os import environ

from dotenv import load_dotenv

__all__ = ("Config", "Images")

load_dotenv()
logger = logging.getLogger(__name__)


class InvalidConfigType(Exception):
    """Raised when an invalid type is used in the environment file."""


class MissingConfig(Exception):
    """Raised when the config value is not found in the environment."""


class MissingConfigType(Exception):
    """Raised when the config type is not part of the value."""


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
        try:
            type_, value = environ[f"HOM_{key}"].split(":", maxsplit=1)
        except KeyError:
            raise MissingConfig()
        except ValueError:
            raise MissingConfigType()

        if type_ == "bool":
            return bool(int(value))

        try:
            return __builtins__[type_](value)  # type: ignore[index]
        except KeyError:
            raise InvalidConfigType()

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
        valid: set[str] = set()
        keys: list[str] = cls.__dict__["__annotations__"].keys()

        for key in keys:
            if key == "DEBUG":
                # Set debug if it doesnt exist
                if not environ.get("HOM_DEBUG"):
                    environ["HOM_DEBUG"] = "bool:0"
                    continue

            try:
                cls[key]
                valid.add(key)
            except MissingConfig:
                cls._error(key, "is missing")
            except InvalidConfigType:
                cls._error(key, "has an invalid type prefix")
            except MissingConfigType:
                cls._error(key, "is missing the type prefix")
            except Exception:
                cls._error(key, "has an invalid value")

        return len(valid) == len(keys)

    @classmethod
    def _error(cls, key: str, error: str) -> None:
        logger.error(f"Required environment variable HOM_{key} {error}")


@t.final
class Images:
    """Discord CDN image links.

    How long will they work?

    Find out next time on:
    Insanely popular chat app pushes breaking changes to production.
    """

    GROUP: t.Final[str] = (
        "https://cdn.discordapp.com/attachments/696219254076342312/1200157429283962880/group.jpg"
    )
    """Example group leader verification."""

    PLAYER: t.Final[str] = (
        "https://cdn.discordapp.com/attachments/696219254076342312/1200157428981977229/player.jpg"
    )
    """Example player verification."""

    def __init__(self) -> None:
        raise RuntimeError("Images should not be instantiated")
