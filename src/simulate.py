"""Geração dos dados simulados: lognormal por grupo, parâmetros vindos dos dados reais."""
import numpy as np

SEED = 42


def make_rng(seed: int = SEED) -> np.random.Generator:
    return np.random.default_rng(seed)


def simulate_dataset(rng, n, mu_a, sigma_a, mu_b, sigma_b, efeito=1.0):
    """Um conjunto simulado com n observações por grupo.

    `efeito` multiplica a mediana do grupo A (efeito = 1 => H0 verdadeira se os parâmetros forem iguais).
    """
    a = rng.lognormal(mu_a + np.log(efeito), sigma_a, n)
    b = rng.lognormal(mu_b, sigma_b, n)
    return a, b


def simulate_null_batch(rng, n, mu, sigma, reps):
    """reps conjuntos sob H0: os dois grupos saem da mesma lognormal (matrizes reps x n)."""
    return rng.lognormal(mu, sigma, (reps, n)), rng.lognormal(mu, sigma, (reps, n))
