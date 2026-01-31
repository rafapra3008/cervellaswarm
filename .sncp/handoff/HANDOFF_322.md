# HANDOFF SESSIONE 322

> **Data:** 31 Gennaio 2026
> **Progetto:** CervellaSwarm
> **Status:** Studio OpenClaw + Piano SNCP 4.0 COMPLETATO!

---

## COSA È STATO FATTO

### Studio OpenClaw (ex-Clawdbot)

**Obiettivo:** Studiare come OpenClaw gestisce la memoria per migliorare SNCP

**Task completati:**

1. **Esplorazione GitHub OpenClaw**
   - Repository: github.com/openclaw
   - Documentazione: docs.openclaw.ai/concepts/memory

2. **Lancio Sciame Analisi**
   | Agente | Output |
   |--------|--------|
   | Architetta (Plan) | Piano SNCP 4.0 completo |
   | Guardiana Ricerca | Validazione info (95-100% accurate) |
   | Ingegnera | Analisi gap tecnico |

3. **Creato SUBROADMAP_SNCP_4.0.md**
   - Path: `.sncp/roadmaps/SUBROADMAP_SNCP_4.0.md`
   - Quick Wins definiti (4 task, ~2 giorni)
   - Fasi future pianificate

---

## SCOPERTE CHIAVE

### SNCP vs OpenClaw

| Aspetto | SNCP 3.0 | OpenClaw | Chi Vince |
|---------|----------|----------|-----------|
| Multi-progetto | ✅ Nativo | ❌ Single workspace | **SNCP** |
| Sicurezza | ✅ No secrets | ❌ Vulnerabilità CRITICHE | **SNCP** |
| Git-native | ✅ 100% | Recommended | **SNCP** |
| Daily logs auto | ❌ Manuale | ✅ Auto (oggi+ieri) | OpenClaw |
| Memory flush | ❌ Manuale | ✅ Pre-compaction | OpenClaw |
| Ricerca | ❌ Grep | ✅ BM25 + embeddings | OpenClaw |

### Decisione

> **Adottare pattern OpenClaw (automazione) mantenendo architettura SNCP (sicurezza).**

---

## FAMIGLIA ATTIVATA

| Agente | Ruolo | Task |
|--------|-------|------|
| Architetta (Plan) | Pianificazione | Piano SNCP 4.0 |
| cervella-guardiana-ricerca | Validazione | Verifica info OpenClaw |
| cervella-ingegnera | Analisi | Gap tecnico SNCP |

---

## FILE MODIFICATI/CREATI

| File | Azione | Note |
|------|--------|------|
| `.sncp/roadmaps/SUBROADMAP_SNCP_4.0.md` | CREATO | Piano completo |
| `.sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md` | MODIFICATO | S322 status |
| `.sncp/handoff/HANDOFF_322.md` | CREATO | Questo file |

---

## PIANO SNCP 4.0 - QUICK WINS

```
+================================================================+
|   SNCP 4.0: Memoria Intelligente                                |
|   Target: 8.8/10 → 9.5/10                                       |
+================================================================+

QUICK WINS (~2 giorni):

  QW1: Auto-load daily logs      [____________________] 0%   [NEXT]
       - scripts/sncp/load-daily-memory.sh
       - Carica oggi + ieri automaticamente
       - Effort: 2-4h

  QW2: Memory flush trigger      [____________________] 0%   [TODO]
       - scripts/swarm/memory-flush.sh
       - Trigger a 75% token budget
       - Effort: 3-4h

  QW3: SessionEnd hook           [____________________] 0%   [NEXT]
       - hooks/session_end_flush.py
       - Flush automatico a fine sessione
       - Effort: 1-2h

  QW4: BM25 search               [____________________] 0%   [TODO]
       - scripts/sncp/smart-search.py
       - Libreria: rank-bm25 (pure Python)
       - Effort: 4-6h

PRIORITÀ: QW1 + QW3 prima (automazione base)
```

---

## PROSSIMA SESSIONE (323)

### Task da fare:

1. **QW1: Auto-load daily logs**
   - Creare `scripts/sncp/load-daily-memory.sh`
   - Modificare session_start hook
   - Test: verifica caricamento oggi + ieri

2. **QW3: SessionEnd hook flush**
   - Creare `hooks/session_end_flush.py`
   - Registrare in settings
   - Test: verifica flush a fine sessione

3. **Se tempo: QW2 + QW4**
   - Memory flush con token trigger
   - BM25 search

### Criteri di successo:
```bash
# Test QW1: Daily logs caricati
./scripts/sncp/load-daily-memory.sh miracollo
# Output: JSON con contenuto oggi + ieri

# Test QW3: SessionEnd hook attivo
grep "session_end" ~/.claude/settings.json
# Output: hook registrato
```

---

## RISORSE

| Risorsa | Path |
|---------|------|
| Roadmap SNCP 4.0 | `.sncp/roadmaps/SUBROADMAP_SNCP_4.0.md` |
| OpenClaw docs | docs.openclaw.ai/concepts/memory |
| PROMPT_RIPRESA | `.sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md` |

---

## COMANDI UTILI

```bash
# Leggere roadmap SNCP 4.0
cat .sncp/roadmaps/SUBROADMAP_SNCP_4.0.md

# Verificare PROMPT_RIPRESA
cat .sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md

# Spawn workers
spawn-workers --list
spawn-workers --backend
```

---

## NOTE IMPORTANTI

- **SNCP già superiore** su organizzazione e sicurezza
- **OpenClaw ha vulnerabilità** CRITICHE - NON copiare la loro security
- **Embeddings opzionali** - BM25 prima, embeddings solo se serve
- **File-based rimane core** - trasparenza e git-native

---

*"La memoria è preziosa. Trattiamola con cura."*
*"Ultrapassar os próprios limites!"*
*Sessione 322 - Cervella & Rafa*
