"""
Parser per task files (.swarm/tasks/)
"""

import os
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class TaskParser:
    """Parser per file task dello swarm"""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.tasks_dir = workspace / ".swarm" / "tasks"
        self.status_dir = workspace / ".swarm" / "status"

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Ritorna tutti i task"""
        if not self.tasks_dir.exists():
            return []

        tasks = []
        task_files = list(self.tasks_dir.glob("TASK_*.md"))

        for task_file in task_files:
            task = self._parse_task_file(task_file)
            if task:
                tasks.append(task)

        return sorted(tasks, key=lambda x: x.get("task_id", ""))

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Ritorna singolo task per ID"""
        task_file = self.tasks_dir / f"{task_id}.md"
        if not task_file.exists():
            return None
        return self._parse_task_file(task_file)

    def get_tasks_by_status(self) -> Dict[str, List[Dict[str, Any]]]:
        """Ritorna task raggruppati per status"""
        all_tasks = self.get_all_tasks()
        by_status = {"ready": [], "working": [], "done": []}

        for task in all_tasks:
            status = task.get("status", "ready")
            if status in by_status:
                by_status[status].append(task)

        return by_status

    def _parse_task_file(self, task_file: Path) -> Optional[Dict[str, Any]]:
        """Parse singolo file task"""
        try:
            content = task_file.read_text(encoding="utf-8")
            task_id = task_file.stem  # TASK_NOME

            # Determina status dai marker files
            status = self._get_task_status(task_id)

            # Estrai metadata
            metadata = self._extract_metadata(content)

            # Costruisci markers
            markers = self._get_markers(task_id)

            # Cerca output
            output_file = self._find_output(task_id)

            # Cerca heartbeat
            heartbeat = self._get_heartbeat(metadata.get("assegnato_a", ""))

            return {
                "task_id": task_id,
                "status": status,
                "ack": {
                    "received": status in ["working", "done"],
                    "understood": status in ["working", "done"],
                    "done": status == "done"
                },
                "metadata": metadata,
                "files": {
                    "definition": str(task_file.relative_to(self.workspace)),
                    "output": output_file,
                    "markers": markers
                },
                "heartbeat": heartbeat
            }
        except Exception as e:
            print(f"Errore parsing {task_file}: {e}")
            return None

    def _get_task_status(self, task_id: str) -> str:
        """Determina status task dai file marker"""
        if (self.tasks_dir / f"{task_id}.done").exists():
            return "done"
        if (self.tasks_dir / f"{task_id}.working").exists():
            return "working"
        if (self.tasks_dir / f"{task_id}.ready").exists():
            return "ready"
        # Default: pending (non ancora ready)
        return "pending"

    def _get_markers(self, task_id: str) -> List[str]:
        """Lista dei marker file presenti"""
        markers = []
        for ext in [".ready", ".working", ".done"]:
            if (self.tasks_dir / f"{task_id}{ext}").exists():
                markers.append(ext)
        return markers

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Estrae metadata dal contenuto task"""
        metadata = {
            "assegnato_a": "",
            "rischio": 1,
            "timeout_minuti": 30,
            "creato": None
        }

        # Pattern: **Assegnato a:** cervella-backend
        assegnato_match = re.search(r"\*\*Assegnato\s*a:\*\*\s*(.+?)(?:\n|$)", content, re.IGNORECASE)
        if assegnato_match:
            metadata["assegnato_a"] = assegnato_match.group(1).strip()

        # Pattern: **Rischio:** 2-MEDIO o **Rischio:** 2
        rischio_match = re.search(r"\*\*Rischio:\*\*\s*(\d)", content, re.IGNORECASE)
        if rischio_match:
            metadata["rischio"] = int(rischio_match.group(1))

        # Pattern: **Timeout:** 30 minuti
        timeout_match = re.search(r"\*\*Timeout:\*\*\s*(\d+)", content, re.IGNORECASE)
        if timeout_match:
            metadata["timeout_minuti"] = int(timeout_match.group(1))

        return metadata

    def _find_output(self, task_id: str) -> Optional[str]:
        """Cerca file output del task"""
        output_file = self.tasks_dir / f"{task_id}_output.md"
        if output_file.exists():
            return str(output_file.relative_to(self.workspace))
        return None

    def _get_heartbeat(self, worker_name: str) -> Optional[Dict[str, Any]]:
        """Recupera info heartbeat per worker"""
        if not worker_name or not self.status_dir.exists():
            return None

        # Estrai nome worker (es: cervella-backend -> backend)
        short_name = worker_name.replace("cervella-", "")
        heartbeat_file = self.status_dir / f"heartbeat_{short_name}.log"

        if not heartbeat_file.exists():
            return None

        try:
            lines = heartbeat_file.read_text().strip().split("\n")
            if not lines:
                return None

            # Ultima riga: timestamp|task|message
            last_line = lines[-1]
            parts = last_line.split("|", 2)
            if len(parts) >= 2:
                timestamp = int(parts[0])
                message = parts[2] if len(parts) > 2 else ""
                seconds_ago = int(datetime.now().timestamp()) - timestamp

                return {
                    "last_update": datetime.fromtimestamp(timestamp).isoformat(),
                    "message": message,
                    "seconds_ago": seconds_ago
                }
        except Exception:
            pass

        return None


class WorkerParser:
    """Parser per stato worker"""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.status_dir = workspace / ".swarm" / "status"
        self.tasks_dir = workspace / ".swarm" / "tasks"

    def get_all_workers(self) -> List[Dict[str, Any]]:
        """Ritorna tutti i worker attivi"""
        workers = []

        if not self.status_dir.exists():
            # Inferisci da task working
            return self._infer_workers_from_tasks()

        # Cerca file worker_*.task
        for task_file in self.status_dir.glob("worker_*.task"):
            worker_name = task_file.stem.replace("worker_", "")
            worker = self._get_worker_status(worker_name)
            if worker:
                workers.append(worker)

        return workers

    def _get_worker_status(self, name: str) -> Optional[Dict[str, Any]]:
        """Ritorna status singolo worker"""
        task_file = self.status_dir / f"worker_{name}.task"
        pid_file = self.status_dir / f"worker_{name}.pid"
        heartbeat_file = self.status_dir / f"heartbeat_{name}.log"

        current_task = None
        if task_file.exists():
            current_task = task_file.read_text().strip()

        pid = None
        is_alive = False
        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                # Check if process alive
                os.kill(pid, 0)
                is_alive = True
            except (ValueError, ProcessLookupError, OSError):
                is_alive = False

        heartbeat = None
        if heartbeat_file.exists():
            heartbeat = self._parse_heartbeat(heartbeat_file)

        return {
            "worker_name": name,
            "status": "active" if current_task else "idle",
            "current_task": current_task,
            "pid": pid,
            "is_alive": is_alive,
            "heartbeat": heartbeat,
            "session_start": None
        }

    def _parse_heartbeat(self, heartbeat_file: Path) -> Optional[Dict[str, Any]]:
        """Parse file heartbeat"""
        try:
            lines = heartbeat_file.read_text().strip().split("\n")
            if not lines:
                return None

            last_line = lines[-1]
            parts = last_line.split("|", 2)
            if len(parts) >= 2:
                timestamp = int(parts[0])
                seconds_ago = int(datetime.now().timestamp()) - timestamp

                # Formatta time_ago
                if seconds_ago < 60:
                    time_ago = f"{seconds_ago}s fa"
                elif seconds_ago < 3600:
                    time_ago = f"{seconds_ago // 60}m fa"
                else:
                    time_ago = f"{seconds_ago // 3600}h fa"

                return {
                    "last_timestamp": timestamp,
                    "last_message": parts[2] if len(parts) > 2 else "",
                    "time_ago": time_ago
                }
        except Exception:
            pass
        return None

    def _infer_workers_from_tasks(self) -> List[Dict[str, Any]]:
        """Inferisce worker da task .working"""
        workers = []
        if not self.tasks_dir.exists():
            return workers

        for working_file in self.tasks_dir.glob("*.working"):
            task_id = working_file.stem
            task_file = self.tasks_dir / f"{task_id}.md"
            if task_file.exists():
                content = task_file.read_text()
                assegnato_match = re.search(r"\*\*Assegnato\s*a:\*\*\s*(.+?)(?:\n|$)", content, re.IGNORECASE)
                if assegnato_match:
                    worker_full = assegnato_match.group(1).strip()
                    worker_name = worker_full.replace("cervella-", "")
                    workers.append({
                        "worker_name": worker_name,
                        "status": "active",
                        "current_task": task_id,
                        "pid": None,
                        "is_alive": True,  # Assume alive se working
                        "heartbeat": None,
                        "session_start": None
                    })

        return workers
