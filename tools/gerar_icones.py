"""Favicon (marcador de estação: linha azul + ponto) e og.jpg. Uso: python tools/gerar_icones.py"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parents[1]
IMG = RAIZ / "assets" / "img"
TINTA, PAPEL, AZUL = (12, 13, 16), (236, 234, 228), (4, 85, 161)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#0c0d10"/><rect x="4" y="27" width="56" height="10" fill="#0455a1"/><circle cx="32" cy="32" r="13" fill="#0c0d10" stroke="#eceae4" stroke-width="6"/></svg>"""

def icone(tam):
    e = 8; s = tam * e
    im = Image.new("RGB", (s, s), TINTA); d = ImageDraw.Draw(im)
    u = s / 64
    d.rectangle((4 * u, 27 * u, 60 * u, 37 * u), fill=AZUL)
    d.ellipse((16 * u, 16 * u, 48 * u, 48 * u), fill=PAPEL)
    d.ellipse((22 * u, 22 * u, 42 * u, 42 * u), fill=TINTA)
    return im.resize((tam, tam), Image.LANCZOS)

def og():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), TINTA); d = ImageDraw.Draw(im)
    foto = ImageOps.fit(Image.open(RAIZ / "assets/obras/olho-nuvem-t.webp").convert("RGB"), (504, 630), centering=(.5, .45))
    im.paste(foto, (W - 504, 0))
    for y in range(0, H, 9):
        for x in range(W - 560, W - 504, 9):
            d.ellipse((x, y, x + 2, y + 2), fill=(70, 72, 78))
    f = lambda t, w: ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", t)
    fonte = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", 170); fonte.set_variation_by_name("Bold")
    sub = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", 34); sub.set_variation_by_name("SemiBold")
    d.text((64, 150), "DIVA", font=fonte, fill=PAPEL)
    d.text((70, 330), "T A T T O O", font=sub, fill=(79, 147, 230))
    d.text((70, 420), "Pontilhismo · Fineline · Blackwork · Old School", font=sub.font_variant(size=26), fill=PAPEL)
    d.rectangle((70, 500, 130, 508), fill=AZUL); d.ellipse((90, 494, 110, 514), fill=TINTA, outline=PAPEL, width=4)
    d.text((148, 490), "Praça da Árvore · São Paulo", font=sub.font_variant(size=26), fill=(154, 156, 163))
    im.save(IMG / "og.jpg", quality=86)

(IMG / "favicon.svg").write_text(SVG, encoding="utf-8")
icone(32).save(IMG / "favicon-32.png")
icone(180).save(IMG / "apple-touch-icon.png")
og()
print("ok")
