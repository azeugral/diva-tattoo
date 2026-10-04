"""Gera as versões WebP das tattoos e o assets/js/obras.js.
Uso: python tools/processar.py  (lê de ../_ref/Diva)"""
import json, pathlib
from PIL import Image, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parents[1]
ORIG = RAIZ.parent / "_ref" / "Diva"
SAIDA = RAIZ / "assets" / "obras"

# prefixo do arquivo, slug, título, estilo, foco vertical do recorte 4:5 (0 topo, 1 base), corte inferior em % (legendas de story)
OBRAS = [
    ("830281675", "betty-boop", "Betty Boop", "old-school", .5, 0),
    ("829226016", "1990-dedos", "1990 nos dedos", "blackwork", .5, 0),
    ("825325967", "1910", "Escudo 1910", "blackwork", .45, 0),
    ("819123738", "escorpiao", "Escorpião", "old-school", .5, 0),
    ("817096459", "aranha", "Aranha", "old-school", .45, 0),
    ("814126751", "harry-potter", "Plataforma 9¾", "fineline", .45, 0),
    ("812940868", "lua-coracao", "Lua e coração", "fineline", .4, 0),
    ("811616679", "z-cruzes", "Z e cruzes", "fineline", .5, 0),
    ("811405260", "cruz-pescoco", "Cruz no pescoço", "blackwork", .3, 0),
    ("810962665", "louros-1973", "Louros 1973", "fineline", .55, 0),
    ("806366157", "tubarao", "Tubarão", "fineline", .45, 0),
    ("806280663", "trinacria", "Trinácria", "fineline", .4, 0),
    ("806141757", "olho-1985", "Olho 1985", "pontilhismo", .3, 22),
    ("797229256", "punhais", "Punhais cruzados", "old-school", .45, 0),
    ("790267484", "sol-espinhos", "Sol de espinhos", "blackwork", .5, 0),
    ("764711626", "floral-braco", "Floral no braço", "blackwork", .5, 0),
    ("749184363", "camaleao", "Camaleão", "blackwork", .5, 0),
    ("748740290", "coracao-pontilhado", "Coração pontilhado", "pontilhismo", .5, 0),
    ("713824089", "olho-nuvem", "Olho na nuvem", "pontilhismo", .45, 0),
    ("653524164", "bussola", "Bússola", "fineline", .4, 0),
    ("640159197", "good-luck", "Good Luck", "blackwork", .4, 0),
    ("825324669", "lettering-mao", "Lettering na mão", "fineline", .5, 0),
]
EXTRAS = [("718221892", "processo")]  # foto dela tatuando

def achar(prefixo):
    return next(ORIG.glob(prefixo + "*"))

def recorte(im, prop, foco):
    w, h = im.size
    if w / h > prop:
        nw = round(h * prop); x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = round(w / prop); y = round((h - nh) * foco)
    return im.crop((0, y, w, y + nh))

def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    dados = []
    for pre, slug, titulo, estilo, foco, corte in OBRAS:
        im = ImageOps.exif_transpose(Image.open(achar(pre))).convert("RGB")
        if corte:
            im = im.crop((0, 0, im.width, round(im.height * (1 - corte / 100))))
        t = recorte(im, 4 / 5, foco).resize((800, 1000), Image.LANCZOS)
        t.save(SAIDA / f"{slug}-t.webp", quality=80, method=6)
        g = im.copy(); g.thumbnail((1600, 1600), Image.LANCZOS)
        g.save(SAIDA / f"{slug}.webp", quality=82, method=6)
        dados.append({"slug": slug, "titulo": titulo, "estilo": estilo, "w": g.width, "h": g.height})
    for pre, slug in EXTRAS:
        im = ImageOps.exif_transpose(Image.open(achar(pre))).convert("RGB")
        recorte(im, 4 / 5, .5).save(RAIZ / "assets" / "img" / f"{slug}.webp", quality=82, method=6)
    # foto dela (versão melhorada que o usuário mandou em 04/10), em cor, levemente dessaturada
    from PIL import ImageEnhance
    f = ImageOps.exif_transpose(Image.open(RAIZ.parent / "_ref" / "foto-dela-hd.webp")).convert("RGB")
    f = ImageOps.fit(f, (1000, 1000), Image.LANCZOS)
    ImageEnhance.Color(f).enhance(.85).save(RAIZ / "assets" / "img" / "diva.webp", quality=84, method=6)
    js = "// gerado por tools/processar.py: não editar à mão\nwindow.OBRAS = " + json.dumps(dados, ensure_ascii=False, indent=1) + ";\n"
    (RAIZ / "assets" / "js" / "obras.js").write_text(js, encoding="utf-8")
    print(len(dados), "obras")

if __name__ == "__main__":
    main()
