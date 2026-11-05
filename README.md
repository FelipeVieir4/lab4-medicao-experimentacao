# Lab04 – Testes de hipótese por dentro

**Dashboard:** `<preencher: link do dashboard publicado>`
**Repositório:** https://github.com/FelipeVieir4/lab4-medicao-experimentacao
**GitHub Projects:** `<preencher>`

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

- `app.py`: dashboard Streamlit
- `data/prs_merge_time.csv`: dados reais (30 PRs por grupo)
- `src/params.py`: estima os parâmetros da simulação a partir dos dados reais
- `src/simulate.py`: geração dos dados simulados
- `src/tests.py`: t de Welch e Mann-Whitney
- `src/plot_g1.py`, `src/plot_g2.py`: gráficos G1 e G2
