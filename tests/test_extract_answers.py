# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

# Standard library imports.
import textwrap

# Local imports.
from scripts.extract_answers import extract_answers


def test_extracts_from_heater_like_repo(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        textwrap.dedent("""
        [project]
        name = "heater-microdrop-plugin"
        version = "1.10.1"
        description = "MicroDrop heater plugin"
        [project.entry-points."microdrop.plugins"]
        heater = "heater_controller"
        [tool.hatch.build.targets.wheel]
        packages = ["heater_controller", "heater_controls_ui", "heater_protocol_controls"]
        [tool.pixi.package.run-dependencies]
        mpremote = ">=1.20"
    """)
    )
    (tmp_path / "microdrop_plugin.toml").write_text(
        textwrap.dedent("""
        schema_version = 1
        name = "heater"
        label = "Heater"
        packages = ["heater_controller", "heater_controls_ui", "heater_protocol_controls"]
        [[groups]]
        name = "heater_ui"
        label = "Heater UI"
        plugins = ["heater_controls_ui.plugin:HeaterControlsUiPlugin"]
        enabled_key = "plugin_group_enabled.heater_ui"
        [[groups]]
        name = "heater_backend"
        label = "Heater backend"
        plugins = ["heater_controller.plugin:HeaterControllerPlugin"]
        enabled_key = "plugin_group_enabled.heater_backend"
    """)
    )
    answers = extract_answers(tmp_path)
    assert answers["package_name"] == "heater-microdrop-plugin"
    assert answers["device_name"] == "heater"
    assert answers["device_label"] == "Heater"
    assert answers["version"] == "1.10.1"
    assert answers["packages"] == [
        "heater_controller",
        "heater_controls_ui",
        "heater_protocol_controls",
    ]
    assert answers["anchor_package"] == "heater_controller"
    assert answers["entry_point_name"] == "heater"
    assert answers["ui_plugins"] == ["heater_controls_ui.plugin:HeaterControlsUiPlugin"]
    assert answers["backend_plugins"] == [
        "heater_controller.plugin:HeaterControllerPlugin"
    ]
    assert answers["run_dependencies"] == {"mpremote": ">=1.20"}
    assert answers["optional_extras"] == {}
    assert answers["has_redis_gated_tests"] is False
