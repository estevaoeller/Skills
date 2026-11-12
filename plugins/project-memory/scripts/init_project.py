#!/usr/bin/env python3
"""Inicializa um projeto com o núcleo adaptativo de memória."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path


def read_skill_version() -> str:
    """Lê a versão do SKILL.md, para a versão gravada nas notas ter uma fonte só.

    Aceita os dois layouts: skill solta (SKILL.md ao lado de scripts/) e plugin (skills/project-memory/SKILL.md).
    """
    root = Path(__file__).resolve().parent.parent
    for skill_md in (root / "SKILL.md", root / "skills" / "project-memory" / "SKILL.md"):
        try:
            for line in skill_md.read_text(encoding="utf-8").splitlines()[:10]:
                if line.startswith("version:"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            continue
    return "unknown"


SKILL_VERSION = read_skill_version()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"Inicializa Project Memory {SKILL_VERSION}")
    parser.add_argument("target", type=Path, help="Pasta de destino do projeto")
    parser.add_argument("--name", default=None, help="Nome do projeto")
    parser.add_argument(
        "--frontmatter",
        choices=("perfil", "nucleo", "nenhum"),
        default="perfil",
        help="Frontmatter da _wiki/ e do _history/: núcleo + perfil de trabalho (padrão), só núcleo, ou nenhum",
    )
    parser.add_argument("--client", default="A definir", help="Cliente (perfil de trabalho)")
    parser.add_argument("--engagement", default="A definir", help="Código do contrato ou projeto (perfil de trabalho)")
    parser.add_argument("--organization", default="A definir", help="Organização (perfil de trabalho)")
    parser.add_argument(
        "--plans-dir",
        default="_wiki/planos",
        help="Pasta dos planos do modo de planejamento, relativa à raiz onde a sessão abre (padrão: _wiki/planos)",
    )
    parser.add_argument("--git", action="store_true", help="Inicializa Git e configura template de commit")
    parser.add_argument("--force", action="store_true", help="Sobrescreve arquivos existentes")
    return parser.parse_args()


def copy_template(template: Path, target: Path, force: bool) -> tuple[int, int]:
    created = 0
    skipped = 0
    for source in template.rglob("*"):
        relative = source.relative_to(template)
        destination = target / relative
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not force:
            skipped += 1
            continue
        shutil.copy2(source, destination)
        created += 1
    return created, skipped


def frontmatter_block(page_type: str, date_br: str, args: argparse.Namespace) -> str:
    """Monta o frontmatter do modo escolhido; vazio no modo nenhum."""
    if args.frontmatter == "nenhum":
        return ""
    lines = ["---"]
    if args.frontmatter == "perfil":
        lines += [
            "domain: Work",
            f"type: {page_type}",
            f"client: {args.client}",
            f"engagement: {args.engagement}",
            f"organization: {args.organization}",
        ]
    else:
        lines.append(f"type: {page_type}")
    lines += [
        f"date_created: {date_br}",
        f"date_modified: {date_br}",
        f"project_memory: {SKILL_VERSION}",
        "related:",
        '  - "[[INDEX]]"',
        "---",
    ]
    return "\n".join(lines)


def replace_placeholders(target: Path, project_name: str, args: argparse.Namespace) -> None:
    today = dt.date.today()
    date_br = today.strftime("%d/%m/%Y")
    profile_unused = f"não usado (frontmatter: {args.frontmatter})"
    use_profile = args.frontmatter == "perfil"
    # Os marcadores de frontmatter vêm primeiro: no modo nenhum somem junto com a linha em branco seguinte.
    replacements = {}
    for marker, page_type in (("{{FRONTMATTER_WIKI}}", "Project Wiki"), ("{{FRONTMATTER_HISTORY}}", "Project History")):
        block = frontmatter_block(page_type, date_br, args)
        replacements[marker if block else marker + "\n\n"] = block
    replacements.update({
        "{{FRONTMATTER_MODE}}": args.frontmatter,
        "{{PROJECT_NAME}}": project_name,
        "{{DATE}}": today.isoformat(),
        "{{DATE_BR}}": date_br,
        "{{CLIENT}}": args.client if use_profile else profile_unused,
        "{{ENGAGEMENT}}": args.engagement if use_profile else profile_unused,
        "{{ORGANIZATION}}": args.organization if use_profile else profile_unused,
    })
    for path in target.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def set_plans_directory(target: Path, plans_dir: str) -> str:
    """Grava plansDirectory no .claude/settings.json do projeto, preservando as demais chaves."""
    settings = target / ".claude" / "settings.json"
    data: dict = {}
    if settings.exists():
        try:
            data = json.loads(settings.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError:
            return f"Aviso: {settings} não é JSON válido; plansDirectory não gravado."
        if data.get("plansDirectory"):
            return f"plansDirectory mantido: {data['plansDirectory']}"
    data["plansDirectory"] = plans_dir
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f"plansDirectory gravado: {plans_dir}"


def init_git(target: Path) -> None:
    try:
        if not (target / ".git").exists():
            subprocess.run(["git", "init"], cwd=target, check=True)
        subprocess.run(
            ["git", "config", "commit.template", str(target / ".gitmessage")],
            cwd=target,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"Aviso: não foi possível configurar Git: {exc}", file=sys.stderr)


def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    template = script_dir.parent / "templates"
    if not template.exists():
        print(f"Template não encontrado: {template}", file=sys.stderr)
        return 1

    target = args.target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    name = args.name or target.name

    created, skipped = copy_template(template, target, args.force)
    replace_placeholders(target, name, args)
    plans_msg = set_plans_directory(target, args.plans_dir)
    if args.git:
        init_git(target)

    print(f"Projeto inicializado em: {target}")
    print(f"Arquivos criados/atualizados: {created}")
    print(f"Arquivos preservados: {skipped}")
    print(plans_msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
