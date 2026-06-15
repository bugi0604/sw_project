from dataclasses import dataclass


@dataclass
class TranslationEntry:
    entry_id: int
    line_number: int
    original_text: str
    translated_text: str = ""
    protected_text: str = ""

    def set_translation(self, translated_text: str) -> None:
        self.translated_text = translated_text