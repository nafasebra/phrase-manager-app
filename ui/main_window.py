import customtkinter as ctk
import pyperclip
from database import Database
from ui.add_dialog import PhraseDialog
from ui.font_manager import AppFonts

from ui.export_import_dialog import ExportImportDialog

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.title("Phrase Manager")
        self.geometry("900x600")
        self.minsize(700, 450)

        ctk.set_appearance_mode("system")   # dark / light / system
        ctk.set_default_color_theme("blue")

        self._build_ui()
        self._refresh()

    # ─── UI ──────────────────────────────────────────────

    def _build_ui(self):
        # بخش اصلی
        main = ctk.CTkFrame(self)
        main.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # نوار بالا
        top_bar = ctk.CTkFrame(main, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 8))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh())
        ctk.CTkEntry(top_bar, textvariable=self.search_var,
                     placeholder_text="🔍 جستجو...", width=300).pack(side="left")

        ctk.CTkButton(top_bar, text="+ افزودن", font=AppFonts.bold(13),
                      command=self._open_add).pack(side="right")

        # export / import button
        ctk.CTkButton(
            top_bar, text="⬆⬇ Export/Import",
            font=AppFonts.bold(13),
            fg_color="gray", hover_color="#555",
            command=self._open_export_import
        ).pack(side="right", padx=(0, 6))


        # لیست phrase ها
        self.scroll_frame = ctk.CTkScrollableFrame(main)
        self.scroll_frame.pack(fill="both", expand=True)

        # نوار پایین
        self.status_label = ctk.CTkLabel(main, text="", text_color="gray")
        self.status_label.pack(anchor="w", pady=(4, 0))

    def _build_phrase_cards(self, phrases):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not phrases:
            ctk.CTkLabel(
                self.scroll_frame,
                text="هیچ phrase ای یافت نشد 🕵️",
                text_color="gray", font=AppFonts.regular(13)
            ).pack(pady=40)
            return

        for phrase in phrases:
            self._make_card(phrase)

    def _make_card(self, phrase):
        card = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        card.pack(fill="x", pady=4, padx=4)

        # ردیف بالایی
        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(8, 2))

        ctk.CTkLabel(
            top, text=phrase.title,
            font=AppFonts.regular(13)
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text=f"[{phrase.category}]",
            text_color="gray", font=AppFonts.regular(13)
        ).pack(side="left", padx=8)

        # دکمه‌های عملیات
        btn_frame = ctk.CTkFrame(top, fg_color="transparent")
        btn_frame.pack(side="right")

        ctk.CTkButton(
            btn_frame, text="کپی", width=70, font=AppFonts.bold(13),
            command=lambda p=phrase: self._copy(p)
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame, text="✏️ ویرایش", width=80, font=AppFonts.bold(13),
            command=lambda p=phrase: self._open_edit(p)
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame, text="🗑 حذف", width=70, font=AppFonts.bold(13),
            fg_color="#c0392b", hover_color="#e74c3c",
            command=lambda p=phrase: self._delete(p)
        ).pack(side="left", padx=3)

        # پیش‌نمایش محتوا
        preview = phrase.content[:120] + ("..." if len(phrase.content) > 120 else "")
        ctk.CTkLabel(
            card, text=preview,
            text_color="gray", wraplength=700, justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 5))

        # تگ‌ها
        if phrase.tags:
            tags_text = "  ".join(f"#{t.strip()}" for t in phrase.tags.split(",") if t.strip())
            ctk.CTkLabel(
                card, text=tags_text,
                text_color="#3498db", font=AppFonts.regular(13)
            ).pack(anchor="w", padx=10, pady=(0, 8))

    # ─── Actions ─────────────────────────────────────────

    def _select_category(self, cat):
        self.selected_cat = cat
        self._refresh()

    def _refresh(self):
        cat    = getattr(self, "selected_cat", "همه")
        search = self.search_var.get()
        phrases = self.db.get_all(category=cat, search=search)
        self._build_phrase_cards(phrases)
        self.status_label.configure(text=f"{len(phrases)} phrase")

    def _open_add(self):
        PhraseDialog(self, self.db, on_save=self._refresh)

    def _open_edit(self, phrase):
        PhraseDialog(self, self.db, phrase=phrase, on_save=self._refresh)

    def _copy(self, phrase):
        pyperclip.copy(phrase.content)
        self.status_label.configure(text=f"'{phrase.title}' کپی شد!")
        self.after(3000, lambda: self.status_label.configure(
            text=f"{len(self.db.get_all())} phrase"
        ))

    def _delete(self, phrase):
        dialog = ctk.CTkInputDialog(
            text=f"برای حذف '{phrase.title}' تایپ کنید: DELETE",
            title="تأیید حذف"
        )
        if dialog.get_input() == "DELETE":
            self.db.delete_phrase(phrase.id)
            self._refresh()

    def _add_category(self):
        dialog = ctk.CTkInputDialog(text="نام دسته‌بندی جدید:", title="دسته جدید")
        name = dialog.get_input()
        if name and name.strip():
            self.db.add_category(name.strip())
            self._refresh()

    def _open_export_import(self):
        ExportImportDialog(self, self.db, on_done=self._refresh)

    def on_close(self):
        self.db.close()
        self.destroy()
