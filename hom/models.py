import enum

__all__ = ("BaseStrEnum", "SupportCategory", "SupportType", "TemplateSection")


class BaseStrEnum(enum.StrEnum):
    """The base enum all string enums inherit from."""

    def __str__(self) -> str:
        return self.value


class SupportCategory(BaseStrEnum):
    """The different support categories."""

    Groups = "**Groups** → Assistance related to groups"
    Names = "**Name Changes** → Assistance related to name changes"
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

    Footer = "footer"
    Categories = "categories"
    QuestionsChannel = "questions_channel"
