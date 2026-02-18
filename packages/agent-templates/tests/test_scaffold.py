# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_templates.scaffold module."""

import pytest
import yaml

from cervellaswarm_agent_templates.scaffold import (
    TEAM_PRESETS,
    TEMPLATE_TYPES,
    WORKER_SPECIALTIES,
    create_agent,
    create_shared_dna,
    create_team,
    create_team_config,
    list_templates,
)

# ---------------------------------------------------------------------------
# list_templates tests
# ---------------------------------------------------------------------------


class TestListTemplates:
    def test_returns_dict_with_types(self):
        result = list_templates()
        assert "types" in result

    def test_returns_dict_with_specialties(self):
        result = list_templates()
        assert "specialties" in result

    def test_returns_dict_with_team_presets(self):
        result = list_templates()
        assert "team_presets" in result

    def test_types_contains_all_four_types(self):
        result = list_templates()
        types = result["types"]
        assert "coordinator" in types
        assert "quality-gate" in types
        assert "architect" in types
        assert "worker" in types

    def test_specialties_contains_expected_keys(self):
        result = list_templates()
        specialties = result["specialties"]
        for key in ["backend", "frontend", "tester", "researcher", "devops", "docs", "generic"]:
            assert key in specialties, f"Missing specialty: {key}"

    def test_team_presets_contains_minimal_standard_full(self):
        result = list_templates()
        presets = result["team_presets"]
        assert "minimal" in presets
        assert "standard" in presets
        assert "full" in presets

    def test_types_values_are_strings(self):
        result = list_templates()
        for key, val in result["types"].items():
            assert isinstance(val, str), f"Type '{key}' display_name should be a string"

    def test_specialties_values_are_strings(self):
        result = list_templates()
        for key, val in result["specialties"].items():
            assert isinstance(val, str), f"Specialty '{key}' description should be a string"

    def test_team_presets_values_are_strings(self):
        result = list_templates()
        for key, val in result["team_presets"].items():
            assert isinstance(val, str), f"Preset '{key}' description should be a string"


# ---------------------------------------------------------------------------
# create_agent tests
# ---------------------------------------------------------------------------


class TestCreateAgentTypes:
    def test_coordinator_creates_file(self, tmp_dir):
        path = create_agent("coordinator", output_dir=tmp_dir)
        assert path.exists()
        assert path.suffix == ".md"

    def test_quality_gate_creates_file(self, tmp_dir):
        path = create_agent("quality-gate", output_dir=tmp_dir)
        assert path.exists()
        assert path.suffix == ".md"

    def test_architect_creates_file(self, tmp_dir):
        path = create_agent("architect", output_dir=tmp_dir)
        assert path.exists()
        assert path.suffix == ".md"

    def test_worker_creates_file(self, tmp_dir):
        path = create_agent("worker", output_dir=tmp_dir)
        assert path.exists()
        assert path.suffix == ".md"

    def test_coordinator_default_name(self, tmp_dir):
        path = create_agent("coordinator", output_dir=tmp_dir)
        assert path.name == "coordinator.md"

    def test_quality_gate_default_name(self, tmp_dir):
        path = create_agent("quality-gate", output_dir=tmp_dir)
        assert path.name == "quality-gate.md"

    def test_architect_default_name(self, tmp_dir):
        path = create_agent("architect", output_dir=tmp_dir)
        assert path.name == "architect.md"

    def test_worker_default_name(self, tmp_dir):
        path = create_agent("worker", output_dir=tmp_dir)
        assert path.name == "worker.md"

    def test_custom_name_used_in_filename(self, tmp_dir):
        path = create_agent("coordinator", name="my-lead", output_dir=tmp_dir)
        assert path.name == "my-lead.md"

    def test_custom_name_substituted_in_content(self, tmp_dir):
        path = create_agent("coordinator", name="super-lead", output_dir=tmp_dir)
        content = path.read_text()
        assert "super-lead" in content

    def test_template_placeholders_replaced(self, tmp_dir):
        path = create_agent("coordinator", output_dir=tmp_dir)
        content = path.read_text()
        assert "{{ name }}" not in content
        assert "{{ display_name }}" not in content
        assert "{{ date }}" not in content
        assert "{{ team_name }}" not in content

    def test_team_name_in_content(self, tmp_dir):
        path = create_agent("coordinator", team_name="alpha-team", output_dir=tmp_dir)
        content = path.read_text()
        assert "alpha-team" in content

    def test_returns_path_object(self, tmp_dir):
        from pathlib import Path
        path = create_agent("worker", output_dir=tmp_dir)
        assert isinstance(path, Path)


