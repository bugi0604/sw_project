import json
from pathlib import Path
from typing import Dict, List

from models import TranslationEntry


class TranslationMemory:
    def __init__(self, memory_path: str = "output/translation_memory.json") -> None:
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(exist_ok=True)

    def load_memory(self) -> Dict[str, str]:
        if not self.memory_path.exists():
            return {}

        try:
            return json.loads(self.memory_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def save_entries(self, entries: List[TranslationEntry]) -> Path:
        memory = self.load_memory()

        for entry in entries:
            if entry.original_text.strip() and entry.translated_text.strip():
                memory[entry.original_text] = entry.translated_text

        self.memory_path.write_text(
            json.dumps(memory, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )

        return self.memory_path

    def apply_memory(self, entries: List[TranslationEntry]) -> List[TranslationEntry]:
        memory = self.load_memory()

        for entry in entries:
            if entry.original_text in memory:
                entry.set_translation(memory[entry.original_text])

        return entries