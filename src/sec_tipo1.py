"""Seção 4 do dashboard: Erro tipo I (G3)."""
import streamlit as st

from src import ui
from src.plot_g3 import fig_g3
from src.q1_type1 import ALFA, REPS, run_type1
from src.scenarios import CENARIOS

TOLERANCIA = 0.01  # "perto de 5%": até 1 ponto percentual de distância


@st.cache_data
def _dados():
    return run_type1()


def render():
    df = _dados()

    def faixa(teste):
        s = df[df["teste"] == teste].set_index("cenario")["erro_tipo1"]
        return s.min(), s.max(), s.idxmin(), s.idxmax()

    w_min, w_max, w_cen_min, _ = faixa("t de Welch")
    m_min, m_max, _, _ = faixa("Mann-Whitney")
    longe = df[(df["erro_tipo1"] - ALFA).abs() > TOLERANCIA]
    desviou = sorted(longe["teste"].unique())
    m_perto = "Mann-Whitney" not in desviou
    w_perto = "t de Welch" not in desviou
    w_longe = int((longe["teste"] == "t de Welch").sum())
    w_onde = "em todas as situações" if w_longe == len(CENARIOS) else f"em {w_longe} das {len(CENARIOS)} situações"

    texto = (
        f"Cada barra é a proporção de {REPS:,} conjuntos simulados **sem efeito** (H₀ verdadeira) em que o teste "
        f"deu p < {ALFA:.2f}; o esperado é algo perto de 5% (consideramos \"perto\" até ±1 ponto percentual). "
        f"O **Mann-Whitney** {'ficou perto de 5% em todas as situações' if m_perto else 'se afastou de 5% em alguma situação'} "
        f"(entre {m_min:.1%} e {m_max:.1%}). "
        f"O **t de Welch** {'também ficou perto de 5%' if w_perto else f'se desviou {w_onde}, ficando **conservador**'} "
        f"(entre {w_min:.1%} e {w_max:.1%}, o menor em \"{CENARIOS[w_cen_min].rotulo}\"): com dados lognormais, os PRs "
        "muito demorados inflam a variância estimada junto com a média, a estatística t raramente cai na região de rejeição "
        "e o teste rejeita H₀ menos vezes do que deveria. "
        "Ser conservador não é \"erro\" grave por si só, mas indica que o Welch está mal calibrado aqui e, como mostra a "
        "seção seguinte, isso vem acompanhado de menos poder."
    )

    with ui.card("tipo1"):
        st.header("4. Erro tipo I")
        graf, txt = ui.colunas()
        with graf:
            ui.grafico(fig_g3(df, ALFA))
        with txt:
            ui.kicker(f"Erro tipo I nas {len(CENARIOS)} situações (esperado: 5%)")
            ui.duelo(f"{ui.br(w_min, pct=True)} – {ui.br(w_max, pct=True)}",
                     f"{ui.br(m_min, pct=True)} – {ui.br(m_max, pct=True)}",
                     "perto de 5%" if w_perto else "conservador", "perto de 5%" if m_perto else "fora de 5% ± 1 p.p.")
            st.markdown(texto)