class TestCreateAgentWorkerSpecialties:
    def test_backend_specialty(self, tmp_dir):
        path = create_agent("worker", specialty="backend", output_dir=tmp_dir)
        assert path.exists()
        content = path.read_text()
        assert "{{ specialty }}" not in content
        assert "{{ specialty_description }}" not in content

    def test_frontend_specialty(self, tmp_dir):
        path = create_agent("worker", specialty="frontend", output_dir=tmp_dir)
        assert path.exists()

    def test_tester_specialty(self, tmp_dir):
        path = create_agent("worker", specialty="tester", output_dir=tmp_dir)
        assert path.exists()

    def test_researcher_specialty(self, tmp_dir):
        path = create_agent("worker", specialty="researcher", output_dir=tmp_dir)
        assert path.exists()

    def test_devops_specialty(self, tmp_dir):
        path = create_agent("worker", specialty="devops", output_dir=tmp_dir)
        assert path.exists()

    def test_docs_specialty(self, tmp_dir):
        path = create_agent("worker", specialty="docs", output_dir=tmp_dir)
        assert path.exists()

    def test_generic_specialty(self, tmp_dir):
        path = create_agent("worker", specialty="generic", output_dir=tmp_dir)
        assert path.exists()

    def test_specialty_name_in_content(self, tmp_dir):
        path = create_agent("worker", specialty="backend", output_dir=tmp_dir)
        content = path.read_text()
        # The specialty title "Backend" should appear in rendered content
        assert "Backend" in content

    def test_all_specialty_placeholders_replaced(self, tmp_dir):
        path = create_agent("worker", specialty="frontend", output_dir=tmp_dir)
        content = path.read_text()
        assert "{{ specialty }}" not in content
        assert "{{ specialty_description }}" not in content
        assert "{{ specialty_details }}" not in content
        assert "{{ allowed_files }}" not in content
        assert "{{ disallowed_files }}" not in content


class TestCreateAgentErrors:
    def test_invalid_type_raises_value_error(self, tmp_dir):
        with pytest.raises(ValueError, match="Unknown agent type"):
            create_agent("superstar", output_dir=tmp_dir)

    def test_invalid_type_message_contains_valid_types(self, tmp_dir):
        with pytest.raises(ValueError) as exc_info:
            create_agent("bad-type", output_dir=tmp_dir)
        msg = str(exc_info.value)
        assert "coordinator" in msg or "worker" in msg

    def test_invalid_specialty_raises_value_error(self, tmp_dir):
        with pytest.raises(ValueError, match="Unknown specialty"):
            create_agent("worker", specialty="blockchain", output_dir=tmp_dir)

    def test_invalid_specialty_message_contains_valid(self, tmp_dir):
        with pytest.raises(ValueError) as exc_info:
            create_agent("worker", specialty="unicorn", output_dir=tmp_dir)
        msg = str(exc_info.value)
        assert "backend" in msg or "frontend" in msg

    def test_specialty_only_checked_for_worker_type(self, tmp_dir):
        # Other types should not care about specialty
        path = create_agent("coordinator", specialty="backend", output_dir=tmp_dir)
        assert path.exists()


class TestCreateAgentOutputDir:
    def test_creates_output_dir_if_not_exists(self, tmp_dir):
        nested = tmp_dir / "new" / "subdir"
        assert not nested.exists()
        path = create_agent("coordinator", output_dir=nested)
        assert nested.exists()
        assert path.exists()

    def test_uses_existing_output_dir(self, tmp_dir):
        path = create_agent("coordinator", output_dir=tmp_dir)
        assert path.parent == tmp_dir

    def test_accepts_string_output_dir(self, tmp_dir):
        path = create_agent("coordinator", output_dir=str(tmp_dir))
        assert path.exists()


