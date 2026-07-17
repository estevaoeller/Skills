# Agent Skills

Repositorio pessoal de skills e plugins reutilizaveis para agentes de IA.

O repositorio tambem esta estruturado como um marketplace independente para o Claude Code.

## Marketplace do Claude Code

Dentro do Claude Code, adicione o marketplace:

```text
/plugin marketplace add estevaoeller/agent-skills
```

Depois, instale a skill desejada:

```text
/plugin install project-memory@estevaoeller-skills
```

Pelo terminal, os comandos equivalentes sao:

```bash
claude plugin marketplace add estevaoeller/agent-skills
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

## Estrutura

```text
.claude-plugin/
  marketplace.json
plugins/
  project-memory/
    .claude-plugin/plugin.json
    skills/project-memory/SKILL.md
    scripts/
    templates/
docs/
scripts/
```

Cada pasta em `plugins/` deve ser autocontida. Plugins instalados pelo marketplace sao copiados para o cache local do Claude Code e nao devem depender de arquivos fora da propria pasta.

## Adicionar uma nova skill

Consulte [`docs/ADDING-A-PLUGIN.md`](docs/ADDING-A-PLUGIN.md).

## Validacao

```bash
claude plugin validate .
python scripts/check_marketplace.py
```

## Licenca

MIT.
