# Changelog

## 3.3.1 (12/11/2026)

- o template deixa de incluir o `.goosehints` (pedido de Estevao Eller em 12/11/2026). Projetos novos não recebem mais o
  arquivo; projetos já criados não são afetados e podem apagá-lo.

## 3.3 (12/11/2026)

- a pasta de histórico passa de `history/` para `_history/`, como a `_wiki/` (o sublinhado mantém a pasta no topo da
  listagem). Quebra de compatibilidade: projetos criados por versão anterior precisam renomear a pasta (ver "Migração");
- as notas criadas pela skill ganham o campo `project_memory: <versão>` no frontmatter, nos modos `perfil` e `nucleo`. A
  versão vem do `version:` do `SKILL.md`, e o campo não muda quando a nota é editada;
- o `init_project.py` lê a versão tanto no layout de skill solta quanto no de plugin.

## 3.2

Origem: pedido de Estevao Eller em 11/11/2026, para que os planos criados no modo de planejamento fiquem junto da memória do
projeto.

- `init_project.py` grava `"plansDirectory": "_wiki/planos"` no `.claude/settings.json` do projeto, preservando as demais chaves
  e sem sobrescrever um valor já definido; a opção `--plans-dir` troca o caminho;
- a seção "Planos" da skill explica o mecanismo: caminho relativo à pasta em que a sessão abre, ajuste quando a `_wiki/` fica
  numa subpasta, renomear o plano de nome automático ao aprová-lo e o que fazer quando a chave não existe;
- a linha "Plano aprovado" de `references/destinos.md` cita o `plansDirectory`.

## Migração de versão anterior para a 3.3

1. Renomear `history/` para `_history/` no projeto.
2. Ajustar as menções à pasta em `AGENTS.md`, `PROJECT.md`, `NOW.md`, `TASKS.md` e `_wiki/INDEX.md`.
3. Manter `type: Project History` no frontmatter dos registros: é o tipo da nota, não o nome da pasta.

As notas antigas não ganham `project_memory` sozinhas. A ausência do campo indica nota criada antes da 3.3.0.

## 3.1

Origem: um mês de uso em um projeto real, revisado por Estevao Eller entre 30 e 31/10/2026.

- a wiki passa de `.wiki/` para `_wiki/`;
- frontmatter portátil na `_wiki/` e no `history/`, em três modos (`perfil` padrão, `nucleo`, `nenhum`), escolhido por perguntas
  na criação do projeto e gravado no `PROJECT.md`; datas DD/MM/AAAA;
- registro sem pedido ao fim de cada passo com gatilho, e linha final `Registrado em:`;
- tabela de destinos (`references/destinos.md`), com registro de achados, `PERGUNTAS.md` e "Destinos deste projeto" no `AGENTS.md`;
- pedido repetido vira regra; consultar wiki e history antes de propor;
- nada se apaga: nota "Revisto mais à frente", `z.old/`, cópia antes de mexer em arquivo em uso;
- regras fixas no topo do `PROJECT.md`; `NOW.md` com até cerca de 150 linhas;
- `TASKS.md` em lista por frente; rastreabilidade de agente e modelo fica opcional;
- regras para várias sessões e agentes no mesmo projeto, e para salvar planos aprovados em `_wiki/planos/`;
- modelos novos: `_wiki/_modelo-pagina.md` e `history/_modelo-registro.md`;
- as cópias locais da skill nos projetos passam a levar `references/` e são geradas por script.

## 3.0 Adaptive

- reduziu o núcleo inicial para seis elementos;
- substituiu perfis fixos por estrutura emergente;
- unificou atividades humanas e fila de agentes em `TASKS.md`, mantendo seções distintas;
- adotou leitura progressiva e proibição de varredura integral automática;
- tornou o histórico sob demanda;
- simplificou o registro de agente, provedor e modelo;
- manteve validação humana separada da conclusão técnica;
- removeu YAML obrigatório por execução, taxonomias antecipadas e pastas vazias especializadas.
