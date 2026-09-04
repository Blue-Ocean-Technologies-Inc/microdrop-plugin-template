# microdrop-plugin-template

A [copier](https://copier.readthedocs.io/) template that owns the shared dev
tooling and packaging skeleton (ruff config, pre-commit hooks, import-linter,
CI workflows, `pyproject.toml`/`microdrop_plugin.toml` scaffolding) common to
the MicroDrop plugin repos — heater, magnet, and fluorescence. Plugin-specific
code stays in each plugin's own repo; only the conventions that should stay
in sync across all three live here.

Apply the template to a new or existing plugin repo with
`pixi exec --spec copier -- copier copy --trust <this dir> <repo> --data-file answers.yml`;
pull in template updates inside an existing plugin repo with
`pixi exec --spec copier -- copier update --trust`.
