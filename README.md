# Lab04 – Testes de hipótese por dentro

**Dashboard:** https://lab04medicaoexperimentacao2.streamlit.app/
**Repositório:** https://github.com/FelipeVieir4/lab4-medicao-experimentacao
**GitHub Projects:** https://github.com/FelipeVieir4/lab4-medicao-experimentacao/projects

Cenário: o tempo até o merge de PRs difere quando há um bot de revisão? Comparamos **t de Welch × Mann-Whitney**
por simulação (lognormal com parâmetros estimados de dados reais do supabase/supabase). Detalhes dos dados em
[data/README_dados.md](data/README_dados.md).

## Como rodar (um único comando)

```bash
pip install -r requirements.txt; python -m streamlit run app.py
```

(O `;` funciona no PowerShell, no CMD não; em Linux/macOS/Git Bash também pode usar `&&`.)

Todos os resultados usam semente fixa (`numpy.random.default_rng(42)`), então saem iguais a cada execução.

## Estrutura

- `app.py`: dashboard Streamlit (monta as seções 1 a 7)
- `data/prs_merge_time.csv`: dados reais (30 PRs por grupo)
- `src/params.py`: estima os parâmetros da simulação a partir dos dados reais
- `src/simulate.py`: geração do conjunto simulado de exemplo
- `src/scenarios.py`: situações simuladas (base, muito assimétrica, outliers, amostra pequena)
- `src/tests.py`: t de Welch e Mann-Whitney
- `src/q1_type1.py`, `src/q2_power.py`: erro tipo I (Q1) e poder (Q2/Q3), 10.000 repetições
- `src/plot_g1.py` a `src/plot_g4.py`: gráficos G1 a G4
- `src/sec_*.py`: seções 4 a 7 do dashboard
