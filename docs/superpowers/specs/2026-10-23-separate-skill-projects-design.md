# Separação dos projetos de skills

## Intenção

Transformar a coleção atual em três unidades independentes: `project-memory`,
`excel-model-review` e um catálogo `agent-skills-marketplace` na raiz atual.
Isso separa produto, histórico e distribuição de cada solução.

## Estrutura aprovada

```text
agent-skills-marketplace/       <- raiz atual; catálogo
  .claude-plugin/marketplace.json
  README.md

project-memory/                 <- fonte do plugin de memória
  .claude-plugin/
  skills/
  scripts/
  templates/
  standalone-kit/

excel-model-review/             <- fonte do plugin de Excel
  .claude-plugin/
  skills/
  scripts/
  tests/
  README.md
```

## Decisões

- `project-memory` preserva o plugin existente e seu kit standalone, mas o kit
  passa a ficar dentro do projeto que o gera.
- `excel-model-review/30bfc4e764da` é tratado como origem a extrair: seus
  arquivos úteis tornam-se a raiz de `excel-model-review`; `.in_use` e
  `__pycache__` não são fonte e devem ser ignorados, não removidos nesta etapa.
- O repositório da raiz torna-se somente o catálogo. Seu `marketplace.json`
  usa fontes GitHub quando os dois projetos forem publicados.
- Não há exclusões durante a migração. Artefatos `.zip` e cópias antigas são
  movidos para uma área de preservação até a publicação dos repositórios.

## Fora de escopo

- Criar repositórios remotos ou publicar no GitHub.
- Apagar caches, zips ou cópias históricas.
- Alterar o comportamento das skills.
