"""Situações simuladas (Q1, Q2 e Q3): um cenário que respeita os pressupostos e outros que os violam.

Em todas, os dados são lognormais com μ e σ estimados dos dados reais (os dois grupos juntos).
O tamanho do efeito `d` é a diferença entre os grupos na escala do log, em desvios-padrão (d = 0 => H₀ verdadeira).
"""
from dataclasses import dataclass
from functools import lru_cache

import numpy as np

from src.params import load_real


@dataclass(frozen=True)
class Cenario:
    nome: str
    rotulo: str
    n: int = 30                  # observações por grupo
    sigma_mult: float = 1.0      # multiplica o σ real (mais assimetria)
    p_outlier: float = 0.0       # probabilidade de cada observação virar outlier
    fator_outlier: float = 1.0   # quanto o outlier é multiplicado


CENARIOS = {
    c.nome: c
    for c in (
        Cenario("base", "Base (n = 30, lognormal real)"),
        Cenario("assimetrica", "Muito assimétrico (σ × 1,5)", sigma_mult=1.5),
        Cenario("outliers", "Com outliers (5% × 20)", p_outlier=0.05, fator_outlier=20.0),
        Cenario("amostra_pequena", "Amostra pequena (n = 10)", n=10),
    )
}

TAMANHOS_EFEITO = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5)


@lru_cache(maxsize=1)
def params_base():
    """μ e σ do log do tempo, com os dois grupos juntos (sob H₀ eles vêm da mesma distribuição)."""
    logs = np.log(load_real()["horas"].to_numpy())
    return float(logs.mean()), float(logs.std(ddof=1))


def gerar(cenario: Cenario, rng, reps: int, d: float = 0.0):
    """reps conjuntos (matrizes reps x n) para o grupo A (com bot) e B (sem bot).

    O grupo A é deslocado em d desvios-padrão na escala do log.
    """
    mu, sigma = params_base()
    s = sigma * cenario.sigma_mult
    a = rng.normal(mu + d * s, s, (reps, cenario.n))
    b = rng.normal(mu, s, (reps, cenario.n))
    a, b = np.exp(a), np.exp(b)
    if cenario.p_outlier > 0:
        for x in (a, b):
            x[rng.random(x.shape) < cenario.p_outlier] *= cenario.fator_outlier
    return a, b
