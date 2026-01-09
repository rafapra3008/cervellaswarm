"""
SNCP Manager - Gestione memoria esterna

Struttura .sncp/:
├── idee/           # Idee, ricerche, analisi
├── memoria/
│   ├── decisioni/  # Decisioni prese con PERCHE
│   ├── sessioni/   # Log sessioni
│   └── lezioni/    # Lezioni apprese
├── coscienza/      # Stato corrente, pensieri
└── config.yaml     # Configurazione progetto
"""

import os
import yaml
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class SNSCPStats:
    """Statistiche SNCP."""
    idee: int
    decisioni: int
    sessioni: int
    lezioni: int


class SNSCPManager:
    """Gestisce la memoria SNCP di un progetto.

    SNCP = Sistema Nervoso Centrale Persistente
    La memoria esterna che persiste tra sessioni.
    """

    STRUCTURE = {
        "idee": {},
        "memoria": {
            "decisioni": {},
            "sessioni": {},
            "lezioni": {},
        },
        "coscienza": {},
    }

    def __init__(self, project_path: str):
        """Inizializza manager per un progetto.

        Args:
            project_path: Path del progetto (dove creare .sncp/).
        """
        self.project_path = Path(project_path)
        self.sncp_path = self.project_path / ".sncp"

    def is_initialized(self) -> bool:
        """Verifica se SNCP è inizializzato."""
        return self.sncp_path.exists()

    def initialize(self) -> None:
        """Inizializza struttura SNCP.

        Crea la cartella .sncp/ con tutte le sottocartelle
        e i file di configurazione iniziali.
        """
        # Crea struttura cartelle
        self._create_structure(self.sncp_path, self.STRUCTURE)

        # Crea config.yaml
        config = {
            "project_name": self.project_path.name,
            "created": datetime.now().isoformat(),
            "cervella_version": "0.1.0",
            "agents": {
                "default_model": "sonnet",
                "enabled": ["backend", "frontend", "tester", "researcher"],
            },
        }
        self._write_yaml(self.sncp_path / "config.yaml", config)

        # Crea README
        readme = """# SNCP - Sistema Nervoso Centrale Persistente

Questa cartella contiene la memoria esterna di Cervella.

## Struttura

- `idee/` - Idee, ricerche, analisi
- `memoria/decisioni/` - Decisioni prese (con il PERCHE)
- `memoria/sessioni/` - Log delle sessioni
- `memoria/lezioni/` - Lezioni apprese
- `coscienza/` - Stato corrente

## Regole

1. **Mai cancellare** - La memoria è preziosa
2. **Sempre documentare** - Il PERCHE conta più del COSA
3. **Struttura chiara** - Un file per concetto

---
*Generato da Cervella*
"""
        (self.sncp_path / "README.md").write_text(readme)

        # Crea stato iniziale coscienza
        stato = f"""# Stato Corrente

> Ultimo aggiornamento: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Progetto
- Nome: {self.project_path.name}
- Path: {self.project_path}

## Cervella
- Inizializzata: SI
- Pronta per lavorare

---
*"Lavoriamo in PACE!"*
"""
        (self.sncp_path / "coscienza" / "stato_corrente.md").write_text(stato)

    def _create_structure(self, base: Path, structure: dict) -> None:
        """Crea ricorsivamente la struttura cartelle."""
        base.mkdir(parents=True, exist_ok=True)
        for name, substructure in structure.items():
            subpath = base / name
            subpath.mkdir(exist_ok=True)
            if substructure:
                self._create_structure(subpath, substructure)

    def _write_yaml(self, path: Path, data: dict) -> None:
        """Scrive dati YAML."""
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    def _read_yaml(self, path: Path) -> dict:
        """Legge dati YAML."""
        with open(path) as f:
            return yaml.safe_load(f) or {}

    def get_stats(self) -> dict:
        """Ottiene statistiche SNCP.

        Returns:
            Dict con conteggi per categoria.
        """
        if not self.is_initialized():
            return {"idee": 0, "decisioni": 0, "sessioni": 0, "lezioni": 0}

        return {
            "idee": self._count_files(self.sncp_path / "idee"),
            "decisioni": self._count_files(self.sncp_path / "memoria" / "decisioni"),
            "sessioni": self._count_files(self.sncp_path / "memoria" / "sessioni"),
            "lezioni": self._count_files(self.sncp_path / "memoria" / "lezioni"),
        }

    def _count_files(self, path: Path) -> int:
        """Conta file markdown in una cartella."""
        if not path.exists():
            return 0
        return len(list(path.glob("*.md")))

    def save_idea(self, title: str, content: str) -> Path:
        """Salva una nuova idea.

        Args:
            title: Titolo dell'idea.
            content: Contenuto markdown.

        Returns:
            Path del file creato.
        """
        filename = self._slugify(title) + ".md"
        filepath = self.sncp_path / "idee" / filename

        full_content = f"""# {title}

> Creato: {datetime.now().strftime("%Y-%m-%d %H:%M")}

{content}
"""
        filepath.write_text(full_content)
        return filepath

    def save_decision(self, title: str, decision: str, why: str) -> Path:
        """Salva una decisione con il PERCHE.

        Args:
            title: Titolo della decisione.
            decision: Cosa si è deciso.
            why: PERCHE si è deciso così.

        Returns:
            Path del file creato.
        """
        date = datetime.now().strftime("%Y%m%d")
        filename = f"{date}_{self._slugify(title)}.md"
        filepath = self.sncp_path / "memoria" / "decisioni" / filename

        content = f"""# {title}

> Data: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Decisione

{decision}

## Perche

{why}

---
*Documentato da Cervella*
"""
        filepath.write_text(content)
        return filepath

    def create_checkpoint(self, message: str) -> Path:
        """Crea un checkpoint dello stato corrente.

        Args:
            message: Messaggio del checkpoint.

        Returns:
            Path del file checkpoint.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"checkpoint_{timestamp}.md"
        filepath = self.sncp_path / "memoria" / "sessioni" / filename

        stats = self.get_stats()
        content = f"""# Checkpoint: {message}

> Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Stato SNCP

| Categoria | Count |
|-----------|-------|
| Idee | {stats['idee']} |
| Decisioni | {stats['decisioni']} |
| Sessioni | {stats['sessioni']} |
| Lezioni | {stats['lezioni']} |

## Note

{message}

---
*Checkpoint automatico Cervella*
"""
        filepath.write_text(content)
        return filepath

    def _slugify(self, text: str) -> str:
        """Converte testo in slug per filename."""
        import re
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", "_", text)
        text = text.strip("_")
        return text[:50]  # Max 50 chars

    def get_config(self) -> dict:
        """Ottiene configurazione progetto."""
        config_path = self.sncp_path / "config.yaml"
        if config_path.exists():
            return self._read_yaml(config_path)
        return {}

    def update_config(self, updates: dict) -> None:
        """Aggiorna configurazione progetto."""
        config = self.get_config()
        config.update(updates)
        self._write_yaml(self.sncp_path / "config.yaml", config)
