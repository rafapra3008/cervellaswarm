#!/usr/bin/env python3
"""
Learning Wizard CLI per CervellaSwarm.
Interfaccia guidata per creare lezioni di qualità.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import sys
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List

# Try Rich, fallback to standard print
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

import sqlite3

# Path database
def get_db_path() -> Path:
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    return project_root / "data" / "swarm_memory.db"

# Template lezioni
TEMPLATES = {
    "bug_fix": {
        "name": "Bug Fix",
        "trigger_template": "Quando si incontra bug simile a: {bug_type}",
        "prevention_template": "Verificare {checklist} prima di implementare"
    },
    "refactor": {
        "name": "Refactoring",
        "trigger_template": "Quando si refactora componenti di tipo: {component_type}",
        "prevention_template": "Test regressione obbligatorio prima e dopo"
    },
    "integration": {
        "name": "Integrazione API/Service",
        "trigger_template": "Quando si integra con: {service_name}",
        "prevention_template": "Checklist pre-integrazione: {checklist}"
    },
    "custom": {
        "name": "Custom (vuoto)",
        "trigger_template": "",
        "prevention_template": ""
    }
}

SEVERITY_LEVELS = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
AGENTS = [
    "cervella-frontend", "cervella-backend", "cervella-tester",
    "cervella-reviewer", "cervella-researcher", "cervella-devops",
    "cervella-docs", "cervella-data", "cervella-security", "cervella-marketing"
]

class LessonWizard:
    """Wizard interattivo per creare lezioni."""

    def __init__(self):
        self.lesson = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trigger": "",
            "context": "",
            "problem": "",
            "root_cause": "",
            "solution": "",
            "prevention": "",
            "example": "",
            "severity": "MEDIUM",
            "agents_involved": [],
            "tags": [],
            "pattern": "",
            "auto_generated": 0,
            "confidence": 0.8,
            "times_applied": 0
        }

    def print_header(self, text: str):
        """Stampa header con stile."""
        if RICH_AVAILABLE:
            console.print(Panel(text, style="bold blue"))
        else:
            print(f"\n{'='*60}\n{text}\n{'='*60}")

    def print_step(self, step: int, total: int, title: str):
        """Stampa step corrente."""
        if RICH_AVAILABLE:
            console.print(f"\n[bold cyan]Step {step}/{total}: {title}[/bold cyan]")
        else:
            print(f"\nStep {step}/{total}: {title}")

    def ask(self, prompt: str, default: str = "") -> str:
        """Chiede input all'utente."""
        if RICH_AVAILABLE:
            return Prompt.ask(prompt, default=default)
        else:
            result = input(f"{prompt} [{default}]: ").strip()
            return result if result else default

    def ask_confirm(self, prompt: str, default: bool = True) -> bool:
        """Chiede conferma."""
        if RICH_AVAILABLE:
            return Confirm.ask(prompt, default=default)
        else:
            result = input(f"{prompt} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
            if not result:
                return default
            return result in ['y', 'yes', 'si', 's']

    def ask_choice(self, prompt: str, choices: List[str]) -> str:
        """Chiede scelta da lista."""
        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")

        while True:
            try:
                idx = int(self.ask("Scegli numero")) - 1
                if 0 <= idx < len(choices):
                    return choices[idx]
            except ValueError:
                pass
            print("Scelta non valida, riprova.")

    def ask_multi_choice(self, prompt: str, choices: List[str]) -> List[str]:
        """Chiede scelta multipla."""
        print(f"\n{prompt}")
        print("(inserisci numeri separati da virgola, es: 1,3,5)")
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")

        selected = []
        while True:
            try:
                input_str = self.ask("Scegli numeri")
                indices = [int(x.strip()) - 1 for x in input_str.split(",")]
                selected = [choices[i] for i in indices if 0 <= i < len(choices)]
                if selected:
                    return selected
            except (ValueError, IndexError):
                pass
            print("Scelta non valida, riprova.")

    def run(self) -> Optional[Dict]:
        """Esegue il wizard completo."""
        self.print_header("🧙 LEARNING WIZARD - Documenta Nuova Lezione")

        # Step 1: Template
        self.print_step(1, 9, "TEMPLATE")
        template_names = [TEMPLATES[k]["name"] for k in TEMPLATES]
        template_choice = self.ask_choice("Che tipo di lezione è?", template_names)
        template_key = [k for k, v in TEMPLATES.items() if v["name"] == template_choice][0]

        # Step 2: Trigger
        self.print_step(2, 9, "TRIGGER")
        print("Quando si applica questa lezione?")
        default_trigger = TEMPLATES[template_key]["trigger_template"]
        self.lesson["trigger"] = self.ask("Trigger", default_trigger)

        # Step 3: Context
        self.print_step(3, 9, "CONTEXT")
        print("Descrivi il contesto (task, agente, situazione)")
        self.lesson["context"] = self.ask("Context")

        # Step 4: Problem
        self.print_step(4, 9, "PROBLEM")
        print("Cosa è andato storto?")
        self.lesson["problem"] = self.ask("Problem")

        # Step 5: Root Cause
        self.print_step(5, 9, "ROOT CAUSE")
        print("Perché è successo? (causa radice)")
        self.lesson["root_cause"] = self.ask("Root Cause")

        # Step 6: Solution
        self.print_step(6, 9, "SOLUTION")
        print("Come è stato risolto?")
        self.lesson["solution"] = self.ask("Solution")

        # Step 7: Prevention
        self.print_step(7, 9, "PREVENTION")
        print("Come prevenire in futuro?")
        default_prevention = TEMPLATES[template_key]["prevention_template"]
        self.lesson["prevention"] = self.ask("Prevention", default_prevention)

        # Step 8: Example
        self.print_step(8, 9, "EXAMPLE")
        print("Esempio concreto (opzionale)")
        self.lesson["example"] = self.ask("Example", "")

        # Step 9: Metadata
        self.print_step(9, 9, "METADATA")

        # Severity
        self.lesson["severity"] = self.ask_choice("Severity?", SEVERITY_LEVELS)

        # Agents
        self.lesson["agents_involved"] = self.ask_multi_choice(
            "Quali agenti devono conoscere questa lezione?",
            AGENTS
        )

        # Tags
        tags_input = self.ask("Tags (separati da virgola)", "")
        if tags_input:
            self.lesson["tags"] = [t.strip() for t in tags_input.split(",")]

        # Pattern name
        self.lesson["pattern"] = self.ask("Pattern name (identificativo breve)", "")

        # Preview
        self.print_preview()

        if self.ask_confirm("Salvare questa lezione?"):
            return self.lesson
        else:
            print("Lezione annullata.")
            return None

    def print_preview(self):
        """Mostra anteprima lezione."""
        self.print_header("📋 ANTEPRIMA LEZIONE")

        preview = f"""
**TRIGGER:** {self.lesson['trigger']}

**CONTEXT:** {self.lesson['context']}

**PROBLEM:** {self.lesson['problem']}

**ROOT CAUSE:** {self.lesson['root_cause']}

**SOLUTION:** {self.lesson['solution']}

**PREVENTION:** {self.lesson['prevention']}

**EXAMPLE:** {self.lesson['example'] or '(nessuno)'}

**SEVERITY:** {self.lesson['severity']}
**AGENTS:** {', '.join(self.lesson['agents_involved'])}
**TAGS:** {', '.join(self.lesson['tags']) if self.lesson['tags'] else '(nessuno)'}
**PATTERN:** {self.lesson['pattern'] or '(nessuno)'}
"""

        if RICH_AVAILABLE:
            console.print(Markdown(preview))
        else:
            print(preview)

    def save_to_db(self) -> bool:
        """Salva lezione nel database."""
        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO lessons_learned (
                    id, timestamp, trigger, context, problem, root_cause,
                    solution, prevention, example, severity, agents_involved,
                    tags, pattern, auto_generated, confidence, times_applied
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.lesson["id"],
                self.lesson["timestamp"],
                self.lesson["trigger"],
                self.lesson["context"],
                self.lesson["problem"],
                self.lesson["root_cause"],
                self.lesson["solution"],
                self.lesson["prevention"],
                self.lesson["example"],
                self.lesson["severity"],
                json.dumps(self.lesson["agents_involved"]),
                json.dumps(self.lesson["tags"]),
                self.lesson["pattern"],
                self.lesson["auto_generated"],
                self.lesson["confidence"],
                self.lesson["times_applied"]
            ))

            conn.commit()
            conn.close()

            print(f"\n✅ Lezione salvata con ID: {self.lesson['id']}")
            return True

        except Exception as e:
            print(f"\n❌ Errore salvataggio: {e}")
            return False

def main():
    """Entry point."""
    print(f"🧙 CervellaSwarm Learning Wizard v{__version__}")
    print("-" * 60)

    if not RICH_AVAILABLE:
        print("⚠️  Rich non disponibile, usando interfaccia base")

    wizard = LessonWizard()
    lesson = wizard.run()

    if lesson:
        if wizard.save_to_db():
            print("\n🎉 Lezione documentata con successo!")
            print(f"   ID: {lesson['id']}")
            print(f"   Pattern: {lesson.get('pattern', 'N/A')}")
        else:
            # Salva come JSON di backup
            backup_path = Path(__file__).parent.parent.parent / "data" / f"lesson_{lesson['id']}.json"
            with open(backup_path, 'w') as f:
                json.dump(lesson, f, indent=2)
            print(f"   Backup salvato: {backup_path}")

if __name__ == "__main__":
    main()
