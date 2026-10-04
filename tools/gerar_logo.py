"""Logo da Diva Tattoo: coroa + "Diva" gótico em degradê roxo + "Tattoo" em pincel + brilho.
Gera assets/img/logo-diva.webp/png (transparente), favicon, apple-touch e og.jpg.
Fontes em ../_ref/fontes (UnifrakturCook, Kaushan Script, Grenze Gotisch). Uso: python tools/gerar_logo.py"""
import math, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parents[1]
FONTES = RAIZ.parent / "_ref" / "fontes"
IMG = RAIZ / "assets" / "img"
TINTA = (10, 8, 13)
ROXO = (155, 77, 255)
ROXO_CLARO = (214, 186, 255)
ROXO_ESCURO = (98, 34, 190)
PAPEL = (240, 234, 246)

def fonte(nome, tam, var=None):
    f = ImageFont.truetype(str(FONTES / nome), tam)
    if var: f.set_variation_by_name(var)
    return f

def degrade(tam, cima, baixo):
    w, h = tam
    g = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        g.putpixel((0, y), tuple(round(cima[i] + (baixo[i] - cima[i]) * t) for i in range(3)))
    return g.resize((w, h))

def brilho(d, cx, cy, r, cor, fino=.18):
    """estrela de 4 pontas (o ✦ dos posts dela)"""
    pts = []
    for i in range(8):
        a = math.pi / 4 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * fino
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=cor)

def coroa(d, cx, base, larg, cor, esp):
    h = larg * .62
    x0, x1 = cx - larg / 2, cx + larg / 2
    pts = [(x0, base), (x0 - larg * .04, base - h * .78), (cx - larg * .24, base - h * .38), (cx, base - h),
           (cx + larg * .24, base - h * .38), (x1 + larg * .04, base - h * .78), (x1, base)]
    d.line(pts + [pts[0]], fill=cor, width=esp, joint="curve")
    d.line([(x0, base + esp * 1.6), (x1, base + esp * 1.6)], fill=cor, width=esp)
    for (x, y) in (pts[1], pts[3], pts[5]):
        r = esp * 1.25
        d.ellipse((x - r, y - r, x + r, y + r), fill=cor)

def logo():
    S = 4  # supersampling
    W, H = 1400 * S, 900 * S
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # "Diva"
    f_diva = fonte("UnifrakturCook-Bold.ttf", 400 * S)
    masc = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(masc)
    bx = md.textbbox((0, 0), "Diva", font=f_diva)
    tw, th = bx[2] - bx[0], bx[3] - bx[1]
    ox, oy = (W - tw) // 2 - bx[0], 250 * S - bx[1]
    md.text((ox, oy), "Diva", font=f_diva, fill=255)
    # contorno claro por baixo (dá o relevo dos posts)
    borda = masc.filter(ImageFilter.MaxFilter(21))
    camada.paste(Image.new("RGBA", (W, H), ROXO_ESCURO + (255,)), (0, 0), borda)
    # degradê só na altura das letras
    g = degrade((W, th), ROXO_CLARO, ROXO)
    cheio = Image.new("RGB", (W, H), ROXO)
    cheio.paste(g, (0, oy + bx[1]))
    camada.paste(cheio, (0, 0), masc)
    d = ImageDraw.Draw(camada)
    # coroa sobre o D
    topo = oy + bx[1]
    coroa(d, (W - tw) // 2 + tw * .5, topo - 34 * S, 112 * S, ROXO_CLARO + (255,), 10 * S)
    # "TATTOO" em pincel, inclinado
    f_tat = fonte("KaushanScript-Regular.ttf", 150 * S)
    t = Image.new("RGBA", (W, 260 * S), (0, 0, 0, 0))
    td = ImageDraw.Draw(t)
    tb = td.textbbox((0, 0), "TATTOO", font=f_tat)
    tx = (W - (tb[2] - tb[0])) // 2 - tb[0]
    td.text((tx, 40 * S), "TATTOO", font=f_tat, fill=TINTA + (255,), stroke_width=10 * S, stroke_fill=TINTA + (255,))
    td.text((tx, 40 * S), "TATTOO", font=f_tat, fill=ROXO + (255,), stroke_width=int(2.5 * S), stroke_fill=ROXO + (255,))
    t = t.rotate(5, resample=Image.BICUBIC, expand=False)
    camada.alpha_composite(t, (110 * S, oy + bx[3] - 80 * S))
    # brilhos
    brilho(d, (W + tw) // 2 + 30 * S, topo + 30 * S, 46 * S, PAPEL + (255,))
    brilho(d, (W - tw) // 2 - 10 * S, oy + bx[3] + 110 * S, 30 * S, ROXO_CLARO + (255,))
    caixa = camada.getbbox()
    camada = camada.crop(caixa)
    return camada.resize((camada.width // S, camada.height // S), Image.LANCZOS)

def icone(tam):
    S = 8; s = tam * S
    im = Image.new("RGB", (s, s), TINTA)
    d = ImageDraw.Draw(im)
    f = fonte("UnifrakturCook-Bold.ttf", int(s * .86))
    bx = d.textbbox((0, 0), "D", font=f)
    x = (s - (bx[2] - bx[0])) / 2 - bx[0]
    y = (s - (bx[3] - bx[1])) / 2 - bx[1] + s * .06
    masc = Image.new("L", (s, s), 0)
    ImageDraw.Draw(masc).text((x, y), "D", font=f, fill=255)
    im.paste(degrade((s, s), ROXO_CLARO, ROXO), (0, 0), masc)
    if tam >= 64:
        coroa(d, s / 2, y + bx[1] - s * .02, s * .26, ROXO_CLARO, max(2, int(s * .022)))
    return im.resize((tam, tam), Image.LANCZOS)

def og(lg):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), TINTA)
    foto = ImageOps.fit(Image.open(RAIZ / "assets/obras/olho-nuvem-t.webp").convert("RGB"), (440, 560), centering=(.5, .45))
    moldura = Image.new("RGB", (452, 572), ROXO)
    moldura.paste(foto, (6, 6))
    moldura = moldura.convert("RGBA").rotate(-3, expand=True, resample=Image.BICUBIC)
    im.paste(moldura, (W - moldura.width - 40, (H - moldura.height) // 2), moldura)
    l = lg.copy(); l.thumbnail((620, 400), Image.LANCZOS)
    im.paste(l, (60, 60), l)
    d = ImageDraw.Draw(im)
    f = fonte("GrenzeGotisch.ttf", 34, "SemiBold")
    d.text((70, 500), "Pontilhismo · Fineline · Blackwork · Old School", font=f, fill=PAPEL)
    d.text((70, 548), "Praça da Árvore · São Paulo", font=f.font_variant(size=28), fill=ROXO_CLARO)
    im.save(IMG / "og.jpg", quality=88)

if __name__ == "__main__":
    lg = logo()
    lg.save(IMG / "logo-diva.png")
    lg.save(IMG / "logo-diva.webp", quality=92, method=6)
    print("logo", lg.size)
    icone(32).save(IMG / "favicon-32.png")
    icone(180).save(IMG / "apple-touch-icon.png")
    icone(512).save(IMG / "icone-512.png")
    og(lg)
