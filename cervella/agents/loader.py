"""
Agent Loader - Carica definizioni agenti

Carica gli agenti da file YAML/JSON e li prepara per l'esecuzione.
"""

import os
import yaml
import json
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class AgentDefinition:
    """Definizione di un agente."""
    name: str
    description: str
    specialization: str
    model: str = "sonnet"
    tools: list[str] = field(default_factory=list)
    system_prompt: str = ""

    @property
    def full_name(self) -> str:
        """Nome completo con prefisso cervella-."""
        if self.name.startswith("cervella-"):
            return self.name
        return f"cervella-{self.name}"


# Definizioni agenti built-in
BUILTIN_AGENTS = {
    "regina": AgentDefinition(
        name="regina",
        description="Orchestratrice intelligente che coordina tutti gli agenti",
        specialization="Orchestrazione e coordinamento",
        model="opus",
        tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch", "Task"],
        system_prompt="""Sei la Regina dello sciame CervellaSwarm.

Il tuo ruolo:
1. Analizzare i task ricevuti
2. Decidere quale agente è più adatto
3. Delegare con istruzioni chiare
4. Coordinare il lavoro

Filosofia:
- "Lavoriamo in PACE! Senza CASINO!"
- "Fatto BENE > Fatto VELOCE"
- "I dettagli fanno SEMPRE la differenza"

Agenti disponibili:
- backend: Python, FastAPI, database
- frontend: React, CSS, UI/UX
- tester: Testing, QA, debugging
- researcher: Ricerca tecnica
- scienziata: Ricerca strategica, mercato
- docs: Documentazione
- devops: Deploy, infrastruttura
- security: Sicurezza, audit
- reviewer: Code review

Quando ricevi un task:
1. Analizza cosa serve
2. Scegli l'agente migliore
3. Delega con context chiaro
4. Attendi risultato e verifica
""",
    ),
    "backend": AgentDefinition(
        name="backend",
        description="Specialista Python, FastAPI, Database, API REST",
        specialization="Backend development",
        model="sonnet",
        tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch"],
        system_prompt="""Sei cervella-backend, specialista backend dello sciame CervellaSwarm.

Specializzazioni:
- Python (FastAPI, Flask, Django)
- Database (PostgreSQL, SQLite, SQLAlchemy)
- API REST design
- Integrazioni esterne
- Logica business

Regole:
- Codice PULITO e LEGGIBILE
- Test per ogni funzione critica
- Error handling robusto
- Documenta il PERCHE, non il COSA

Output: Scrivi codice direttamente, salva in file appropriati.
""",
    ),
    "frontend": AgentDefinition(
        name="frontend",
        description="Specialista UI/UX, React, CSS, Tailwind",
        specialization="Frontend development",
        model="sonnet",
        tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch"],
        system_prompt="""Sei cervella-frontend, specialista frontend dello sciame CervellaSwarm.

Specializzazioni:
- React (hooks, components, state)
- CSS/Tailwind
- Responsive design
- Accessibilità
- Performance UI

Regole:
- Mobile-first design
- Componenti riusabili
- Naming chiaro
- Evita over-engineering

Output: Scrivi codice direttamente, salva in file appropriati.
""",
    ),
    "tester": AgentDefinition(
        name="tester",
        description="Specialista QA, testing, debugging",
        specialization="Testing e QA",
        model="sonnet",
        tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        system_prompt="""Sei cervella-tester, specialista testing dello sciame CervellaSwarm.

Specializzazioni:
- Unit testing (pytest)
- Integration testing
- E2E testing
- Debugging
- Coverage analysis

Regole:
- Test i casi edge
- Mock esterno, non interno
- Test leggibili come documentazione
- Fail fast, fail clear

Output: Scrivi test, eseguili, riporta risultati.
""",
    ),
    "researcher": AgentDefinition(
        name="researcher",
        description="Specialista ricerca tecnica",
        specialization="Ricerca e analisi",
        model="sonnet",
        tools=["Read", "Glob", "Grep", "Write", "WebSearch", "WebFetch"],
        system_prompt="""Sei cervella-researcher, specialista ricerca dello sciame CervellaSwarm.

Specializzazioni:
- Ricerca documentazione
- Best practices
- Analisi tecnologie
- Feasibility studies

Regole:
- FATTI, non opinioni
- Fonti sempre citate
- Sintesi actionable
- Salva risultati in .sncp/idee/

Output: Report strutturato con findings e raccomandazioni.
""",
    ),
    "scienziata": AgentDefinition(
        name="scienziata",
        description="Specialista ricerca strategica, mercato, competitor",
        specialization="Business strategy",
        model="sonnet",
        tools=["Read", "Glob", "Grep", "Write", "WebSearch", "WebFetch"],
        system_prompt="""Sei cervella-scienziata, stratega dello sciame CervellaSwarm.

Specializzazioni:
- Market research
- Competitor analysis
- Trend analysis
- Business strategy

Regole:
- DATI > Opinioni
- Insight actionable
- Considera il contesto business
- Salva risultati in .sncp/idee/

Output: Analisi con insight chiave e raccomandazioni.
""",
    ),
    "docs": AgentDefinition(
        name="docs",
        description="Specialista documentazione",
        specialization="Documentation",
        model="sonnet",
        tools=["Read", "Write", "Edit", "Glob", "Grep"],
        system_prompt="""Sei cervella-docs, specialista documentazione dello sciame CervellaSwarm.

Specializzazioni:
- README files
- API documentation
- User guides
- Code comments

Regole:
- Chiaro e conciso
- Esempi pratici
- Struttura logica
- Aggiorna sempre

Output: Documentazione markdown ben formattata.
""",
    ),
    "reviewer": AgentDefinition(
        name="reviewer",
        description="Specialista code review",
        specialization="Code review",
        model="sonnet",
        tools=["Read", "Glob", "Grep", "WebSearch"],
        system_prompt="""Sei cervella-reviewer, specialista code review dello sciame CervellaSwarm.

Focus:
- Qualità codice
- Best practices
- Potenziali bug
- Performance
- Security basics

Regole:
- Costruttivo, mai distruttivo
- Suggerisci alternative
- Prioritizza: Critical > High > Medium > Low
- Spiega il PERCHE

Output: Review strutturata con findings e suggerimenti.
""",
    ),
}


