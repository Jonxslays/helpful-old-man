import enum


class BaseStrEnum(enum.StrEnum):
    def __str__(self) -> str:
        return self.value


class SupportCategory(BaseStrEnum):
    Groups = "Groups → Assistance related to groups"
    Names = "Name Changes → Assistance related to name changes"
    Patreon = "Patreon → Request help with Patreon benefits"
    ApiKey = "API Key → Request an API key for development"
    Other = "Other → For all other inquiries"


class SupportType(BaseStrEnum):
    VerifyGroup = "Verify my group (for groups with 50+ members)"
    ResetGroupVerification = "Reset my verification code"
    RemoveFromGroup = "Remove me from a group"
    Other = "Other"

    ApproveNameChange = "Approve a pending name change"
    ReviewNameChange = "Review a denied name change"
    DeleteNameChanges = "Delete my name change history"
