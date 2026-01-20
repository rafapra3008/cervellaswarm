"""
Tier Manager - Gestisce tier, limiti e usage tracking

Tier disponibili:
- FREE: 3 agenti base, 50 task/mese (BYOK)
- PRO: 17 agenti, unlimited (BYOK + $20/mese)
- TEAM: 17 agenti, unlimited, features team ($40/user)
- ENTERPRISE: 16+ agenti custom, unlimited ($60+)
"""

import os
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from pathlib import Path
import yaml


class TierType(Enum):
    """Livelli di accesso disponibili."""
    FREE = "free"
    PRO = "pro"
    TEAM = "team"
    ENTERPRISE = "enterprise"


@dataclass
class TierConfig:
    """Configurazione per un tier."""
    name: str
    display_name: str
    agents_allowed: list[str]
    tasks_per_month: int  # -1 = unlimited
    price_monthly: int  # in USD
    features: list[str] = field(default_factory=list)

    @property
    def is_unlimited(self) -> bool:
        """True se tasks illimitati."""
        return self.tasks_per_month == -1


# Agenti base disponibili per FREE tier
FREE_AGENTS = ["backend", "frontend", "tester"]

# Tutti gli agenti (17)
ALL_AGENTS = [
    "regina", "backend", "frontend", "tester", "researcher",
    "scienziata", "docs", "reviewer", "data", "devops",
    "security", "marketing", "ingegnera", "architect",
    "guardiana-ops", "guardiana-qualita", "guardiana-ricerca"
]

# Configurazioni tier
TIER_CONFIGS = {
    TierType.FREE: TierConfig(
        name="free",
        display_name="Free",
        agents_allowed=FREE_AGENTS,
        tasks_per_month=50,
        price_monthly=0,
        features=[
            "3 agenti base (backend, frontend, tester)",
            "50 task/mese",
            "BYOK (porta la tua API key)",
            "Memoria SNCP",
        ],
    ),
    TierType.PRO: TierConfig(
        name="pro",
        display_name="Pro",
        agents_allowed=ALL_AGENTS,
        tasks_per_month=-1,  # unlimited
        price_monthly=20,
        features=[
            "17 agenti specializzati",
            "Task illimitati",
            "BYOK (porta la tua API key)",
            "Memoria SNCP",
            "Supporto email",
        ],
    ),
    TierType.TEAM: TierConfig(
        name="team",
        display_name="Team",
        agents_allowed=ALL_AGENTS,
        tasks_per_month=-1,
        price_monthly=40,
        features=[
            "Tutto di Pro",
            "Gestione team",
            "Dashboard condivisa",
            "Supporto prioritario",
        ],
    ),
    TierType.ENTERPRISE: TierConfig(
        name="enterprise",
        display_name="Enterprise",
        agents_allowed=ALL_AGENTS,  # + custom
        tasks_per_month=-1,
        price_monthly=60,
        features=[
            "Tutto di Team",
            "Agenti custom",
            "SSO",
            "Self-hosted option",
            "SLA dedicato",
        ],
    ),
}


@dataclass
class UsageStats:
    """Statistiche di utilizzo."""
    tasks_this_month: int = 0
    tasks_total: int = 0
    month_start: str = ""
    last_task: str = ""


