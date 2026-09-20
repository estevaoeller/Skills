# Excel Model Review

Plugin experimental para revisar modelos Excel em duas perspectivas complementares:

- 'excel-model-diff': identifica o que mudou entre duas versoes, reportando areas/blocos funcionais em vez de uma lista celula a celula;
- 'excel-model-evolution': reconstrói como o modelo foi sendo construido ao longo de uma sequencia ordenada de versoes.

As duas skills compartilham um motor Python read-only. As mudancas celulares ficam preservadas como evidencia auditavel, mas nao sao a unidade principal do relatorio.

## Instalar pelo marketplace

~~~text
/plugin marketplace add estevaoeller/Skills
/plugin install excel-model-review@estevaoeller-skills
~~~

Pelo terminal:

~~~bash
claude plugin marketplace add estevaoeller/Skills
claude plugin install excel-model-review@estevaoeller-skills
~~~

## Dependencia Python

Requer Python 3.10+ e 'openpyxl':

~~~bash
python -m pip install "openpyxl>=3.1,<4"
~~~

## Invocar

~~~text
/excel-model-review:excel-model-diff
/excel-model-review:excel-model-evolution
~~~

O Claude Code tambem pode selecionar as skills automaticamente quando a descricao for pertinente.

## Principio de desenho

O motor separa quatro camadas:

1. evidencia: celulas/formulas/valores alterados;
2. estrutura: agrupamento das alteracoes em areas locais;
3. contexto semantico: inferencia de rotulo a partir de textos proximos;
4. interpretacao: leitura feita pelo agente sobre o relatorio estrutural.

## Saidas do diff

- 'summary.md': relatorio principal por area;
- 'areas.csv': uma linha por area alterada;
- 'evidence_cells.csv': evidencia celular secundaria;
- 'diff.json': resultado completo para maquina.

## Saidas do evolution

- 'evolution.md': linha do tempo por area funcional;
- 'evolution.json': evidencias e eventos consolidados.

## Limitacoes atuais

- formulas sao comparadas como texto; Excel nao e recalculado;
- Power Query, Power Pivot/Data Model, VBA, charts, shapes e conexoes externas ainda nao recebem analise semantica profunda;
- agrupamento de areas e inferencia de rotulos sao heuristicos e devem ser validados em layouts ambiguos.
