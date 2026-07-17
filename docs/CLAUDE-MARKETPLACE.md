# Publicacao como marketplace do Claude Code

Este repositorio ja contem os dois manifestos necessarios:

- `.claude-plugin/marketplace.json`: catalogo do marketplace;
- `plugins/<plugin>/.claude-plugin/plugin.json`: manifesto de cada plugin.

## Nome do marketplace

O repositorio se chama `agent-skills`, mas o identificador publico do marketplace e:

```text
estevaoeller-skills
```

O nome `agent-skills` nao deve ser usado como identificador do marketplace porque e reservado pelo Claude Code.

## Publicar

Depois de copiar estes arquivos para o repositorio:

```bash
git add .
git commit -m "Add Claude Code marketplace and project-memory plugin"
git push origin main
```

## Instalar a partir do GitHub

No Claude Code:

```text
/plugin marketplace add estevaoeller/agent-skills
/plugin install project-memory@estevaoeller-skills
```

Ou pelo terminal:

```bash
claude plugin marketplace add estevaoeller/agent-skills
claude plugin install project-memory@estevaoeller-skills
```

## Atualizar

Apos publicar alteracoes:

```text
/plugin marketplace update estevaoeller-skills
/plugin update project-memory@estevaoeller-skills
```

Enquanto o campo `version` for omitido dos manifestos, cada novo commit Git pode ser tratado como uma nova versao. Quando o repositorio amadurecer, pode-se adotar versionamento semantico, lembrando de incrementar a versao a cada release.

## Validar antes de publicar

Na raiz do repositorio:

```bash
claude plugin validate .
python scripts/check_marketplace.py
```

## Testar localmente

```bash
claude plugin marketplace add /caminho/para/agent-skills
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
claude plugin marketplace add estevaoeller/agent-skills --scope project
claude plugin install project-memory@estevaoeller-skills --scope project
```

## Regra de isolamento

Cada plugin deve carregar seus proprios arquivos dentro da respectiva pasta. Nao utilize referencias como `../shared`, pois plugins instalados sao copiados para um cache separado.
