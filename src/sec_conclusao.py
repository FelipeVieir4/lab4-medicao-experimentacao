"""Seção 7 do dashboard: Conclusão (expectativa × resultado e recomendação)."""
import streamlit as st

from src import ui
from src.params import load_real
from src.q2_power import run_power
from src.tests import mannwhitney, welch


@st.cache_data
def _erro_tipo1():
    """Faixa do erro tipo I de cada teste entre as situações; None se a Q1 (src/q1_type1.py) ainda não existe."""
    try:
        from src.q1_type1 import run_type1
    except ModuleNotFoundError:
        return None
    df = run_type1()
    return {t: (float(g["erro_tipo1"].min()), float(g["erro_tipo1"].max())) for t, g in df.groupby("teste")}


@st.cache_data
def _resumo():
    df = load_real()
    com = df.loc[df["grupo"] == "com_bot", "horas"].to_numpy()
    sem = df.loc[df["grupo"] == "sem_bot", "horas"].to_numpy()
    pw = run_power()
    base = pw[pw["cenario"] == "base"]
    return welch(com, sem), mannwhitney(com, sem), base


def render():
    w, m, base = _resumo()
    tipo1 = _erro_tipo1()
    if tipo1:
        (wl, wh), (ml, mh) = tipo1["t de Welch"], tipo1["Mann-Whitney"]
        tipo1_txt = (f"No erro tipo I, o Mann-Whitney ficou entre {ml:.1%} e {mh:.1%} nas quatro situações, "
                     f"e o Welch entre {wl:.1%} e {wh:.1%}, ou seja, conservador: quase não rejeita H₀ quando deveria rejeitar 5%.")
    else:
        tipo1_txt = "O erro tipo I de cada teste está na seção 4."

    p = lambda teste, d: float(base[(base["teste"] == teste) & (base["d"] == d)]["poder"].iloc[0])
    with ui.card("conclusao"):
        st.header("7. Conclusão")
        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
            ui.kicker("O que esperávamos × o que encontramos")
            st.markdown(f"""Antes de simular, esperávamos que o **Mann-Whitney** se saísse melhor, porque os tempos de merge
são muito assimétricos e o Welch depende de médias, que os PRs demorados distorcem. A simulação confirmou isso. {tipo1_txt}
No poder, com d = 0,5 o Mann-Whitney detecta o efeito {p('Mann-Whitney', 0.5):.0%} das vezes e o Welch {p('t de Welch', 0.5):.0%};
o Mann-Whitney foi melhor em todas as situações, inclusive com outliers e amostra pequena. Nos dados reais (30 PRs por grupo),
o Mann-Whitney rejeitou H₀ (p = {m['p_valor']:.3f}) e o Welch não (p = {w['p_valor']:.3f}), o mesmo padrão da simulação.""")
        with c2:
            ui.kicker("Recomendação")
            st.markdown("""Para comparar o tempo até o merge com e sem bot, use o **Mann-Whitney**: ele mantém o erro tipo I perto de 5%
e tem bem mais poder com dados assimétricos. A escolha mudaria se os dados fossem aproximadamente simétricos (o Welch
perderia pouco, e compara médias, que têm interpretação direta em horas), se a pergunta fosse especificamente sobre a **média** (por exemplo, custo total de espera),
ou com amostras muito grandes, em que os dois tendem a concordar.""")
        with c3:
            ui.kicker("Principal limitação")
            st.markdown("""O estudo é observacional e usa um único repositório com 30 PRs por grupo: PRs com bot podem ser diferentes dos
sem bot (tamanho, tipo de mudança), então a diferença encontrada não prova que o bot causa a mudança no tempo. Além disso, a simulação assume
uma lognormal; outras formas de assimetria podem dar resultados diferentes.""")
