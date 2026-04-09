import customtkinter as ctk
from models.phrase import Phrase

class PhraseDialog(ctk.CTkToplevel):
    def __init__(self, parent, db, phrase: Phrase = None, on_save=None):
        super().__init__(parent)
        self.db = db
        self.phrase = phrase or Phrase.empty()
        self.on_save = on_save
        self.result = None

        title = "ویرایش Phrase" if phrase else "افزودن Phrase جدید"
        self.title(title)
        self.geometry("500x450")
        self.resizable(False, False)
        self.grab_set()  # modal

        self._build_ui()

        if phrase:
            self._load_phrase()

    def _build_ui(self):
        pad = {"padx": 15, "pady": 6}

        # عنوان
        ctk.CTkLabel(self, text="عنوان:").pack(anchor="w", **pad)
        self.entry_title = ctk.CTkEntry(self, width=460, placeholder_text="عنوان phrase...")
        self.entry_title.pack(**pad)

        # دسته‌بندی
        ctk.CTkLabel(self, text="دسته‌بندی:").pack(anchor="w", **pad)
        categories = self.db.get_categories()
        categories = [c for c in categories if c != "همه"]
        self.combo_cat = ctk.CTkComboBox(self, values=categories, width=460)
        self.combo_cat.pack(**pad)

        # تگ‌ها
        ctk.CTkLabel(self, text="تگ‌ها (با کاما جدا کنید):").pack(anchor="w", **pad)
        self.entry_tags = ctk.CTkEntry(self, width=460, placeholder_text="python, snippet, ...")
        self.entry_tags.pack(**pad)

        # محتوا
        ctk.CTkLabel(self, text="محتوا:").pack(anchor="w", **pad)
        self.text_content = ctk.CTkTextbox(self, width=460, height=150)
        self.text_content.pack(**pad)

        # دکمه‌ها
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="ذخیره", width=120,
            command=self._save
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, text="انصراف", width=120,
            fg_color="gray", command=self.destroy
        ).pack(side="left", padx=10)

    def _load_phrase(self):
        self.entry_title.insert(0, self.phrase.title)
        self.combo_cat.set(self.phrase.category)
        self.entry_tags.insert(0, self.phrase.tags)
        self.text_content.insert("1.0", self.phrase.content)

    def _save(self):
        title   = self.entry_title.get().strip()
        content = self.text_content.get("1.0", "end").strip()

        if not title or not content:
            # نمایش خطا
            ctk.CTkLabel(self, text="⚠ عنوان و محتوا اجباری هستند",
                         text_color="red").pack()
            return

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
