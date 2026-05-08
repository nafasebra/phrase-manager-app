import tkinter as tk
from tkinter import font as tkfont
import customtkinter as ctk
from pathlib import Path

FONTS_DIR = Path(__file__).parent.parent / "assets" / "fonts"

def load_font(font_path: str | Path) -> str:
    font_path = Path(font_path)
    if not font_path.exists():
        raise FileNotFoundError(f"Font not found: {font_path}")

    # Load font in tkinter
    _load_platform(font_path)

    # Read font name from file
    name = _get_font_name(font_path)
    return name


def _load_platform(font_path: Path):
    """Load font based on operating system"""
    import platform
    system = platform.system()

    if system == "Windows":
        import ctypes
        ctypes.windll.gdi32.AddFontResourceExW(str(font_path), 0x10, 0)

    elif system == "Darwin":  # macOS
        import subprocess
        subprocess.run(["cp", str(font_path),
                        Path.home() / "Library/Fonts/"], check=False)

    # Linux and fallback — tkinter loads directly
    # Via pyglet or method below:
    try:
        import pyglet
        pyglet.font.add_file(str(font_path))
    except ImportError:
        pass  # No problem if pyglet is not available


def _get_font_name(font_path: Path) -> str:
    """Read font name from TTF file"""
    try:
        # First method: with fonttools
        from fontTools.ttLib import TTFont
        tt = TTFont(str(font_path))
        name_table = tt["name"]
        for record in name_table.names:
            if record.nameID == 4:  # Full name
                return record.toUnicode()
    except ImportError:
        pass

    # Second method: use file name as font name
    return font_path.stem


class AppFonts:
    _initialized = False
    family = "TkDefaultFont"  # fallback

    @classmethod
    def init(cls, font_path: str | Path):
        if cls._initialized:
            return
        try:
            cls.family = load_font(font_path)
            print(f"✅ Font loaded: {cls.family}")
        except Exception as e:
            print(f"⚠ Font not loaded, using default font: {e}")
        cls._initialized = True

    @classmethod
    def get(cls, size: int = 13, weight: str = "normal") -> ctk.CTkFont:
        return ctk.CTkFont(family=cls.family, size=size, weight=weight)

    @classmethod
    def bold(cls, size: int = 13) -> ctk.CTkFont:
        return cls.get(size=size, weight="bold")

    @classmethod
    def regular(cls, size: int = 13) -> ctk.CTkFont:
        return cls.get(size=size, weight="bold")