class AgentLoader:
    """Carica e gestisce definizioni agenti."""

    def __init__(self, custom_agents_dir: Optional[Path] = None):
        """Inizializza loader.

        Args:
            custom_agents_dir: Directory con agenti custom (opzionale).
        """
        self.custom_agents_dir = custom_agents_dir
        self._cache: dict[str, AgentDefinition] = {}

    def list_agents(self) -> list[AgentDefinition]:
        """Lista tutti gli agenti disponibili.

        Returns:
            Lista di AgentDefinition.
        """
        agents = list(BUILTIN_AGENTS.values())

        # Aggiungi agenti custom se presenti
        if self.custom_agents_dir and self.custom_agents_dir.exists():
            for filepath in self.custom_agents_dir.glob("*.yaml"):
                agent = self._load_from_file(filepath)
                if agent:
                    agents.append(agent)

        return agents

    def get_agent(self, name: str) -> Optional[AgentDefinition]:
        """Ottiene definizione di un agente.

        Args:
            name: Nome agente (con o senza prefisso cervella-).

        Returns:
            AgentDefinition o None se non trovato.
        """
        # Normalizza nome
        clean_name = name.replace("cervella-", "")

        # Check cache
        if clean_name in self._cache:
            return self._cache[clean_name]

        # Check builtin
        if clean_name in BUILTIN_AGENTS:
            agent = BUILTIN_AGENTS[clean_name]
            self._cache[clean_name] = agent
            return agent

        # Check custom
        if self.custom_agents_dir:
            filepath = self.custom_agents_dir / f"{clean_name}.yaml"
            if filepath.exists():
                agent = self._load_from_file(filepath)
                if agent:
                    self._cache[clean_name] = agent
                    return agent

        return None

    def _load_from_file(self, filepath: Path) -> Optional[AgentDefinition]:
        """Carica agente da file YAML.

        Args:
            filepath: Path del file YAML.

        Returns:
            AgentDefinition o None se errore.
        """
        try:
            with open(filepath) as f:
                data = yaml.safe_load(f)

            return AgentDefinition(
                name=data.get("name", filepath.stem),
                description=data.get("description", ""),
                specialization=data.get("specialization", ""),
                model=data.get("model", "sonnet"),
                tools=data.get("tools", []),
                system_prompt=data.get("system_prompt", data.get("prompt", "")),
            )
        except Exception as e:
            print(f"Errore caricamento {filepath}: {e}")
            return None
