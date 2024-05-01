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
        return self._templates[section.value.lower()]

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
        """Gets the template for the "Other" ticket.

        Returns:
            The requested template.
        """
        return self._get_template_with_reminder(TemplateSection.Other)

    def get_api_key_template(self) -> Template:
        """Gets the template for the "API Key" ticket.

        Returns:
            The requested template.
        """
        return self._get_template_with_reminder(TemplateSection.ApiKey)

    def get_patreon_template(self) -> Template:
        """Gets the template for the "Patreon" ticket.

        Returns:
            The requested template.
        """
        template = self._get_template_with_reminder(TemplateSection.Patreon, False)

        if not template.populated:
            template.populate(TemplateSection.PatreonChannel, str(Config.PATREON_CHANNEL))
            template.populated = True

        return template

    def get_verify_group_template(self) -> Template:
        """Gets the template for the "Verify Group" ticket.

        Returns:
            The requested template.
        """
        template = self._get_template_with_reminder(TemplateSection.VerifyGroup, False)

        if not template.populated:
            screenshot = self.get_template(TemplateSection.ScreenshotFull)
            template.populate(TemplateSection.ScreenshotFull, screenshot.content)
            template.populated = True

        return template

    def get_reset_group_verification_template(self) -> Template:
        """Gets the template for the "Reset group verification" ticket.

        Returns:
            The requested template.
        """
        template = self._get_template_with_reminder(TemplateSection.ResetGroupVerification, False)

        if not template.populated:
            screenshot = self.get_template(TemplateSection.ScreenshotFull)
            template.populate(TemplateSection.ScreenshotFull, screenshot.content)
            template.populated = True

        return template

    def get_remove_from_group_template(self) -> Template:
        """Gets the template for the "Reset from group" ticket.

        Returns:
            The requested template.
        """
        template = self._get_template_with_reminder(TemplateSection.RemoveFromGroup, False)

        if not template.populated:
            screenshot = self.get_template(TemplateSection.ScreenshotMinimal)
            template.populate(TemplateSection.ScreenshotMinimal, screenshot.content)
            template.populated = True

        return template

    def get_approve_name_change_template(self) -> Template:
        """Gets the template for the "Approve name change" ticket.

        Returns:
            The requested template.
        """
        return self._get_template_with_reminder(TemplateSection.ApproveNameChange)

    def get_delete_name_changes_template(self) -> Template:
        """Gets the template for the "Delete name changes" ticket.

        Returns:
            The requested template.
        """
        template = self._get_template_with_reminder(TemplateSection.DeleteNameChanges, False)

        if not template.populated:
            screenshot = self.get_template(TemplateSection.ScreenshotMinimal)
            template.populate(TemplateSection.ScreenshotMinimal, screenshot.content)
            template.populated = True

        return template

    def get_review_name_change_template(self) -> Template:
        """Gets the template for the "Review name change" ticket.

        Returns:
            The requested template.
        """
        return self._get_template_with_reminder(TemplateSection.ReviewNameChange)

    def _get_template_with_reminder(
        self, section: TemplateSection, mark_populated: bool = True
    ) -> Template:
        """Gets a template and only populates the reminder section.

        Args:
            section: The template section to get.
            mark_populated: Whether or not to mark the template as populated.

        Returns:
            The requested template.
        """
        template = self.get_template(section)

        if not template.populated:
            reminder = self.get_template(TemplateSection.Reminder)
            template.populate(TemplateSection.Reminder, reminder.content)
            template.content += "\u200b\n\u200b"  # Padding above footer

            if mark_populated:
                template.populated = True

        return template
