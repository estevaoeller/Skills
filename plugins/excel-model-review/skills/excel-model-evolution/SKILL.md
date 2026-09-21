---
name: excel-model-evolution
description: Reconstrói como um modelo Excel foi construido e evoluiu ao longo de versoes ordenadas. Usa areas funcionais e evidencia semantica do workbook, distinguindo fatos explicitos, referencias internas e inferencias. Use para mapear surgimento, expansao, reorganizacao e mudanca de logica de blocos entre varios .xlsx/.xlsm.
---

# Excel Model Evolution

Reconstrua **como o modelo chegou da versao inicial ao estado atual**. Nao e apenas um multi-diff.

## Regra epistemica

**Nao ocultar o salto entre observacao e interpretacao.**

Classifique afirmacoes relevantes como:
- **Explícito**: documentado/nomeado no workbook.
- **Referenciado**: explicado ou apontado por outra area/aba.
- **Inferido**: deduzido por estrutura, formulas, dependencias ou sequencia das versoes.
- **Nao identificado**: evidencia insuficiente.

Uma fase de desenvolvimento como "refinamento metodologico" e inferencia, salvo se o proprio arquivo a documentar.

## Unidade de analise

Use areas funcionais: premissas, demanda, projecoes, CAPEX, OPEX, receita, financiamento, fluxo, indicadores, sensibilidades e outros blocos efetivamente encontrados.

Antes de nomear cada bloco, procure no workbook inteiro:
- titulos/cabecalhos e rotulos;
- notas, comentarios e textos auxiliares;
- nomes definidos e tabelas;
- abas metodologicas, memorias, instrucoes e passo a passo;
- formulas/referencias entre abas;
- textos pequenos que descrevam operacoes ou finalidade.

## Procedimento

1. Estabeleca a ordem das versoes.
2. Compare pares consecutivos pelo motor estrutural.
3. Mapeie contexto semantico de cada versao, nao apenas celulas alteradas.
4. Converta diffs em eventos: bloco criado, expandido, reduzido, removido, reorganizado, logica introduzida/alterada, dependencia criada/removida, hardcode introduzido/removido.
5. Consolide eventos da mesma area usando rotulo + estrutura + proximidade + referencias, nao somente coordenadas.
6. Separe observacao da interpretacao.
7. Para inferencias, registre base, confianca e ponto a confirmar.
8. Nao atribua intencao de projeto sem evidencia.
9. Nao modifique os workbooks.

## Comando

~~~bash
python "$CLAUDE_PLUGIN_ROOT/scripts/evolution.py" "v01.xlsx" "v02.xlsx" "v03.xlsx" "v04.xlsx" --out "excel-model-evolution-report"
~~~

## Formato de resposta

Comece pela linha do tempo estrutural e depois organize por area. Em cada evento relevante mostre:
- versao/transicao;
- area e intervalo;
- evento observado;
- fonte/status da identificacao;
- interpretacao, se houver;
- status da interpretacao;
- evidencia;
- confianca;
- pendencia de validacao.

Fases como estruturacao inicial, inclusao de premissas, construcao de motores, integracao, calibracao e consolidacao so devem ser usadas quando sustentadas; marque-as como inferidas quando forem interpretacao.

## Distincao

Responde **"como o modelo foi construido/evoluiu entre versoes?"**. Para duas versoes especificas, use excel-model-diff.
