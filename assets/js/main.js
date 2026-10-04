// Diva Tattoo — comportamento comum às páginas
const CONFIG = {
  // CONFIRMAR: número com DDI, só dígitos (ex.: 5511999999999). Vazio = copia a mensagem e abre a DM do Instagram.
  whatsapp: "",
  instagram: "divatattoo_oficial",
};

const ESTILOS = {
  pontilhismo: "Pontilhismo",
  fineline: "Fineline",
  blackwork: "Blackwork",
  "old-school": "Old School",
};

const reduzido = matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- contato ---------- */
async function enviarMensagem(texto) {
  if (CONFIG.whatsapp) {
    location.href = `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(texto)}`;
    return "whatsapp";
  }
  try { await navigator.clipboard.writeText(texto); } catch (e) { /* sem permissão: segue para a DM */ }
  window.open(`https://ig.me/m/${CONFIG.instagram}`, "_blank", "noopener");
  return "instagram";
}

document.addEventListener("click", (e) => {
  const a = e.target.closest("[data-contato]");
  if (!a) return;
  e.preventDefault();
  enviarMensagem(a.dataset.contato || "Oi! Quero fazer uma tattoo.");
});

/* ---------- revelar ao rolar (só abaixo da dobra) ---------- */
function revelar() {
  const els = document.querySelectorAll(".revela");
  if (reduzido || !("IntersectionObserver" in window)) { els.forEach((el) => el.classList.add("visivel")); return; }
  const io = new IntersectionObserver((ents) => {
    ents.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("visivel"); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  els.forEach((el) => {
    if (el.getBoundingClientRect().top < innerHeight) el.classList.add("visivel");
    else io.observe(el);
  });
}

/* ---------- grade de trabalhos ---------- */
function cartao(o, i) {
  return `<figure class="obra" role="button" tabindex="0" data-i="${i}" aria-label="${o.titulo}, ${ESTILOS[o.estilo]}. Ampliar">
    <img src="assets/obras/${o.slug}-t.webp?v=1" alt="Tattoo ${o.titulo}, ${ESTILOS[o.estilo]}" width="800" height="1000" loading="lazy" decoding="async">
    <figcaption>${o.titulo} · ${ESTILOS[o.estilo]}</figcaption>
  </figure>`;
}

function montarGrade(grade) {
  const todas = window.OBRAS || [];
  const limite = Number(grade.dataset.limite) || 0;
  const filtros = document.querySelector(".filtros");
  let lista = todas;

  const desenhar = () => {
    const estilo = filtros ? location.hash.slice(1) : "";
    lista = ESTILOS[estilo] ? todas.filter((o) => o.estilo === estilo) : todas;
    if (limite) lista = lista.slice(0, limite);
    grade.innerHTML = lista.map(cartao).join("");
    if (filtros) {
      filtros.querySelectorAll("a").forEach((a) => a.setAttribute("aria-current", String(a.hash.slice(1) === (ESTILOS[estilo] ? estilo : "todos"))));
    }
  };
  desenhar();

  addEventListener("hashchange", () => {
    if (reduzido) return desenhar();
    grade.classList.add("trocando");
    setTimeout(() => { desenhar(); requestAnimationFrame(() => grade.classList.remove("trocando")); }, 200);
  });

  const abrir = (el) => ampliar(lista, Number(el.dataset.i));
  grade.addEventListener("click", (e) => { const el = e.target.closest(".obra"); if (el) abrir(el); });
  grade.addEventListener("keydown", (e) => {
    const el = e.target.closest(".obra");
    if (el && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); abrir(el); }
  });
}

/* ---------- visualização ampliada ---------- */
let amplia;
function ampliar(lista, i) {
  if (!amplia) {
    amplia = document.createElement("div");
    amplia.className = "amplia";
    amplia.setAttribute("role", "dialog");
    amplia.setAttribute("aria-modal", "true");
    amplia.innerHTML = `
      <img alt="">
      <p class="amplia__legenda"></p>
      <button class="amplia__fechar" aria-label="Fechar"><svg viewBox="0 0 32 32"><path d="M8 8l16 16M24 8L8 24"/></svg></button>
      <button class="amplia__ant" aria-label="Anterior"><svg viewBox="0 0 32 32"><path d="M20 6L10 16l10 10"/></svg></button>
      <button class="amplia__prox" aria-label="Próxima"><svg viewBox="0 0 32 32"><path d="M12 6l10 10-10 10"/></svg></button>`;
    document.body.append(amplia);
  }
  const img = amplia.querySelector("img");
  const leg = amplia.querySelector(".amplia__legenda");
  let atual = i;
  const mostrar = (n) => {
    atual = (n + lista.length) % lista.length;
    const o = lista[atual];
    img.style.opacity = 0;
    const nova = new Image();
    nova.onload = () => { img.src = nova.src; img.alt = `Tattoo ${o.titulo}`; img.style.opacity = 1; };
    nova.src = `assets/obras/${o.slug}.webp?v=1`;
    leg.textContent = `${o.titulo} · ${ESTILOS[o.estilo]} · ${atual + 1}/${lista.length}`;
  };
  const fechar = () => {
    amplia.classList.remove("aberta");
    document.body.style.overflow = "";
    removeEventListener("keydown", teclas);
  };
  const teclas = (e) => {
    if (e.key === "Escape") fechar();
    if (e.key === "ArrowLeft") mostrar(atual - 1);
    if (e.key === "ArrowRight") mostrar(atual + 1);
  };
  amplia.onclick = (e) => {
    if (e.target.closest(".amplia__ant")) return mostrar(atual - 1);
    if (e.target.closest(".amplia__prox")) return mostrar(atual + 1);
    if (e.target === amplia || e.target.closest(".amplia__fechar")) fechar();
  };
  // arrastar para trocar no toque
  let x0 = null;
  img.onpointerdown = (e) => { x0 = e.clientX; };
  img.onpointerup = (e) => {
    if (x0 === null) return;
    const dx = e.clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) mostrar(atual + (dx < 0 ? 1 : -1));
  };
  addEventListener("keydown", teclas);
  document.body.style.overflow = "hidden";
  mostrar(i);
  requestAnimationFrame(() => amplia.classList.add("aberta"));
  amplia.querySelector(".amplia__fechar").focus({ preventScroll: true });
}

