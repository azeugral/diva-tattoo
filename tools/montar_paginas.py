"""Monta as páginas da raiz a partir de tools/paginas/*.html (só o <main>) + cabeçalho e rodapé comuns.
Cada arquivo começa com 3 linhas:  título | descrição | item do menu ativo (ou -)
Uso: python tools/montar_paginas.py"""
import pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parents[1]
V = 2  # subir a cada deploy que mude CSS/JS
ATUAL = ' aria-current="page"'
MENU = [("index.html", "Início"), ("trabalhos.html", "Trabalhos"), ("cuidados.html", "Cuidados"), ("orcamento.html", "Orçamento")]

CABECA = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0a080d">
<meta property="og:type" content="website">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/og.jpg">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Grenze+Gotisch:wght@600;700;800&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Kaushan+Script&display=swap">
<link rel="stylesheet" href="assets/css/estilo.css?v={v}">
</head>
<body>
<header class="topo">
  <div class="wrap topo__in">
    <a class="marca" href="index.html" aria-label="Diva Tattoo, início"><img src="assets/img/logo-diva.webp?v={v}" alt="Diva Tattoo" width="824" height="556"></a>
    <nav aria-label="Principal"><ul class="menu">{menu}</ul></nav>
  </div>
</header>
<main id="conteudo">
"""

RODAPE = """</main>
<footer class="rodape">
  <div class="wrap">
    <div class="rodape__in">
      <div>
        <a class="marca" href="index.html"><img src="assets/img/logo-diva.webp?v={v}" alt="Diva Tattoo" width="824" height="556" loading="lazy" style="height:96px"></a>
        <p>Pontilhismo, fineline, blackwork e old school na Praça da Árvore, São Paulo.</p>
        <span class="estacao"><span class="estacao__linha" aria-hidden="true"></span>Praça da Árvore · Linha 1-Azul</span>
      </div>
      <div>
        <h4>Páginas</h4>
        <ul>{paginas}</ul>
      </div>
      <div>
        <h4>Redes</h4>
        <ul>
          <li><a href="https://www.instagram.com/divatattoo_oficial/" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="#" data-contato="Oi! Quero fazer uma tattoo.">Mensagem</a></li>
        </ul>
      </div>
    </div>
    <div class="rodape__fim">
      <span>© <span data-ano>2026</span> Diva Tattoo</span>
      <span>Site por <a href="https://lrgz.com.br" target="_blank" rel="noopener">L R G Z</a></span>
    </div>
  </div>
</footer>
{scripts}<script src="assets/js/main.js?v={v}" defer></script>
</body>
</html>
"""

def main():
    for f in sorted((RAIZ / "tools" / "paginas").glob("*.html")):
        linhas = f.read_text(encoding="utf-8").split("\n")
        titulo, desc, ativo = (l.strip() for l in linhas[:3])
        corpo = "\n".join(linhas[3:])
        menu = "".join(
            f'<li><a href="{h}"{ATUAL if h == ativo else ""}>{n}</a></li>' for h, n in MENU)
        paginas = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in MENU)
        scripts = f'<script src="assets/js/obras.js?v={V}" defer></script>\n' if "data-grade" in corpo else ""
        html = CABECA.format(titulo=titulo, desc=desc, menu=menu, v=V) + corpo.rstrip() + "\n" + RODAPE.format(paginas=paginas, scripts=scripts, v=V)
        (RAIZ / f.name).write_text(html, encoding="utf-8")
        print("ok", f.name)

if __name__ == "__main__":
    main()
