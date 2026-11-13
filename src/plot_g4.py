"""G4: curvas de poder dos dois testes no mesmo gráfico (proporção de rejeições × tamanho do efeito)."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.theme import ALTURA, CINZA, CORES_TESTE, VERMELHO
from src.scenarios import CENARIOS

META_PODER = 0.8


def fig_g4(df, alfa=0.05):
    """df: saída de run_power (cenario, d, teste, poder)."""
    nomes = list(CENARIOS)
    fig = make_subplots(rows=2, cols=2, shared_xaxes=True, shared_yaxes=True,
                        subplot_titles=[CENARIOS[n].rotulo for n in nomes],
                        vertical_spacing=0.16, horizontal_spacing=0.06)
    for i, nome in enumerate(nomes):
        row, col = i // 2 + 1, i % 2 + 1
        for teste, cor in CORES_TESTE.items():
            sub = df[(df["cenario"] == nome) & (df["teste"] == teste)]
            fig.add_trace(
                go.Scatter(x=sub["d"], y=sub["poder"], mode="lines+markers", name=teste, legendgroup=teste,
                           line=dict(color=cor, width=2), showlegend=(i == 0),
                           hovertemplate=f"{teste}<br>d = %{{x}}<br>poder = %{{y:.0%}}<extra></extra>"),
                row=row, col=col,
            )
        # Linhas de referência rotuladas em cada painel, para leitura sem consultar o título.
        fig.add_hline(y=alfa, line=dict(color=VERMELHO, dash="dot", width=1), row=row, col=col,
                      annotation_text=f"α = {alfa:.0%} (erro permitido)", annotation_position="top right",
                      annotation_font=dict(size=10, color=VERMELHO))
        fig.add_hline(y=META_PODER, line=dict(color=CINZA, dash="dash", width=1), row=row, col=col,
                      annotation_text=f"{META_PODER:.0%} = poder adequado", annotation_position="bottom right",
                      annotation_font=dict(size=10, color=CINZA))
    fig.update_xaxes(showticklabels=True, tickvals=[0, 0.25, 0.5, 0.75, 1, 1.5])
    fig.update_xaxes(title_text="Tamanho do efeito d (0 = bot sem efeito)", row=2)
    fig.update_yaxes(range=[0, 1.04], tickformat=".0%", dtick=0.2, showticklabels=True)
    fig.update_yaxes(title_text="Poder (% de bases em que detectou)", col=1)
    fig.update_layout(title="G4 – Poder: com que frequência cada teste detecta o efeito do bot",
                      legend_title_text="Teste", height=ALTURA)
    return fig
