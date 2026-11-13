# Changelog

## Unreleased

- Catalogo passa a listar somente plugins promovidos para `plugins/<nome>/`. Saem `excel-model-review` e `homelab` (apontavam para
  repositorios privados). Documentos internos da separacao (`docs/superpowers/`, `MIGRATION.md`, `ADDING-A-PLUGIN.md`) saem do
  repositorio; README e CLAUDE-MARKETPLACE atualizados.

- `project-memory` 3.3.0 passa a ser distribuido dentro do catalogo (`plugins/project-memory/`), somente na versao final,
  com README e CHANGELOG proprios. A entrada do `marketplace.json` deixa de apontar para um repositorio
  externo; o repositorio de trabalho da skill e separado e privado.

- Estrutura inicial do marketplace `estevaoeller-skills`.
- Inclusao do plugin `project-memory`.
- Documentacao para publicacao, instalacao, validacao e criacao de novos plugins.
