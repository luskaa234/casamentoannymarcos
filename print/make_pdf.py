"""Renders the static (no JS/envelope/countdown) print version of the site
as a 4-page A4 PDF at 300 DPI, using only local fonts (print/fonts).
"""
import os

from PIL import Image, ImageDraw

import fonts as F
from render_common import (
    CREME, CREME_2, DOURADO, TEXTO, VERDE_CLARO, VERDE_ESCURO, VERDE_MEDIO,
    Canvas, draw_centered, draw_corner_brackets, draw_divider,
    draw_eucalyptus_corner, draw_gold_frame, draw_monogram,
    draw_paragraph_centered, draw_tracked_text, paste_qr, text_width, wrap_text,
)

HERE = os.path.dirname(__file__)
QR_DIR = os.path.join(HERE, "..", "assets", "qr")

PAGE_W_MM, PAGE_H_MM = 210, 297


def new_page(bg=CREME):
    c = Canvas(PAGE_W_MM, PAGE_H_MM, bg=bg)
    draw_gold_frame(c.img, margin_px=c.s(70), inset=c.s(16))
    draw_corner_brackets(c.img, margin_px=c.s(96), size_px=c.s(56))
    return c


def draw_ribbon(base_img, center_xy, text, font, fg=CREME, bg=DOURADO, angle=-40, pad=18):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    w = int(d.textlength(text, font=font)) + pad * 2
    h = font.size + pad
    banner = Image.new("RGBA", (w, h), (*bg, 255))
    bd = ImageDraw.Draw(banner)
    tw = bd.textlength(text, font=font)
    bd.text(((w - tw) / 2, (h - font.size) / 2 - font.size * 0.08), text, font=font, fill=fg)
    banner = banner.rotate(angle, expand=True, resample=Image.BICUBIC)
    cx, cy = center_xy
    base_img.paste(banner, (round(cx - banner.width / 2), round(cy - banner.height / 2)), banner)


def draw_chapel(base_img, center_x, top_y, scale=1.0):
    d = ImageDraw.Draw(base_img)
    s = scale

    def p(x, y):
        return (center_x + x * s, top_y + y * s)

    d.rectangle([p(-90, 120), p(90, 340)], fill=CREME_2, outline=VERDE_ESCURO, width=round(5 * s))
    d.polygon([p(-110, 120), p(0, 20), p(110, 120)], fill=VERDE_MEDIO, outline=VERDE_ESCURO, width=round(5 * s))
    d.rectangle([p(120, 0), p(190, 340)], fill=CREME_2, outline=VERDE_ESCURO, width=round(5 * s))
    d.polygon([p(110, 0), p(155, -60), p(200, 0)], fill=VERDE_ESCURO, outline=VERDE_ESCURO, width=round(5 * s))
    d.line([p(155, -100), p(155, -55)], fill=DOURADO, width=round(9 * s))
    d.line([p(135, -80), p(175, -80)], fill=DOURADO, width=round(9 * s))
    d.rounded_rectangle([p(-25, 260), p(25, 340)], radius=round(25 * s), fill=CREME, outline=VERDE_ESCURO, width=round(5 * s))
    for wx in (-58, 58):
        d.rounded_rectangle([p(wx - 18, 165), p(wx + 18, 220)], radius=round(16 * s), fill=VERDE_CLARO, outline=VERDE_ESCURO, width=round(4 * s))
    d.rounded_rectangle([p(120 + 15, 120), p(190 - 15, 175)], radius=round(14 * s), fill=VERDE_CLARO, outline=VERDE_ESCURO, width=round(4 * s))
    d.ellipse([p(-150, 320), p(-70, 355)], fill=VERDE_MEDIO)
    d.ellipse([p(90, 330), p(180, 360)], fill=VERDE_MEDIO)
    d.ellipse([p(200, 330), p(260, 358)], fill=VERDE_MEDIO)


def icon_heart(base_img, center_xy, size, color=VERDE_ESCURO):
    cx, cy = center_xy
    s = size / 48
    d = ImageDraw.Draw(base_img)
    pts = []
    import math
    for i in range(65):
        t = i / 64 * 2 * math.pi
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s * 1.15, cy + y * s * 1.15))
    d.polygon(pts, fill=color)


