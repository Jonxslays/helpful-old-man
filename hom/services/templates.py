import logging
from pathlib import Path

from hom.config import Config
from hom.models import BaseStrEnum
from hom.models import SupportCategory
from hom.models import SupportType
from hom.models import Template
from hom.models import TemplateSection

__all__ = ("TemplateService",)

logger = logging.getLogger(__name__)

GROUP_CATEGORIES = (
    SupportCategory.Groups,
    SupportType.VerifyGroup,
    SupportType.ResetGroupVerification,
    SupportType.RemoveFromGroup,
    SupportType.Other,
)

NAME_CATEGORIES = (
    SupportCategory.Names,
    SupportType.ApproveNameChange,
    SupportType.DeleteNameChanges,
    SupportType.Other,
)


class TemplateService:
    __slots__ = ("_templates",)

    def __init__(self) -> None:
        self._templates: dict[str, Template] = {}

        for path in Path("hom/data/templates").glob("[!_]*.md"):
            if path.is_dir():
                continue

            name = path.stem.replace("-", "").lower()
            self.add_template(name, path.read_text().strip())
            logger.debug(f"Loaded {path.stem} template")

        logger.info(f"Loaded {len(self._templates)} support message templates!")

    def add_template(self, name: str, content: str) -> None:
        """Adds a template to the service for use later.

        Args:
            name: The name of the template.
            content: The template content.
        """
        self._templates[name] = Template(name, content)

    def get_template(self, message_type: BaseStrEnum | None = None) -> Template:
        """Gets the template for the given message type.

        Args:
            message_type: The template type to get, or the main support template if `None`.

        Returns:
            The requested template.
        """
        name = message_type.name.lower() if message_type else "support"
        return self._templates[name]

    def get_support_template(self) -> Template:
        """Gets the template for the support channel embed.

        Returns:
            The requested template with placeholders replaced.
        """
        template = self.get_template()

        if not template.replaced:
            template.replace(self._get_categories_replacement(), TemplateSection.Categories)
            template.replace(str(Config.QUESTIONS_CHANNEL), TemplateSection.QuestionsChannel)
            template.replaced = True

        return template

    def _get_categories_replacement(self) -> str:
        """Gets the support categories formatted for the support embed.

        Returns:
            The requested categories string.
        """
        sections: list[tuple[BaseStrEnum, ...]] = []
        categories: tuple[SupportCategory | SupportType, ...]

        for category in SupportCategory:
            if category is SupportCategory.Groups:
                categories = GROUP_CATEGORIES

            elif category is SupportCategory.Names:
                categories = NAME_CATEGORIES

            else:
                categories = (category,)

            sections.append(categories)

        return "\n\n".join("\n- ".join(s) for s in sections)
