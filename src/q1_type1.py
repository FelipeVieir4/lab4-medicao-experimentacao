"""Q1 e Q3 (erro tipo I): proporção de rejeições de H₀ quando não há efeito, em cada situação simulada."""
import pandas as pd

from src.scenarios import CENARIOS, gerar
from src.simulate import SEED, make_rng
from src.tests import pvalues_batch

REPS = 10_000
ALFA = 0.05


def run_type1(reps: int = REPS, alfa: float = ALFA, seed: int = SEED) -> pd.DataFrame:
    """Colunas: cenario, teste, erro_tipo1 (proporção de p < alfa com H₀ verdadeira, d = 0).

    Q1 = linha do cenário "base"; Q3 = linhas dos demais cenários (violações dos pressupostos).
    """
    rng = make_rng(seed)
    linhas = []
    for nome, cen in CENARIOS.items():
        a, b = gerar(cen, rng, reps, d=0.0)
        p_welch, p_mw = pvalues_batch(a, b)
        linhas.append({"cenario": nome, "teste": "t de Welch", "erro_tipo1": float((p_welch < alfa).mean())})
        linhas.append({"cenario": nome, "teste": "Mann-Whitney", "erro_tipo1": float((p_mw < alfa).mean())})
    return pd.DataFrame(linhas)
