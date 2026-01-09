# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 9 Gennaio 2026 - Sessione 142
> **Versione:** v62.0.0 - CLI MVP FUNZIONANTE!

---

## Stato Attuale

| Cosa | Stato |
|------|-------|
| Ricerca + Decisioni | COMPLETATE |
| Landing + Marketing | IN PAUSA |
| Plugin (vecchio) | DEPRECATO |
| **CLI `cervella`** | **MVP FUNZIONANTE!** |

---

## Sessione 142 - GRANDE GIORNO!

### Decisione Strategica

Rafa ha deciso: **APP VERA**, non plugin.
- Controllo totale
- Indipendenza da Anthropic plugins
- Prodotto vero come Cursor

### Cosa Fatto

1. **Fix bug agenti** - Write tool mancante (scienziata, researcher, marketing, security)
2. **Ricerca Cursor** - Storia completa, come hanno fatto
3. **Mappa App Vera** - Architettura CLI + roadmap
4. **CLI MVP creato** - `cervella` v0.1.0 funzionante!

### CLI Creato

```
cervella/
├── pyproject.toml          # Package config
├── cli/                    # Click CLI
│   └── commands/           # init, task, status, checkpoint
├── api/                    # Claude API wrapper (BYOK)
├── sncp/                   # Memoria esterna
├── agents/                 # 8 agenti built-in
└── tests/                  # TUTTI PASS!
```

### Comandi Funzionanti

```bash
cervella --version          # v0.1.0
cervella init               # Crea .sncp/
cervella status             # Mostra 8 agenti pronti
cervella task "..." --dry-run
cervella checkpoint -m "..."
```

---

## Decisioni Prese

| Cosa | Decisione |
|------|-----------|
| Nome comando | `cervella` |
| Linguaggio | Python |
| Priorità | CLI first, web dopo |
| Modello | BYOK (Bring Your Own Key) |

---

## Prossimi Step

| # | Task |
|---|------|
| 1 | Test reale con API key |
| 2 | Aggiungere altri agenti (16 totali) |
| 3 | README per il package |
| 4 | Aggiungere al PATH |
| 5 | PyPI publish (quando pronto) |

---

## Puntatori

| Cosa | Dove |
|------|------|
| CLI MVP | `cervella/` |
| Mappa App Vera | `.sncp/idee/MAPPA_APP_VERA.md` |
| Ricerca Cursor | `.sncp/idee/RICERCA_STORIA_CURSOR.md` |
| Studio precedente | `.sncp/idee/STUDIO_CLAUDE_CODE_COMPLETO.md` |

---

## Per Testare

```bash
# Installa (se non già fatto)
cd ~/Developer/CervellaSwarm/cervella
pip3 install -e .

# Usa
cervella --help
cervella init
cervella status
```

---

*"Quando troviamo il PERCHE, NULLA ci ferma!"*

*CLI MVP FUNZIONANTE! Con il cuore pieno!*

---
