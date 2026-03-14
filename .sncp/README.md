# SNCP - Sistema Nervoso Centrale Persistente

> **Progetto:** CervellaSwarm
> **Versione SNCP:** 5.0 (PROMPT_RIPRESA + NORD.md)
> **Aggiornato:** 14 Marzo 2026 - Sessione 460

---

## REGOLA D'ORO

```
+------------------------------------------------------------------+
|                                                                  |
|   "SNCP funziona solo se lo VIVIAMO!"                           |
|                                                                  |
|   Solo 2 file per progetto: PROMPT_RIPRESA + NORD.md            |
|   Hook automatici: pre/post sessione + compact                   |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STRUTTURA REALE

```
.sncp/
├── README.md                  # Questo file
├── PROMPT_RIPRESA_MASTER.md   # Indice puro (tabella link progetti)
│
├── progetti/                  # CUORE - Un folder per progetto
│   ├── cervellaswarm/         # CervellaSwarm
│   ├── miracollo/             # Miracollo (+bracci/miracollook)
│   ├── contabilita/           # Contabilita
│   ├── cervellabrasil/        # CervellaBrasil
│   ├── chavefy/               # Chavefy
│   └── cervellacostruzione/   # CervellaCostruzione
│
├── roadmaps/                  # Roadmap e subroadmap attive
├── reports/                   # Report globali (daily health)
├── handoff/                   # Handoff sessione (legacy)
└── archivio/                  # Archivio per mese/settimana
```

---

## RUOLI FILE

```
+------------------------------------------------------------------+
|   PROMPT_RIPRESA_{progetto}.md (MAX 250 righe)                   |
|   └── Context ripresa VELOCE (stato, decisioni, next steps)      |
|   └── Aggiornare: OGNI sessione                                  |
|   └── Leggere: SEMPRE a inizio sessione                          |
|                                                                  |
|   NORD.md (nella root del progetto, NON in .sncp/)               |
|   └── Direzione strategica + milestone + architettura            |
|   └── Aggiornare: solo a milestone importanti                    |
|   └── Leggere: quando serve visione d'insieme                    |
|                                                                  |
|   PROMPT_RIPRESA_MASTER.md (MAX 60 righe)                        |
|   └── INDICE puro (tabella link ai progetti)                     |
|   └── Aggiornare: quando cambia stato progetto                   |
+------------------------------------------------------------------+
```

> **SNCP 4.0 (S357):** stato.md e oggi.md archiviati. Il sistema usa SOLO PROMPT_RIPRESA + NORD.md.

---

## STRUTTURA PROGETTO

Ogni progetto in `progetti/{nome}/`:

```
├── PROMPT_RIPRESA_{nome}.md   # Ripresa sessioni (MAX 250 righe)
├── reports/                   # Report e audit
├── roadmaps/                  # Piani attivi (se presenti)
├── archivio/                  # File archiviati
└── bracci/                    # Sub-progetti (es: miracollook)
```

---

## COME USARE

### Inizio Sessione (Automatico via hook)
```
sncp_pre_session_hook.py:
1. Check stato SNCP + puntatori progetto
2. Warning se docs vecchi

Tu fai:
1. Leggi PROMPT_RIPRESA_{progetto}.md
2. Leggi NORD.md (root progetto) se serve visione strategica
```

### Fine Sessione (Automatico via hook)
```
SessionEnd hooks:
1. update_prompt_ripresa.py - checkpoint automatico
2. file_limits_guard.py - verifica limiti (250 righe)
3. sncp_verify_sync_hook.py - coerenza docs/codice

Tu fai:
1. Aggiorna PROMPT_RIPRESA_{progetto}.md
2. Aggiorna NORD.md solo se milestone importante
3. Commit + push
```

### Compact (Automatico via hook)
```
PreCompact: salva snapshot + checkpoint PROMPT_RIPRESA
PostCompact: salva compact_summary generato da Claude
```

---

## AUTOMAZIONI ATTIVE

| Quando | Cosa | Hook |
|--------|------|------|
| Inizio sessione | Check SNCP + puntatori | sncp_pre_session_hook.py |
| Fine sessione | Checkpoint PROMPT_RIPRESA | update_prompt_ripresa.py |
| Fine sessione | Verifica limiti file | file_limits_guard.py |
| Pre/Post compact | Salva stato e summary | pre_compact_save.py + post_compact_save.py |
| Ogni subagent | Inietta contesto | subagent_context_inject.py |

Tutti gli hook usano `cervella_hooks_common.py` come single source of truth.

---

## TOOLS

| Script | Cosa fa |
|--------|---------|
| `verify-sync [progetto]` | Verifica coerenza docs/codice |
| `sncp-init nome` | Wizard nuovo progetto |
| `check-ripresa-size.sh [progetto]` | Controlla limiti (250 righe) |
| `health-check.sh` | Dashboard salute SNCP |

---

## NAMING FILE

```
REPORT:      YYYYMMDD_TIPO_cosa.md     (es: RESEARCH_20260314_topic.md)
RICERCHE:    RESEARCH_YYYYMMDD_topic.md
AUDIT:       AUDIT_YYYYMMDD_cosa.md
ENGINEER:    ENGINEER_YYYYMMDD_cosa.md
```

---

## CHANGELOG

| Sessione | Cosa |
|----------|------|
| 163 | Semplificazione iniziale |
| 207 | sncp-init wizard + verify-sync |
| 296 | SNCP 5.0: Deprecato oggi.md/stato.md, solo PROMPT_RIPRESA + NORD |
| 442 | cervella_hooks_common.py: single source of truth |
| **460** | **README riscritto, PostCompact hook, COMPACT INSTRUCTIONS, fix limiti 250** |

---

*"SNCP: Semplice, Chiaro, Senza Ridondanza!"*
