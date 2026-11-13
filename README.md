# Estevao Eller Skills Marketplace

Este repositorio e o catalogo de plugins reutilizaveis para Claude Code. Cada plugin vive aqui, em
`plugins/<nome>/`, somente na versao final (funcional e limpa), com README e changelog proprios. O desenvolvimento
(memoria, wiki, historico e testes) acontece em repositorios de trabalho privados e nao faz parte deste.

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
| `excel-model-review` | Comparacao e evolucao estrutural de modelos Excel, em duas skills (`excel-model-diff` e `excel-model-evolution`) | Inicial |

## Estrutura

```text
.claude-plugin/
  marketplace.json             <- indice de plugins
plugins/
  project-memory/              <- versao final, README e CHANGELOG do plugin
  excel-model-review/          <- versao final, README e CHANGELOG do plugin
docs/
scripts/
  check_marketplace.py          <- valida o indice
```

Cada entrada do `marketplace.json` aponta para `./plugins/<nome>`. Plugins novos entram por promocao: a versao final e
sanitizada e copiada para `plugins/<nome>/` e registrada no indice.

## Adicionar uma nova skill

Copie a versao final e sanitizada para `plugins/<nome>/`, registre-a em `.claude-plugin/marketplace.json` e acrescente a
linha na tabela do catalogo. Depois valide (abaixo).



```bash
claude plugin validate .
python scripts/check_marketplace.py
```

## Licenca

MIT.
