# Estevao Eller Skills Marketplace

Este repositorio e somente o catalogo de plugins reutilizaveis para Claude Code.
As fontes de cada plugin vivem, sao testadas e sao versionadas em seus
proprios repositorios.

## Marketplace do Claude Code

Dentro do Claude Code, adicione o marketplace:

```text
/plugin marketplace add estevaoeller/agent-skills-marketplace
```

Depois, instale a skill desejada:

```text
/plugin install project-memory@estevaoeller-skills
```

Pelo terminal, os comandos equivalentes sao:

```bash
claude plugin marketplace add estevaoeller/agent-skills-marketplace
claude plugin install project-memory@estevaoeller-skills
```

A skill instalada pode ser invocada explicitamente por:

```text
/project-memory:project-memory
```

O Claude Code tambem pode seleciona-la automaticamente quando a descricao for pertinente a tarefa.

## Catalogo

| Plugin | Descricao | Status |
|---|---|---|
| `project-memory` | Memoria operacional progressiva para projetos | Inicial |
| `excel-model-review` | Comparacao e evolucao estrutural de modelos Excel | Inicial |
| `homelab` | Protocolo de manutencao e operacao do Homelab | Inicial |

## Estrutura

```text
.claude-plugin/
  marketplace.json             <- indice de plugins externos
docs/
scripts/
  check_marketplace.py          <- valida o indice
```

Cada entrada do catalogo aponta para um repositorio GitHub independente, que
contem seu proprio `.claude-plugin/plugin.json` e suas fontes. Consulte
[`docs/MIGRATION.md`](docs/MIGRATION.md) para os caminhos que foram separados.

No workspace local, este catálogo ainda fica temporariamente em `01_Skills/` e será
renomeado para `marketplace/` quando a sessão que o mantém aberto for encerrada. Os
projetos de trabalho já ficam como pastas irmãs: `../project-memory/`,
`../excel-model-review/` e `../homelab/`. O último usa o repositório privado
`estevaoeller/skills-private`.

## Adicionar uma nova skill

Adicione uma entrada em `.claude-plugin/marketplace.json` que aponte para o
repositorio GitHub do novo plugin.

## Validacao

```bash
claude plugin validate .
python scripts/check_marketplace.py
```

## Licenca

MIT.
