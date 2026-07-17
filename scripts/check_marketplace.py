#!/usr/bin/env python3
"""Valida a estrutura basica do marketplace sem depender do Claude Code."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED = {
    "agent-skills",
    "anthropic-agent-skills",
    "anthropic-marketplace",
    "anthropic-plugins",
    "claude-code-marketplace",
    "claude-code-plugins",
    "claude-plugins-official",
    "knowledge-work-plugins",
    "life-sciences",
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Arquivo ausente: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON invalido em {path}: {exc}") from exc


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    marketplace_path = root / ".claude-plugin" / "marketplace.json"

    try:
        marketplace = load_json(marketplace_path)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    name = marketplace.get("name")
    if not isinstance(name, str) or not KEBAB.fullmatch(name):
        errors.append("O nome do marketplace deve estar em kebab-case.")
    if name in RESERVED:
        errors.append(f"O nome do marketplace e reservado: {name}")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("O marketplace precisa conter pelo menos um plugin.")
        plugins = []

    seen: set[str] = set()
    for index, plugin in enumerate(plugins):
        label = f"plugins[{index}]"
        plugin_name = plugin.get("name") if isinstance(plugin, dict) else None
        source = plugin.get("source") if isinstance(plugin, dict) else None

        if not isinstance(plugin_name, str) or not KEBAB.fullmatch(plugin_name):
            errors.append(f"{label}.name deve estar em kebab-case.")
            continue
        if plugin_name in seen:
            errors.append(f"Plugin duplicado: {plugin_name}")
        seen.add(plugin_name)

        if not isinstance(source, str) or not source.startswith("./") or ".." in Path(source).parts:
            errors.append(f"{label}.source deve ser um caminho relativo iniciado por './' e sem '..'.")
            continue

        plugin_root = root / source[2:]
        manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
        try:
            manifest = load_json(manifest_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if manifest.get("name") != plugin_name:
            errors.append(
                f"Nome divergente: marketplace={plugin_name}, plugin.json={manifest.get('name')!r}"
            )

        skills_dir = plugin_root / "skills"
        skill_files = list(skills_dir.glob("*/SKILL.md")) if skills_dir.exists() else []
        if not skill_files and not (plugin_root / "SKILL.md").exists():
            errors.append(f"Nenhuma skill encontrada em {plugin_root}")

    if errors:
        print("Marketplace invalido:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Marketplace valido: {name}")
    print(f"Plugins registrados: {len(plugins)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
