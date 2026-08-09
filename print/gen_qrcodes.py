"""Generate the Pix (EMV BR Code) and WhatsApp QR codes used by the invite."""
import base64
import io
import os

import qrcode


def crc16_ccitt(payload: str) -> str:
    poly = 0x1021
    crc = 0xFFFF
    for byte in payload.encode("utf-8"):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def emv_field(field_id: str, value: str) -> str:
    return f"{field_id}{len(value):02d}{value}"


def build_pix_payload(key: str, name: str, city: str, amount: str | None = None, txid: str = "***") -> str:
    name = name[:25]
    city = city[:15]

    merchant_account = emv_field("00", "BR.GOV.BCB.PIX") + emv_field("01", key)
    additional_data = emv_field("05", txid)

    payload = (
        emv_field("00", "01")
        + emv_field("01", "11")
        + emv_field("26", merchant_account)
        + emv_field("52", "0000")
        + emv_field("53", "986")
        + (emv_field("54", amount) if amount else "")
        + emv_field("58", "BR")
        + emv_field("59", name)
        + emv_field("60", city)
        + emv_field("62", additional_data)
        + "6304"
    )
    return payload + crc16_ccitt(payload)


def make_qr_png(data: str, out_path: str, box_size: int = 12, border: int = 2,
                 fill="#42502f", back="#faf6ee") -> str:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back).convert("RGB")
    img.save(out_path)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "qr")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    pix_payload = build_pix_payload(
        key="+5598991585935",
        name="IHANNY GABRIELLY",
        city="CHAPADINHA",
    )
    print("PIX PAYLOAD:", pix_payload)

    pix_b64 = make_qr_png(pix_payload, os.path.join(out_dir, "qr-pix.png"))

    wa_text = (
        "Ola! Confirmamos com alegria nossa presenca no casamento de "
        "Ihanny Gabrielly e Marcos Ryan, no dia 26/06/2027. Ate la! "
    )
    import urllib.parse
    wa_link = "https://wa.me/5598991585935?text=" + urllib.parse.quote(wa_text)
    print("WHATSAPP LINK:", wa_link)

    wa_b64 = make_qr_png(wa_link, os.path.join(out_dir, "qr-whatsapp.png"))

    with open(os.path.join(out_dir, "qr-pix.b64.txt"), "w") as f:
        f.write(pix_b64)
    with open(os.path.join(out_dir, "qr-whatsapp.b64.txt"), "w") as f:
        f.write(wa_b64)

    with open(os.path.join(out_dir, "pix-payload.txt"), "w") as f:
        f.write(pix_payload)
    with open(os.path.join(out_dir, "whatsapp-link.txt"), "w") as f:
        f.write(wa_link)

    print("Done. Files written to", out_dir)
