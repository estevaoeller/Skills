---
name: excel-model-evolution
description: Reconstrói como um modelo Excel financeiro, economico, operacional ou analitico foi construido e evoluiu ao longo de uma sequencia ordenada de versoes .xlsx/.xlsm. Use quando o usuario quiser uma linha do tempo da construcao, novos blocos funcionais, expansao/reducao de areas, evolucao de logica de calculo ou mudancas repetidas na mesma secao rotulada. A unidade principal e a area funcional, nao a celula individual.
---

# Excel Model Evolution

Reconstrua **como o modelo se desenvolveu ao longo do tempo** a partir de uma sequencia ordenada de workbooks.

## Pergunta central

Esta skill responde: **Como o modelo chegou da versao inicial ao estado atual?**

Nao e apenas um multi-diff de celulas.

## Unidade de analise

Use areas/blocos funcionais como Premissas Macroeconomicas, Demanda, Projecao de Economias, CAPEX/Cronograma de Investimentos, OPEX, Receita, Financiamento, Fluxo de Caixa, Indicadores e Sensibilidades.

Infira os nomes a partir de rotulos/cabecalhos proximos e mantenha aba + coordenadas como evidencia.

## Procedimento

1. Estabeleca a ordem cronologica/logica das versoes.
2. Verifique a dependencia com 'python -c "import openpyxl; print(openpyxl.__version__)"'.
3. Se openpyxl nao estiver instalado, informe que a skill requer openpyxl>=3.1,<4 e instale apenas se o usuario autorizar a alteracao do ambiente.
4. Compare cada par consecutivo pelo motor estrutural compartilhado.
5. Converta as mudancas par a par em eventos de evolucao.
6. Consolide eventos que aparentem referir-se a mesma area/rotulo.
7. Construa uma linha do tempo mostrando quando uma area aparece, expande/contrai, altera a logica, troca formulas e hardcodes, recebe revisoes repetidas ou desaparece.
8. Use mudancas celulares apenas como evidencia de suporte.
9. Nao atribua intencao de projeto sem evidencia suficiente.
10. Nao modifique os workbooks de origem.

## Comando

Forneca os arquivos do mais antigo para o mais novo:

~~~bash
python "$CLAUDE_PLUGIN_ROOT/scripts/evolution.py" \
  "modelo_v01.xlsx" \
  "modelo_v02.xlsx" \
  "modelo_v03.xlsx" \
  "modelo_v04.xlsx" \
  --out "excel-model-evolution-report"
~~~

## Saidas

- evolution.md: linha do tempo legivel por area funcional;
- evolution.json: evidencia par a par e threads consolidadas.

## Formato de resposta

Comece com uma narrativa curta da construcao e depois organize por area.

Quando util, identifique fases interpretativas como estruturacao inicial, inclusao de premissas, construcao dos motores de calculo, integracao entre modulos, refinamento/calibracao e consolidacao do modelo.

Deixe claro quando essas fases forem inferidas e nao explicitamente documentadas.

## Distincao

Esta skill responde **"como o modelo foi construido/evoluiu entre versoes?"**.

Para uma comparacao focada entre duas versoes, use 'excel-model-diff'.