# ---------------------------------------------------------------------------
# create_shared_dna tests
# ---------------------------------------------------------------------------


class TestCreateSharedDna:
    def test_creates_shared_dna_file(self, tmp_dir):
        path = create_shared_dna(output_dir=tmp_dir)
        assert path.exists()
        assert path.name == "_shared_dna.md"

    def test_team_name_substituted(self, tmp_dir):
        path = create_shared_dna(output_dir=tmp_dir, team_name="test-team")
        content = path.read_text()
        assert "test-team" in content

    def test_no_unresolved_placeholders(self, tmp_dir):
        path = create_shared_dna(output_dir=tmp_dir, team_name="my-team")
        content = path.read_text()
        assert "{{ team_name }}" not in content

    def test_default_team_name(self, tmp_dir):
        path = create_shared_dna(output_dir=tmp_dir)
        content = path.read_text()
        assert "my-team" in content

    def test_creates_output_dir_if_needed(self, tmp_dir):
        nested = tmp_dir / "agents"
        path = create_shared_dna(output_dir=nested)
        assert nested.exists()
        assert path.exists()

    def test_returns_path_object(self, tmp_dir):
        from pathlib import Path
        path = create_shared_dna(output_dir=tmp_dir)
        assert isinstance(path, Path)


# ---------------------------------------------------------------------------
# create_team_config tests
# ---------------------------------------------------------------------------


