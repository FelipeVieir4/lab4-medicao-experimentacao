"""Os dois testes que respondem à mesma pergunta: t de Welch e Mann-Whitney (bicaudais)."""
import numpy as np
from scipy import stats


def welch(a, b) -> dict:
    r = stats.ttest_ind(a, b, equal_var=False)
    df = float(r.df)
    return {"teste": "t de Welch", "estatistica": float(r.statistic), "p_valor": float(r.pvalue), "gl": df}


def mannwhitney(a, b) -> dict:
    # Aproximação normal sem correção de continuidade, para casar com o z mostrado no G2.
    r = stats.mannwhitneyu(a, b, alternative="two-sided", method="asymptotic", use_continuity=False)
    z = mw_z(np.asarray(a)[None, :], np.asarray(b)[None, :])[0]
    return {"teste": "Mann-Whitney", "estatistica": float(z), "p_valor": float(r.pvalue), "U": float(r.statistic)}


def welch_t_batch(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Estatística t de Welch para cada linha de a e b (matrizes reps x n)."""
    va, vb = a.var(axis=1, ddof=1), b.var(axis=1, ddof=1)
    return (a.mean(axis=1) - b.mean(axis=1)) / np.sqrt(va / a.shape[1] + vb / b.shape[1])


def mw_z_batch(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return mw_z(a, b)


def mw_z(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """z do Mann-Whitney (aproximação normal) para cada linha; sem empates (dados contínuos)."""
    n1, n2 = a.shape[1], b.shape[1]
    ranks = stats.rankdata(np.concatenate([a, b], axis=1), axis=1)
    u = ranks[:, :n1].sum(axis=1) - n1 * (n1 + 1) / 2
    mean_u = n1 * n2 / 2
    sd_u = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    return (u - mean_u) / sd_u