def icon_star(base_img, center_xy, size, color=VERDE_ESCURO):
    import math
    cx, cy = center_xy
    pts = []
    for i in range(10):
        r = size / 2 if i % 2 == 0 else size / 4.4
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    ImageDraw.Draw(base_img).polygon(pts, fill=color)


def icon_crown(base_img, center_xy, size, color=VERDE_ESCURO):
    cx, cy = center_xy
    w, h = size * 1.25, size * 0.8
    x0, y0 = cx - w / 2, cy - h / 2
    pts = [
        (x0, y0 + h * 0.35), (x0 + w * 0.2, y0 + h * 0.75), (x0 + w * 0.35, y0 + h * 0.15),
        (x0 + w * 0.5, y0 + h * 0.6), (x0 + w * 0.65, y0 + h * 0.15), (x0 + w * 0.8, y0 + h * 0.75),
        (x0 + w, y0 + h * 0.35), (x0 + w * 0.85, y0 + h), (x0 + w * 0.15, y0 + h),
    ]
    ImageDraw.Draw(base_img).polygon(pts, fill=color)


def eyebrow(c, cx, y, text, size=17, tracking=3, color=VERDE_MEDIO, weight=500):
    draw_tracked_text(c.draw, (0, c.s(y)), text, c.font(F.cinzel, size, weight=weight),
                       color, tracking=c.s(tracking), anchor_center_x=c.s(cx))


def eyebrow_cursive(c, cx, y, text, size=44, color=DOURADO):
    draw_centered(c.draw, c.s(cx), c.s(y), text, c.font(F.parisienne, size), color)


# ---------------------------------------------------------------- page 1
def page_cover():
    c = new_page()
    cx = c.final_w / 2

    draw_eucalyptus_corner(c.img, (c.s(130), c.s(130)), scale=c.scale * 1.9)
    draw_eucalyptus_corner(c.img, (c.s(c.final_w - 130), c.s(130)), flip_x=True, scale=c.scale * 1.9)
    draw_eucalyptus_corner(c.img, (c.s(130), c.s(c.final_h - 130)), flip_y=True, scale=c.scale * 1.9)
    draw_eucalyptus_corner(c.img, (c.s(c.final_w - 130), c.s(c.final_h - 130)), flip_x=True, flip_y=True, scale=c.scale * 1.9)

    y = 980
    y = draw_paragraph_centered(
        c.draw, c.s(cx), c.s(y),
        '"Nem olhos viram, nem ouvidos ouviram o que Deus preparou para nós. '
        'Um futuro certo cheio de esperança e paz."',
        c.font(F.cormorant, 30, italic=True), VERDE_ESCURO, max_width=c.s(1500), line_height=c.s(44),
    ) / c.scale
    y += 4
    eyebrow(c, cx, y, "— CORÍNTIOS 2:9", size=18, tracking=3)
    y += 90

    draw_centered(c.draw, c.s(cx), c.s(y), "Com a bênção de Deus e de seus pais,", c.font(F.cormorant, 30), TEXTO)
    y += 52
    draw_centered(c.draw, c.s(cx), c.s(y), "Francisca e Antonio", c.font(F.cormorant, 30, weight="Medium", italic=True), VERDE_ESCURO)
    y += 46
    draw_centered(c.draw, c.s(cx), c.s(y), "Luciene e Francisco", c.font(F.cormorant, 30, weight="Medium", italic=True), VERDE_ESCURO)
    y += 76

    draw_centered(c.draw, c.s(cx), c.s(y), "convidam você para celebrar o amor e a união de", c.font(F.cormorant, 30), TEXTO)
    y += 110

    draw_centered(c.draw, c.s(cx), c.s(y), "Ihanny Gabrielly", c.font(F.beau_rivage, 190), VERDE_ESCURO)
    y += 168
    draw_centered(c.draw, c.s(cx), c.s(y), "&", c.font(F.mrs_saint_delafield, 130), VERDE_ESCURO)
    y += 118
    draw_centered(c.draw, c.s(cx), c.s(y), "Marcos Ryan", c.font(F.beau_rivage, 190), VERDE_ESCURO)
    y += 190

    draw_divider(c.draw, c.s(cx), c.s(y), c.s(420))
    y += 90

    draw_tracked_text(c.draw, (0, c.s(y)), "26 DE JUNHO DE 2027", c.font(F.cinzel, 52, weight=600),
                       VERDE_ESCURO, tracking=c.s(7), anchor_center_x=c.s(cx))
    y += 70
    draw_centered(c.draw, c.s(cx), c.s(y), "Sábado, às 16 horas", c.font(F.cormorant, 38, italic=True), VERDE_MEDIO)
    y += 130

    draw_monogram(c.draw, c.s(cx), c.s(y), size_big=c.s(58), size_amp=c.s(48))
    y += 90
    eyebrow(c, cx, y, "CONVITE DE CASAMENTO", size=19, tracking=5)

    return c


