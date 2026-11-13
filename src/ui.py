"""Componentes visuais do dashboard: abas, cartões arredondados, transições e blocos simétricos (Welch | Mann-Whitney)."""
from html import escape

import streamlit as st

from src import theme  # noqa: F401  (registra o template Plotly)
from src.theme import CORES_TESTE, FONTE

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root {
  --ease: cubic-bezier(.2, .8, .2, 1);
  --txt: #1D1D1F; --txt2: #6E6E73; --linha: rgba(0,0,0,.06);
}
html, body, .stApp, .stMarkdown, .stCaption, h1, h2, h3, h4, p, li, td, th, button {
  font-family: Inter, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif !important;
}
.stApp {
  background:
    radial-gradient(1200px 600px at 0% -10%, rgba(10,132,255,.10), transparent 60%),
    radial-gradient(900px 500px at 100% 0%, rgba(94,92,230,.10), transparent 60%),
    radial-gradient(900px 600px at 50% 120%, rgba(255,159,10,.07), transparent 60%),
    #F5F5F7;
  background-attachment: fixed;
}
header[data-testid="stHeader"] { display: none; }
.block-container { max-width: 1680px; padding: 1.1rem 2.2rem 1.2rem; }
.stMarkdown p, .stMarkdown li { line-height: 1.6; color: var(--txt); font-size: .95rem; }
[data-testid="stCaptionContainer"] { color: var(--txt2) !important; }

/* Cabeçalho compacto */
.topo { display: flex; align-items: center; justify-content: space-between; gap: 24px; flex-wrap: wrap;
  margin-bottom: .35rem; animation: surgir .6s var(--ease) both; }
