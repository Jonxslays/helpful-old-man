from hom.client import Client
from hom.config import Config
from hom.models import BaseStrEnum
from hom.models import SupportCategory
from hom.models import SupportType
from hom.models import TemplateSection

__all__ = ("Replacer",)


class Replacer:
    @classmethod
    def replace(cls, text: str, replacement: str, section: TemplateSection) -> str:
        return text.replace(f"{{{{{section.value}}}}}", replacement)

    @classmethod
    def replace_support_template(cls, client: Client) -> str:
        text = client.get_support_template()
        questions_channel = str(Config.QUESTIONS_CHANNEL)
        questions_section = TemplateSection.QuestionsChannel
        categories = cls._get_categories_replacement()
        text = cls.replace(text, categories, TemplateSection.Categories)
        return cls.replace(text, questions_channel, questions_section)

    @classmethod
    def _get_categories_replacement(cls) -> str:
        sections: list[tuple[BaseStrEnum, ...]] = []

        for category in SupportCategory:
            if category is SupportCategory.Groups:
                sections.append(
                    (
                        SupportCategory.Groups,
                        SupportType.VerifyGroup,
                        SupportType.ResetGroupVerification,
                        SupportType.RemoveFromGroup,
                        SupportType.Other,
                    )
                )

            elif category is SupportCategory.Names:
                sections.append(
                    (
                        SupportCategory.Names,
                        SupportType.ApproveNameChange,
                        SupportType.DeleteNameChanges,
                        SupportType.Other,
                    )
                )

            else:
                sections.append((category,))

        return "\n\n".join("\n- ".join(s) for s in sections)
