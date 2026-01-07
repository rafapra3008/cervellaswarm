"""
Parser per file Markdown (.md) -> JSON strutturato
"""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class MarkdownParser:
    """Parser per file markdown del progetto CervellaSwarm"""

    def __init__(self, workspace: Path):
        self.workspace = workspace

    def parse_nord(self) -> Dict[str, Any]:
        """Parse NORD.md e ritorna struttura JSON"""
        nord_path = self.workspace / "NORD.md"
        if not nord_path.exists():
            return {"source_file": "NORD.md", "current_session": None}

        content = nord_path.read_text(encoding="utf-8")

        result = {
            "source_file": "NORD.md",
            "current_session": self._extract_session(content),
            "stato_reale": self._extract_stato_reale(content),
            "pezzi": self._extract_pezzi(content),
        }
        return result

    def parse_roadmap(self) -> Dict[str, Any]:
        """Parse ROADMAP_SACRA.md e ritorna struttura JSON"""
        roadmap_path = self.workspace / "ROADMAP_SACRA.md"
        if not roadmap_path.exists():
            return {"source_file": "ROADMAP_SACRA.md", "current_phase": None}

        content = roadmap_path.read_text(encoding="utf-8")

        result = {
            "source_file": "ROADMAP_SACRA.md",
            "current_phase": self._extract_current_phase(content),
            "completed_phases": self._extract_completed_phases(content),
        }
        return result

    def parse_mappa(self) -> Dict[str, Any]:
        """Parse MAPPA_CERVELLASWARM_IDE.md o simile"""
        # Cerca file mappa
        mappa_files = list(self.workspace.glob("MAPPA*.md"))
        if not mappa_files:
            # Prova in docs/roadmap/
            mappa_files = list((self.workspace / "docs" / "roadmap").glob("*.md"))

        steps = []
        for mappa_file in mappa_files:
            content = mappa_file.read_text(encoding="utf-8")
            steps.extend(self._extract_steps(content))

        return {"steps": steps}

    def get_project_info(self) -> Dict[str, Any]:
        """Estrae info progetto da CLAUDE.md o NORD.md"""
        claude_path = self.workspace / "CLAUDE.md"
        if claude_path.exists():
            content = claude_path.read_text(encoding="utf-8")
            name = self._extract_project_name(content)
            claim = self._extract_claim(content)
            return {
                "name": name or "CervellaSwarm",
                "claim": claim or "",
                "objective": "LIBERTA GEOGRAFICA"
            }
        return {
            "name": "CervellaSwarm",
            "claim": "",
            "objective": "LIBERTA GEOGRAFICA"
        }

    def _extract_session(self, content: str) -> Optional[Dict[str, Any]]:
        """Estrae info sessione da contenuto"""
        # Pattern: **SESSIONE 111 - 6 Gennaio 2026: LA SESSIONE DEGLI STUDI!**
        pattern = r"\*\*SESSIONE\s+(\d+)\s*[-:]\s*(\d+\s+\w+\s+\d+)[:\s]+(.+?)\*\*"
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return {
                "number": int(match.group(1)),
                "date": match.group(2).strip(),
                "title": match.group(3).strip()
            }

        # Pattern alternativo: SESSIONE 111
        pattern2 = r"SESSIONE\s+(\d+)"
        match2 = re.search(pattern2, content, re.IGNORECASE)
        if match2:
            return {
                "number": int(match2.group(1)),
                "date": "",
                "title": ""
            }
        return None

    def _extract_stato_reale(self, content: str) -> List[Dict[str, str]]:
        """Estrae lista stato reale"""
        stato_reale = []
        # Pattern: | Nome | FUNZIONANTE | o simile
        pattern = r"\|\s*(.+?)\s*\|\s*(FUNZIONANTE|FATTO|IN CORSO|PARCHEGGIATO|TODO)\s*\|"
        for match in re.finditer(pattern, content, re.IGNORECASE):
            name = match.group(1).strip()
            status = match.group(2).strip().upper()
            if name and not name.startswith("---") and name != "Cosa":
                stato_reale.append({"name": name, "status": status})
        return stato_reale

    def _extract_pezzi(self, content: str) -> List[Dict[str, Any]]:
        """Estrae lista pezzi con percentuali"""
        pezzi = []
        # Pattern per percentuali: NOME ... 70%
        pattern = r"\|\s*(.+?)\s*\|\s*(PARCHEGGIATO|FATTO|IN CORSO|TODO)\s*\|\s*(\d+)%?\s*\|"
        for match in re.finditer(pattern, content, re.IGNORECASE):
            name = match.group(1).strip()
            status = match.group(2).strip().upper()
            percent = int(match.group(3))
            if name and not name.startswith("---"):
                pezzi.append({"name": name, "status": status, "percent": percent})
        return pezzi

    def _extract_current_phase(self, content: str) -> Optional[Dict[str, Any]]:
        """Estrae fase corrente"""
        # Pattern: ## FASE X: Nome
        pattern = r"##\s*FASE\s+(\d+)[:\s]+(.+?)(?:\n|$)"
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            # Prende l'ultima fase trovata come "corrente"
            last_match = matches[-1]
            return {
                "number": int(last_match.group(1)),
                "name": last_match.group(2).strip(),
                "status": "IN CORSO"
            }
        return None

    def _extract_completed_phases(self, content: str) -> List[Dict[str, Any]]:
        """Estrae fasi completate"""
        completed = []
        # Pattern per fasi con checkmark
        pattern = r"\[x\]\s*FASE\s+(\d+)[:\s]+(.+?)(?:\n|$)"
        for match in re.finditer(pattern, content, re.IGNORECASE):
            completed.append({
                "number": int(match.group(1)),
                "name": match.group(2).strip(),
                "completed_at": ""  # Non sempre disponibile
            })
        return completed

    def _extract_steps(self, content: str) -> List[Dict[str, Any]]:
        """Estrae step da file mappa"""
        steps = []

        # Pattern: ## STEP X: Nome
        step_pattern = r"##\s*STEP\s+(\d+)[:\s]+(.+?)(?=##\s*STEP|$)"
        for match in re.finditer(step_pattern, content, re.DOTALL | re.IGNORECASE):
            step_num = int(match.group(1))
            step_content = match.group(2)
            step_name = step_content.split("\n")[0].strip()

            # Determina status
            status = "pending"
            if "[x]" in step_content.lower() or "completato" in step_content.lower():
                status = "completed"
            elif "in corso" in step_content.lower() or "working" in step_content.lower():
                status = "in_progress"

            # Estrai substeps
            substeps = self._extract_substeps(step_content, step_num)

            steps.append({
                "number": step_num,
                "name": step_name,
                "status": status,
                "substeps": substeps
            })

        return steps

    def _extract_substeps(self, content: str, step_num: int) -> List[Dict[str, Any]]:
        """Estrae substeps da contenuto step"""
        substeps = []

        # Pattern: - [ ] Nome substep o - [x] Nome substep
        pattern = r"-\s*\[([ x])\]\s*(.+?)(?=\n|$)"
        for i, match in enumerate(re.finditer(pattern, content, re.IGNORECASE)):
            is_done = match.group(1).lower() == "x"
            name = match.group(2).strip()
            substeps.append({
                "id": f"{step_num}.{i+1}",
                "name": name,
                "status": "completed" if is_done else "pending"
            })

        return substeps

    def _extract_project_name(self, content: str) -> Optional[str]:
        """Estrae nome progetto"""
        pattern = r"#\s*(.+?)(?:\s*[-:])?"
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()
        return None

    def _extract_claim(self, content: str) -> Optional[str]:
        """Estrae claim progetto"""
        # Pattern per claim tra virgolette
        pattern = r'"([^"]+)"'
        matches = re.findall(pattern, content)
        for m in matches:
            if len(m) > 20 and len(m) < 200:
                return m
        return None
