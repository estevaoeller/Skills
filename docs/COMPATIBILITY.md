# Compatibilidade

## Claude Code

Distribuição principal, pelo marketplace. O Claude Code descobre as skills em `plugins/<nome>/skills/`.

## Outros agentes

- `project-memory`: o projeto inicializado recebe um `AGENTS.md` e uma cópia local da skill em `.agents/skills/project-memory/`,
  lidos pelo Codex e por agentes compatíveis com `AGENTS.md`.
- `excel-model-review`: as skills são Markdown e o motor é Python (`scripts/`, com `openpyxl`), então podem ser adaptados a outro
  agente copiando a pasta do plugin.

Scripts e templates ficam dentro de cada plugin para que ele seja autocontido.
