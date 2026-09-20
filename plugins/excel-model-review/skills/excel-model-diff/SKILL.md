---
name: excel-model-diff
description: Compara duas versoes de um modelo Excel financeiro, economico, operacional ou analitico no nivel de areas/blocos estruturais, e nao celula a celula. Use quando o usuario quiser detectar o que mudou entre dois .xlsx/.xlsm, identificar secoes alteradas, inferir um rotulo humano proximo para cada area e distinguir mudancas de logica/hardcode de mudancas comuns de premissas. Mantem evidencia celular apenas para auditoria.
---

# Excel Model Diff

Compare duas versoes Excel usando **areas funcionais como unidade principal de analise**.

## Principio central

Nao apresente um dump celula a celula como resultado principal. As celulas sao evidencia para detectar, delimitar e explicar blocos alterados.

O relatorio principal deve responder:

- qual area da planilha mudou;
- o que essa area aparentemente representa;
- onde ela esta localizada;
- que tipo de mudanca estrutural ou de logica ocorreu;
- quanta evidencia sustenta a conclusao;
- se o rotulo ou a interpretacao precisam de validacao manual.

## Inferencia de rotulo

Para cada area alterada, infira um nome a partir do contexto do workbook. Priorize:

1. rotulo textual imediatamente a esquerda;
2. titulo/cabecalho imediatamente acima;
3. titulo dentro da borda superior esquerda do bloco;
4. titulo proximo em negrito ou celula mesclada;
5. contexto textual proximo;
6. coordenadas como fallback.

Mantenha sempre aba e intervalo para rastreabilidade.

Exemplo preferido: 'CAPEX!F22:M41 — Cronograma de Investimentos', em vez de uma lista de F22, G22, H22 etc.

## Procedimento

1. Identifique qual arquivo e a versao base/anterior e qual e a revisada/posterior.
2. Verifique a dependencia com 'python -c "import openpyxl; print(openpyxl.__version__)"'.
3. Se openpyxl nao estiver instalado, informe que a skill requer openpyxl>=3.1,<4 e instale apenas se o usuario autorizar a alteracao do ambiente.
4. Execute o comparador estrutural do plugin.
5. Leia primeiro summary.md e areas.csv.
6. Consulte evidence_cells.csv somente para investigar ou validar uma area.
7. Reporte por area funcional, nao por celulas individuais.
8. Marque explicitamente rotulos inferidos que parecam ambiguos.
9. Nao modifique nem salve os arquivos Excel de origem.

## Comando

~~~bash
python "$CLAUDE_PLUGIN_ROOT/scripts/compare_structural.py" "OLD.xlsx" "NEW.xlsx" --out "excel-model-diff-report"
~~~

Para ajustar o agrupamento:

~~~bash
python "$CLAUDE_PLUGIN_ROOT/scripts/compare_structural.py" "OLD.xlsx" "NEW.xlsx" --row-gap 3 --col-gap 3 --out "excel-model-diff-report"
~~~

## Saidas

- summary.md: revisao principal por area;
- areas.csv: uma linha por area estrutural alterada;
- evidence_cells.csv: evidencia celular para auditoria/debug;
- diff.json: resultado completo para processamento.

## Formato de resposta

Prefira uma tabela: 'Aba | Area | Rotulo inferido | Tipo de mudanca | Evidencia | Observacao'.

Depois explique apenas as areas mais relevantes. Nao cole toda a evidencia celular salvo se o usuario pedir.

## Distincao

Esta skill responde **"o que mudou entre estas duas versoes?"**.

Se a tarefa for reconstruir como um modelo foi sendo construido ao longo de varias versoes, use 'excel-model-evolution'.
