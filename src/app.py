from pathlib import Path
from typing import List, Optional

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from models import TranslationEntry
from parser import RenPyScriptParser
from translator import TranslationManager


class RenPyTranslatorApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("RenPy Game Translator")
        self.root.geometry("1100x720")
        self.root.minsize(950, 650)

        self.current_file: Optional[Path] = None
        self.entries: List[TranslationEntry] = []
        self.selected_entry: Optional[TranslationEntry] = None

        self.parser = RenPyScriptParser()
        self.translation_manager = TranslationManager()

        self.file_path_var = tk.StringVar(value="No file selected")
        self.status_var = tk.StringVar(value="Ready")
        self.source_language_var = tk.StringVar(value="Korean")
        self.target_language_var = tk.StringVar(value="English")

        self._create_widgets()

    def run(self) -> None:
        self.root.mainloop()

    def _create_widgets(self) -> None:
        self._create_header()
        self._create_file_controls()
        self._create_language_controls()
        self._create_result_table()
        self._create_detail_editor()
        self._create_status_bar()

    def _create_header(self) -> None:
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            header_frame,
            text="RenPy Game Translator",
            font=("Arial", 18, "bold"),
        )
        title_label.pack(anchor=tk.W)

        subtitle_label = ttk.Label(
            header_frame,
            text="A desktop tool for extracting and translating Ren'Py .rpy script text",
            font=("Arial", 10),
        )
        subtitle_label.pack(anchor=tk.W, pady=(4, 0))

    def _create_file_controls(self) -> None:
        file_frame = ttk.LabelFrame(self.root, text="Project File", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        path_label = ttk.Label(file_frame, textvariable=self.file_path_var)
        path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        select_button = ttk.Button(
            file_frame,
            text="Select .rpy File",
            command=self.select_file,
        )
        select_button.pack(side=tk.LEFT, padx=5)

        analyze_button = ttk.Button(
            file_frame,
            text="Analyze",
            command=self.analyze_script,
        )
        analyze_button.pack(side=tk.LEFT, padx=5)

        translate_button = ttk.Button(
            file_frame,
            text="Translate",
            command=self.translate_script,
        )
        translate_button.pack(side=tk.LEFT, padx=5)

    def _create_language_controls(self) -> None:
        language_frame = ttk.LabelFrame(self.root, text="Translation Settings", padding=10)
        language_frame.pack(fill=tk.X, padx=10, pady=5)

        source_label = ttk.Label(language_frame, text="Source Language:")
        source_label.pack(side=tk.LEFT)

        source_combo = ttk.Combobox(
            language_frame,
            textvariable=self.source_language_var,
            values=["Korean", "English", "Japanese"],
            state="readonly",
            width=15,
        )
        source_combo.pack(side=tk.LEFT, padx=(5, 20))

        target_label = ttk.Label(language_frame, text="Target Language:")
        target_label.pack(side=tk.LEFT)

        target_combo = ttk.Combobox(
            language_frame,
            textvariable=self.target_language_var,
            values=["English", "Korean", "Japanese"],
            state="readonly",
            width=15,
        )
        target_combo.pack(side=tk.LEFT, padx=5)

    def _create_result_table(self) -> None:
        table_frame = ttk.LabelFrame(self.root, text="Translation Result", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("id", "line", "original", "translated")
        self.result_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12,
        )

        self.result_table.heading("id", text="ID")
        self.result_table.heading("line", text="Line")
        self.result_table.heading("original", text="Original Text")
        self.result_table.heading("translated", text="Translated Text")

        self.result_table.column("id", width=50, anchor=tk.CENTER)
        self.result_table.column("line", width=70, anchor=tk.CENTER)
        self.result_table.column("original", width=450)
        self.result_table.column("translated", width=450)

        y_scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.result_table.yview,
        )
        x_scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.HORIZONTAL,
            command=self.result_table.xview,
        )

        self.result_table.configure(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
        )

        self.result_table.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.result_table.bind("<<TreeviewSelect>>", self.on_entry_selected)

    def _create_detail_editor(self) -> None:
        editor_frame = ttk.LabelFrame(self.root, text="Translation Editor", padding=10)
        editor_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

        original_frame = ttk.LabelFrame(editor_frame, text="Original Text", padding=5)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.original_text_box = tk.Text(
            original_frame,
            height=6,
            wrap=tk.WORD,
            state=tk.DISABLED,
        )
        self.original_text_box.pack(fill=tk.BOTH, expand=True)

        translated_frame = ttk.LabelFrame(editor_frame, text="Translated Text", padding=5)
        translated_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.translated_text_box = tk.Text(
            translated_frame,
            height=6,
            wrap=tk.WORD,
        )
        self.translated_text_box.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        button_frame.pack(fill=tk.X)

        save_button = ttk.Button(
            button_frame,
            text="Save Edited Translation",
            command=self.save_edited_translation,
        )
        save_button.pack(side=tk.RIGHT)

    def _create_status_bar(self) -> None:
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            anchor=tk.W,
            relief=tk.SUNKEN,
            padding=5,
        )
        status_label.pack(fill=tk.X)

    def select_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select Ren'Py script file",
            filetypes=[("Ren'Py Script", "*.rpy"), ("All Files", "*.*")],
        )

        if not file_path:
            return

        self.current_file = Path(file_path)
        self.file_path_var.set(str(self.current_file))
        self.status_var.set("File selected. Click Analyze to extract text.")

        self.entries = []
        self.selected_entry = None
        self._clear_table()
        self._clear_editor()

    def analyze_script(self) -> None:
        if self.current_file is None:
            messagebox.showwarning("Warning", "Please select a .rpy file first.")
            return

        try:
            self.entries = self.parser.parse_file(str(self.current_file))
            self.selected_entry = None
            self._refresh_table()
            self._clear_editor()

            self.status_var.set(f"Analysis completed. Extracted {len(self.entries)} text entries.")
            messagebox.showinfo("Analysis Complete", f"Extracted {len(self.entries)} text entries.")

        except Exception as error:
            messagebox.showerror("Analysis Error", str(error))
            self.status_var.set("Analysis failed.")

    def translate_script(self) -> None:
        if not self.entries:
            messagebox.showwarning("Warning", "Please analyze a script before translation.")
            return

        source_language = self.source_language_var.get()
        target_language = self.target_language_var.get()

        self.translation_manager.set_language_option(source_language, target_language)
        self.entries = self.translation_manager.translate_entries(self.entries)

        self._refresh_table()
        self.status_var.set("Translation completed.")
        messagebox.showinfo("Translation Complete", "Translation completed successfully.")

    def on_entry_selected(self, event) -> None:
        selected_items = self.result_table.selection()

        if not selected_items:
            return

        item_id = selected_items[0]
        values = self.result_table.item(item_id, "values")

        if not values:
            return

        entry_id = int(values[0])
        self.selected_entry = self._find_entry_by_id(entry_id)

        if self.selected_entry is not None:
            self._show_entry_in_editor(self.selected_entry)

    def save_edited_translation(self) -> None:
        if self.selected_entry is None:
            messagebox.showwarning("Warning", "Please select an entry to edit.")
            return

        edited_text = self.translated_text_box.get("1.0", tk.END).strip()

        if not edited_text:
            messagebox.showwarning("Warning", "Translated text cannot be empty.")
            return

        self.selected_entry.set_translation(edited_text)
        self._refresh_table()
        self._show_entry_in_editor(self.selected_entry)

        self.status_var.set(f"Edited translation saved for entry #{self.selected_entry.entry_id}.")

    def _find_entry_by_id(self, entry_id: int) -> Optional[TranslationEntry]:
        for entry in self.entries:
            if entry.entry_id == entry_id:
                return entry
        return None

    def _show_entry_in_editor(self, entry: TranslationEntry) -> None:
        self.original_text_box.configure(state=tk.NORMAL)
        self.original_text_box.delete("1.0", tk.END)
        self.original_text_box.insert(tk.END, entry.original_text)
        self.original_text_box.configure(state=tk.DISABLED)

        self.translated_text_box.delete("1.0", tk.END)
        self.translated_text_box.insert(tk.END, entry.translated_text)

    def _clear_editor(self) -> None:
        self.original_text_box.configure(state=tk.NORMAL)
        self.original_text_box.delete("1.0", tk.END)
        self.original_text_box.configure(state=tk.DISABLED)

        self.translated_text_box.delete("1.0", tk.END)

    def _clear_table(self) -> None:
        for item in self.result_table.get_children():
            self.result_table.delete(item)

    def _refresh_table(self) -> None:
        self._clear_table()

        for entry in self.entries:
            self.result_table.insert(
                "",
                tk.END,
                values=(
                    entry.entry_id,
                    entry.line_number,
                    entry.original_text,
                    entry.translated_text,
                ),
            )