# microdrop-plugin-template

A [copier](https://copier.readthedocs.io/) template for the shared dev
tooling of MicroDrop plugin repos — heater, magnet, fluorescence, and future
ones. It is **tooling-only**: it owns the conventions that should stay in
sync across every plugin repo, not the plugin's own Python packages. Applying
it to a repo renders:

- `ruff.toml` — lint/format config (line length, target, `CPY001` copyright
  header rule, import-section ordering)
- `.pre-commit-config.yaml` — commitizen, `check-ast`/`check-merge-conflict`/
  `check-added-large-files`, ruff, `insert-license`, the shared
  [`microdrop-dev-hooks`](https://github.com/Blue-Ocean-Technologies-Inc/microdrop-dev-hooks)
  (`stamp-import-sections`, `forbid-scratch-files`), and a local
  `import-linter` hook
- `.importlinter` — the plugin-decoupling contract
- `.copyright-header.txt` — the header `insert-license` stamps onto `.py`
  files
- `AGENTS.md` — working-environment and code-style notes for agents
- `LICENSE` — AGPL-3.0, verbatim from Microdrop; the header that
  `insert-license` adds states that the license is "included in LICENSE"
- `.gitignore` — replaces the file with the template's ignore list
  (`.pixi/*`, caches, etc.); repo-specific ignores need to be added to the
  template or re-added after applying it
- `microdrop_plugin.toml` — the plugin manifest (groups, entry points)
- `pyproject.toml` — packaging skeleton: project metadata, the
  `microdrop.plugins` entry point, `[tool.hatch.build]`, `[tool.pixi.package]`,
  and the `[tool.commitizen]` config
- `CHANGELOG.md.j2` — the commitizen changelog template, shared verbatim so
  every repo's `CHANGELOG.md` renders the same way
- `.github/workflows/conventional-commits.yml`, `publish.yml`,
  `unit-tests.yml` — CI: commit-message linting, the automatic conda
  release, and the pytest/import-linter gate (ruff runs in the pre-commit
  hooks, not in CI)
- `.copier-answers.yml` — copier's own bookkeeping, so `copier update` knows
  what was rendered from what template version

Everything else in a plugin repo — the plugin's own packages, tests, and
README — is untouched.

## Apply to an existing plugin

Extract the answers from the plugin's current checkout, then render the
template into it:

```bash
pixi exec --spec pyyaml -- python scripts/extract_answers.py <plugin-repo> > answers.yml
pixi exec --spec copier -- copier copy --trust --data-file answers.yml <this-dir> <plugin-repo>
```

Review the diff before committing — the extractor reads `pyproject.toml`,
`microdrop_plugin.toml`, and `.pre-commit-config.yaml`, but a few answers
(`microdrop_dev_hooks_rev`, `has_redis_gated_tests`) are worth double-checking
by hand.

## Update later

Once a plugin repo has been rendered once (it has `.copier-answers.yml`),
pull in template changes with:

```bash
pixi exec --spec copier -- copier update --trust
```

run from inside the plugin repo.

## Design

- The pre-commit hooks that are shared across repos (`stamp-import-sections`,
  `forbid-scratch-files`) come from
  [`microdrop-dev-hooks`](https://github.com/Blue-Ocean-Technologies-Inc/microdrop-dev-hooks),
  pinned by `rev` in `.pre-commit-config.yaml.jinja` — bump the rev here to
  roll out a hook change to every plugin.
- Tests and `import-linter` run in the `pixi-microdrop` workspace's `test`
  environment, with the plugin repo cloned under `microdrop-py/`.
  Import-linter needs the Microdrop packages importable to tell a plugin's
  `consts` module (the only cross-plugin-safe import) from its internals, and
  that's only possible from inside the workspace where Microdrop's `src` is
  installed editable.
- The template is tooling-only today; scaffolding for brand-new plugins
  (rather than retrofitting existing ones) may be added later.

See
[`docs/superpowers/specs/2026-09-04-convention-rollout-design.md`](https://github.com/Blue-Ocean-Technologies-Inc/Microdrop/blob/main/docs/superpowers/specs/2026-09-04-convention-rollout-design.md)
(lands with Microdrop PR #664) in the Microdrop repo for the full design
rationale behind this rollout.
