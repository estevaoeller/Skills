# Excel Model Review

Plugin experimental para revisar modelos Excel em duas perspectivas complementares:

- `excel-model-diff`: identifica o que mudou entre duas versões, reportando áreas/blocos funcionais em vez de uma lista célula a célula;
- `excel-model-evolution`: reconstrói como o modelo foi sendo construído ao longo de uma sequência ordenada de versões.

As duas skills compartilham um motor Python read-only. As mudanças celulares ficam preservadas como evidência auditável, mas não são a unidade principal do relatório.

## Visão geral

```mermaid
flowchart TD
    A[Arquivos Excel] --> B[Evidência bruta<br/>células, fórmulas e valores]
    B --> C[Mapeamento estrutural<br/>áreas e blocos]
    C --> D[Contexto semântico<br/>títulos, rótulos, notas,<br/>nomes definidos e referências]
    D --> E{Modo de análise}

    E --> F[excel-model-diff]
    E --> G[excel-model-evolution]

    F --> H[O que mudou<br/>entre A e B?]
    G --> I[Como o modelo<br/>foi construído?]

    H --> J[Relatório por área]
    I --> K[Linha do tempo por área]

    B -. evidência auditável .-> J
    B -. evidência auditável .-> K
```

A ideia central é separar **detecção** de **interpretação**. O motor identifica alterações elementares; a skill tenta agrupá-las em áreas funcionais e buscar evidência no próprio workbook antes de interpretar o significado da mudança.

## As duas skills

```mermaid
flowchart LR
    subgraph DIFF["excel-model-diff"]
        A1[Versão A] --> C1[Comparação]
        B1[Versão B] --> C1
        C1 --> D1[Áreas alteradas]
        D1 --> E1[Lógica, estrutura,<br/>premissas e hardcodes]
    end

    subgraph EVO["excel-model-evolution"]
        V1[v01] --> V2[v02]
        V2 --> V3[v03]
        V3 --> V4[v04]
        V1 --> C2[Comparações consecutivas]
        V2 --> C2
        V3 --> C2
        V4 --> C2
        C2 --> D2[Eventos por área]
        D2 --> E2[Trajetória de construção]
    end
```

Em termos simples:

- **Diff:** “o que mudou entre estas duas versões?”
- **Evolution:** “como este modelo chegou ao estado atual?”

## Unidade de análise

O relatório principal não deve ser uma lista célula a célula.

```mermaid
flowchart TD
    A[Alterações celulares] --> B[Agrupamento espacial]
    B --> C[Área candidata]
    C --> D[Busca de contexto]
    D --> E[Título ou rótulo]
    D --> F[Notas e comentários]
    D --> G[Nomes definidos e tabelas]
    D --> H[Referências entre abas]
    E --> I[Área funcional identificada]
    F --> I
    G --> I
    H --> I
    I --> J[Relatório estrutural]
```

Exemplo:

```text
Aba: CAPEX
Área: D4:F5
Identificação: Cronograma de Investimentos

Mudança:
- horizonte ampliado;
- valores alterados;
- nova coluna temporal.

Evidência celular:
D5, E5, F4, F5
```

As células continuam disponíveis para auditoria, mas ficam em segundo plano.

## Regra epistemológica

A documentação e as respostas devem tornar explícito o salto entre observação e interpretação.

```mermaid
flowchart LR
    A[Evidência observada] --> B{Há identificação<br/>no workbook?}
    B -->|Sim, direta| C[Explícito]
    B -->|Sim, em outra área| D[Referenciado]
    B -->|Não| E{Estrutura e fórmulas<br/>permitem interpretação?}
    E -->|Sim| F[Inferido]
    E -->|Não| G[Não identificado]

    F --> H[Registrar base,<br/>confiança e validação]
```

Os quatro status são:

- **Explícito:** o próprio workbook nomeia ou descreve a área ou a mudança;
- **Referenciado:** outra parte do workbook identifica ou documenta aquela área;
- **Inferido:** o significado é deduzido pela estrutura, fórmulas, dependências ou sequência das versões;
- **Não identificado:** a evidência não é suficiente.

Nome da área e interpretação da mudança podem ter status diferentes.

## Fluxo do excel-model-diff

```mermaid
flowchart TD
    A[Modelo anterior] --> C[Comparador estrutural]
    B[Modelo revisado] --> C

    C --> D[Detectar mudanças elementares]
    D --> E[Agrupar em áreas]
    E --> F[Inferir rótulo inicial]
    F --> G[Buscar contexto no workbook]
    G --> H[Classificar mudança]

    H --> I1[Bloco criado/removido]
    H --> I2[Bloco expandido/reduzido]
    H --> I3[Lógica alterada]
    H --> I4[Hardcode introduzido]
    H --> I5[Premissa/valor alterado]

    I1 --> J[Relatório por área]
    I2 --> J
    I3 --> J
    I4 --> J
    I5 --> J

    D -.-> K[evidence_cells.csv]
    J --> L[summary.md / areas.csv]
```

## Fluxo do excel-model-evolution

```mermaid
flowchart TD
    V1[v01] --> P1[v01 → v02]
    V2[v02] --> P1

    V2 --> P2[v02 → v03]
    V3[v03] --> P2

    V3 --> P3[v03 → v04]
    V4[v04] --> P3

    P1 --> E[Eventos estruturais]
    P2 --> E
    P3 --> E

    E --> M[Associar eventos<br/>da mesma área]

    M --> T1[Primeiro surgimento]
    M --> T2[Expansão/redução]
    M --> T3[Mudança de lógica]
    M --> T4[Nova dependência]
    M --> T5[Reorganização]

    T1 --> R[Linha do tempo da área]
    T2 --> R
    T3 --> R
    T4 --> R
    T5 --> R
```

Uma trajetória pode resultar, por exemplo, em:

```text
Demanda — Projeção de Economias

v01 → v02: bloco incluído
v02 → v03: horizonte expandido
v03 → v04: lógica de cálculo alterada
v04 → v05: ligação criada com a aba Receita
```

## Instalar pelo marketplace

```text
/plugin marketplace add estevaoeller/Skills
/plugin install excel-model-review@estevaoeller-skills
```

Pelo terminal:

```bash
claude plugin marketplace add estevaoeller/Skills
claude plugin install excel-model-review@estevaoeller-skills
```

## Dependência Python

Requer Python 3.10+ e `openpyxl`:

```bash
python -m pip install "openpyxl>=3.1,<4"
```

## Invocar

```text
/excel-model-review:excel-model-diff
/excel-model-review:excel-model-evolution
```

O Claude Code também pode selecionar as skills automaticamente quando a descrição for pertinente.

## Saídas do diff

- `summary.md`: relatório principal por área;
- `areas.csv`: uma linha por área alterada;
- `evidence_cells.csv`: evidência celular secundária;
- `diff.json`: resultado completo para máquina.

## Saídas do evolution

- `evolution.md`: linha do tempo por área funcional;
- `evolution.json`: evidências e eventos consolidados.

## Limitações atuais

- fórmulas são comparadas como texto; Excel não é recalculado;
- Power Query, Power Pivot/Data Model, VBA, charts, shapes e conexões externas ainda não recebem análise semântica profunda;
- agrupamento de áreas e inferência de rótulos são heurísticos e devem ser validados em layouts ambíguos;
- a associação da mesma área entre versões ainda depende principalmente de rótulo, posição e proximidade estrutural.
