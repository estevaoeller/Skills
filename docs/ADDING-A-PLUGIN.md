# Adicionar uma nova skill ou plugin

## 1. Criar a pasta

```text
plugins/nome-do-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── nome-da-skill/
│       └── SKILL.md
├── README.md
├── scripts/       # opcional
└── templates/     # opcional
```

Use nomes em `kebab-case`, sem espacos.

## 2. Criar o manifesto do plugin

Exemplo minimo:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "nome-do-plugin",
  "displayName": "Nome do Plugin",
  "description": "Descricao objetiva do plugin.",
  "author": {
    "name": "Estevao Eller"
  },
  "repository": "https://github.com/estevaoeller/agent-skills",
  "license": "MIT",
  "skills": "./skills/"
}
```

## 3. Registrar no marketplace

Adicione uma entrada ao array `plugins` em `.claude-plugin/marketplace.json`:

```json
{
  "name": "nome-do-plugin",
  "source": "./plugins/nome-do-plugin",
  "description": "Descricao objetiva.",
  "category": "productivity",
  "tags": ["tag-1", "tag-2"],
  "strict": true
}
```

## 4. Validar

```bash
claude plugin validate .
python scripts/check_marketplace.py
```

## 5. Testar

```bash
claude plugin marketplace update estevaoeller-skills
claude plugin install nome-do-plugin@estevaoeller-skills
```

A skill sera exposta com namespace. Por exemplo:

```text
/nome-do-plugin:nome-da-skill
```

## 6. Publicar

```bash
git add .
git commit -m "Add nome-do-plugin"
git push
```

## Versionamento

No inicio, omita o campo `version`. Assim, novos commits do repositorio sao percebidos como novas versoes. Adote versoes explicitas somente quando houver processo de release; nesse caso, incremente a versao em toda publicacao.
