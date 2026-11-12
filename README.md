# Estevao Eller Skills Marketplace

Este repositorio e o catalogo de plugins reutilizaveis para Claude Code. O plugin
`project-memory` vive aqui, em `plugins/project-memory/`, somente na versao final,
com README e changelog proprios. Os demais plugins apontam para repositorios proprios.
O desenvolvimento do `project-memory` (memoria, wiki, historico e testes) acontece em
outro repositorio, de trabalho, e nao faz parte deste.

## Marketplace do Claude Code

Dentro do Claude Code, adicione o marketplace:

```text
/plugin marketplace add estevaoeller/Skills
```

Depois, instale a skill desejada:

```text
/plugin install project-memory@estevaoeller-skills
```

Pelo terminal, os comandos equivalentes sao:

```bash
claude plugin marketplace add estevaoeller/Skills
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
| `project-memory` | Memoria operacional progressiva para projetos (3.3.0, [changelog](plugins/project-memory/CHANGELOG.md)) | Inicial |
| `excel-model-review` | Comparacao e evolucao estrutural de modelos Excel | Inicial |
| `homelab` | Protocolo de manutencao e operacao do Homelab | Inicial |

## Estrutura

```text
.claude-plugin/
  marketplace.json             <- indice de plugins
plugins/
  project-memory/              <- versao final, README e CHANGELOG do plugin
docs/
scripts/
  check_marketplace.py          <- valida o indice
```

A entrada do `project-memory` aponta para `./plugins/project-memory`. As demais
entradas apontam para um repositorio GitHub independente, que contem seu proprio
`.claude-plugin/plugin.json` e suas fontes. Consulte
[`docs/MIGRATION.md`](docs/MIGRATION.md) para os caminhos que foram separados.

No workspace local, este catálogo fica em `marketplace/`. Os projetos de
trabalho de `excel-model-review` e `homelab` ficam como pastas irmãs:
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
