"""
Agent Runner - Esegue task tramite agenti

La Regina analizza il task e lo delega all'agente più adatto.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from api.client import ClaudeClient, Message
from agents.loader import AgentLoader, AgentDefinition


@dataclass
class TaskResult:
    """Risultato di un task."""
    success: bool
    output: str
    agent_used: str
    files_created: list[str] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)
    error: Optional[str] = None


class AgentRunner:
    """Esegue task delegandoli agli agenti appropriati.

    Flow:
    1. Riceve task description
    2. Regina analizza e sceglie agente
    3. Agente esegue task
    4. Risultato ritorna
    """

    def __init__(self, client: ClaudeClient, project_path: Optional[str] = None):
        """Inizializza runner.

        Args:
            client: ClaudeClient per chiamate API.
            project_path: Path del progetto (default: cwd).
        """
        self.client = client
        self.project_path = Path(project_path or os.getcwd())
        self.loader = AgentLoader()

    def run_task(
        self,
        description: str,
        agent_name: Optional[str] = None,
        context: Optional[str] = None,
    ) -> TaskResult:
        """Esegue un task.

        Se agent_name è specificato, usa quell'agente.
        Altrimenti, la Regina decide quale usare.

        Args:
            description: Descrizione del task.
            agent_name: Nome agente specifico (opzionale).
            context: Context aggiuntivo (opzionale).

        Returns:
            TaskResult con output e metadata.
        """
        # Determina agente
        if agent_name:
            agent = self.loader.get_agent(agent_name)
            if not agent:
                return TaskResult(
                    success=False,
                    output="",
                    agent_used="none",
                    error=f"Agente '{agent_name}' non trovato",
                )
        else:
            # Regina decide
            agent = self._regina_decide(description)

        # Esegui con l'agente scelto
        return self._execute_with_agent(agent, description, context)

    def _regina_decide(self, description: str) -> AgentDefinition:
        """La Regina decide quale agente usare.

        Args:
            description: Descrizione del task.

        Returns:
            AgentDefinition dell'agente scelto.
        """
        regina = self.loader.get_agent("regina")

        # Costruisci prompt per decisione
        decision_prompt = f"""Analizza questo task e decidi quale agente è più adatto.

TASK: {description}

AGENTI DISPONIBILI:
- backend: Python, FastAPI, database, API
- frontend: React, CSS, UI/UX
- tester: Testing, QA, debugging
- researcher: Ricerca tecnica, documentazione
- scienziata: Ricerca strategica, mercato
- docs: Documentazione
- reviewer: Code review

Rispondi SOLO con il nome dell'agente (es: "backend" o "frontend").
Se il task richiede coordinamento complesso, rispondi "regina".
"""

        response = self.client.quick(decision_prompt, system=regina.system_prompt)

        # Parse risposta
        agent_name = response.strip().lower().replace("cervella-", "")

        # Valida che sia un agente esistente
        agent = self.loader.get_agent(agent_name)
        if not agent:
            # Fallback a regina
            agent = regina

        return agent

    def _execute_with_agent(
        self,
        agent: AgentDefinition,
        description: str,
        context: Optional[str] = None,
    ) -> TaskResult:
        """Esegue task con un agente specifico.

        Args:
            agent: Definizione dell'agente.
            description: Descrizione del task.
            context: Context aggiuntivo.

        Returns:
            TaskResult.
        """
        # Costruisci prompt completo
        task_prompt = f"""TASK: {description}

PROJECT PATH: {self.project_path}

{f"CONTEXT AGGIUNTIVO: {context}" if context else ""}

Esegui il task e rispondi con:
1. Cosa hai fatto
2. File creati/modificati (se applicabile)
3. Risultato finale

Lavora con CALMA e PRECISIONE. "Fatto BENE > Fatto VELOCE"
"""

        # Scegli modello
        model = self.client.OPUS_MODEL if agent.model == "opus" else self.client.DEFAULT_MODEL

        try:
            messages = [Message(role="user", content=task_prompt)]
            response = self.client.send(
                messages,
                system=agent.system_prompt,
                model=model,
                max_tokens=4096,
            )

            # Parse risposta per estrarre file
            files_created = self._extract_files_from_response(response.content, "creat")
            files_modified = self._extract_files_from_response(response.content, "modific")

            return TaskResult(
                success=True,
                output=response.content,
                agent_used=agent.full_name,
                files_created=files_created,
                files_modified=files_modified,
            )

        except Exception as e:
            return TaskResult(
                success=False,
                output="",
                agent_used=agent.full_name,
                error=str(e),
            )

    def _extract_files_from_response(self, response: str, keyword: str) -> list[str]:
        """Estrae nomi file dalla risposta.

        Cerca pattern come "creato: file.py" o "modificato file.py"

        Args:
            response: Testo della risposta.
            keyword: Keyword da cercare (creat/modific).

        Returns:
            Lista di path file trovati.
        """
        import re

        files = []

        # Pattern per trovare file paths
        # Cerca dopo keyword: qualcosa.estensione
        pattern = rf"{keyword}[iao]*[:\s]+([^\s]+\.[a-z]+)"
        matches = re.findall(pattern, response.lower())
        files.extend(matches)

        # Pattern per backticks
        pattern = r"`([^`]+\.[a-z]+)`"
        matches = re.findall(pattern, response)
        files.extend(matches)

        # Deduplica e filtra
        seen = set()
        result = []
        for f in files:
            if f not in seen and not f.startswith("http"):
                seen.add(f)
                result.append(f)

        return result[:10]  # Max 10 file


class ReginaOrchestrator:
    """Orchestratore avanzato per task complessi.

    Per task che richiedono più agenti in sequenza.
    """

    def __init__(self, client: ClaudeClient):
        self.client = client
        self.runner = AgentRunner(client)
        self.loader = AgentLoader()

    def orchestrate(self, description: str) -> list[TaskResult]:
        """Orchestra un task complesso.

        La Regina divide il task in subtask e li assegna
        agli agenti appropriati in sequenza.

        Args:
            description: Descrizione del task complesso.

        Returns:
            Lista di TaskResult, uno per subtask.
        """
        # Prima: Regina analizza e divide
        regina = self.loader.get_agent("regina")

        plan_prompt = f"""Analizza questo task complesso e crea un piano di esecuzione.

TASK: {description}

Per ogni step, indica:
1. Descrizione subtask
2. Agente suggerito
3. Dipendenze (quali step devono completarsi prima)

Formato risposta:
STEP 1: [descrizione] -> AGENTE: [nome]
STEP 2: [descrizione] -> AGENTE: [nome] (DOPO: 1)
...

Max 5 step. Sii conciso.
"""

        response = self.client.quick(plan_prompt, system=regina.system_prompt)

        # Parse piano ed esegui
        steps = self._parse_plan(response)
        results = []

        for step_desc, agent_name in steps:
            result = self.runner.run_task(step_desc, agent_name=agent_name)
            results.append(result)

            # Stop se un step fallisce
            if not result.success:
                break

        return results

    def _parse_plan(self, response: str) -> list[tuple[str, str]]:
        """Parse piano dalla risposta Regina.

        Returns:
            Lista di (descrizione, agente) tuple.
        """
        import re

        steps = []
        lines = response.strip().split("\n")

        for line in lines:
            # Cerca pattern "STEP N: ... -> AGENTE: ..."
            match = re.search(r"STEP \d+:\s*(.+?)\s*->\s*AGENTE:\s*(\w+)", line, re.IGNORECASE)
            if match:
                desc = match.group(1).strip()
                agent = match.group(2).strip().lower()
                steps.append((desc, agent))

        return steps[:5]  # Max 5 step
