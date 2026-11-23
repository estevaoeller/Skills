# Publicacao como marketplace do Claude Code

Este repositorio ja contem os dois manifestos necessarios:

- `.claude-plugin/marketplace.json`: catalogo do marketplace;
- `plugins/<plugin>/.claude-plugin/plugin.json`: manifesto de cada plugin.

## Nome do marketplace

O repositorio se chama `Skills` e o identificador publico do marketplace e:

```text
estevaoeller-skills
```

O nome `agent-skills` nao deve ser usado como identificador do marketplace porque e reservado pelo Claude Code.

## Instalar a partir do GitHub

No Claude Code:

```text
/plugin marketplace add estevaoeller/Skills
/plugin install project-memory@estevaoeller-skills
```

Ou pelo terminal:

```bash
claude plugin marketplace add estevaoeller/Skills
claude plugin install project-memory@estevaoeller-skills
```

## Atualizar

Apos publicar alteracoes:

```text
/plugin marketplace update estevaoeller-skills
/plugin update project-memory@estevaoeller-skills
```

Os manifestos `plugin.json` nao trazem o campo `version`, de proposito: assim cada novo commit e tratado como versao nova e chega a quem atualizar. O `claude plugin validate` avisa a ausencia, mas nao bloqueia. Se o campo for adotado, sera preciso incrementa-lo a cada publicacao, ou a atualizacao nao chega.

## Validar antes de publicar

Na raiz do repositorio:

```bash
claude plugin validate .
python scripts/check_marketplace.py
```

## Testar localmente

```bash
claude plugin marketplace add /caminho/para/o/clone/deste/repositorio
claude plugin install project-memory@estevaoeller-skills
```

Dentro de uma sessao do Claude Code:

```text
/project-memory:project-memory
```

## Escopos

Instalacao pessoal, disponivel em todos os projetos:

```bash
claude plugin install project-memory@estevaoeller-skills --scope user
```

Instalacao registrada no projeto e compartilhada com colaboradores:

```bash
claude plugin marketplace add estevaoeller/Skills --scope project
claude plugin install project-memory@estevaoeller-skills --scope project
```

## Regra de isolamento

Cada plugin deve carregar seus proprios arquivos dentro da respectiva pasta. Nao utilize referencias como `../shared`, pois plugins instalados sao copiados para um cache separado.
