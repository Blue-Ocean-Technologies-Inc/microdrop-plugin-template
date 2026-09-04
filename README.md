# microdrop-plugin-template

A [copier](https://copier.readthedocs.io/) template that owns the shared dev
tooling and packaging skeleton (ruff config, pre-commit hooks, import-linter,
CI workflows, `pyproject.toml`/`microdrop_plugin.toml` scaffolding) common to
the MicroDrop plugin repos — heater, magnet, and fluorescence. Plugin-specific
code stays in each plugin's own repo; only the conventions that should stay
in sync across all three live here.

To apply the template to a new or existing plugin repo:

```bash
pixi exec --spec copier -- copier copy --trust <this dir> <repo> --data-file answers.yml
```

To pull in template updates inside an existing plugin repo:

```bash
pixi exec --spec copier -- copier update --trust
```

`scripts/extract_answers.py` derives an `answers.yml` from an existing
plugin checkout, so a repo already carrying the shared config can be
migrated onto the template without retyping its answers by hand:

```bash
python scripts/extract_answers.py <plugin-repo-path> > answers.yml
```
