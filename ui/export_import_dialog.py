import customtkinter as ctk
from tkinter import filedialog, messagebox
from ui.font_manager import AppFonts

class ExportImportDialog(ctk.CTkToplevel):
    def __init__(self, parent, db, on_done=None):
        super().__init__(parent)
        self.db = db
        self.on_done = on_done

        self.title("Export / Import")
        self.geometry("420x320")
        self.resizable(False, False)
        self.grab_set()
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="Export / Import داده‌ها",
            font=AppFonts.bold(15)
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            self, text="فرمت پشتیبانی‌شده: JSON",
            text_color="gray", font=AppFonts.regular(12)
        ).pack(pady=(0, 16))

        # ─── Export ───────────────────────────────────────
        export_frame = ctk.CTkFrame(self)
        export_frame.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(
            export_frame, text="Export",
            font=AppFonts.bold(13)
        ).pack(anchor="e", padx=12, pady=(8, 2))

        ctk.CTkLabel(
            export_frame,
            text="همه phrase ها رو در یک فایل JSON ذخیره می‌کنه.",
            text_color="gray", font=AppFonts.regular(12)
        ).pack(anchor="e", padx=12)

        ctk.CTkButton(
            export_frame, text="انتخاب مسیر و Export",
            font=AppFonts.bold(13), command=self._do_export
        ).pack(anchor="e", padx=12, pady=(6, 10))

        # ─── Import ───────────────────────────────────────
        import_frame = ctk.CTkFrame(self)
        import_frame.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(
            import_frame, text="Import",
            font=AppFonts.bold(13)
        ).pack(anchor="e", padx=12, pady=(8, 2))

        self.overwrite_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            import_frame,
            text="داده‌های فعلی پاک بشن (Overwrite)",
            variable=self.overwrite_var,
            font=AppFonts.regular(12)
        ).pack(anchor="e", padx=12)

        ctk.CTkButton(
            import_frame, text="انتخاب فایل و Import",
            font=AppFonts.bold(13), command=self._do_import
        ).pack(anchor="e", padx=12, pady=(6, 10))

        # ─── وضعیت ────────────────────────────────────────
        self.status_label = ctk.CTkLabel(
            self, text="", text_color="gray",
            font=AppFonts.regular(12), wraplength=380
        )
        self.status_label.pack(pady=(8, 0))

    # ─── Actions ──────────────────────────────────────────

    def _do_export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="ذخیره فایل Export"
        )
        if not path:
            return
        try:
            count = self.db.export_to_json(path)
            self._set_status(f"✅ {count} phrase با موفقیت export شد.", "green")
        except Exception as e:
            self._set_status(f"❌ خطا: {e}", "#e74c3c")

    def _do_import(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="انتخاب فایل Import"
        )
        if not path:
            return

        if self.overwrite_var.get():
            if not messagebox.askyesno(
                "تأیید", "همه داده‌های فعلی پاک میشن. ادامه میدی؟"
            ):
                return

        try:
            result = self.db.import_from_json(path, overwrite=self.overwrite_var.get())
            msg = f"✅ {result['imported']} وارد شد"
            if result["skipped"]:
                msg += f" | ⚠️ {result['skipped']} رد شد"
            if result["errors"]:
                msg += f" | ❌ {len(result['errors'])} خطا"
            self._set_status(msg, "green")
            if self.on_done:
                self.on_done()
        except Exception as e:
            self._set_status(f"❌ خطا در خواندن فایل: {e}", "#e74c3c")

    def _set_status(self, text: str, color: str):
        self.status_label.configure(text=text, text_color=color)

