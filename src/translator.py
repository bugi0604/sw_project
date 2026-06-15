from typing import Dict, List

from models import TranslationEntry


class DemoTranslator:
    """
    DemoTranslator is used when an external translation API key is not available.
    It provides sample translations for common Ren'Py script sentences and
    keeps the program executable in an offline environment.
    """

    def __init__(self) -> None:
        self.sample_dictionary: Dict[str, str] = {
            "안녕하세요. 이 게임에 오신 것을 환영합니다.": "Hello. Welcome to this game.",
            "오늘은 정말 좋은 날이네요.": "Today is a really nice day.",
            "이 문장은 내레이션입니다.": "This sentence is narration.",
            "당신의 이름은 [player_name]입니다.": "Your name is [player_name].",
            "어디로 갈까요?": "Where should we go?",
            "학교": "School",
            "학교로 이동합니다.": "Moving to school.",
            "집": "Home",
            "집으로 이동합니다.": "Moving home.",
        }

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        if text in self.sample_dictionary:
            return self.sample_dictionary[text]

        return f"[{target_language}] {text}"


class TranslationManager:
    """
    TranslationManager controls the translation process.
    The current implementation uses DemoTranslator, but this class is designed
    so that DeepL API or Google Translation API can be connected later.
    """

    def __init__(self, source_language: str = "Korean", target_language: str = "English") -> None:
        self.source_language = source_language
        self.target_language = target_language
        self.translator = DemoTranslator()

    def set_language_option(self, source_language: str, target_language: str) -> None:
        self.source_language = source_language
        self.target_language = target_language

    def translate_entries(self, entries: List[TranslationEntry]) -> List[TranslationEntry]:
        translated_entries: List[TranslationEntry] = []

        for entry in entries:
            translated_text = self.translator.translate(
                entry.original_text,
                self.source_language,
                self.target_language,
            )

            entry.set_translation(translated_text)
            translated_entries.append(entry)

        return translated_entries

    def translate_single_text(self, text: str) -> str:
        return self.translator.translate(
            text,
            self.source_language,
            self.target_language,
        )