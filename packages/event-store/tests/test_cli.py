# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_event_store.cli module."""

import json
import sys

import pytest

from cervellaswarm_event_store.cli import (
    main,
    main_init,
    main_log,
    main_query,
    main_stats,
    main_lessons,
    main_patterns,
    _get_version,
)
from cervellaswarm_event_store.writer import Event, Lesson


class TestGetVersion:
    def test_returns_string(self):
        v = _get_version()
        assert isinstance(v, str)
        assert len(v) > 0

    def test_fallback_version(self):
        # When package not installed, returns fallback
        v = _get_version()
        assert "." in v


class TestMainInit:
    def test_init_creates_db(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_init([f"--db-path={db}"])
        assert db.exists()

    def test_init_json_output(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_init([f"--db-path={db}", "--json"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["status"] == "ok"
        assert "db_path" in data

    def test_init_text_output(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_init([f"--db-path={db}"])
        out = capsys.readouterr().out
        assert "initialized" in out.lower() or str(db) in out


class TestMainLog:
    def test_log_event_success(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_log([
            f"--db-path={db}",
            "--type=task_completed",
            "--agent=backend",
            "--project=proj",
        ])
        out = capsys.readouterr().out
        assert len(out.strip()) > 0

    def test_log_event_json_output(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_log([
            f"--db-path={db}",
            "--type=task_completed",
            "--json",
        ])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["status"] == "ok"
        assert "event_id" in data

    def test_log_with_success_flag(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_log([
            f"--db-path={db}",
            "--type=task_completed",
            "--success",
            "--json",
        ])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["status"] == "ok"

    def test_log_with_fail_flag(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_log([
            f"--db-path={db}",
            "--type=task_failed",
            "--fail",
            "--error-message=something broke",
            "--json",
        ])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["status"] == "ok"

    def test_log_invalid_type_exits(self, tmp_path):
        db = tmp_path / "test.db"
        with pytest.raises(SystemExit) as exc:
            main_log([
                f"--db-path={db}",
                "--type=invalid_type",
                "--json",
            ])
        assert exc.value.code == 1

    def test_log_with_tags(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_log([
            f"--db-path={db}",
            "--type=custom",
            "--tags=a,b,c",
            "--json",
        ])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["status"] == "ok"

    def test_log_with_duration(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_log([
            f"--db-path={db}",
            "--type=task_completed",
            "--duration-ms=1500",
            "--json",
        ])
        data = json.loads(capsys.readouterr().out)
        assert data["status"] == "ok"


class TestMainQuery:
    def _seed(self, db_path):
        from cervellaswarm_event_store.database import EventStore
        with EventStore(db_path) as store:
            store.log_event(Event(event_type="task_completed", agent_name="backend",
                                  project="proj", success=True))
            store.log_event(Event(event_type="task_failed", agent_name="frontend",
                                  project="proj", success=False))

    def test_query_all_json(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_query([f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 2

    def test_query_filter_agent(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_query([f"--db-path={db}", "--agent=backend", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 1

    def test_query_filter_project(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_query([f"--db-path={db}", "--project=proj", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 2

    def test_query_filter_type(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_query([f"--db-path={db}", "--type=task_failed", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 1

    def test_query_limit(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_query([f"--db-path={db}", "--limit=1", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 1

    def test_query_text_output(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_query([f"--db-path={db}"])
        out = capsys.readouterr().out
        assert "Events" in out

    def test_query_empty_store(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_init([f"--db-path={db}"])
        capsys.readouterr()  # consume init output
        main_query([f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 0


class TestMainStats:
    def _seed(self, db_path):
        from cervellaswarm_event_store.database import EventStore
        with EventStore(db_path) as store:
            store.log_event(Event(event_type="task_completed", agent_name="backend",
                                  project="proj", success=True))
            store.log_event(Event(event_type="task_failed", agent_name="frontend",
                                  project="other", success=False))

    def test_stats_json(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_stats([f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total_events"] == 2
        assert "success_rate" in data
        assert "by_agent" in data

    def test_stats_text(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_stats([f"--db-path={db}"])
        out = capsys.readouterr().out
        assert "Statistics" in out or "Events" in out

    def test_stats_project_filter(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_stats([f"--db-path={db}", "--project=proj", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total_events"] == 1
        assert data["project_filter"] == "proj"


class TestMainLessons:
    def _seed(self, db_path):
        from cervellaswarm_event_store.database import EventStore
        with EventStore(db_path) as store:
            store.log_lesson(Lesson(problem="test problem", solution="test solution",
                                    confidence=0.8, project="proj"))

    def test_lessons_json(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_lessons([f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 1

    def test_lessons_text(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed(db)
        main_lessons([f"--db-path={db}"])
        out = capsys.readouterr().out
        assert "Lessons" in out

    def test_lessons_limit(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        from cervellaswarm_event_store.database import EventStore
        with EventStore(db) as store:
            for i in range(5):
                store.log_lesson(Lesson(problem=f"prob {i}"))
        main_lessons([f"--db-path={db}", "--limit=2", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 2

    def test_lessons_empty_store(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_init([f"--db-path={db}"])
        capsys.readouterr()  # consume init output
        main_lessons([f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 0


class TestMainPatterns:
    def _seed_errors(self, db_path, message, count=3):
        from cervellaswarm_event_store.database import EventStore
        with EventStore(db_path) as store:
            for _ in range(count):
                store.log_event(Event(event_type="task_failed", success=False,
                                      error_message=message, agent_name="backend"))

    def test_patterns_json_no_patterns(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_init([f"--db-path={db}"])
        capsys.readouterr()  # consume init output
        main_patterns([f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 0

    def test_patterns_json_with_pattern(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed_errors(db, "Connection timeout after 30s", count=3)
        main_patterns([f"--db-path={db}", "--min-occurrences=3", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["total"] >= 1

    def test_patterns_text_no_patterns(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        main_init([f"--db-path={db}"])
        main_patterns([f"--db-path={db}"])
        out = capsys.readouterr().out
        assert "No recurring" in out or "0" in out

    def test_patterns_text_with_pattern(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed_errors(db, "DB error occurred", count=5)
        main_patterns([f"--db-path={db}", "--min-occurrences=3"])
        out = capsys.readouterr().out
        assert "Pattern" in out or "Error" in out or "pattern" in out.lower()

    def test_patterns_days_arg(self, tmp_path, capsys):
        db = tmp_path / "test.db"
        self._seed_errors(db, "Network failure", count=3)
        main_patterns([f"--db-path={db}", "--days=1", "--min-occurrences=3", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert "total" in data


class TestMainDispatch:
    def test_no_command_shows_help(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main([])
        assert exc.value.code == 0

    def test_version_flag(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0

    def test_init_subcommand(self, tmp_path, capsys):
        db = tmp_path / "x.db"
        main(["init", f"--db-path={db}"])
        assert db.exists()

    def test_log_subcommand(self, tmp_path, capsys):
        db = tmp_path / "x.db"
        main(["log", f"--db-path={db}", "--type=custom", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["status"] == "ok"

    def test_query_subcommand(self, tmp_path, capsys):
        db = tmp_path / "x.db"
        main(["query", f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert "total" in data

    def test_stats_subcommand(self, tmp_path, capsys):
        db = tmp_path / "x.db"
        main(["stats", f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert "total_events" in data

    def test_lessons_subcommand(self, tmp_path, capsys):
        db = tmp_path / "x.db"
        main(["lessons", f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert "total" in data

    def test_patterns_subcommand(self, tmp_path, capsys):
        db = tmp_path / "x.db"
        main(["patterns", f"--db-path={db}", "--json"])
        data = json.loads(capsys.readouterr().out)
        assert "total" in data
