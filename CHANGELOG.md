# Changelog do catálogo

Mudanças no catálogo como um todo. As mudanças de cada plugin ficam no changelog dele, em `plugins/<nome>/CHANGELOG.md`.

## Não publicado

- README reescrito: tabela com versão, função e requisitos de cada plugin, uma seção por plugin e a relação entre eles.
  README, CHANGELOG e `docs/COMPATIBILITY.md` passam a ter acentuação.
- Sai o `CONTRIBUTING.md`: o procedimento de publicação não faz parte do repositório público.
- `docs/` atualizados para os dois plugins.

## 12/11/2026

- `project-memory` 3.3.0 passa a ser distribuído dentro do catálogo (`plugins/project-memory/`), somente na versão final, com
  README e changelog próprios. A entrada do `marketplace.json` deixa de apontar para um repositório externo.
- O catálogo passa a listar somente plugins publicados em `plugins/<nome>/`. Saem as entradas que apontavam para repositórios
  privados. Documentos internos da separação (`docs/superpowers/`, `MIGRATION.md`, `ADDING-A-PLUGIN.md`) saem do repositório.
- `project-memory` 3.3.1: o template deixa de incluir o `.goosehints`; a seção do Goose sai do `docs/COMPATIBILITY.md`.
- `excel-model-review` entra no catálogo (`plugins/excel-model-review/`), somente na versão final, com as skills
  `excel-model-diff` e `excel-model-evolution`.

## 27/10/2026

- Os plugins passam a viver em repositórios próprios, e o catálogo apenas aponta para eles (revertido em 12/11/2026).

## 20/09/2026

- Inclusão do plugin `excel-model-review`.

## 17/07/2026

- Estrutura inicial do marketplace `estevaoeller-skills`, com o plugin `project-memory` e a documentação de publicação,
  instalação e validação.
