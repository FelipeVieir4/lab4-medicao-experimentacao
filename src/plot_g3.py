"""G3: erro tipo I dos dois testes em cada situação simulada, com linha em 5% (Q1 e Q3)."""
import plotly.graph_objects as go

from src.theme import ALTURA, CORES_TESTE, VERMELHO
from src.scenarios import CENARIOS


def fig_g3(df, alfa=0.05):
    """df: saída de run_type1 (cenario, teste, erro_tipo1)."""
    nomes = list(CENARIOS)
    rotulos = [CENARIOS[n].rotulo for n in nomes]
    fig = go.Figure()
    for teste, cor in CORES_TESTE.items():
        sub = df[df["teste"] == teste].set_index("cenario").reindex(nomes)
        valores = sub["erro_tipo1"] * 100
        fig.add_trace(
            go.Bar(x=rotulos, y=valores, name=teste, marker_color=cor,
                   text=[f"{v:.1f}%" for v in valores], textposition="outside",
                   hovertemplate="%{x}<br>" + teste + ": %{y:.2f}%<extra></extra>")
        )
    fig.add_hline(y=alfa * 100, line=dict(color=VERMELHO, dash="dash", width=1.5),
                  annotation_text=f"α = {alfa:.0%} (esperado)", annotation_position="top left")
    topo = max(alfa * 100, float(df["erro_tipo1"].max()) * 100) * 1.3
    fig.update_xaxes(title_text="Situação simulada (H₀ verdadeira, d = 0)")
    fig.update_yaxes(title_text="Erro tipo I (% de conjuntos com p < α)", range=[0, topo], ticksuffix="%")
    fig.update_layout(title="G3 – Erro tipo I: t de Welch × Mann-Whitney em cada situação (linha em 5%)",
                      barmode="group", bargap=0.3, bargroupgap=0.08, legend_title_text="Teste", height=ALTURA)
    return fig
