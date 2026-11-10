"""G4: curvas de poder dos dois testes no mesmo gráfico (proporção de rejeições × tamanho do efeito)."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.plot_g2 import CORES_TESTE
from src.scenarios import CENARIOS


def fig_g4(df, alfa=0.05):
    """df: saída de run_power (cenario, d, teste, poder)."""
    nomes = list(CENARIOS)
    fig = make_subplots(rows=2, cols=2, shared_xaxes=True, shared_yaxes=True,
                        subplot_titles=[CENARIOS[n].rotulo for n in nomes],
                        vertical_spacing=0.14, horizontal_spacing=0.05)
    for i, nome in enumerate(nomes):
        row, col = i // 2 + 1, i % 2 + 1
        for teste, cor in CORES_TESTE.items():
            sub = df[(df["cenario"] == nome) & (df["teste"] == teste)]
            fig.add_trace(
                go.Scatter(x=sub["d"], y=sub["poder"], mode="lines+markers", name=teste, legendgroup=teste,
                           line=dict(color=cor, width=2), showlegend=(i == 0)),
                row=row, col=col,
            )
        fig.add_hline(y=alfa, line=dict(color="gray", dash="dot"), row=row, col=col)
        fig.add_hline(y=0.8, line=dict(color="gray", dash="dash"), row=row, col=col)
    fig.update_xaxes(title_text="Tamanho do efeito d (desvios-padrão do log do tempo)", row=2)
    fig.update_yaxes(title_text="Proporção de rejeições (poder)", range=[0, 1.02], col=1)
    fig.update_layout(title="G4 – Curvas de poder: t de Welch × Mann-Whitney (linhas: 5% e 80%)",
                      legend_title_text="Teste", height=620)
    return fig
