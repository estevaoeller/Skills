# Project Memory

Plugin de memoria operacional progressiva para projetos conduzidos por pessoas e agentes de IA.

Versao atual: 3.3.0. As mudancas de cada versao estao em [CHANGELOG.md](CHANGELOG.md).

## O que ele instala

A skill `project-memory`, contendo:

- protocolo de leitura minima;
- estado atual em `NOW.md`;
- tarefas em `TASKS.md`;
- conhecimento duravel em `_wiki/` (o sublinhado mantem a pasta no topo da listagem);
- historico consultado apenas quando necessario;
- registro automatico ao fim de cada passo relevante, com destino certo para cada tipo de informacao;
- frontmatter portatil (Obsidian) opcional na `_wiki/` e no `_history/`, com o campo `project_memory` (versao da skill que criou a nota);
- script de inicializacao;
- modelos para Claude Code, Codex, Goose e outros agentes.

## Instalar pelo marketplace

```text
/plugin marketplace add estevaoeller/Skills
/plugin install project-memory@estevaoeller-skills
```

## Invocar no Claude Code

```text
/project-memory:project-memory
```

Exemplo de solicitacao:

```text
Use project-memory para inicializar a memoria deste projeto.
```

## Inicializar manualmente um projeto

Localize a pasta do plugin instalado ou copie este diretorio e execute:

```bash
python scripts/init_project.py /caminho/do/projeto --name "Nome do projeto" --git
```

O script preserva arquivos existentes por padrao. Use `--force` somente quando quiser substitui-los.

Frontmatter da `_wiki/` e do `_history/`: `--frontmatter perfil` (padrao: nucleo + perfil de trabalho), `nucleo` ou `nenhum`.
No modo `perfil`, `--client`, `--engagement` e `--organization` preenchem o perfil. Pelo agente, a skill faz essas perguntas
antes de criar o projeto, e quem escolhe "padrao" pula todas.

## Estrutura criada no projeto

```text
AGENTS.md
CLAUDE.md
PROJECT.md
NOW.md
TASKS.md
_wiki/INDEX.md
_wiki/_modelo-pagina.md
_history/README.md
_history/_modelo-registro.md
.claude/skills/project-memory/
.agents/skills/project-memory/
```

A estrutura deve crescer conforme necessidades reais, sem criar antecipadamente categorias vazias.

## Atualizar de uma versao anterior

A partir da 3.3.0 a pasta de historico se chama `_history/` (antes `history/`). A skill nao renomeia pastas de projetos que
ja existem. Em um projeto criado por versao anterior, renomeie `history/` para `_history/` e ajuste as mencoes a ela em
`AGENTS.md`, `PROJECT.md`, `NOW.md`, `TASKS.md` e `_wiki/INDEX.md`. O valor `type: Project History` do frontmatter nao muda.