# ---------------------------------------------------------------- page 2
def page_ceremony_reception():
    c = new_page()
    cx = c.final_w / 2

    draw_eucalyptus_corner(c.img, (c.s(130), c.s(130)), scale=c.scale * 1.9)
    draw_eucalyptus_corner(c.img, (c.s(c.final_w - 130), c.s(130)), flip_x=True, scale=c.scale * 1.9)
    draw_eucalyptus_corner(c.img, (c.s(130), c.s(c.final_h - 130)), flip_y=True, scale=c.scale * 1.9)
    draw_eucalyptus_corner(c.img, (c.s(c.final_w - 130), c.s(c.final_h - 130)), flip_x=True, flip_y=True, scale=c.scale * 1.9)

    y = 720

    eyebrow_cursive(c, cx, y, "Cerimônia religiosa", size=54)
    y += 110
    draw_chapel(c.img, c.s(cx), c.s(y), scale=c.scale * 2.15)
    y += 780

    draw_centered(c.draw, c.s(cx), c.s(y), "Paróquia de Cristo Rei", c.font(F.playfair, 56, weight="Medium", italic=True), VERDE_ESCURO)
    y += 78
    y = draw_paragraph_centered(
        c.draw, c.s(cx), c.s(y),
        "Av. Augustinho Ribeiro, 212–248, Chapadinha – MA, 65500-000",
        c.font(F.cormorant, 34), TEXTO, max_width=c.s(1400), line_height=c.s(46),
    ) / c.scale
    y += 12
    eyebrow(c, cx, y, "26 DE JUNHO DE 2027 · 16H00", size=20, tracking=3)
    y += 130

    draw_divider(c.draw, c.s(cx), c.s(y), c.s(360))
    y += 110

    eyebrow(c, cx, y, "FESTA", size=19, tracking=5)
    y += 66
    draw_centered(c.draw, c.s(cx), c.s(y), "Balneário Meireles", c.font(F.playfair, 56, weight="Medium", italic=True), VERDE_ESCURO)
    y += 76
    draw_centered(c.draw, c.s(cx), c.s(y), "Confraternização após a cerimônia", c.font(F.cormorant, 32), TEXTO)

    y = c.final_h - 200
    draw_monogram(c.draw, c.s(cx), c.s(y), size_big=c.s(34), size_amp=c.s(28))

    return c


