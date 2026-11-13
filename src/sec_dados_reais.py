"""Seção 6 do dashboard: Dados reais (tabela com os dois testes)."""
import numpy as np
import streamlit as st

from src import ui
from src.params import load_real
from src.real_analysis import ALFA, analisar
from src.theme import CORES_GRUPO


def _magnitude_r(r: float) -> str:
    """Faixas usuais para |r| / |delta de Cliff| (Romano et al., 2006)."""
    r = abs(r)
    return "desprezível" if r < 0.147 else "pequeno" if r < 0.33 else "médio" if r < 0.474 else "grande"


def _magnitude_d(d: float) -> str:
    """Faixas de Cohen para |d|."""
    d = abs(d)
    return "desprezível" if d < 0.2 else "pequeno" if d < 0.5 else "médio" if d < 0.8 else "grande"


@st.cache_data
def _dados():
    df = load_real()
    med = df.groupby("grupo")["horas"].median()
    return analisar(df), float(med["com_bot"]), float(med["sem_bot"]), df.groupby("grupo").size().to_dict()


def render():
    res, med_com, med_sem, n = _dados()
    tabela = res.rename(columns={
        "teste": "Teste", "estatistica": "Estatística (t ou z)", "p_valor": "p-valor",
        "tamanho_efeito": "Tamanho do efeito (d de Cohen / r bisserial)", "conclusao": "Conclusão",
    })
    w = res.set_index("teste").loc["t de Welch"]
    m = res.set_index("teste").loc["Mann-Whitney"]
    mesma = (w["p_valor"] < ALFA) == (m["p_valor"] < ALFA)

    with ui.card("reais"):
        st.header("6. Dados reais")
        tab, txt = ui.colunas()
        with tab:
            ui.kicker(f"Resultado dos dois testes ({n['com_bot']} PRs com bot × {n['sem_bot']} sem bot)")
            ui.duelo(f"p = {ui.br(w['p_valor'], 3)}", f"p = {ui.br(m['p_valor'], 4)}",
                     f"d de Cohen = {ui.br(w['tamanho_efeito'], 2)} · {w['conclusao']}",
                     f"r bisserial = {ui.br(m['tamanho_efeito'], 2)} · {m['conclusao']}")
            st.dataframe(
                tabela.style.format({"Estatística (t ou z)": "{:.2f}", "p-valor": "{:.4f}",
                                     "Tamanho do efeito (d de Cohen / r bisserial)": "{:.2f}"}),
                hide_index=True, width="stretch",
            )
            ui.tiles([("Mediana com bot", CORES_GRUPO["com_bot"], f"{ui.br(med_com)} h", "tempo até o merge"),
                      ("Mediana sem bot", CORES_GRUPO["sem_bot"], f"{ui.br(med_sem)} h", "tempo até o merge")])
        with txt:
            _texto(w, m, n, mesma, med_com, med_sem)


def _texto(w, m, n, mesma, med_com, med_sem):
    st.markdown(
        f"Com os {n['com_bot']} PRs com bot e {n['sem_bot']} sem bot, o **t de Welch** deu t = {w['estatistica']:.2f}, "
        f"p = {w['p_valor']:.3f} e d de Cohen = {w['tamanho_efeito']:.2f} (efeito {_magnitude_d(w['tamanho_efeito'])}), e "
        f"**{w['conclusao']}**; o **Mann-Whitney** deu z = {m['estatistica']:.2f}, p = {m['p_valor']:.4f} e correlação "
        f"bisserial por postos r = {m['tamanho_efeito']:.2f} (efeito {_magnitude_r(m['tamanho_efeito'])}), e **{m['conclusao']}**. "
        + ("Os dois testes chegaram à **mesma conclusão**. " if mesma else
           "Os dois testes **não chegaram à mesma conclusão**: o efeito tem tamanho parecido nos dois (em torno de 0,4), "
           "mas a variância inflada pelos PRs muito demorados deixa o Welch sem poder, como previsto pelas seções 4 e 5. ")
        + f"r = {m['tamanho_efeito']:.2f} quer dizer que, sorteando um PR de cada grupo, o com bot demora mais em cerca de "
        f"{(1 + m['tamanho_efeito']) / 2:.0%} das vezes, e a mediana passa de {med_sem:.1f} h (sem bot) para {med_com:.1f} h "
        "(com bot), quase um dia a mais: uma diferença com **importância prática** para quem espera o merge, embora o estudo "
        "seja observacional e não prove que o bot é a causa."
    )
