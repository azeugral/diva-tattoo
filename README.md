# Diva Tattoo

Site da tatuadora Diva ([@divatattoo_oficial](https://www.instagram.com/divatattoo_oficial/)), na Praça da Árvore (Linha 1-Azul), São Paulo.
Estilos: pontilhismo, fineline, blackwork e old school.

HTML, CSS e JS puros, sem build. Prévia em GitHub Pages, com `noindex` e `robots.txt` bloqueando até ter domínio.

## Estrutura

- `index.html`, `trabalhos.html`, `orcamento.html`, `cuidados.html`, `404.html`: **gerados**. Editar o `<main>` em `tools/paginas/*.html` e rodar `python tools/montar_paginas.py` (cabeçalho, rodapé e `?v=` vêm de lá).
- `assets/obras/`: tattoos em WebP, `-t` = recorte 4:5 800×1000, sem sufixo = inteira até 1600 px.
- `assets/js/obras.js`: **gerado** por `python tools/processar.py` a partir da lista `OBRAS` do script (lê os originais de `../_ref/Diva`).
- `assets/js/main.js`: `CONFIG.whatsapp` e `CONFIG.instagram`, grade, filtro por hash, imagem ampliada, orçamento.
- `tools/gerar_icones.py`: favicon (marcador de estação) e `og.jpg`.

A cada deploy que mude CSS/JS, subir `V` em `tools/montar_paginas.py` e remontar.

## CONFIRMAR

Tudo que está pendente aparece no site com contorno tracejado azul (`.a-confirmar`).

1. Nome dela (o site usa só "Diva") e texto do "Quem tatua".
2. Foto dela em boa resolução (a recebida tem 100×100 px). Hoje o Sobre usa um frame dela tatuando.
3. WhatsApp com DDI. Sem ele, o orçamento copia a mensagem e abre a DM do Instagram.
4. Endereço do estúdio, ou confirmar que ele só é enviado depois de marcar.
5. Dias e horários de atendimento.
6. Regras do sinal e forma de pagamento.
7. Texto de cuidados (destaque "cuidados." do Instagram) e frequência da pomada.
8. Passo a passo do destaque "medindo sua arte".
9. Classificação de estilo de cada tattoo (feita por mim, em `tools/processar.py`).
10. Fotos com legenda de story por cima (Plataforma 9¾ tem "Eu amo Harry Potter"): pedir os originais.
11. Escudo 1910 (marca de clube): ok mostrar no portfólio?
12. Desenhos autorais / flash disponíveis (destaque "autorais").
13. Logo, se ela tiver. Hoje a marca é tipográfica.
14. Domínio.
