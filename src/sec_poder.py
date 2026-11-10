"""Seção 5 do dashboard: Poder (G4)."""
import streamlit as st

from src.plot_g4 import fig_g4
from src.q2_power import ALFA, REPS, run_power


@st.cache_data
def _dados():
    return run_power()


def render():
    df = _dados()
    st.header("5. Poder")
    st.plotly_chart(fig_g4(df, ALFA), width="stretch")

    def poder(cen, teste, d):
        return float(df[(df["cenario"] == cen) & (df["teste"] == teste) & (df["d"] == d)]["poder"].iloc[0])

    mw_base, w_base = poder("base", "Mann-Whitney", 0.5), poder("base", "t de Welch", 0.5)
    mw_max, w_max = poder("base", "Mann-Whitney", 1.5), poder("base", "t de Welch", 1.5)
    mw_peq, w_peq = poder("amostra_pequena", "Mann-Whitney", 1.0), poder("amostra_pequena", "t de Welch", 1.0)
    st.markdown(
        f"Cada ponto é a proporção de {REPS:,} conjuntos simulados em que o teste rejeitou H₀ (α = {ALFA:.2f}); "
        "d = 0 é o caso sem efeito, e as linhas tracejadas marcam 5% e 80%. "
        f"Com dados lognormais, o **Mann-Whitney detecta melhor o efeito em todas as situações**: com d = 0,5 no cenário base, "
        f"ele rejeita {mw_base:.0%} das vezes contra {w_base:.0%} do Welch. "
        f"A vantagem não muda de lado, só de tamanho: o Welch chega a apenas {w_max:.0%} com d = 1,5 no cenário base, enquanto o Mann-Whitney chega a {mw_max:.0%}. "
        f"Com amostras pequenas (n = 10) os dois perdem poder (com d = 1: {mw_peq:.0%} contra {w_peq:.0%})."
    )
