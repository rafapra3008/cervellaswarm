#!/usr/bin/env python3
"""
CervellaSwarm Prompt Builder - Template Prompt Dinamici per Task Paralleli

Genera prompt personalizzati per api che lavorano in parallelo,
garantendo interfacce concordate e zero conflitti.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class AgentType(Enum):
    """Tipi di agenti disponibili."""
    FRONTEND = "cervella-frontend"
    BACKEND = "cervella-backend"
    TESTER = "cervella-tester"
    DOCS = "cervella-docs"
    REVIEWER = "cervella-reviewer"
    DATA = "cervella-data"
    DEVOPS = "cervella-devops"

@dataclass
class TaskContext:
    """Contesto condiviso tra tutte le api."""
    task_name: str
    task_description: str
    total_agents: int
    interfaces: Dict[str, str]  # nome -> definizione (es. API endpoint, TypeScript interface)
    constraints: List[str]

@dataclass
class AgentTask:
    """Task specifico per una singola ape."""
    agent_type: AgentType
    files_to_modify: List[str]
    specific_instructions: str
    other_agents_work: Dict[str, str]  # agent_name -> descrizione lavoro

class PromptBuilder:
    """Genera prompt per task paralleli."""

    AGENT_EMOJI = {
        AgentType.FRONTEND: "🎨",
        AgentType.BACKEND: "⚙️",
        AgentType.TESTER: "🧪",
        AgentType.DOCS: "📝",
        AgentType.REVIEWER: "📋",
        AgentType.DATA: "📊",
        AgentType.DEVOPS: "🚀",
    }

    def build_prompt(self, context: TaskContext, agent_task: AgentTask) -> str:
        """
        Genera prompt completo per un'ape.

        Returns:
            Stringa markdown con prompt completo
        """
        emoji = self.AGENT_EMOJI.get(agent_task.agent_type, "🐝")
        agent_name = agent_task.agent_type.value

        # Header
        lines = [
            f"# TASK PARALLELO: {context.task_name}",
            "",
            "## CONTESTO CONDIVISO",
            f"Tu fai parte di uno sciame di {context.total_agents} 🐝 che lavorano IN PARALLELO.",
            "",
            "### Il Task Completo",
            context.task_description,
            "",
            f"### La Tua Parte ({emoji} {agent_name})",
            agent_task.specific_instructions,
            "",
        ]

        # Files da modificare
        if agent_task.files_to_modify:
            lines.append("### File da Modificare")
            for f in agent_task.files_to_modify:
                lines.append(f"- `{f}`")
            lines.append("")

        # Altre api
        if agent_task.other_agents_work:
            lines.append("### Le Altre 🐝")
            for other_agent, work in agent_task.other_agents_work.items():
                lines.append(f"- **{other_agent}**: {work}")
            lines.append("")

        # Interfacce concordate
        if context.interfaces:
            lines.append("## INTERFACCE CONCORDATE")
            lines.append("")
            for name, definition in context.interfaces.items():
                lines.append(f"### {name}")
                lines.append("```")
                lines.append(definition)
                lines.append("```")
                lines.append("")

        # Constraints
        lines.append("## CONSTRAINTS")
        lines.append("")
        for i, constraint in enumerate(context.constraints, 1):
            lines.append(f"{i}. ✅ {constraint}")
        lines.append("")

        # Checklist
        lines.extend([
            "## CHECKLIST COMPLETAMENTO",
            "",
            "- [ ] File modificati come richiesto",
            "- [ ] Interfacce rispettate al 100%",
            "- [ ] Test del tuo dominio passano",
            "- [ ] Nessun file fuori dominio toccato",
            "",
            "## PROSSIMO STEP",
            "Quando finisci, la Regina farà MERGE + REVIEW!",
        ])

        return "\n".join(lines)

    def build_parallel_prompts(
        self,
        context: TaskContext,
        agent_tasks: List[AgentTask]
    ) -> Dict[str, str]:
        """
        Genera prompt per TUTTE le api coinvolte.

        Returns:
            Dict[agent_name, prompt_text]
        """
        result = {}
        for task in agent_tasks:
            prompt = self.build_prompt(context, task)
            result[task.agent_type.value] = prompt
        return result


def create_example() -> tuple:
    """Crea un esempio di TaskContext e AgentTasks."""

    context = TaskContext(
        task_name="User Profile Feature",
        task_description="Implementare pagina profilo utente con edit/save",
        total_agents=3,
        interfaces={
            "API Endpoint": "GET /api/user/profile → { name, email, avatar }\nPUT /api/user/profile → { name, email } → 200 OK",
            "UserProfile Type": "interface UserProfile {\n  name: string;\n  email: string;\n  avatar?: string;\n}"
        },
        constraints=[
            "NON modificare file fuori dal tuo dominio",
            "Rispetta ESATTAMENTE le interfacce concordate",
            "Se vedi problema cross-domain → STOP + CHIEDI alla Regina",
            "Commit con prefix [PARALLEL-{dominio}]"
        ]
    )

    frontend_task = AgentTask(
        agent_type=AgentType.FRONTEND,
        files_to_modify=["components/UserProfile.jsx", "styles/profile.css"],
        specific_instructions="1. Crea componente UserProfile.jsx\n2. Form di edit con validazione\n3. Integrazione con API /api/user/profile",
        other_agents_work={
            "cervella-backend": "Sta creando endpoint API + validazione server",
            "cervella-tester": "Sta preparando test E2E del flusso"
        }
    )

    backend_task = AgentTask(
        agent_type=AgentType.BACKEND,
        files_to_modify=["api/user.py", "models/user.py"],
        specific_instructions="1. Endpoint GET/PUT /api/user/profile\n2. Validazione Pydantic\n3. Update database",
        other_agents_work={
            "cervella-frontend": "Sta creando UI + form",
            "cervella-tester": "Sta preparando test E2E"
        }
    )

    tester_task = AgentTask(
        agent_type=AgentType.TESTER,
        files_to_modify=["tests/test_user_profile.py"],
        specific_instructions="1. Test E2E del flusso completo\n2. Test unitari API\n3. Test validazione form",
        other_agents_work={
            "cervella-frontend": "Sta creando UI",
            "cervella-backend": "Sta creando API"
        }
    )

    return context, [frontend_task, backend_task, tester_task]


def main():
    """CLI per test."""
    import argparse

    parser = argparse.ArgumentParser(description="CervellaSwarm Prompt Builder")
    parser.add_argument("--example", "-e", action="store_true", help="Mostra esempio completo")
    parser.add_argument("--agent", "-a", choices=["frontend", "backend", "tester"], help="Mostra solo prompt per un agent")
    args = parser.parse_args()

    if args.example or args.agent:
        builder = PromptBuilder()
        context, tasks = create_example()

        if args.agent:
            # Mostra solo un agent
            agent_map = {"frontend": 0, "backend": 1, "tester": 2}
            task = tasks[agent_map[args.agent]]
            print(builder.build_prompt(context, task))
        else:
            # Mostra tutti
            prompts = builder.build_parallel_prompts(context, tasks)
            for agent_name, prompt in prompts.items():
                print("=" * 70)
                print(f"PROMPT PER: {agent_name}")
                print("=" * 70)
                print(prompt)
                print("\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
