"""Paleta única do projeto (cores de sistema do macOS) e template Plotly usado em todos os gráficos."""
import plotly.graph_objects as go
import plotly.io as pio

FONTE = 'Inter, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif'

TEXTO = "#1D1D1F"
TEXTO_2 = "#6E6E73"
GRADE = "#E5E5EA"
CINZA = "#8E8E93"

AZUL = "#0A84FF"       # t de Welch
LARANJA = "#FF9F0A"    # Mann-Whitney
INDIGO = "#5E5CE6"     # grupo com bot
MENTA = "#00C7BE"      # grupo sem bot
VERMELHO = "#FF3B30"   # região de rejeição / α

CORES_TESTE = {"t de Welch": AZUL, "Mann-Whitney": LARANJA}
CORES_GRUPO = {"com_bot": INDIGO, "sem_bot": MENTA}

ALTURA = 540  # todos os gráficos com a mesma altura (cabe na tela sem rolagem)

_eixo = dict(gridcolor=GRADE, linecolor=GRADE, zeroline=False, ticks="",
             tickfont=dict(color=TEXTO_2, size=11), title=dict(font=dict(color=TEXTO_2, size=12)))

pio.templates["mac"] = go.layout.Template(layout=dict(
    font=dict(family=FONTE, size=13, color=TEXTO),
    title=dict(font=dict(size=15, color=TEXTO, weight=600), x=0, xanchor="left", y=0.97, yanchor="top"),
    paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",  # mesmo branco do cartão
    colorway=[AZUL, LARANJA, INDIGO, MENTA, VERMELHO, CINZA],
    xaxis=_eixo, yaxis=_eixo,
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18, yanchor="top",
                bgcolor="rgba(0,0,0,0)", font=dict(size=12, color=TEXTO_2), title=dict(font=dict(color=TEXTO_2))),
    margin=dict(l=8, r=8, t=64, b=8),
    annotationdefaults=dict(font=dict(size=12, color=TEXTO_2)),
    hoverlabel=dict(bgcolor="white", bordercolor=GRADE, font=dict(family=FONTE, color=TEXTO)),
    barcornerradius=6,
    height=ALTURA,
))
pio.templates.default = "plotly_white+mac"
