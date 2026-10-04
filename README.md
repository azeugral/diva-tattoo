# Diva Tattoo

Site da tatuadora Diva ([@divatattoo_oficial](https://www.instagram.com/divatattoo_oficial/)), na Praça da Árvore (Linha 1-Azul), São Paulo.
Estilos: pontilhismo, fineline, blackwork e old school.

HTML, CSS e JS puros, sem build. Prévia em GitHub Pages, com `noindex` e `robots.txt` bloqueando até ter domínio.

## Estrutura

- `index.html`, `trabalhos.html`, `orcamento.html`, `cuidados.html`, `404.html`: **gerados**. Editar o `<main>` em `tools/paginas/*.html` e rodar `python tools/montar_paginas.py` (cabeçalho, rodapé e `?v=` vêm de lá).
- `assets/obras/`: tattoos em WebP, `-t` = recorte 4:5 800×1000, sem sufixo = inteira até 1600 px.
- `assets/js/obras.js`: **gerado** por `python tools/processar.py` a partir da lista `OBRAS` do script (lê os originais de `../_ref/Diva`).
- `assets/js/main.js`: `CONFIG.whatsapp` e `CONFIG.instagram`, grade, filtro por hash, imagem ampliada, orçamento.
- `tools/gerar_logo.py`: logo, favicon, apple-touch e `og.jpg`.

A cada deploy que mude CSS/JS, subir `V` em `tools/montar_paginas.py` e remontar.

## Identidade (v2, 04/10)

Tirada dos posts dela: preto `#0a080d` com roxo forte `#9b4dff` (claro `#c9a2ff`), gótico e pincel.
- Logo gerado por `python tools/gerar_logo.py` ("Diva" em UnifrakturCook com degradê + "Tattoo" em Kaushan Script + brilhos ✦). Fontes em `../_ref/fontes`. Também gera favicon, apple-touch e `og.jpg`.
- Site: títulos em Grenze Gotisch, frases de destaque em Kaushan Script, texto e rótulos em IBM Plex Sans.
- Grão em todo o fundo, brilho roxo nos cantos, ✦ como separador e foto da abertura com borda rasgada roxa.
- O marcador de estação continua azul (é a Linha 1-Azul de verdade).

## A preencher

Campos sem dado aparecem como `<span class="a-preencher">a preencher</span>`.

1. Endereço e horários de atendimento (Início › Onde fica).
2. WhatsApp com DDI em `assets/js/main.js` (`CONFIG.whatsapp`). Sem ele, o orçamento copia a mensagem e abre a DM do Instagram.
3. Nome dela e foto em boa resolução. A abertura usa `_ref/foto-dela-hd.webp` (versão melhorada que o usuário mandou).
4. Textos de cuidados, sinal e medição estão genéricos: trocar pelos dela quando vierem.
5. Classificação de estilo de cada tattoo (feita por mim, em `tools/processar.py`).
6. Plataforma 9¾ tem legenda de story por cima: pedir o original. Escudo 1910 (marca de clube): ok mostrar?
7. Domínio.
