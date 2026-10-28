# Separate Skill Projects Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate the current collection into independent `project-memory` and `excel-model-review` project directories while retaining the root as the marketplace catalog.

**Architecture:** Move the Project Memory plugin and its standalone kit into one project directory. Extract the useful contents of the Excel installation copy into a clean project directory, excluding runtime cache from its source layout. Leave the root with only marketplace-level metadata, documentation, and migration records.

**Tech Stack:** Git, Claude Code plugin manifests, Python scripts.

**Spec:** `docs/superpowers/specs/2026-10-23-separate-skill-projects-design.md`

## Global Constraints

- Preserve all existing files; do not delete cache or release artifacts.
- Preserve currently modified user files without overwriting them.
- Do not create or publish GitHub repositories in this migration.
- Do not change skill behavior or script interfaces.

## Review Focus

- Marketplace entries must reference the intended future GitHub repositories, not removed relative plugin paths.
- `project-memory`'s generated kit must retain the same source/plugin relationship.
- Excel cache markers (`.in_use`) and bytecode (`__pycache__`) must not be presented as source files.
- Existing local edits in `README.md` and Project Memory templates must survive their moves.
- Project manifests must remain discoverable at each project root.

---

### Task 1: Establish the project boundaries

**Files:**
- Create: `project-memory/`
- Create: `excel-model-review/`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: Existing project directories in the repository root.
- Produces: Two clean project roots with preserved source files.

- [ ] **Step 1: Create the two project root directories**

Create `project-memory/` and `excel-model-review/` without overwriting existing content.

- [ ] **Step 2: Move the Project Memory plugin, standalone kit, and its release artifacts into `project-memory/`**

Move `plugins/project-memory/`, `project-memory-wiki-kit-v3/`, and the Project Memory zip so they are owned by one project.

- [ ] **Step 3: Extract the Excel source into `excel-model-review/`**

Move the contents of `excel-model-review/30bfc4e764da/` to the clean project root, retaining `.in_use` in a preserved cache subdirectory rather than source layout.

- [ ] **Step 4: Add cache rules to the relevant `.gitignore` files**

Ignore Python bytecode and `.in_use/` directories in the Excel project.

- [ ] **Step 5: Verify the intended source files remain present**

Run: `git status --short` and list each project root.

Expected: Both roots contain their manifests, skills, scripts, and documentation; no source content is missing.

### Task 2: Convert the root into a marketplace catalog

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md`
- Create: `docs/MIGRATION.md`

**Interfaces:**
- Consumes: The two project names and their future GitHub repository names.
- Produces: A catalog that advertises `project-memory` and `excel-model-review` as external plugin sources.

- [ ] **Step 1: Replace relative marketplace sources with GitHub source descriptors**

Use `estevaoeller/project-memory` and `estevaoeller/excel-model-review` as the future repository references.

- [ ] **Step 2: Rewrite the root README as a marketplace catalog README**

Document that this repository is an index and link to the two independent project directories/repositories.

- [ ] **Step 3: Add migration documentation**

Record where the original paths moved and what remains to publish remotely.

- [ ] **Step 4: Validate marketplace JSON**

Run: `python scripts/check_marketplace.py`

Expected: The marketplace JSON parses and exposes both entries.

### Task 3: Validate each standalone project

**Files:**
- Modify: `project-memory/README.md`
- Modify: `excel-model-review/README.md`

**Interfaces:**
- Consumes: New project-root layouts.
- Produces: Self-contained project documentation.

- [ ] **Step 1: Update Project Memory paths and README references**

Ensure its build script and standalone-kit documentation resolve from its new project root.

- [ ] **Step 2: Update the Excel README references**

Ensure it names its two skills and documents the local test command.

- [ ] **Step 3: Run project validation commands**

Run: `python project-memory/scripts/build_wiki_kit.py --check` and `python -m pytest excel-model-review/tests -q`.

Expected: The Project Memory kit reports synchronized output and the Excel tests pass.

- [ ] **Step 4: Review the migration diff**

Run: `git status --short` and inspect renamed, modified, and untracked files.

Expected: All changes are explainable as a move, catalog update, or documentation update.
