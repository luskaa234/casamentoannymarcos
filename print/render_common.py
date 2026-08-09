"""Shared high-DPI rendering helpers for the print deliverables.

Everything is drawn at SUPERSAMPLE x the final pixel size and then downscaled
with LANCZOS, which is what keeps small serif/script text crisp at 300 DPI
without depending on a browser/wkhtmltopdf renderer.
"""
import math
import os

from PIL import Image, ImageDraw

import fonts as F

DPI = 300
SUPERSAMPLE = 4

VERDE_ESCURO = (66, 80, 47)
VERDE_MEDIO = (116, 132, 87)
VERDE_CLARO = (174, 189, 144)
CREME = (250, 246, 238)
CREME_2 = (242, 236, 221)
DOURADO = (178, 140, 76)
TEXTO = (58, 63, 46)
LINHA = (66, 80, 47)


def mm_to_px(mm: float, dpi: int = DPI) -> int:
    return round(mm / 25.4 * dpi)


class Canvas:
    def __init__(self, width_mm: float, height_mm: float, bg=CREME):
        self.dpi = DPI
        self.final_w = mm_to_px(width_mm)
        self.final_h = mm_to_px(height_mm)
        self.scale = SUPERSAMPLE
        self.w = self.final_w * self.scale
        self.h = self.final_h * self.scale
        self.img = Image.new("RGB", (self.w, self.h), bg)
        self.draw = ImageDraw.Draw(self.img)

    def s(self, px: float) -> int:
        """Scale a "final-resolution" px value up to supersampled space."""
        return round(px * self.scale)

    def font(self, loader, size_final, **kwargs):
        """Load a font sized for final-resolution px, at supersampled size."""
        return loader(self.s(size_final), **kwargs)

    def finalize(self) -> Image.Image:
        return self.img.resize((self.final_w, self.final_h), Image.LANCZOS)

    def save_png(self, path: str):
        self.finalize().save(path, dpi=(self.dpi, self.dpi))


def text_width(draw: ImageDraw.ImageDraw, text: str, font) -> float:
    return draw.textlength(text, font=font)


def draw_tracked_text(draw, xy, text, font, fill, tracking=0, anchor_center_x=None):
    """Draw text with letter-spacing; if anchor_center_x is given, xy[0] is ignored
    and the whole tracked string is centered horizontally on that x."""
    x, y = xy
    widths = [text_width(draw, ch, font) for ch in text]
    total = sum(widths) + tracking * max(0, len(text) - 1)
    if anchor_center_x is not None:
        x = anchor_center_x - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking
    return total


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_width(draw, trial, font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, font, fill):
    w = text_width(draw, text, font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return w


def draw_paragraph_centered(draw, cx, y, text, font, fill, max_width, line_height, align="center"):
    lines = wrap_text(draw, text, font, max_width)
    for line in lines:
        w = text_width(draw, line, font)
        x = cx - w / 2 if align == "center" else cx
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def draw_divider(draw, cx, y, width, color=DOURADO, line_color=(200, 195, 175)):
    half = width / 2
    draw.line([(cx - half, y), (cx - 14, y)], fill=line_color, width=2)
    draw.line([(cx + 14, y), (cx + half, y)], fill=line_color, width=2)
    d = 7
    diamond = [(cx, y - d), (cx + d, y), (cx, y + d), (cx - d, y)]
    draw.polygon(diamond, fill=color)


def draw_gold_frame(img: Image.Image, margin_px: int, color=DOURADO, width=3, inset=10):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    draw.rectangle(
        [margin_px, margin_px, w - margin_px, h - margin_px],
        outline=color, width=width,
    )
    draw.rectangle(
        [margin_px + inset, margin_px + inset, w - margin_px - inset, h - margin_px - inset],
        outline=color, width=1,
    )


def draw_corner_brackets(img: Image.Image, margin_px: int, size_px: int, color=DOURADO, width=4):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    m = margin_px
    s = size_px
    # top-left
    draw.line([(m, m + s), (m, m), (m + s, m)], fill=color, width=width)
    # top-right
    draw.line([(w - m - s, m), (w - m, m), (w - m, m + s)], fill=color, width=width)
    # bottom-left
    draw.line([(m, h - m - s), (m, h - m), (m + s, h - m)], fill=color, width=width)
    # bottom-right
    draw.line([(w - m - s, h - m), (w - m, h - m), (w - m, h - m - s)], fill=color, width=width)


def _leaf(size, color):
    """A single supersampled eucalyptus leaf as a rotatable RGBA sprite."""
    leaf = Image.new("RGBA", (size * 2, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(leaf)
    d.ellipse([0, 0, size * 2, size], fill=color)
    return leaf


def draw_eucalyptus_corner(img: Image.Image, origin, flip_x=False, flip_y=False, scale=1.0):
    """Paints a small branch-of-leaves motif with its stem anchored at `origin`."""
    ox, oy = origin
    sx = -1 if flip_x else 1
    sy = -1 if flip_y else 1
    leaves = [
        # (dist_along_stem, offset_perp, leaf_len, leaf_w, angle_deg, color)
        (10, 6, 46, 22, -35, VERDE_CLARO),
        (55, 14, 52, 24, -20, VERDE_MEDIO),
        (100, 24, 48, 22, 8, VERDE_CLARO),
        (150, 38, 54, 24, 32, VERDE_MEDIO),
        (195, 54, 42, 20, 58, VERDE_CLARO),
        (40, 4, 30, 15, -55, VERDE_MEDIO),
    ]
    stem_pts = [(ox + sx * t * scale, oy + sy * t * 0.72 * scale) for t in range(0, 210, 4)]
    ImageDraw.Draw(img).line(stem_pts, fill=VERDE_MEDIO, width=max(2, round(2 * scale)))
    for dist, off, length, width, angle, color in leaves:
        cx = ox + sx * dist * scale
        cy = oy + sy * dist * 0.72 * scale + sy * off * scale
        leaf = _leaf(round(length * scale / 2), color)
        eff_angle = angle if not flip_x else 180 - angle
        eff_angle = eff_angle if not flip_y else -eff_angle
        leaf = leaf.resize((round(length * scale), round(width * scale)))
        leaf = leaf.rotate(eff_angle, expand=True)
        img.paste(leaf, (round(cx - leaf.width / 2), round(cy - leaf.height / 2)), leaf)


def draw_monogram(draw, cx, y, size_big=64, size_amp=52, color=VERDE_ESCURO, amp_color=None):
    amp_color = amp_color or color
    f_letters = F.playfair(size_big, "SemiBold")
    f_amp = F.mrs_saint_delafield(size_amp)
    i_w = text_width(draw, "I", f_letters)
    amp_w = text_width(draw, "&", f_amp)
    m_w = text_width(draw, "M", f_letters)
    gap = size_big * 0.18
    total = i_w + gap + amp_w + gap + m_w
    x = cx - total / 2
    draw.text((x, y), "I", font=f_letters, fill=color)
    x += i_w + gap
    draw.text((x, y - size_big * 0.06), "&", font=f_amp, fill=amp_color)
    x += amp_w + gap
    draw.text((x, y), "M", font=f_letters, fill=color)


def paste_qr(base_img: Image.Image, qr_path: str, center_xy, size_px: int):
    qr = Image.open(qr_path).convert("RGB").resize((size_px, size_px), Image.LANCZOS)
    cx, cy = center_xy
    base_img.paste(qr, (round(cx - size_px / 2), round(cy - size_px / 2)))
