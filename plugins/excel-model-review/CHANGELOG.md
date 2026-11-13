# Changelog

## Primeira publicação no catálogo (12/11/2026)

- o plugin passa a ser distribuído dentro do catálogo (`plugins/excel-model-review/`), somente na versão final: as duas skills
  (`excel-model-diff` e `excel-model-evolution`), o motor Python compartilhado em `scripts/` e o README;
- inclui a correção de células com data e hora (por exemplo, `=TODAY()` congelado), que antes quebravam a geração do JSON;
- o desenvolvimento (testes, casos reais e documentação de trabalho) fica em repositório de trabalho privado.
