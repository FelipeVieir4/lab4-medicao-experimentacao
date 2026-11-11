"""Dashboard do Lab04 – Testes de hipótese por dentro (Sprint 1: cenário, dados e como os testes funcionam)."""
import sys
from pathlib import Path

import numpy as np
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.params import estimate_params, load_real
from src.plot_g1 import fig_g1
from src.plot_g2 import fig_g2
from src.simulate import make_rng, simulate_dataset, simulate_null_batch
from src.tests import mannwhitney, mw_z_batch, welch, welch_t_batch
from src.theme import CORES_GRUPO
from src import ui

N_SIM = 30          # observações por grupo no conjunto simulado
REPS_H0 = 10_000    # conjuntos simulados sob H0 para o G2

REPO_URL = "https://github.com/FelipeVieir4/lab4-medicao-experimentacao"
PROJECTS_URL = "<preencher: link do GitHub Projects>"
DASHBOARD_URL = "<preencher: link do dashboard publicado>"


@st.cache_data
def run_analysis():
    df = load_real()
    params = estimate_params(df)
    pa, pb = params["com_bot"], params["sem_bot"]
    rng = make_rng()  # semente fixa 42
    sim_a, sim_b = simulate_dataset(rng, N_SIM, pa["mu"], pa["sigma"], pb["mu"], pb["sigma"])
    # Sob H0 os dois grupos vêm da mesma lognormal (parâmetros dos dados reais agrupados).
    logs = np.log(df["horas"].to_numpy())
    null_a, null_b = simulate_null_batch(rng, N_SIM, float(logs.mean()), float(logs.std(ddof=1)), REPS_H0)
    return {
        "df": df, "params": params, "sim_a": sim_a, "sim_b": sim_b,
        "t_null": welch_t_batch(null_a, null_b), "z_null": mw_z_batch(null_a, null_b),
        "welch_sim": welch(sim_a, sim_b), "mw_sim": mannwhitney(sim_a, sim_b),
    }


def decisao(p, alfa=0.05):
    return "rejeita H₀" if p < alfa else "não rejeita H₀"


st.set_page_config(page_title="Lab04 – Testes de hipótese por dentro", layout="wide")
ui.aplicar_estilo()
r = run_analysis()
df, params = r["df"], r["params"]
pa, pb = params["com_bot"], params["sem_bot"]

ui.topo(
    "Testes de hipótese por dentro: t de Welch × Mann-Whitney",
    "Lab04 · Laboratório de Experimentação de Software",
    [("Dashboard", DASHBOARD_URL), ("Repositório", REPO_URL), ("GitHub Projects", PROJECTS_URL)],
)

ABAS = ["1 · Cenário", "2 · Os dados", "3 · Como os testes funcionam", "4 · Erro tipo I",
        "5 · Poder", "6 · Dados reais", "7 · Conclusão"]
abas = st.tabs(ABAS)

with abas[0]:
    # 1. Cenário
    with ui.card("cenario"):
        st.header("1. Cenário")
        esq, dir_ = st.columns(2, gap="large")
        with esq:
            ui.kicker("Pergunta e hipóteses")
            st.markdown(
                """
    **Pergunta:** o tempo até o merge de um pull request é diferente quando ele passa por um bot de revisão?

    - **H₀:** com e sem bot, o tempo até o merge vem da mesma distribuição (não há diferença).
      Para o Welch, isso significa médias iguais; para o Mann-Whitney, P(tempo com bot > tempo sem bot) = 0,5.
    - **H₁:** o tempo difere entre os grupos (teste **bicaudal**, porque não sabemos de antemão se o bot acelera ou atrasa).
    """
            )
            ui.kicker("Expectativa antes de simular")
            st.markdown(
                "Tempos de merge são assimétricos, com cauda longa. Esperamos que o Mann-Whitney se saia melhor, porque não "
                "depende da normalidade e é menos afetado pelos PRs muito demorados, que inflam a média e a variância."
            )
        with dir_:
            ui.kicker("Dois testes para a mesma pergunta")
            ui.duelo("médias", "postos", "compara as médias dos grupos", "qual grupo tende a ter valores maiores")
            ui.kicker("Dados reais")
            ui.tiles([("Com bot de revisão", CORES_GRUPO["com_bot"], f"{pa['n']} PRs", "mergeados"),
                      ("Sem bot de revisão", CORES_GRUPO["sem_bot"], f"{pb['n']} PRs", "mergeados")])
            st.markdown(
                "Do repositório público [supabase/supabase](https://github.com/supabase/supabase) (PRs criados entre 23/10/2026 "
                "e 05/11/2026, coletados com `gh pr list` e amostrados com semente 42). Um PR conta como \"com bot\" se recebeu "
                "ao menos uma revisão de uma conta de bot (ex.: CodeRabbit, Copilot); PRs abertos por bots foram excluídos. "
                "O tempo é `mergedAt − createdAt`, em horas."
            )