class TierManager:
    """Gestisce tier e usage per un progetto.

    Salva lo stato in .sncp/tier.yaml
    """

    def __init__(self, sncp_path: Path):
        """Inizializza manager.

        Args:
            sncp_path: Path della cartella .sncp/
        """
        self.sncp_path = Path(sncp_path)
        self.tier_file = self.sncp_path / "tier.yaml"
        self._tier: Optional[TierType] = None
        self._usage: Optional[UsageStats] = None

    def _load(self) -> dict:
        """Carica dati da file."""
        if self.tier_file.exists():
            with open(self.tier_file) as f:
                return yaml.safe_load(f) or {}
        return {}

    def _save(self, data: dict) -> None:
        """Salva dati su file."""
        self.sncp_path.mkdir(parents=True, exist_ok=True)
        with open(self.tier_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    def get_tier(self) -> TierType:
        """Ottiene tier corrente.

        Returns:
            TierType (default FREE se non configurato).
        """
        if self._tier is not None:
            return self._tier

        data = self._load()
        tier_name = data.get("tier", "free")

        try:
            self._tier = TierType(tier_name)
        except ValueError:
            self._tier = TierType.FREE

        return self._tier

    def set_tier(self, tier: TierType) -> None:
        """Imposta tier.

        Args:
            tier: Nuovo tier da impostare.
        """
        data = self._load()
        data["tier"] = tier.value
        data["tier_changed"] = datetime.now().isoformat()
        self._save(data)
        self._tier = tier

    def get_config(self) -> TierConfig:
        """Ottiene configurazione del tier corrente."""
        return TIER_CONFIGS[self.get_tier()]

    def get_usage(self) -> UsageStats:
        """Ottiene statistiche usage correnti.

        Resetta automaticamente se cambio mese.
        """
        if self._usage is not None:
            return self._usage

        data = self._load()
        usage_data = data.get("usage", {})

        current_month = datetime.now().strftime("%Y-%m")
        stored_month = usage_data.get("month_start", "")

        # Reset se nuovo mese
        if stored_month != current_month:
            self._usage = UsageStats(
                tasks_this_month=0,
                tasks_total=usage_data.get("tasks_total", 0),
                month_start=current_month,
                last_task=""
            )
            self._save_usage()
        else:
            self._usage = UsageStats(
                tasks_this_month=usage_data.get("tasks_this_month", 0),
                tasks_total=usage_data.get("tasks_total", 0),
                month_start=stored_month,
                last_task=usage_data.get("last_task", "")
            )

        return self._usage

    def _save_usage(self) -> None:
        """Salva usage stats."""
        data = self._load()
        data["usage"] = {
            "tasks_this_month": self._usage.tasks_this_month,
            "tasks_total": self._usage.tasks_total,
            "month_start": self._usage.month_start,
            "last_task": self._usage.last_task,
        }
        self._save(data)

    def record_task(self) -> None:
        """Registra esecuzione di un task."""
        usage = self.get_usage()
        usage.tasks_this_month += 1
        usage.tasks_total += 1
        usage.last_task = datetime.now().isoformat()
        self._save_usage()

    def can_run_task(self) -> tuple[bool, str]:
        """Verifica se l'utente può eseguire un task.

        Returns:
            Tupla (può eseguire, messaggio se no).
        """
        config = self.get_config()

        # Unlimited
        if config.is_unlimited:
            return True, ""

        usage = self.get_usage()
        remaining = config.tasks_per_month - usage.tasks_this_month

        if remaining <= 0:
            return False, (
                f"Hai raggiunto il limite di {config.tasks_per_month} task/mese "
                f"per il tier {config.display_name}.\n"
                f"Upgrade a Pro per task illimitati: cervella upgrade"
            )

        # Warning se vicino al limite
        if remaining <= 5:
            return True, f"Attenzione: {remaining} task rimanenti questo mese."

        return True, ""

    def can_use_agent(self, agent_name: str) -> tuple[bool, str]:
        """Verifica se l'agente è disponibile per il tier.

        Args:
            agent_name: Nome dell'agente (con o senza prefisso cervella-).

        Returns:
            Tupla (può usare, messaggio se no).
        """
        config = self.get_config()
        clean_name = agent_name.replace("cervella-", "")

        if clean_name in config.agents_allowed:
            return True, ""

        return False, (
            f"L'agente '{clean_name}' non è disponibile nel tier {config.display_name}.\n"
            f"Agenti disponibili: {', '.join(config.agents_allowed)}\n"
            f"Upgrade a Pro per tutti i 17 agenti: cervella upgrade"
        )

    def get_available_agents(self) -> list[str]:
        """Lista agenti disponibili per il tier corrente."""
        return self.get_config().agents_allowed

    def get_status_summary(self) -> dict:
        """Ottiene riepilogo stato per display.

        Returns:
            Dict con informazioni formattate.
        """
        config = self.get_config()
        usage = self.get_usage()

        if config.is_unlimited:
            tasks_display = "Illimitati"
            remaining = -1
        else:
            remaining = config.tasks_per_month - usage.tasks_this_month
            tasks_display = f"{usage.tasks_this_month}/{config.tasks_per_month}"

        return {
            "tier": config.display_name,
            "tier_type": self.get_tier().value,
            "price": f"${config.price_monthly}/mese" if config.price_monthly > 0 else "Gratis",
            "agents_count": len(config.agents_allowed),
            "agents_total": len(ALL_AGENTS),
            "tasks_display": tasks_display,
            "tasks_remaining": remaining,
            "tasks_this_month": usage.tasks_this_month,
            "tasks_total": usage.tasks_total,
            "is_unlimited": config.is_unlimited,
            "features": config.features,
        }