# ---------------------------------------------------------------- page 3
def page_gifts():
    c = new_page(bg=VERDE_ESCURO)
    cx = c.final_w / 2
    y = 560

    eyebrow(c, cx, y, "LISTA DE PRESENTES", size=19, tracking=5, color=DOURADO)
    y += 74
    y = draw_paragraph_centered(
        c.draw, c.s(cx), c.s(y), "Um carinho para nossa nova história",
        c.font(F.playfair, 58, weight="SemiBold"), CREME, max_width=c.s(1700), line_height=c.s(70),
    ) / c.scale
    y += 20
    y = draw_paragraph_centered(
        c.draw, c.s(cx), c.s(y),
        "A presença de vocês é o nosso maior presente. Para quem desejar nos "
        "presentear, preparamos algumas opções via Pix.",
        c.font(F.cormorant, 30), CREME_2, max_width=c.s(1500), line_height=c.s(42),
    ) / c.scale
    y += 60

    tiers = [
        ("Com carinho", "R$ 150,00", "Um gesto de carinho para os primeiros\ndetalhes do nosso lar.", icon_heart),
        ("Mais escolhido", "R$ 250,00", "Uma contribuição para construirmos\nmemórias na nossa nova fase.", icon_star),
        ("Com amor", "R$ 350,00", "Um presente marcante para celebrar\no início da nossa vida a dois.", icon_crown),
    ]
    card_w, card_h, gap = 640, 700, 60
    total_w = card_w * 3 + gap * 2
    x0 = cx - total_w / 2
    card_top = y

    for i, (ribbon, value, desc, icon_fn) in enumerate(tiers):
        cx_card = x0 + i * (card_w + gap) + card_w / 2
        x1, y1 = c.s(cx_card - card_w / 2), c.s(card_top)
        x2, y2 = c.s(cx_card + card_w / 2), c.s(card_top + card_h)
        c.draw.rounded_rectangle([x1, y1, x2, y2], radius=c.s(14), fill=CREME)
        icon_fn(c.img, (c.s(cx_card), y1 + c.s(110)), c.s(70), VERDE_ESCURO)
        eyebrow(c, cx_card, card_top + 170, "PRESENTE ESPECIAL", size=14, tracking=2.5, color=VERDE_MEDIO)
        draw_centered(c.draw, c.s(cx_card), c.s(card_top + 210), value, c.font(F.playfair, 46, weight="SemiBold", italic=True), VERDE_ESCURO)
        yy = card_top + 300
        for line in desc.split("\n"):
            draw_centered(c.draw, c.s(cx_card), c.s(yy), line, c.font(F.cormorant, 26), TEXTO)
            yy += 36
        draw_ribbon(c.img, (x2 - c.s(70), y1 + c.s(80)), ribbon.upper(), c.font(F.cinzel, 16, weight=500))

    y = card_top + card_h + 90

    pix_w, pix_h = total_w, 760
    x1, y1 = c.s(cx - pix_w / 2), c.s(y)
    x2, y2 = c.s(cx + pix_w / 2), c.s(y + pix_h)
    c.draw.rounded_rectangle([x1, y1, x2, y2], radius=c.s(14), fill=CREME)
    yy = y + 80
    eyebrow(c, cx, yy, "CHAVE PIX (CELULAR)", size=17, tracking=2.5, color=VERDE_MEDIO)
    yy += 64
    draw_centered(c.draw, c.s(cx), c.s(yy), "(98) 99158-5935", c.font(F.playfair, 48, weight="SemiBold"), VERDE_ESCURO)
    yy += 100
    paste_qr(c.img, os.path.join(QR_DIR, "qr-pix.png"), (c.s(cx), c.s(yy) + c.s(210)), c.s(420))

    y = c.final_h - 200
    draw_monogram(c.draw, c.s(cx), c.s(y), size_big=c.s(34), size_amp=c.s(28), color=CREME, amp_color=DOURADO)

    return c


# ---------------------------------------------------------------- page 4
def draw_manual_item(c, x, y, w, icon_char, label, desc):
    r = 46
    cx_icon = x + r
    c.draw.ellipse([c.s(cx_icon - r), c.s(y), c.s(cx_icon + r), c.s(y + r * 2)], fill=VERDE_ESCURO)
    f_icon = F.symbol(c.s(34))
    bbox = c.draw.textbbox((0, 0), icon_char, font=f_icon)
    iw, ih = bbox[2] - bbox[0], bbox[3] - bbox[1]
    c.draw.text((c.s(cx_icon) - iw / 2 - bbox[0], c.s(y + r) - ih / 2 - bbox[1]), icon_char, font=f_icon, fill=CREME)

    tx = x + r * 2 + 26
    f_label = c.font(F.cinzel, 16, weight=500)
    draw_tracked_text(c.draw, (c.s(tx), c.s(y + 2)), label.upper(), f_label, VERDE_ESCURO, tracking=c.s(1.2))
    lines = wrap_text(c.draw, desc, c.font(F.cormorant, 22), c.s(w - r * 2 - 26))
    yy = y + 44
    for line in lines:
        c.draw.text((c.s(tx), c.s(yy)), line, font=c.font(F.cormorant, 22), fill=TEXTO)
        yy += 30
    return max(y + r * 2, yy) + 26


