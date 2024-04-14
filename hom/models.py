import enum
from dataclasses import dataclass

__all__ = ("BaseStrEnum", "SupportCategory", "SupportType", "Template", "TemplateSection")


class BaseStrEnum(enum.StrEnum):
    """The base enum all string enums inherit from."""

    def __str__(self) -> str:
        return self.value


class SupportCategory(BaseStrEnum):
    """The different support categories."""

    Groups = "**Groups** → Request help related to a group"
    Names = "**Name Changes** → Request help with a name change"
    Patreon = "**Patreon** → Request help with Patreon benefits"
    ApiKey = "**API Key** → Request an API key for development"
    Other = "**Other** → For all other inquiries"


class SupportType(BaseStrEnum):
    """The different support ticket types."""

    VerifyGroup = "Verify my group (for groups with 50+ members)"
    ResetGroupVerification = "Reset my verification code"
    RemoveFromGroup = "Remove me from a group"

    ApproveNameChange = "Approve a pending name change"
    ReviewNameChange = "Review a denied name change"
    DeleteNameChanges = "Delete my name change history"

    Other = "Other"


class TemplateSection(BaseStrEnum):
    """Different sections of the templates."""

    Categories = "categories"
    PatreonChannel = "patreon_channel"
    Private = "private"
    QuestionsChannel = "questions_channel"
    Reminder = "reminder"
    ScreenshotFull = "screenshot_full"
    ScreenshotMinimal = "screenshot_minimal"


@dataclass
class Template:
    name: str
    """The name of the template."""

    content: str
    """The template content."""

    replaced: bool = False
    """Whether or not the content placeholders have been replaced."""

    def replace(self, replacement: str, section: TemplateSection) -> None:
        """Replaces the content of the section with the replacement.

        Args:
            replacement: The text to replace with.
            section: The section to replace.
        """
        self.content.replace(f"{{{{{section.value}}}}}", replacement)
