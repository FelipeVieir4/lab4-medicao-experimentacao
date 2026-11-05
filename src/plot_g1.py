"""G1: dados reais ao lado dos dados simulados (histograma de cada grupo)."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CORES_GRUPO = {"com_bot": "#2a9d8f", "sem_bot": "#8d6e63"}
ROTULOS = {"com_bot": "Com bot de revisão", "sem_bot": "Sem bot de revisão"}


def fig_g1(real, simulado, bin_size=10, x_max=250):
    """real/simulado: dict grupo -> array de horas."""
    grupos = list(ROTULOS)
    fig = make_subplots(
        rows=2, cols=2, shared_xaxes=True, shared_yaxes=True,
        row_titles=["Dados reais", "Dados simulados"],
        column_titles=[ROTULOS[g] for g in grupos],
        vertical_spacing=0.1, horizontal_spacing=0.05,
    )
    for col, g in enumerate(grupos, start=1):
        for row, fonte in enumerate((real, simulado), start=1):
            fig.add_trace(
                go.Histogram(
                    x=fonte[g], xbins=dict(start=0, end=x_max, size=bin_size),
                    marker_color=CORES_GRUPO[g], name=ROTULOS[g], legendgroup=g,
                    showlegend=(row == 1),
                ),
                row=row, col=col,
            )
    fig.update_xaxes(title_text="Horas até o merge", range=[0, x_max], row=2)
    fig.update_yaxes(title_text="Nº de PRs", col=1)
    fig.update_layout(
        title="G1 – Tempo até o merge: dados reais × simulados (lognormal)",
        legend_title_text="Grupo", height=520, bargap=0.05,
    )
    return fig
