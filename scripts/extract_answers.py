# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Derive copier answers from an existing MicroDrop plugin repo checkout.

Reads a plugin repo's ``pyproject.toml``, ``microdrop_plugin.toml``, and
``.pre-commit-config.yaml`` and prints the answers a `copier copy` of
`microdrop-plugin-template` would need to reproduce its shared config.
"""

# Standard library imports.
import sys
from pathlib import Path

import tomllib

# Third-party imports.
import yaml


def _read_pyproject(repo_path):
    """Return package_name, version, description, packages, entry point name/module,
    run_dependencies, and optional_extras from pyproject.toml."""
    data = tomllib.loads((repo_path / "pyproject.toml").read_text())
    project = data["project"]

    entry_points = project.get("entry-points", {}).get("microdrop.plugins", {})
    [(entry_point_name, anchor_package)] = entry_points.items()

    packages = data["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    run_dependencies = (
        data.get("tool", {})
        .get("pixi", {})
        .get("package", {})
        .get("run-dependencies", {})
    )
    optional_extras = project.get("optional-dependencies", {})

    return {
        "package_name": project["name"],
        "version": project["version"],
        "description": project["description"],
        "packages": packages,
        "entry_point_name": entry_point_name,
        "anchor_package": anchor_package,
        "run_dependencies": run_dependencies,
        "optional_extras": optional_extras,
    }


def _read_manifest(repo_path):
    """Return device_name, device_label, and the ui/backend group plugins+labels
    from microdrop_plugin.toml."""
    data = tomllib.loads((repo_path / "microdrop_plugin.toml").read_text())

    ui_group = next(g for g in data["groups"] if g["name"].endswith("_ui"))
    backend_group = next(g for g in data["groups"] if g["name"].endswith("_backend"))

    return {
        "device_name": data["name"],
        "device_label": data["label"],
        "ui_group_label": ui_group["label"],
        "ui_plugins": ui_group["plugins"],
        "backend_group_label": backend_group["label"],
        "backend_plugins": backend_group["plugins"],
    }


def _read_large_file_exclude(repo_path):
    """Return the `exclude` regex of the `check-added-large-files` hook in the
    repo's .pre-commit-config.yaml, or "" if there is none."""
    config_path = repo_path / ".pre-commit-config.yaml"
    if not config_path.exists():
        return ""

    config = yaml.safe_load(config_path.read_text())
    for repo in config.get("repos", []):
        for hook in repo.get("hooks", []):
            if hook.get("id") == "check-added-large-files":
                return hook.get("exclude", "")

    return ""


def _has_redis_gated_tests(repo_path):
    """Return whether the repo has a `tests_with_redis_server_need` directory."""
    return any(repo_path.rglob("tests_with_redis_server_need"))


def extract_answers(repo_path):
    """Derive the copier answers for `microdrop-plugin-template` from an
    existing plugin repo checkout at `repo_path`."""
    repo_path = Path(repo_path)

    answers = {}
    answers.update(_read_pyproject(repo_path))
    answers.update(_read_manifest(repo_path))
    answers["large_file_exclude"] = _read_large_file_exclude(repo_path)
    answers["has_redis_gated_tests"] = _has_redis_gated_tests(repo_path)

    return answers


def main():
    repo_path = Path(sys.argv[1])
    answers = extract_answers(repo_path)
    print(yaml.safe_dump(answers, sort_keys=False))


if __name__ == "__main__":
    main()
