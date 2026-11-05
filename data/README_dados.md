# Dados reais

- **Fonte:** pull requests mergeados do repositório público [supabase/supabase](https://github.com/supabase/supabase).
- **Coleta (05/11/2026):** `gh pr list -R supabase/supabase --state merged --limit 250 --json number,createdAt,mergedAt,author,reviews`
  (PRs criados entre 23/10/2026 e 05/11/2026).
- **Variável:** `horas` = `mergedAt − createdAt`, em horas.
- **Grupos:**
  - `com_bot`: o PR recebeu ao menos uma revisão de conta de bot (ex.: CodeRabbit, Copilot).
  - `sem_bot`: nenhuma revisão de bot.
  - PRs abertos por contas de bot (Renovate etc.) foram excluídos.
- **Amostra:** 30 PRs por grupo, sorteados com `random_state=42` entre os 135 (com bot) e 87 (sem bot) PRs elegíveis.
- **Arquivo:** `prs_merge_time.csv` (colunas `grupo`, `pr_numero`, `horas`).
- **Limitação:** o grupo com bot pode diferir do grupo sem bot em tamanho/tipo de PR, então a comparação é observacional.
