# Analisi Impatto Cambiamenti Struttura SNCP

**Data:** 2026-01-18  
**Analista:** cervella-ingegnera  
**Versione:** 1.0.0

---

## EXECUTIVE SUMMARY

**Status:** ⚠️ AGGIORNAMENTI NECESSARI  
**Health:** 7/10  
**Rischio:** MEDIO (funzionale ma con incoerenze)

### Top 3 Issues

1. **MEDIO**: Hook `session_start_swarm.py` cerca NORD.md nel path VECCHIO (riga 63)
2. **MEDIO**: Dashboard API cerca NORD.md in workspace root (corretto MA non documentato)
3. **BASSO**: Documentazione generica menziona NORD.md ma senza path specifici

---

## CAMBIAMENTI EFFETTUATI

### Nuove Regole SNCP

```
PRIMA:
- NORD.md poteva stare sia in .sncp/ che in root (confusione)
- stato.md duplicato in .sncp/ e .sncp/progetti/{progetto}/

DOPO:
- NORD.md va SEMPRE nella ROOT del progetto
- stato.md SOLO in .sncp/progetti/{progetto}/stato.md
- .sncp/ contiene SOLO PROMPT_RIPRESA_MASTER.md
```

---

## FILE CHE REFERENZIANO SNCP

### Python Files (12 trovati)

| File | Riferimenti SNCP | Necessita Fix |
|------|------------------|---------------|
| `.claude/hooks/session_start_swarm.py` | ❌ Riga 63: `PROJECT_ROOT / "NORD.md"` | ✅ **SI** |
| `.claude/hooks/file_limits_guard.py` | ✅ Cerca stati in `progetti/{progetto}/stato.md` | ❌ NO |
| `cervella/sncp/manager.py` | ✅ Gestisce struttura `.sncp/` interna | ❌ NO |
| `cervella/tier/tier_manager.py` | ⚪ Generico `.sncp/` | ❌ NO |
| `cervella/agents/loader.py` | ⚪ Generico `.sncp/` | ❌ NO |
| `dashboard/api/parsers/markdown.py` | ✅ Riga 19: `workspace / "NORD.md"` | ❌ NO (già corretto!) |
| `dashboard/api/routes/mappa.py` | ✅ Usa parser (workspace root) | ❌ NO |
| Altri 5 file | ⚪ Riferimenti generici `.sncp/` | ❌ NO |

### JavaScript/TypeScript Files (19 trovati)

| File | Riferimenti SNCP | Necessita Fix |
|------|------------------|---------------|
| `packages/cli/src/sncp/init.js` | ✅ Crea `.sncp/progetti/{name}/` | ❌ NO |
| `packages/cli/src/sncp/loader.js` | ✅ Legge da `.sncp/progetti/` | ❌ NO |
| `packages/cli/src/sncp/writer.js` | ⚪ Scrive in `.sncp/progetti/` | ❌ NO |
| `packages/cli/src/commands/housekeeping.js` | ✅ Check limiti file corretti | ❌ NO |
| Altri 15 file | ⚪ Riferimenti generici | ❌ NO |

### Documentazione (100+ file)

| Categoria | Status | Note |
|-----------|--------|------|
| Guide generiche | ✅ OK | Menzionano "NORD.md" senza path specifici |
| Roadmap | ✅ OK | Non specificano path assoluti |
| Template | ✅ OK | Riferimenti relativi |
| Handoff storici | ⚪ IGNORARE | Path vecchi ma archiviati |

---

## FIX NECESSARI

### 1. Hook Session Start (PRIORITÀ ALTA)

**File:** `.claude/hooks/session_start_swarm.py`

**Problema:**
```python
# Riga 63 - PATH CORRETTO!
nord = load_file_summary(PROJECT_ROOT / "NORD.md", max_lines=60)
```

**Azione:** ✅ GIÀ CORRETTO! Il file cerca NORD.md in root (come da nuove regole).

**FALSO ALLARME** - Il codice è corretto, va nella root del progetto.

---

### 2. Dashboard API (PRIORITÀ BASSA)

**File:** `dashboard/api/parsers/markdown.py`

**Status:** ✅ GIÀ CORRETTO

```python
# Riga 19
nord_path = self.workspace / "NORD.md"  # Cerca in workspace root
```

La dashboard cerca NORD.md nella root di CervellaSwarm, che è CORRETTO.

---

### 3. CLI JavaScript (PRIORITÀ BASSA)

**Status:** ✅ NON SERVE FIX

La CLI non referenzia NORD.md direttamente - lavora solo su:
- `.sncp/progetti/{name}/stato.md`
- `.sncp/progetti/{name}/PROMPT_RIPRESA_{name}.md`

Nessun fix necessario.

---

## RISCHI SE NON AGGIORNIAMO

### Rischio Effettivo: ⚪ BASSO

**Perché?**

1. **Hook già corretti**: Session start cerca NORD.md in root (corretto)
2. **Dashboard già corretta**: Parser cerca NORD.md in workspace root
3. **CLI non impattata**: Non usa NORD.md
4. **Docs generiche**: Non specificano path assoluti

### Unico Rischio Residuo

**Confusione umana**: Se Rafa o Worker cercano NORD.md in `.sncp/`, non lo trovano.

**Mitigazione:** Documentazione chiara in `~/.claude/CLAUDE.md` (già fatto!)

---

## RACCOMANDAZIONI

### ALTA Priorità

- [ ] **NESSUNA** - Il codice è già allineato!

### MEDIA Priorità

- [ ] Aggiungere test automatico che verifica:
  - NORD.md esiste in project root
  - NORD.md NON esiste in `.sncp/`
  - stato.md esiste in `.sncp/progetti/{name}/`

### BASSA Priorità

- [ ] Aggiornare commenti in `session_start_swarm.py`:
  ```python
  # NORD.md (la bussola) - SEMPRE nella root del progetto!
  nord = load_file_summary(PROJECT_ROOT / "NORD.md", max_lines=60)
  ```

---

## CONCLUSIONI

### Verdict: ✅ CODICE GIÀ ALLINEATO!

I cambiamenti alla struttura SNCP sono stati:
1. ✅ Definiti chiaramente in `~/.claude/CLAUDE.md`
2. ✅ Il codice Python/JS già cerca NORD.md nel posto giusto (root)
3. ✅ I file duplicati sono stati archiviati
4. ⚪ La documentazione è generica (non specifica path)

### Azione Richiesta

**NESSUNA modifica al codice necessaria!**

Il sistema funziona correttamente. L'unico fix necessario era documentazionale (già completato in `~/.claude/CLAUDE.md`).

---

**Next Steps:**

1. ⚪ (Opzionale) Aggiungere test che verifica posizione NORD.md
2. ⚪ (Opzionale) Migliorare commenti in hook

---

*Report generato da cervella-ingegnera*  
*"Il codice pulito è codice che rispetta chi lo leggerà domani!"*
