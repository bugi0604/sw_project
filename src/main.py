from pathlib import Path

from parser import RenPyScriptParser


def main():
    sample_path = Path("samples/sample_script.rpy")

    parser = RenPyScriptParser()
    entries = parser.parse_file(str(sample_path))

    print("RenPy Game Translator")
    print("=====================")
    print(f"Loaded file: {sample_path}")
    print(f"Extracted text count: {len(entries)}")
    print()

    for entry in entries:
        print(f"[{entry.entry_id}] line {entry.line_number}: {entry.original_text}")
        print(f"    protected: {entry.protected_text}")


if __name__ == "__main__":
    main()