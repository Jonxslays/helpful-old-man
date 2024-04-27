import logging
from pathlib import Path

from hom.config import Config
from hom.models import Template
from hom.models import TemplateSection

__all__ = ("TemplateService",)

logger = logging.getLogger(__name__)


class TemplateService:
    __slots__ = ("_templates",)

    def __init__(self) -> None:
        self._templates: dict[str, Template] = {}

        for path in Path("hom/data/templates").glob("[!_]*.md"):
            if path.is_dir():
                continue

            name = path.stem.lower()
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

    def get_template(self, section: TemplateSection) -> Template:
        """Gets the template for the given section.

        Args:
            section: The template section to get.

        Returns:
            The requested template.
        """
        return self._templates[section.name.lower()]

    def get_support_template(self) -> Template:
        """Gets the template for the support channel embed.

        Returns:
            The requested template.
        """
        template = self.get_template(TemplateSection.Support)

        if not template.populated:
            template.populate(TemplateSection.QuestionsChannel, str(Config.QUESTIONS_CHANNEL))
            template.populated = True

        return template

    def get_other_template(self) -> Template:
        """Gets the template for the an "Other" ticket.

        Returns:
            The requested template.
        """
        return self._get_template_with_reminder_only(TemplateSection.Other)

    def get_api_key_template(self) -> Template:
        """Gets the template for the an "API Key" ticket.

        Returns:
            The requested template.
        """
        return self._get_template_with_reminder_only(TemplateSection.ApiKey)

    def _get_template_with_reminder_only(self, section: TemplateSection) -> Template:
        """Gets a template and only replaces the reminder section.

        Args:
            section: The template section to get.

        Returns:
            The requested template.
        """
        template = self.get_template(section)

        if not template.populated:
            reminder = self.get_template(TemplateSection.Reminder)
            template.populate(TemplateSection.Reminder, reminder.content)
            template.content += "\u200b\n\u200b"  # Padding above footer
            template.populated = True

        return template
