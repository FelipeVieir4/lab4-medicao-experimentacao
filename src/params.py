"""Carrega os dados reais e estima os parâmetros da simulação (lognormal por grupo)."""
from pathlib import Path

import numpy as np
import pandas as pd

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "prs_merge_time.csv"
GRUPOS = ("com_bot", "sem_bot")


def load_real(path: Path = CSV_PATH) -> pd.DataFrame:
    """Colunas: grupo, pr_numero, horas (tempo até o merge)."""
    return pd.read_csv(path)


def estimate_params(df: pd.DataFrame) -> dict:
    """Para cada grupo: mu e sigma da lognormal (média e desvio de log(horas)) e a mediana."""
    params = {}
    for g in GRUPOS:
        logs = np.log(df.loc[df["grupo"] == g, "horas"].to_numpy())
        mu, sigma = float(logs.mean()), float(logs.std(ddof=1))
        params[g] = {"mu": mu, "sigma": sigma, "mediana": float(np.exp(mu)), "n": int(len(logs))}
    return params
