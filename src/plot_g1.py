"""G1: dados reais ao lado dos dados simulados (histograma de cada grupo)."""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.theme import ALTURA, CORES_GRUPO

ROTULOS = {"com_bot": "Com bot de revisão", "sem_bot": "Sem bot de revisão"}


def fig_g1(real, simulado, bin_size=10, x_max=250):
    """real/simulado: dict grupo -> array de horas."""
    grupos = list(ROTULOS)
    bordas = np.arange(0, x_max + bin_size, bin_size)
    # Teto do eixo y calculado a partir das contagens: evita que o autorange corte as barras mais altas.
    y_max = max(np.histogram(np.clip(f[g], 0, x_max), bins=bordas)[0].max()
                for f in (real, simulado) for g in grupos)
    fig = make_subplots(
        rows=2, cols=2, shared_xaxes=True, shared_yaxes=True,
        row_titles=["Dados reais", "Dados simulados"],
        column_titles=[ROTULOS[g] for g in grupos],
        vertical_spacing=0.16, horizontal_spacing=0.06,
    )
    for col, g in enumerate(grupos, start=1):
        for row, fonte in enumerate((real, simulado), start=1):
            fig.add_trace(
                go.Histogram(
                    x=fonte[g], xbins=dict(start=0, end=x_max, size=bin_size),
                    marker_color=CORES_GRUPO[g], name=ROTULOS[g], legendgroup=g,
                    showlegend=(row == 1),
                    hovertemplate="%{x} h: %{y} PRs<extra></extra>",
                ),
                row=row, col=col,
            )
    # Rótulos de eixo em todos os painéis, para leitura imediata.
    fig.update_xaxes(range=[0, x_max], showticklabels=True, ticksuffix=" h")
    fig.update_xaxes(title_text="Horas até o merge (faixas de 10 h)", row=2)
    fig.update_yaxes(range=[0, y_max * 1.1], showticklabels=True,
                     dtick=max(1, int(np.ceil(y_max / 5))))
    fig.update_yaxes(title_text="Nº de PRs", col=1)
    fig.update_layout(
        title="G1 – Tempo até o merge: dados reais × simulados (lognormal)",
        legend_title_text="Grupo", height=ALTURA, bargap=0.08,
        margin=dict(b=8, t=72),
    )
    return fig
