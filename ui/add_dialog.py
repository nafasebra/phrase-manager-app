import customtkinter as ctk
from models.phrase import Phrase
from ui.font_manager import AppFonts

class PhraseDialog(ctk.CTkToplevel):
    def __init__(self, parent, db, phrase: Phrase = None, on_save=None):
        super().__init__(parent)
        self.db = db
        self.phrase = phrase or Phrase.empty()
        self.on_save = on_save

        title = "Edit Phrase" if phrase else "Add New Phrase"
        self.title(title)
        self.geometry("500x480")
        self.resizable(False, False)
        self.grab_set()

        self._build_ui()

        if phrase:
            self._load_phrase()

    def _build_ui(self):
        pad = {"padx": 15, "pady": 6}

        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="Title:", font=AppFonts.get(13)).pack(anchor="e", **pad)
        self.entry_title = ctk.CTkEntry(scroll, width=440, placeholder_text="Phrase title...", font=AppFonts.get(13))
        self.entry_title.pack(**pad)

        ctk.CTkLabel(scroll, text="Category:", font=AppFonts.get(13)).pack(anchor="e", **pad)
        categories = [c for c in self.db.get_categories() if c != "All"]
        self.combo_cat = ctk.CTkComboBox(scroll, values=categories, width=440, font=AppFonts.get(13))
        self.combo_cat.pack(**pad)

        ctk.CTkLabel(scroll, text="Tags (comma separated):", font=AppFonts.get(13)).pack(anchor="e", **pad)
        self.entry_tags = ctk.CTkEntry(scroll, width=440, placeholder_text="python, snippet, ...", font=AppFonts.get(13))
        self.entry_tags.pack(**pad)

        ctk.CTkLabel(scroll, text="Content:", font=AppFonts.get(13)).pack(anchor="e", **pad)
        self.text_content = ctk.CTkTextbox(scroll, width=440, height=150, font=AppFonts.get(13))
        self.text_content.pack(**pad)

        self.error_label = ctk.CTkLabel(scroll, text="", text_color="red", font=AppFonts.get(12))
        self.error_label.pack()

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=12)

        ctk.CTkButton(btn_frame, text="Save", width=120, font=AppFonts.bold(13), command=self._save).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", width=120, font=AppFonts.get(13), fg_color="gray", command=self.destroy).pack(side="left", padx=10)

    def _load_phrase(self):
        self.entry_title.insert(0, self.phrase.title)
        self.combo_cat.set(self.phrase.category)
        self.entry_tags.insert(0, self.phrase.tags)
        self.text_content.insert("1.0", self.phrase.content)

    def _save(self):
        title   = self.entry_title.get().strip()
        content = self.text_content.get("1.0", "end").strip()

        if not title or not content:
            self.error_label.configure(text="Title and content are required")
            return

        self.error_label.configure(text="")
        self.phrase.title    = title
        self.phrase.content  = content
        self.phrase.category = self.combo_cat.get()
        self.phrase.tags     = self.entry_tags.get().strip()

        if self.phrase.id:
            self.db.update_phrase(self.phrase)
        else:
            self.db.add_phrase(self.phrase)

        if self.on_save:
            self.on_save()
        self.destroy()
