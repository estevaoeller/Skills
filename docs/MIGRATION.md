# Separação dos projetos

Esta raiz, `01_Skills/`, é somente o catálogo do marketplace. As fontes de trabalho
são projetos irmãos, cada qual com manifesto e Git próprios. O nome final planejado
para esta pasta é `marketplace/`; a renomeação está pendente porque a sessão atual
mantém `01_Skills/` aberto.

## Destinos

| Conteúdo anterior | Novo destino |
|---|---|
| `plugins/project-memory/` | `../project-memory/` |
| `project-memory-wiki-kit-v3/project-memory-wiki-kit-v3/` | `../project-memory/standalone-kit/` |
| `scripts/build_wiki_kit.py` | `../project-memory/scripts/build_wiki_kit.py` |
| `excel-model-review/30bfc4e764da/` | `../excel-model-review/` |
| `.in_use/` do Excel | `../excel-model-review/_migration-cache/` |
| `01_Skills/homelab/` (histórico) | `../homelab/` |

## Próximo passo externo

Criar e publicar os repositórios GitHub `estevaoeller/project-memory` e
`estevaoeller/excel-model-review`. O catálogo já os referencia e passará a
instalá-los quando eles existirem remotamente.

O plugin `homelab` mantém o remoto privado existente
`estevaoeller/skills-private`; instalar ou acessar suas fontes exige acesso a esse
repositório privado.

## Nota histórica

Os caminhos sem `../` nesta tabela representam a disposição anterior, quando os
projetos estavam aninhados no catálogo `01_Skills/`. Os caminhos com `../` são os
caminhos ativos desde a migração de 2026-10-25.
