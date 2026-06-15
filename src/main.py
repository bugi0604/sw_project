from pathlib import Path

from parser import RenPyScriptParser
from translator import TranslationManager


def main():
    sample_path = Path("samples/sample_script.rpy")

    parser = RenPyScriptParser()
    entries = parser.parse_file(str(sample_path))

    translation_manager = TranslationManager(
        source_language="Korean",
        target_language="English",
    )

    translated_entries = translation_manager.translate_entries(entries)

    print("RenPy Game Translator")
    print("=====================")
    print(f"Loaded file: {sample_path}")
    print(f"Extracted text count: {len(translated_entries)}")
    print()

    for entry in translated_entries:
        print(f"[{entry.entry_id}] line {entry.line_number}")
        print(f"Original   : {entry.original_text}")
        print(f"Translated : {entry.translated_text}")
        print()


if __name__ == "__main__":
    main()