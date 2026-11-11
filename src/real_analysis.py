"""Seção 6: os dois testes aplicados aos dados reais, com tamanho do efeito e conclusão."""
import numpy as np
import pandas as pd

from src.tests import mannwhitney, welch

ALFA = 0.05


def cohen_d(a, b) -> float:
    """d de Cohen com desvio-padrão combinado (positivo => grupo A tem média maior)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return float((a.mean() - b.mean()) / sp)


def rank_biserial(u: float, na: int, nb: int) -> float:
    """Correlação bisserial por postos: r = 2U/(na·nb) − 1 (igual ao delta de Cliff sem empates).

    U é o do grupo A; r > 0 => valores do grupo A tendem a ser maiores. Vai de −1 a 1.
    """
    return float(2 * u / (na * nb) - 1)


def _conclusao(p: float, alfa: float = ALFA) -> str:
    alfa_txt = f"{alfa:.2f}".replace(".", ",")
    return f"{'rejeita' if p < alfa else 'não rejeita'} H₀ (α = {alfa_txt})"


def analisar(df: pd.DataFrame, alfa: float = ALFA) -> pd.DataFrame:
    """df: saída de load_real() (grupo, pr_numero, horas). Grupo A = com bot, B = sem bot.

    Colunas: teste, estatistica, p_valor, tamanho_efeito, conclusao.
    """
    a = df.loc[df["grupo"] == "com_bot", "horas"].to_numpy()
    b = df.loc[df["grupo"] == "sem_bot", "horas"].to_numpy()
    w, m = welch(a, b), mannwhitney(a, b)
    return pd.DataFrame([
        {"teste": "t de Welch", "estatistica": w["estatistica"], "p_valor": w["p_valor"],
         "tamanho_efeito": cohen_d(a, b), "conclusao": _conclusao(w["p_valor"], alfa)},
        {"teste": "Mann-Whitney", "estatistica": m["estatistica"], "p_valor": m["p_valor"],
         "tamanho_efeito": rank_biserial(m["U"], len(a), len(b)), "conclusao": _conclusao(m["p_valor"], alfa)},
    ])
