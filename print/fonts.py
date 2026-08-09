"""Local font loader for the print pipeline (no internet dependency at render time).

All TTFs live in print/fonts/ (fetched once from the Google Fonts OFL repo).
Variable fonts are set to a named instance or explicit weight axis value.
"""
import os

from PIL import ImageFont

FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")


def _load(filename: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


def beau_rivage(size: int) -> ImageFont.FreeTypeFont:
    return _load("BeauRivage-Regular.ttf", size)


def mrs_saint_delafield(size: int) -> ImageFont.FreeTypeFont:
    return _load("MrsSaintDelafield-Regular.ttf", size)


def parisienne(size: int) -> ImageFont.FreeTypeFont:
    return _load("Parisienne-Regular.ttf", size)


def playfair(size: int, weight: str = "Medium", italic: bool = False) -> ImageFont.FreeTypeFont:
    filename = "PlayfairDisplay-Italic[wght].ttf" if italic else "PlayfairDisplay[wght].ttf"
    font = _load(filename, size)
    name = (weight + " Italic") if italic and weight != "Italic" else weight
    font.set_variation_by_name(name.encode())
    return font


def cormorant(size: int, weight: str = "Regular", italic: bool = False) -> ImageFont.FreeTypeFont:
    filename = "CormorantGaramond-Italic[wght].ttf" if italic else "CormorantGaramond[wght].ttf"
    font = _load(filename, size)
    if italic:
        name = "Italic" if weight == "Regular" else weight + " Italic"
    else:
        name = weight
    font.set_variation_by_name(name.encode())
    return font


def cinzel(size: int, weight: int = 500) -> ImageFont.FreeTypeFont:
    font = _load("Cinzel[wght].ttf", size)
    font.set_variation_by_axes([weight])
    return font


_SYMBOL_PATHS = [r"C:\Windows\Fonts\seguisym.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def symbol(size: int) -> ImageFont.FreeTypeFont:
    """Broad-coverage font for pictographic glyphs (checkmarks, clocks, ...)
    that the decorative brand fonts don't include."""
    for path in _SYMBOL_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)
