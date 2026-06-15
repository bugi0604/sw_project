import re
from pathlib import Path
from typing import List

from models import TranslationEntry


class RenPyScriptParser:
    def __init__(self) -> None:
        self.entries: List[TranslationEntry] = []

    def parse_file(self, file_path: str) -> List[TranslationEntry]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix != ".rpy":
            raise ValueError("Only .rpy files are supported.")

        content = path.read_text(encoding="utf-8")
        return self.parse_content(content)

    def parse_content(self, content: str) -> List[TranslationEntry]:
        self.entries = []
        lines = content.splitlines()

        entry_id = 1

        for index, line in enumerate(lines, start=1):
            if self._should_skip_line(line):
                continue

            quoted_texts = self._extract_quoted_texts(line)

            for text in quoted_texts:
                if not text.strip():
                    continue

                protected_text = self._protect_variables_and_tags(text)

                entry = TranslationEntry(
                    entry_id=entry_id,
                    line_number=index,
                    original_text=text,
                    protected_text=protected_text,
                )

                self.entries.append(entry)
                entry_id += 1

        return self.entries

    def _should_skip_line(self, line: str) -> bool:
        stripped = line.strip()

        if not stripped:
            return True

        if stripped.startswith("#"):
            return True

        skipped_prefixes = (
            "label ",
            "return",
            "$",
            "define ",
            "default ",
            "image ",
            "init ",
            "python:",
            "screen ",
            "transform ",
            "if ",
            "elif ",
            "else:",
            "jump ",
            "call ",
            "scene ",
            "show ",
            "hide ",
            "play ",
            "stop ",
            "with ",
        )

        return stripped.startswith(skipped_prefixes)

    def _extract_quoted_texts(self, line: str) -> List[str]:
        pattern = r'"((?:[^"\\]|\\.)*)"'
        return re.findall(pattern, line)

    def _protect_variables_and_tags(self, text: str) -> str:
        protected = text

        variables = re.findall(r"\[[^\]]+\]", protected)
        for index, variable in enumerate(variables):
            protected = protected.replace(variable, f"__VAR_{index}__")

        tags = re.findall(r"\{[^}]+\}", protected)
        for index, tag in enumerate(tags):
            protected = protected.replace(tag, f"__TAG_{index}__")

        return protected

    def get_entries(self) -> List[TranslationEntry]:
        return self.entries