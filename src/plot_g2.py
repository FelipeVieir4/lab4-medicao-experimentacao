"""G2: distribuição da estatística do teste sob H0, região de rejeição e p-valor de um exemplo."""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

CORES_TESTE = {"t de Welch": "#1f77b4", "Mann-Whitney": "#ff7f0e"}
ALFA = 0.05


def _area(fig, x, y, cor, nome, row, col, opacity, show=True, largura=0):
    fig.add_trace(
        go.Scatter(x=x, y=y, mode="lines", fill="tozeroy", line=dict(width=largura, color=cor), fillcolor=cor,
                   opacity=opacity, name=nome, showlegend=show, legendgroup=nome, hoverinfo="skip"),
        row=row, col=col,
    )


def fig_g2(t_null, z_null, welch_res, mw_res, alfa=ALFA):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("t de Welch", "Mann-Whitney (z)"))
    paineis = [
        ("t de Welch", t_null, welch_res, stats.t(df=welch_res["gl"]), 1),
        ("Mann-Whitney", z_null, mw_res, stats.norm(), 2),
    ]
    for nome, sim, res, dist, col in paineis:
        cor = CORES_TESTE[nome]
        fig.add_trace(
            go.Histogram(x=sim, histnorm="probability density", xbins=dict(size=0.25), marker_color=cor,
                         opacity=0.35, name=f"{nome}: estatística simulada sob H0", legendgroup=nome),
            row=1, col=col,
        )
        xs = np.linspace(-6, 6, 600)
        fig.add_trace(go.Scatter(x=xs, y=dist.pdf(xs), mode="lines", line=dict(color=cor, width=2),
                                 name=f"{nome}: densidade teórica", legendgroup=nome), row=1, col=col)
        crit = dist.ppf(1 - alfa / 2)
        obs = res["estatistica"]
        cauda = xs[xs <= -abs(obs)], xs[xs >= abs(obs)]
        for k, seg in enumerate(cauda):
            if len(seg):
                _area(fig, seg, dist.pdf(seg), "#000000", f"p-valor do exemplo", 1, col, 0.5, show=(col == 1 and k == 0))
        esq, dir_ = xs[xs <= -crit], xs[xs >= crit]
        _area(fig, esq, dist.pdf(esq), "#d62728", f"Região de rejeição (α = {alfa:.2f})", 1, col, 0.7, show=(col == 1), largura=2)
        _area(fig, dir_, dist.pdf(dir_), "#d62728", f"Região de rejeição (α = {alfa:.2f})", 1, col, 0.7, show=False, largura=2)
        fig.add_vline(x=obs, line=dict(color="black", dash="dash"), row=1, col=col)
        fig.add_annotation(x=obs + (0.2 if obs > 0 else -0.2), y=0.33, xref=f"x{col}" if col > 1 else "x", yref=f"y{col}" if col > 1 else "y",
                           text=f"obs = {obs:.2f}<br>p = {res['p_valor']:.3f}", showarrow=False,
                           xanchor="left" if obs > 0 else "right")
        fig.update_xaxes(title_text="Valor da estatística (adimensional)", range=[-6, 6], row=1, col=col)
    fig.update_yaxes(title_text="Densidade", col=1)
    fig.update_layout(title="G2 – Estatística do teste sob H0, região de rejeição e p-valor do exemplo",
                      height=480, bargap=0.02, legend=dict(orientation="h", y=-0.3))
    return fig
