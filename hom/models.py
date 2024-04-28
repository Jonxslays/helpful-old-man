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

    ApiKey = "api-key"
    ApproveNameChange = "approve-name-change"
    AwaitingResponse = "awaiting-response"
    DeleteNameChanges = "delete-name-changes"
    Other = "other"
    Patreon = "patreon"
    PatreonChannel = "patreon-channel"
    Private = "private"
    QuestionsChannel = "questions-channel"
    Reminder = "reminder"
    RemoveFromGroup = "remove-from-group"
    ResetGroupVerification = "reset-group-verification"
    ReviewNameChange = "review-name-change"
    ScreenshotFull = "screenshot-full"
    ScreenshotMinimal = "screenshot-minimal"
    Support = "support"
    VerifyGroup = "verify-group"


@dataclass(slots=True)
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
    """A support ticket for a user."""

    user: hikari.Snowflakeish
    """The ID of the user who opened this ticket."""

    channel: hikari.Snowflakeish
    """The ID of the channel for this ticket."""

    description: str | None
    """The description of this ticket."""

    new: bool
    """If true, this ticket was just created."""

    def is_closed(self) -> bool:
        return (self.description or "").endswith("CLOSED")