.topo .kick { font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: var(--txt2); font-weight: 600; }
.topo h1 { font-size: 1.6rem !important; font-weight: 700; letter-spacing: -.03em; margin: 0; padding: .15rem 0 0; color: var(--txt); }
.topo h1 span { background: linear-gradient(90deg, #0A84FF, #5E5CE6 55%, #FF9F0A); -webkit-background-clip: text; background-clip: text; color: transparent; }

/* Abas = controle segmentado com indicador deslizante */
.stTabs [data-baseweb="tab-list"] {
  gap: 2px; padding: 4px; background: rgba(118,118,128,.12); border-radius: 14px; width: fit-content; max-width: 100%;
  backdrop-filter: blur(20px); overflow-x: auto; scrollbar-width: none;
}
.stTabs [data-baseweb="tab"] {
  height: 36px; padding: 0 16px; border-radius: 10px; background: transparent !important; z-index: 1;
  color: var(--txt2); font-weight: 500; font-size: .88rem; transition: color .25s var(--ease);
}
.stTabs [data-baseweb="tab"] p { font-size: .88rem; font-weight: 500; }
.stTabs [data-baseweb="tab"]:hover { color: var(--txt); }
.stTabs [data-baseweb="tab"][aria-selected="true"] { color: var(--txt); }
.stTabs [data-baseweb="tab"][aria-selected="true"] p { font-weight: 600; }
.stTabs [data-baseweb="tab-highlight"] {
  height: calc(100% - 8px) !important; bottom: 4px !important; border-radius: 10px; z-index: 0;
  background: #FFFFFF !important; box-shadow: 0 1px 2px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.08);
  transition: left .45s var(--ease), width .45s var(--ease) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none; }
.stTabs [data-baseweb="tab-panel"] { padding-top: .9rem; }
.stTabs [data-baseweb="tab-panel"] > div { animation: surgir .5s var(--ease) both; }

@keyframes surgir { from { opacity: 0; transform: translateY(10px) scale(.995); } to { opacity: 1; transform: none; } }
@keyframes subir { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }

/* Cartão */
div[class*="st-key-card-"] {
  background: #FFFFFF;
  border: 1px solid rgba(255,255,255,.7); border-radius: 22px;
  box-shadow: 0 0 0 1px var(--linha), 0 2px 6px rgba(0,0,0,.03), 0 24px 48px -12px rgba(0,0,0,.10);
  padding: 22px 30px 24px;
}
div[class*="st-key-card-"] h2 { font-size: 1.3rem; font-weight: 650; letter-spacing: -.02em; padding: 0 0 .2rem; color: var(--txt); }
div[class*="st-key-card-"] h2 a { display: none; }

/* Pílulas de link */
.pills { display: flex; flex-wrap: wrap; gap: 8px; }
.pill { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: 999px;
  background: rgba(255,255,255,.75); box-shadow: 0 0 0 1px var(--linha); color: var(--txt) !important;
  font-size: .8rem; font-weight: 500; text-decoration: none !important; transition: all .25s var(--ease); }
.pill b { color: var(--txt2); font-weight: 500; }
a.pill:hover { transform: translateY(-1px); box-shadow: 0 0 0 1px rgba(10,132,255,.35), 0 6px 16px rgba(10,132,255,.15); }

/* Blocos lado a lado (Welch | Mann-Whitney) */
.tiles { display: grid; grid-template-columns: repeat(var(--n, 2), 1fr); gap: 12px; margin: .1rem 0 .9rem; }
.tile { position: relative; overflow: hidden; background: linear-gradient(180deg, #FBFBFD, #F4F4F7); border-radius: 16px; padding: 14px 16px;
  box-shadow: 0 0 0 1px var(--linha), 0 1px 2px rgba(0,0,0,.04);
  transition: transform .3s var(--ease), box-shadow .3s var(--ease); animation: subir .55s var(--ease) both; }
.tile:nth-child(2) { animation-delay: .07s; } .tile:nth-child(3) { animation-delay: .14s; }
.tile::before { content: ""; position: absolute; inset: 0 auto 0 0; width: 3px; background: var(--c); }
.tile:hover { transform: translateY(-2px); box-shadow: 0 0 0 1px var(--linha), 0 12px 24px -8px rgba(0,0,0,.15); }
.tile .lbl { display: flex; align-items: center; gap: 7px; font-size: .76rem; color: var(--txt2); font-weight: 500; }
.tile .dot { width: 8px; height: 8px; border-radius: 50%; flex: none; background: var(--c); box-shadow: 0 0 0 3px color-mix(in srgb, var(--c) 20%, transparent); }
.tile .val { font-size: 1.5rem; font-weight: 650; letter-spacing: -.025em; color: var(--txt); margin-top: 4px; }
.tile .sub { font-size: .76rem; color: var(--txt2); margin-top: 2px; }
.kicker { font-size: .8rem; letter-spacing: .01em; color: var(--txt2); font-weight: 600; margin-bottom: .4rem; }

/* Mensagem final em destaque */
.destaque { position: relative; overflow: hidden; border-radius: 18px; padding: 18px 24px; margin: .2rem 0 1.1rem;
  background: linear-gradient(135deg, rgba(10,132,255,.08), rgba(94,92,230,.08) 55%, rgba(255,159,10,.08));
  box-shadow: 0 0 0 1px rgba(10,132,255,.18); animation: subir .55s var(--ease) both; }
.destaque .t { font-size: .8rem; font-weight: 600; color: #0A84FF; margin-bottom: .35rem; }
.destaque .f { font-size: 1.12rem; line-height: 1.55; font-weight: 500; color: var(--txt); letter-spacing: -.01em; }
.destaque .n { font-size: .78rem; color: var(--txt2); margin-top: .5rem; }

[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; box-shadow: 0 0 0 1px var(--linha); }
[data-testid="stPlotlyChart"] { border-radius: 16px; overflow: hidden; }
</style>
"""


def aplicar_estilo():
    st.markdown(_CSS, unsafe_allow_html=True)


def card(nome: str):
    """Cartão translúcido com cantos arredondados."""
    return st.container(key=f"card-{nome}")


def colunas():
    """Divisão padrão de toda seção com gráfico: gráfico (3) | texto (2)."""
    return st.columns([3, 2], gap="large", vertical_alignment="center")


def grafico(fig):
    # Definidos na própria figura: o Streamlit troca fundo e fonte quando eles vêm só do template.
    fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font_family=FONTE)
    st.plotly_chart(fig, width="stretch", theme=None, config={"displaylogo": False, "displayModeBar": False})


def br(x: float, casas: int = 1, pct: bool = False) -> str:
    """Número no formato brasileiro (vírgula decimal)."""
    s = f"{x * 100 if pct else x:.{casas}f}".replace(".", ",")
    return s + ("%" if pct else "")


def kicker(texto: str):
    st.markdown(f'<div class="kicker">{escape(texto)}</div>', unsafe_allow_html=True)


def tiles(itens):
    """itens: lista de (rótulo, cor, valor, subtítulo). Renderiza blocos lado a lado."""
    html = "".join(
        f'<div class="tile" style="--c:{cor}"><div class="lbl"><span class="dot"></span>{escape(rot)}</div>'
        f'<div class="val">{escape(val)}</div><div class="sub">{escape(sub)}</div></div>'
        for rot, cor, val, sub in itens
    )
    st.markdown(f'<div class="tiles" style="--n:{len(itens)}">{html}</div>', unsafe_allow_html=True)


def duelo(welch_val: str, mw_val: str, sub_w: str = "", sub_m: str = ""):
    """Welch sempre à esquerda, Mann-Whitney sempre à direita."""
    tiles([("t de Welch", CORES_TESTE["t de Welch"], welch_val, sub_w),
           ("Mann-Whitney", CORES_TESTE["Mann-Whitney"], mw_val, sub_m)])


def destaque(titulo: str, frase_html: str, nota: str = ""):
    """Faixa de destaque com a mensagem principal. frase_html já deve vir escapada (aceita <b>)."""
    n = f'<div class="n">{escape(nota)}</div>' if nota else ""
    st.markdown(f'<div class="destaque"><div class="t">{escape(titulo)}</div><div class="f">{frase_html}</div>{n}</div>',
                unsafe_allow_html=True)


def pills(links):
    """links: lista de (rótulo, url). URLs que não começam com http viram texto."""
    partes = []
    for rot, url in links:
        if str(url).startswith("http"):
            partes.append(f'<a class="pill" href="{escape(url)}" target="_blank"><b>{escape(rot)}</b> {escape(url.split("//")[-1])}</a>')
        else:
            partes.append(f'<span class="pill"><b>{escape(rot)}</b> {escape(str(url))}</span>')
    st.markdown(f'<div class="pills" style="justify-content:flex-end">{"".join(partes)}</div>', unsafe_allow_html=True)


def topo(titulo: str, kicker_txt: str, links):
    """Cabeçalho em uma linha: título à esquerda, links à direita."""
    t1, _, t2 = titulo.partition(":")
    titulo_html = f"{escape(t1)}:<span>{escape(t2)}</span>" if t2 else escape(titulo)
    esq, dir_ = st.columns([3, 2], vertical_alignment="center")
    with esq:
        st.markdown(f'<div class="topo"><div><div class="kick">{escape(kicker_txt)}</div><h1>{titulo_html}</h1></div></div>',
                    unsafe_allow_html=True)
    with dir_:
        pills(links)
