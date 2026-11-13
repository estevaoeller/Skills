---
name: excel-model-diff
description: Compara duas versões de um modelo Excel no nível de áreas funcionais. Mapeia estrutura e contexto antes de interpretar mudanças, procura títulos, rótulos, notas, comentários, nomes definidos, tabelas e referências entre abas, e separa evidência explícita, referência documental e inferência. Use para detectar o que mudou entre dois .xlsx/.xlsm sem produzir um dump célula a célula.
---

# Excel Model Diff

Compare duas versões Excel usando **áreas funcionais como unidade principal de análise**. As células são evidência, não o relatório.

## Esquema da análise

```mermaid
flowchart TD
    A[Modelo anterior] --> C[Detectar diferenças]
    B[Modelo revisado] --> C

    C --> D[Alterações celulares]
    D --> E[Agrupar alterações próximas]
    E --> F[Área estrutural candidata]

    F --> G[Buscar contexto no workbook]
    G --> G1[Títulos e rótulos]
    G --> G2[Notas e comentários]
    G --> G3[Nomes definidos e tabelas]
    G --> G4[Referências entre abas]

    G1 --> H[Identificar área funcional]
    G2 --> H
    G3 --> H
    G4 --> H

    H --> I[Classificar a mudança]
    I --> J[Relatório por área]

    D -. evidência .-> J
```

O caminho desejado é:

```text
células alteradas
      ↓
área afetada
      ↓
nome/rótulo da área
      ↓
tipo de mudança
      ↓
interpretação e relevância
```

## Regra epistêmica

**Não ocultar o salto entre observação e interpretação.**

```mermaid
flowchart LR
    A[Observação] --> B{Há evidência textual<br/>ou estrutural suficiente?}
    B -->|Nomeado no próprio bloco| C[Explícito]
    B -->|Documentado em outra área| D[Referenciado]
    B -->|Somente dedutível| E[Inferido]
    B -->|Insuficiente| F[Não identificado]
    E --> G[Base + confiança + confirmação]
```

Separe sempre:

- **Explícito**: o próprio workbook nomeia ou descreve a área/mudança.
- **Referenciado**: outra parte do workbook identifica, documenta ou aponta para a área.
- **Inferido**: significado ou finalidade deduzidos por estrutura, fórmulas, dependências ou conteúdo.
- **Não identificado**: evidência insuficiente.

Nome do bloco e interpretação da mudança podem ter status diferentes. Exemplo: o nome "População Total" pode ser explícito, enquanto "internalização da série antes estática" é uma inferência.

## Mapeamento antes do diff

Antes de dar nome a uma área, procure contexto no workbook inteiro:

1. títulos, subtítulos e cabeçalhos;
2. rótulos à esquerda/acima e textos auxiliares;
3. células mescladas, negrito, bordas e mudanças visuais que marquem seções;
4. comentários/notas de célula;
5. nomes definidos e nomes de tabelas;
6. abas de metodologia, memória, premissas, instruções, notas ou "passo a passo";
7. fórmulas e referências que liguem o bloco a outras abas;
8. textos explicativos pequenos, inclusive expressões como ajuste, projeção, estimativa, fonte, premissa, calculado conforme, multiplica, divide, utilizado em, método e modelo.

Não trate automaticamente rótulos de linha, municípios, anos ou categorias como título do bloco.

## Procedimento

1. Identifique base/anterior e revisada/posterior.
2. Verifique `openpyxl>=3.1,<4`.
3. Execute o comparador estrutural.
4. Leia primeiro `summary.md` e `areas.csv`.
5. Para cada área material, busque evidência semântica no workbook antes de aceitar o rótulo geométrico.
6. Consulte `evidence_cells.csv` para validar a mudança, não para montar o relatório principal.
7. Registre a proveniência do nome e da interpretação.
8. Crie pendência quando a interpretação exigir confirmação humana.
9. Não modifique nem salve os arquivos de origem.

## Comando

```bash
python "$CLAUDE_PLUGIN_ROOT/scripts/compare_structural.py" "OLD.xlsx" "NEW.xlsx" --out "excel-model-diff-report"
```

## Formato de resposta

Tabela principal:

`Aba | Área | Identificação | Status do nome | Mudança | Status da interpretação | Evidência | Pendência`.

Depois explique apenas as áreas relevantes.

Para inferências, use:

- **Inferência**
- **Base da inferência**
- **Confiança**: alta/média/baixa
- **Confirmar**: pergunta ou verificação necessária

Nunca apresente uma inferência como fato documentado.

## Distinção

```mermaid
flowchart LR
    A[Versão A] --> C[excel-model-diff]
    B[Versão B] --> C
    C --> D["O que mudou?"]
```

Responde **"o que mudou entre estas duas versões?"**. Para história de construção ao longo de várias versões, use `excel-model-evolution`.