def page_rsvp_manual():
    c = new_page(bg=CREME_2)
    cx = c.final_w / 2

    draw_eucalyptus_corner(c.img, (c.s(130), c.s(130)), scale=c.scale * 1.9)
    draw_eucalyptus_corner(c.img, (c.s(c.final_w - 130), c.s(130)), flip_x=True, scale=c.scale * 1.9)

    y = 420

    draw_centered(c.draw, c.s(cx), c.s(y), "Confirme sua presença", c.font(F.playfair, 54, weight="SemiBold", italic=True), VERDE_ESCURO)
    y += 90

    paragraphs = [
        "Pedimos a gentileza de confirmar sua presença até o dia 26/05. Sua "
        "confirmação é essencial para a organização do nosso grande dia.",
        "Após essa data, infelizmente não poderemos aceitar novas confirmações, "
        "pois precisaremos finalizar a lista de convidados e informar a "
        "quantidade definitiva aos nossos fornecedores.",
        "Agradecemos pela compreensão e esperamos celebrar esse momento tão "
        "especial com você!",
    ]
    for para in paragraphs:
        y = draw_paragraph_centered(c.draw, c.s(cx), c.s(y), para, c.font(F.cormorant, 28), TEXTO,
                                     max_width=c.s(1500), line_height=c.s(40)) / c.scale
        y += 22

    y += 10
    paste_qr(c.img, os.path.join(QR_DIR, "qr-whatsapp.png"), (c.s(cx), c.s(y) + c.s(130)), c.s(260))
    y += 280
    draw_centered(c.draw, c.s(cx), c.s(y), "Aponte a câmera para confirmar presença pelo WhatsApp",
                  c.font(F.cormorant, 24, italic=True), VERDE_MEDIO)
    y += 90

    draw_divider(c.draw, c.s(cx), c.s(y), c.s(360))
    y += 80

    draw_centered(c.draw, c.s(cx), c.s(y), "Querido(a)", c.font(F.playfair, 44, weight="SemiBold"), VERDE_ESCURO)
    y += 62
    draw_centered(c.draw, c.s(cx), c.s(y), "convidado(a)", c.font(F.parisienne, 52), DOURADO)
    y += 90

    items = [
        ("✓", "Confirme presença", "Nos ajude com a organização confirmando com antecedência."),
        ("◷", "Seja pontual", "Chegue com antecedência para não perder nenhum momento."),
        ("♱", "Participe da cerimônia", "Vivencie conosco cada instante desse momento sagrado."),
        ("✉", "Convite individual/familiar", "O convite é válido apenas para os nomes indicados."),
        ("✆", "Celular no silencioso", "Ajude a manter o clima de respeito durante a cerimônia."),
        ("◈", "Não atrapalhe os fotógrafos", "Evite circular na frente durante os registros oficiais."),
        ("♡", "Não use branco", "Cor reservada exclusivamente à noiva."),
        ("❧", "Evite o verde", "Cor reservada aos padrinhos."),
        ("⚑", "Se beber, não dirija", "Cuide de você e das pessoas ao seu redor."),
        ("✦", "Aproveite e celebre", "Esse dia é uma festa do amor — divirta-se com a gente!"),
    ]
    col_w = 780
    gap = 80
    x0 = cx - (col_w * 2 + gap) / 2
    col_y = [y, y]
    for i, (icon_char, label, desc) in enumerate(items):
        col = i % 2
        x = x0 + col * (col_w + gap)
        col_y[col] = draw_manual_item(c, x, col_y[col], col_w, icon_char, label, desc)

    y = max(col_y) + 30
    draw_centered(c.draw, c.s(cx), c.s(y), "Obrigado por fazer parte da nossa história.", c.font(F.cormorant, 28), TEXTO)
    y += 42
    draw_centered(c.draw, c.s(cx), c.s(y), "Estamos ansiosos para viver esse dia ao seu lado!",
                  c.font(F.mrs_saint_delafield, 44), DOURADO)
    y += 90

    eyebrow(c, cx, y, "COM AMOR", size=16, tracking=4)
    y += 48
    draw_monogram(c.draw, c.s(cx), c.s(y), size_big=c.s(40), size_amp=c.s(32))

    return c


def build():
    pages = [page_cover(), page_ceremony_reception(), page_gifts(), page_rsvp_manual()]
    finals = [p.finalize() for p in pages]
    for i, img in enumerate(finals, start=1):
        img.save(os.path.join(HERE, f"pagina-{i}.png"), dpi=(300, 300))
    out_path = os.path.join(HERE, "convite-impressao-A4.pdf")
    finals[0].save(out_path, save_all=True, append_images=finals[1:], resolution=300.0)
    print("Saved", out_path, "and", len(finals), "page PNGs")
    return out_path


if __name__ == "__main__":
    build()
