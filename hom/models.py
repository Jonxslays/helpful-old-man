import enum
from dataclasses import dataclass

import hikari

__all__ = ("BaseStrEnum", "Template", "TemplateSection", "Ticket")


class BaseStrEnum(enum.StrEnum):
    """The base enum all string enums inherit from."""

    def __str__(self) -> str:
        return self.value


class TemplateSection(BaseStrEnum):
    """Different sections of the templates."""

    PatreonChannel = "patreon_channel"
    Private = "private"
    QuestionsChannel = "questions_channel"
    Reminder = "reminder"
    ScreenshotFull = "screenshot_full"
    ScreenshotMinimal = "screenshot_minimal"


@dataclass
class Template:
    """A template used by HOM for message/embed content."""

    name: str
    """The name of the template."""

    content: str
    """The template content."""

    populated: bool = False
    """Whether or not the content placeholders have been populated."""

    def populate(self, section: TemplateSection, content: str) -> None:
        """Populates the content of the section with the content.

        Args:
            section: The section to populate.
            content: The content to populate with.
        """
        self.content = self.content.replace(f"{{{{{section.value}}}}}", content)


@dataclass(slots=True)
class Ticket:
    user: hikari.Snowflakeish
    channel: hikari.Snowflakeish
