---
name: excel-model-diff
description: Compara duas versoes de um modelo Excel no nivel de areas funcionais. Mapeia estrutura e contexto antes de interpretar mudancas, procura titulos, rotulos, notas, comentarios, nomes definidos, tabelas e referencias entre abas, e separa evidencia explicita, referencia documental e inferencia. Use para detectar o que mudou entre dois .xlsx/.xlsm sem produzir um dump celula a celula.
---

# Excel Model Diff

Compare duas versoes Excel usando **areas funcionais como unidade principal de analise**. As celulas sao evidencia, nao o relatorio.

## Regra epistemica

**Nao ocultar o salto entre observacao e interpretacao.**

Separe sempre:
- **Explícito**: o proprio workbook nomeia ou descreve a area/mudanca.
- **Referenciado**: outra parte do workbook identifica, documenta ou aponta para a area.
- **Inferido**: significado ou finalidade deduzidos por estrutura, formulas, dependencias ou conteudo.
- **Nao identificado**: evidencia insuficiente.

Nome do bloco e interpretacao da mudanca podem ter status diferentes. Exemplo: o nome "Populacao Total" pode ser explicito, enquanto "internalizacao da serie antes estatica" e uma inferencia.

## Mapeamento antes do diff

Antes de dar nome a uma area, procure contexto no workbook inteiro:
1. titulos, subtitulos e cabecalhos;
2. rotulos a esquerda/acima e textos auxiliares;
3. celulas mescladas, negrito, bordas e mudancas visuais que marquem secoes;
4. comentarios/notas de celula;
5. nomes definidos e nomes de tabelas;
6. abas de metodologia, memoria, premissas, instrucoes, notas ou "passo a passo";
7. formulas e referencias que liguem o bloco a outras abas;
8. textos explicativos pequenos, inclusive expressoes como ajuste, projecao, estimativa, fonte, premissa, calculado conforme, multiplica, divide, utilizado em, metodo e modelo.

Nao trate automaticamente rotulos de linha, municipios, anos ou categorias como titulo do bloco.

## Procedimento

1. Identifique base/anterior e revisada/posterior.
2. Verifique openpyxl>=3.1,<4.
3. Execute o comparador estrutural.
4. Leia primeiro summary.md e areas.csv.
5. Para cada area material, busque evidencia semantica no workbook antes de aceitar o rotulo geometrico.
6. Consulte evidence_cells.csv para validar a mudanca, nao para montar o relatorio principal.
7. Registre a proveniencia do nome e da interpretacao.
8. Crie pendencia quando a interpretacao exigir confirmacao humana.
9. Nao modifique nem salve os arquivos de origem.

## Comando

~~~bash
python "$CLAUDE_PLUGIN_ROOT/scripts/compare_structural.py" "OLD.xlsx" "NEW.xlsx" --out "excel-model-diff-report"
~~~

## Formato de resposta

Tabela principal:
'Aba | Area | Identificacao | Status do nome | Mudanca | Status da interpretacao | Evidencia | Pendencia'.

Depois explique apenas as areas relevantes.

Para inferencias, use:
- **Inferencia**
- **Base da inferencia**
- **Confianca**: alta/media/baixa
- **Confirmar**: pergunta ou verificacao necessaria

Nunca apresente uma inferencia como fato documentado.

## Distincao

Responde **"o que mudou entre estas duas versoes?"**. Para historia de construcao ao longo de varias versoes, use excel-model-evolution.
