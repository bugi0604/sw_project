import re
from typing import List

from models import TranslationEntry


class QualityChecker:
    def check_entries(self, entries: List[TranslationEntry]) -> List[str]:
        issues: List[str] = []

        if not entries:
            issues.append("No translation entries found.")
            return issues

        for entry in entries:
            issues.extend(self._check_single_entry(entry))

        if not issues:
            issues.append("No quality issues found.")

        return issues

    def _check_single_entry(self, entry: TranslationEntry) -> List[str]:
        issues: List[str] = []

        if not entry.translated_text.strip():
            issues.append(f"Entry #{entry.entry_id}: translated text is empty.")

        if entry.original_text.strip() == entry.translated_text.strip():
            issues.append(f"Entry #{entry.entry_id}: translated text is same as original.")

        original_variables = self._extract_variables(entry.original_text)
        translated_variables = self._extract_variables(entry.translated_text)

        for variable in original_variables:
            if variable not in translated_variables:
                issues.append(
                    f"Entry #{entry.entry_id}: variable {variable} is missing in translated text."
                )

        original_tags = self._extract_tags(entry.original_text)
        translated_tags = self._extract_tags(entry.translated_text)

        for tag in original_tags:
            if tag not in translated_tags:
                issues.append(
                    f"Entry #{entry.entry_id}: tag {tag} is missing in translated text."
                )

        return issues

    def _extract_variables(self, text: str) -> List[str]:
        return re.findall(r"\[[^\]]+\]", text)

    def _extract_tags(self, text: str) -> List[str]:
        return re.findall(r"\{[^}]+\}", text)