/* ---------- orçamento ---------- */
function montarOrcamento(form) {
  const aviso = form.querySelector(".aviso");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const v = (k) => (d.get(k) || "").toString().trim();
    if (!v("nome") || !v("ideia")) { aviso.textContent = "Preencha pelo menos o nome e a ideia."; return; }
    const larg = v("largura"), alt = v("altura");
    const se = (cond, txt) => (cond ? txt : null);
    const linhas = [
      `Oi! Meu nome é ${v("nome")} e quero fazer uma tattoo.`,
      "",
      `Ideia: ${v("ideia")}`,
      se(v("estilo"), `Estilo: ${v("estilo")}`),
      se(v("local"), `Local do corpo: ${v("local")}`),
      se(larg || alt, `Tamanho aproximado: ${larg || "?"} x ${alt || "?"} cm`),
      se(v("primeira"), `Primeira tattoo: ${v("primeira")}`),
      se(v("dias"), `Melhores dias: ${v("dias")}`),
      "",
      "Posso mandar a referência por aqui.",
    ].filter((l) => l !== null);
    const canal = await enviarMensagem(linhas.join("\n"));
    aviso.textContent = canal === "instagram"
      ? "Mensagem copiada. Cole na conversa do Instagram que abriu."
      : "Abrindo o WhatsApp…";
  });
}

/* ---------- início ---------- */
document.querySelectorAll("[data-grade]").forEach(montarGrade);
document.querySelectorAll("form[data-orcamento]").forEach(montarOrcamento);
revelar();
const ano = document.querySelector("[data-ano]");
if (ano) ano.textContent = new Date().getFullYear();
