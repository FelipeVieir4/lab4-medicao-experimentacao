"""Q2 e Q3 (poder): proporção de rejeições de H₀ quando existe efeito, em cada situação simulada."""
import pandas as pd

from src.scenarios import CENARIOS, TAMANHOS_EFEITO, gerar
from src.simulate import SEED, make_rng
from src.tests import pvalues_batch

REPS = 10_000
ALFA = 0.05


def run_power(reps: int = REPS, alfa: float = ALFA, seed: int = SEED, tamanhos=TAMANHOS_EFEITO) -> pd.DataFrame:
    """Colunas: cenario, d, teste, poder (proporção de p < alfa).

    Q2 = linhas do cenário "base"; Q3 = linhas dos demais cenários (violações dos pressupostos).
    Com d = 0 o "poder" é, na verdade, o erro tipo I.
    """
    rng = make_rng(seed)
    linhas = []
    for nome, cen in CENARIOS.items():
        for d in tamanhos:
            a, b = gerar(cen, rng, reps, d)
            p_welch, p_mw = pvalues_batch(a, b)
            linhas.append({"cenario": nome, "d": d, "teste": "t de Welch", "poder": float((p_welch < alfa).mean())})
            linhas.append({"cenario": nome, "d": d, "teste": "Mann-Whitney", "poder": float((p_mw < alfa).mean())})
    return pd.DataFrame(linhas)
