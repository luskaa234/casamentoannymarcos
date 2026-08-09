"""Renders the single physical invitation card, 105x148mm at 300 DPI.

Uses only local TTFs (print/fonts) and Pillow with 4x supersampling for
crisp text -- no wkhtmltopdf / headless browser involved, per the brief.
"""
import os

import fonts as F
from render_common import (
    CREME, DOURADO, TEXTO, VERDE_ESCURO, VERDE_MEDIO,
    Canvas, draw_centered, draw_corner_brackets, draw_divider,
    draw_eucalyptus_corner, draw_gold_frame, draw_monogram,
    draw_paragraph_centered, draw_tracked_text, paste_qr,
)

HERE = os.path.dirname(__file__)
QR_DIR = os.path.join(HERE, "..", "assets", "qr")


def build():
    c = Canvas(105, 148)
    cx = c.final_w / 2

    draw_eucalyptus_corner(c.img, (c.s(66), c.s(66)), scale=c.scale * 0.95)
    draw_eucalyptus_corner(c.img, (c.s(c.final_w - 66), c.s(c.final_h - 66)),
                            flip_x=True, flip_y=True, scale=c.scale * 0.95)

    draw_gold_frame(c.img, margin_px=c.s(34), inset=c.s(9))
    draw_corner_brackets(c.img, margin_px=c.s(50), size_px=c.s(30))

    y = 270

    draw_monogram(c.draw, c.s(cx), c.s(y), size_big=c.s(46), size_amp=c.s(38))
    y += 78

    draw_tracked_text(
        c.draw, (0, c.s(y)), "CONVITE DE CASAMENTO",
        c.font(F.cinzel, 17, weight=500), VERDE_MEDIO,
        tracking=c.s(3), anchor_center_x=c.s(cx),
    )
    y += 56

    draw_centered(c.draw, c.s(cx), c.s(y), "Ihanny Gabrielly", c.font(F.beau_rivage, 92), VERDE_ESCURO)
    y += 82
    draw_centered(c.draw, c.s(cx), c.s(y), "&", c.font(F.mrs_saint_delafield, 64), VERDE_ESCURO)
    y += 58
    draw_centered(c.draw, c.s(cx), c.s(y), "Marcos Ryan", c.font(F.beau_rivage, 92), VERDE_ESCURO)
    y += 96

    draw_divider(c.draw, c.s(cx), c.s(y), c.s(230))
    y += 46

    draw_tracked_text(
        c.draw, (0, c.s(y)), "26 DE JUNHO DE 2027",
        c.font(F.cinzel, 30, weight=600), VERDE_ESCURO,
        tracking=c.s(4), anchor_center_x=c.s(cx),
    )
    y += 42
    draw_centered(c.draw, c.s(cx), c.s(y), "Sábado, às 16 horas", c.font(F.cormorant, 24, italic=True), VERDE_MEDIO)
    y += 58

    verse = (
        '"Nem olhos viram, nem ouvidos ouviram o que Deus preparou para nós. '
        'Um futuro certo cheio de esperança e paz."'
    )
    y = draw_paragraph_centered(
        c.draw, c.s(cx), c.s(y), verse, c.font(F.cormorant, 21, italic=True),
        VERDE_ESCURO, max_width=c.s(940), line_height=c.s(30),
    ) / c.scale
    y += 4
    draw_tracked_text(
        c.draw, (0, c.s(y)), "— CORÍNTIOS 2:9",
        c.font(F.cinzel, 14, weight=500), VERDE_MEDIO,
        tracking=c.s(2), anchor_center_x=c.s(cx),
    )
    y += 48

    draw_centered(c.draw, c.s(cx), c.s(y), "Paróquia de Cristo Rei",
                  c.font(F.playfair, 32, weight="Medium", italic=True), VERDE_ESCURO)
    y += 46
    y = draw_paragraph_centered(
        c.draw, c.s(cx), c.s(y),
        "Av. Augustinho Ribeiro, 212–248, Chapadinha – MA, 65500-000",
        c.font(F.cormorant, 22), TEXTO, max_width=c.s(880), line_height=c.s(29),
    ) / c.scale
    y += 6
    draw_tracked_text(
        c.draw, (0, c.s(y)), "26 DE JUNHO DE 2027 · 16H00",
        c.font(F.cinzel, 15, weight=500), VERDE_MEDIO,
        tracking=c.s(2), anchor_center_x=c.s(cx),
    )
    y += 54

    qr_size = 300
    gap = 70
    left_cx = cx - gap / 2 - qr_size / 2
    right_cx = cx + gap / 2 + qr_size / 2
    paste_qr(c.img, os.path.join(QR_DIR, "qr-pix.png"), (c.s(left_cx), c.s(y + qr_size / 2)), c.s(qr_size))
    paste_qr(c.img, os.path.join(QR_DIR, "qr-whatsapp.png"), (c.s(right_cx), c.s(y + qr_size / 2)), c.s(qr_size))
    y += qr_size + 18
    draw_tracked_text(c.draw, (0, c.s(y)), "PRESENTEAR (PIX)", c.font(F.cinzel, 14, weight=500),
                       VERDE_MEDIO, tracking=c.s(1.5), anchor_center_x=c.s(left_cx))
    draw_tracked_text(c.draw, (0, c.s(y)), "CONFIRMAR PRESENÇA", c.font(F.cinzel, 14, weight=500),
                       VERDE_MEDIO, tracking=c.s(1.5), anchor_center_x=c.s(right_cx))
    y += 40

    draw_tracked_text(c.draw, (0, c.s(y)), "COM AMOR", c.font(F.cinzel, 15, weight=500),
                       VERDE_MEDIO, tracking=c.s(3), anchor_center_x=c.s(cx))
    y += 34
    draw_monogram(c.draw, c.s(cx), c.s(y), size_big=c.s(30), size_amp=c.s(24))

    out_path = os.path.join(HERE, "convite-cartao-105x148mm.png")
    c.save_png(out_path)
    print("Saved", out_path, "final size", c.final_w, "x", c.final_h, "px @", c.dpi, "dpi")
    return out_path


if __name__ == "__main__":
    build()