with abas[1]:
    # 2. Os dados (G1)
    real = {g: df.loc[df["grupo"] == g, "horas"].to_numpy() for g in ("com_bot", "sem_bot")}
    sim = {"com_bot": r["sim_a"], "sem_bot": r["sim_b"]}
    with ui.card("dados"):
        st.header("2. Os dados")
        graf, txt = ui.colunas()
        with graf:
            ui.grafico(fig_g1(real, sim))
        with txt:
            ui.tiles([("Mediana com bot", CORES_GRUPO["com_bot"], f"{ui.br(np.median(real['com_bot']))} h",
                       f"média {ui.br(real['com_bot'].mean())} h"),
                      ("Mediana sem bot", CORES_GRUPO["sem_bot"], f"{ui.br(np.median(real['sem_bot']))} h",
                       f"média {ui.br(real['sem_bot'].mean())} h")])
            st.markdown(
                f"Os dados reais são muito assimétricos: a maioria dos PRs é mergeada em poucas horas, e alguns demoram dias "
                f"(sem bot: mediana de {np.median(real['sem_bot']):.1f} h, média de {real['sem_bot'].mean():.1f} h; "
                f"com bot: mediana de {np.median(real['com_bot']):.1f} h, média de {real['com_bot'].mean():.1f} h). "
                f"Por isso simulamos cada grupo com uma **lognormal**, com μ e σ do log do tempo real "
                f"(com bot: μ = {pa['mu']:.2f}, σ = {pa['sigma']:.2f}; sem bot: μ = {pb['mu']:.2f}, σ = {pb['sigma']:.2f}). "
                "Eixo cortado em 250 h; os dados simulados têm cauda um pouco mais longa."
            )

with abas[2]:
    # 3. Como os testes funcionam (G2)
    w, m = r["welch_sim"], r["mw_sim"]
    with ui.card("testes"):
        st.header("3. Como os testes funcionam")
        graf, txt = ui.colunas()
        with graf:
            ui.grafico(fig_g2(r["t_null"], r["z_null"], w, m))
        with txt:
            ui.duelo(f"p = {ui.br(w['p_valor'], 3)}", f"p = {ui.br(m['p_valor'], 4)}",
                     f"t = {ui.br(w['estatistica'], 2)} · {decisao(w['p_valor'])}",
                     f"z = {ui.br(m['estatistica'], 2)} · {decisao(m['p_valor'])}")
            st.markdown(
                f"O Welch compara as **médias** dos dois grupos, divididas pelo erro-padrão; o Mann-Whitney compara os **postos** "
                f"(qual grupo tende a ter valores maiores). Cada gráfico mostra a distribuição da estatística quando H₀ é verdadeira "
                f"({REPS_H0:,} conjuntos simulados, em barras, e a curva teórica); a área vermelha é a região de rejeição "
                f"(α = 0,05, 2,5% em cada cauda). No conjunto simulado de exemplo ({N_SIM} PRs por grupo, semente 42), "
                f"o Welch deu t = {w['estatistica']:.2f} e **p = {w['p_valor']:.3f}** ({decisao(w['p_valor'])}), enquanto o Mann-Whitney deu "
                f"z = {m['estatistica']:.2f} e **p = {m['p_valor']:.4f}** ({decisao(m['p_valor'])}). "
                "O p-valor (área preta) é a probabilidade de uma estatística tão extrema ou mais, **se H₀ fosse verdadeira**; "
                "ele não é a probabilidade de H₀ ser verdadeira."
            )
            st.caption("Nota: as barras do Welch ficam mais assimétricas que a curva t porque os dados são lognormais. "
                       "É exatamente essa discrepância que as próximas etapas (erro tipo I e poder) vão medir.")

# Seções 4 a 7, cada uma em seu arquivo (src/sec_*.py). Uma seção cujo arquivo ainda não existe é ignorada.
import importlib

for aba, modulo in zip(abas[3:], ("sec_tipo1", "sec_poder", "sec_dados_reais", "sec_conclusao")):
    try:
        secao = importlib.import_module(f"src.{modulo}")
    except ModuleNotFoundError as e:
        if e.name != f"src.{modulo}":
            raise
        with aba:
            st.info("Seção ainda não implementada.")
        continue
    with aba:
        secao.render()
