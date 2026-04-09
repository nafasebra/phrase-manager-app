import customtkinter as ctk
from ui.main_window import MainWindow
from ui.font_manager import AppFonts
from pathlib import Path

if __name__ == "__main__":
    AppFonts.init(Path("assets/Vazir.ttf"))
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