class TestCreateTeamConfig:
    def test_minimal_preset_creates_yaml(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        assert path.exists()
        assert path.name == "team.yaml"

    def test_standard_preset_creates_yaml(self, tmp_dir):
        path = create_team_config("standard", output_dir=tmp_dir)
        assert path.exists()

    def test_full_preset_creates_yaml(self, tmp_dir):
        path = create_team_config("full", output_dir=tmp_dir)
        assert path.exists()

    def test_invalid_preset_raises_value_error(self, tmp_dir):
        with pytest.raises(ValueError, match="Unknown preset"):
            create_team_config("mega", output_dir=tmp_dir)

    def test_invalid_preset_message_contains_valid(self, tmp_dir):
        with pytest.raises(ValueError) as exc_info:
            create_team_config("bad", output_dir=tmp_dir)
        msg = str(exc_info.value)
        assert "minimal" in msg or "standard" in msg or "full" in msg

    def test_output_is_valid_yaml(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        content = path.read_text()
        data = yaml.safe_load(content)
        assert isinstance(data, dict)

    def test_yaml_contains_team_name(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir, team_name="alpha")
        data = yaml.safe_load(path.read_text())
        assert data["name"] == "alpha"

    def test_yaml_contains_agents_list(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        data = yaml.safe_load(path.read_text())
        assert "agents" in data
        assert isinstance(data["agents"], list)
        assert len(data["agents"]) > 0

    def test_yaml_has_entry_point(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        data = yaml.safe_load(path.read_text())
        assert "entry_point" in data
        assert data["entry_point"] == "lead"

    def test_yaml_has_process(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        data = yaml.safe_load(path.read_text())
        assert data["process"] == "hierarchical"

    def test_standard_has_more_agents_than_minimal(self, tmp_dir):
        min_path = create_team_config("minimal", output_dir=tmp_dir / "min")
        std_path = create_team_config("standard", output_dir=tmp_dir / "std")
        min_data = yaml.safe_load(min_path.read_text())
        std_data = yaml.safe_load(std_path.read_text())
        assert len(std_data["agents"]) > len(min_data["agents"])

    def test_full_has_more_agents_than_standard(self, tmp_dir):
        std_path = create_team_config("standard", output_dir=tmp_dir / "std")
        full_path = create_team_config("full", output_dir=tmp_dir / "full")
        std_data = yaml.safe_load(std_path.read_text())
        full_data = yaml.safe_load(full_path.read_text())
        assert len(full_data["agents"]) > len(std_data["agents"])

    def test_agent_entries_have_required_keys(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        data = yaml.safe_load(path.read_text())
        for agent in data["agents"]:
            assert "name" in agent
            assert "type" in agent
            assert "role" in agent

    def test_coordinator_gets_lead_role(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        data = yaml.safe_load(path.read_text())
        coordinator = next(a for a in data["agents"] if a["type"] == "coordinator")
        assert coordinator["role"] == "lead"

    def test_quality_gate_gets_validator_role(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        data = yaml.safe_load(path.read_text())
        qa = next(a for a in data["agents"] if a["type"] == "quality-gate")
        assert qa["role"] == "validator"

    def test_worker_gets_worker_role(self, tmp_dir):
        path = create_team_config("minimal", output_dir=tmp_dir)
        data = yaml.safe_load(path.read_text())
        worker = next(a for a in data["agents"] if a["type"] == "worker")
        assert worker["role"] == "worker"


# ---------------------------------------------------------------------------
# create_team tests
# ---------------------------------------------------------------------------


class TestCreateTeam:
    def test_minimal_preset_creates_files(self, tmp_dir):
        files = create_team("minimal", output_dir=tmp_dir)
        assert len(files) > 0
        for f in files:
            assert f.exists()

    def test_standard_preset_creates_files(self, tmp_dir):
        files = create_team("standard", output_dir=tmp_dir)
        assert len(files) > 0
        for f in files:
            assert f.exists()

    def test_full_preset_creates_files(self, tmp_dir):
        files = create_team("full", output_dir=tmp_dir)
        assert len(files) > 0
        for f in files:
            assert f.exists()

    def test_invalid_preset_raises_value_error(self, tmp_dir):
        with pytest.raises(ValueError, match="Unknown preset"):
            create_team("turbo", output_dir=tmp_dir)

    def test_minimal_file_count(self, tmp_dir):
        # minimal: 1 shared_dna + 1 team.yaml + 3 agents = 5
        files = create_team("minimal", output_dir=tmp_dir)
        assert len(files) == 5

    def test_standard_file_count(self, tmp_dir):
        # standard: 1 shared_dna + 1 team.yaml + 7 agents = 9
        files = create_team("standard", output_dir=tmp_dir)
        assert len(files) == 9

    def test_full_file_count(self, tmp_dir):
        # full: 1 shared_dna + 1 team.yaml + 17 agents = 19
        files = create_team("full", output_dir=tmp_dir)
        assert len(files) == 19

    def test_shared_dna_always_included(self, tmp_dir):
        files = create_team("minimal", output_dir=tmp_dir)
        names = [f.name for f in files]
        assert "_shared_dna.md" in names

    def test_team_yaml_always_included(self, tmp_dir):
        files = create_team("minimal", output_dir=tmp_dir)
        names = [f.name for f in files]
        assert "team.yaml" in names

    def test_all_files_in_output_dir(self, tmp_dir):
        files = create_team("minimal", output_dir=tmp_dir)
        for f in files:
            assert f.parent == tmp_dir

    def test_team_name_propagated_to_files(self, tmp_dir):
        files = create_team("minimal", output_dir=tmp_dir, team_name="beta-squad")
        # Check team.yaml
        team_yaml = next(f for f in files if f.name == "team.yaml")
        data = yaml.safe_load(team_yaml.read_text())
        assert data["name"] == "beta-squad"

    def test_returns_list_of_path_objects(self, tmp_dir):
        from pathlib import Path
        files = create_team("minimal", output_dir=tmp_dir)
        assert isinstance(files, list)
        for f in files:
            assert isinstance(f, Path)

    def test_full_has_more_files_than_minimal(self, tmp_dir):
        min_files = create_team("minimal", output_dir=tmp_dir / "min")
        full_files = create_team("full", output_dir=tmp_dir / "full")
        assert len(full_files) > len(min_files)

    def test_all_agent_md_files_exist(self, tmp_dir):
        files = create_team("minimal", output_dir=tmp_dir)
        md_files = [f for f in files if f.suffix == ".md" and f.name != "_shared_dna.md"]
        assert len(md_files) > 0
        for f in md_files:
            assert f.exists()
            assert f.stat().st_size > 0

    def test_creates_output_dir_if_needed(self, tmp_dir):
        nested = tmp_dir / "new_team"
        assert not nested.exists()
        files = create_team("minimal", output_dir=nested)
        assert nested.exists()
        assert len(files) == 5
