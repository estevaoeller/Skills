# Separação dos projetos

Esta raiz, `marketplace/` (antes `01_Skills/`), é somente o catálogo do marketplace.
As fontes de trabalho são projetos irmãos, cada qual com manifesto e Git próprios.

## Destinos

| Conteúdo anterior | Novo destino |
|---|---|
| `plugins/project-memory/` | `../project-memory/` |
| `project-memory-wiki-kit-v3/project-memory-wiki-kit-v3/` | `../project-memory/standalone-kit/` |
| `scripts/build_wiki_kit.py` | `../project-memory/scripts/build_wiki_kit.py` |
| `excel-model-review/30bfc4e764da/` | `../excel-model-review/` |
| `.in_use/` do Excel | `../excel-model-review/_migration-cache/` |
| `01_Skills/homelab/` (histórico) | `../homelab/` |

## Status

Concluído. Os repositórios GitHub `estevaoeller/project-memory` e
`estevaoeller/excel-model-review` foram criados, publicados (públicos) e o
catálogo já os instala a partir deles. O plugin `homelab` usa o remoto privado
existente `estevaoeller/skills-private`; instalar ou acessar suas fontes exige
acesso a esse repositório privado.

## Nota histórica

Os caminhos sem `../` nesta tabela representam a disposição anterior, quando os
projetos estavam aninhados no catálogo (então chamado `01_Skills/`). Os caminhos
com `../` são os caminhos ativos desde a migração de 2026-10-25.
