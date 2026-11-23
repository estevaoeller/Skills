# Skills de Estevão Eller

Catálogo de plugins para o Claude Code. Cada plugin está em `plugins/<nome>/` na versão final, com README e changelog próprios.

## Plugins disponíveis

| Plugin | Versão | O que faz | Requisitos |
|---|---|---|---|
| [`project-memory`](plugins/project-memory/) | 3.3.1 | Mantém, em arquivos Markdown dentro do projeto, o estado atual, as pendências, as decisões e o conhecimento acumulado, para que qualquer sessão nova retome o trabalho lendo três arquivos | Python 3 para o script de inicialização (só biblioteca padrão) |
| [`excel-model-review`](plugins/excel-model-review/) | experimental, sem número de versão | Compara versões de um modelo Excel e reconstrói como ele evoluiu, relatando por áreas funcionais em vez de célula a célula | Python 3 e `openpyxl` (`requirements.txt` do plugin) |

### project-memory

Uma skill (`project-memory`). Cria no projeto um núcleo de três arquivos (`PROJECT.md`, `NOW.md`, `TASKS.md`), uma wiki
(`_wiki/`) e um histórico (`_history/`), e orienta o agente a registrar cada informação no seu lugar ao fim de cada passo
relevante, sem esperar pedido. Funciona com o Claude Code e com agentes que leem `AGENTS.md`. Detalhes e migração entre versões
no [README](plugins/project-memory/README.md) e no [changelog](plugins/project-memory/CHANGELOG.md) do plugin.

### excel-model-review

Duas skills complementares sobre o mesmo motor Python, que só lê os arquivos:

- `excel-model-diff` responde "o que mudou entre a versão A e a versão B";
- `excel-model-evolution` responde "como o modelo chegou da primeira versão à atual", ao longo de uma sequência ordenada de
  versões.

As duas mapeiam a estrutura e o contexto do workbook (títulos, rótulos, notas, nomes definidos, referências entre abas) antes de
interpretar as mudanças, e separam o que é evidência explícita do que é inferência. As células alteradas ficam guardadas como
evidência para auditoria. Detalhes no [README](plugins/excel-model-review/README.md) do plugin.

### Relação entre os plugins

Os dois plugins são independentes: instalar um não exige o outro, e nenhum lê arquivo do outro. A relação existe só dentro do
`excel-model-review`, entre as suas duas skills.

## Instalação

No Claude Code:

```text
/plugin marketplace add estevaoeller/Skills
/plugin install project-memory@estevaoeller-skills
/plugin install excel-model-review@estevaoeller-skills
```

Pelo terminal:

```bash
claude plugin marketplace add estevaoeller/Skills
claude plugin install project-memory@estevaoeller-skills
claude plugin install excel-model-review@estevaoeller-skills
```

Instalado, o plugin pode ser chamado pelo nome da skill (por exemplo, `/project-memory:project-memory`), e o Claude Code também
o seleciona sozinho quando a descrição da skill corresponde à tarefa. Para receber versões novas:

```text
/plugin marketplace update estevaoeller-skills
/plugin update <plugin>@estevaoeller-skills
```

## Estrutura do repositório

```text
.claude-plugin/marketplace.json   índice dos plugins do catálogo
plugins/<nome>/                   um plugin, autocontido (skills, scripts, README, CHANGELOG)
docs/                             publicação e compatibilidade
scripts/check_marketplace.py      valida o índice
CHANGELOG.md                      mudanças do catálogo (as de cada plugin ficam no changelog dele)
```

## Licença

MIT.
