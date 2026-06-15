import csv
import re
from pathlib import Path
from typing import List

from models import TranslationEntry


class FileGenerator:
    def __init__(self, output_dir: str = "output") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_translated_file(
        self,
        original_file_path: str,
        entries: List[TranslationEntry],
    ) -> Path:
        original_path = Path(original_file_path)

        if not original_path.exists():
            raise FileNotFoundError("Original file does not exist.")

        if original_path.suffix != ".rpy":
            raise ValueError("Only .rpy files can be exported.")

        lines = original_path.read_text(encoding="utf-8").splitlines()
        entry_map = {entry.line_number: entry for entry in entries}

        translated_lines = []

        for line_number, line in enumerate(lines, start=1):
            if line_number in entry_map:
                translated_line = self._replace_first_quoted_text(line, entry_map[line_number])
                translated_lines.append(translated_line)
            else:
                translated_lines.append(line)

        output_name = f"{original_path.stem}_translated{original_path.suffix}"
        output_path = self.output_dir / output_name
        output_path.write_text("\n".join(translated_lines), encoding="utf-8")

        return output_path

    def export_translation_csv(self, entries: List[TranslationEntry]) -> Path:
        output_path = self.output_dir / "translation_result.csv"

        with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["ID", "Line", "Original Text", "Translated Text"])

            for entry in entries:
                writer.writerow([
                    entry.entry_id,
                    entry.line_number,
                    entry.original_text,
                    entry.translated_text,
                ])

        return output_path

    def _replace_first_quoted_text(self, line: str, entry: TranslationEntry) -> str:
        translated_text = entry.translated_text.strip()

        if not translated_text:
            translated_text = entry.original_text

        escaped_text = translated_text.replace("\\", "\\\\").replace('"', '\\"')

        return re.sub(
            r'"((?:[^"\\]|\\.)*)"',
            f'"{escaped_text}"',
            line,
            count=1,
        )