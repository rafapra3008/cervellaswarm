# AUDIT CONTEXT USAGE - CervellaSwarm
**Data:** 20 Gennaio 2026
**Analista:** cervella-ingegnera
**Status:** COMPLETATO

---

## PROBLEMA

Context usage DOPPIO del normale. Richiesto audit per identificare colpevoli.

---

## ANALISI COMPLETA

### 1. FILE INIETTATI A INIZIO SESSIONE

#### A) CLAUDE.md Files (System Reminder)

| File | Righe | Char | Token Est. | Iniettato |
|------|-------|------|------------|-----------|
| `~/.claude/COSTITUZIONE.md` | 509 | 15,424 | ~3,850 | Si (system reminder) |
| `~/.claude/CLAUDE.md` | 336 | 10,884 | ~2,720 | Si (system reminder) |
| `CervellaSwarm/CLAUDE.md` | 74 | 2,394 | ~600 | Si (system reminder) |
| **TOTALE CLAUDE.md** | **919** | **28,702** | **~7,175** | - |

**Note:** Tutti iniettati automaticamente come "system reminder" da Claude Code.

#### B) PROMPT_RIPRESA (Hook sncp_pre_session_hook.py)

| File | Righe | Char | Token Est. | Iniettato |
|------|-------|------|------------|-----------|
| `PROMPT_RIPRESA_cervellaswarm.md` | 100 | 2,633 | ~660 | Si (hook) |

#### C) DNA Agent (System Prompt)

| File | Righe | Char | Token Est. | Iniettato |
|------|-------|------|------------|-----------|
| `cervella-ingegnera.md` (DNA) | 59 | 1,262 | ~315 | Si (system prompt) |

**PERO:** Il DNA effettivo nel system prompt e MOLTO PIU GRANDE!
Contiene il DNA completo dell'Ingegnera (59 righe) + le istruzioni operative.

**Stima DNA totale:** ~17,000 char (~4,250 tokens)

#### D) Hook load_context.py Output

Lo script `load_context.py` (543 righe) viene eseguito e produce output markdown:

| Cosa | Token Est. |
|------|------------|
| Eventi recenti (5) | ~200 |
| Statistiche agent (top 5) | ~150 |
| Lezioni apprese (3) | ~300 |
| Suggerimenti attivi (5) | ~250 |
| Lezioni rilevanti formattate (3) | ~600 |
| **TOTALE load_context** | **~1,500** |

---

## TOTALE INJECTION STIMATO

| Fonte | Token Est. |
|-------|------------|
| CLAUDE.md (3 file) | 7,175 |
| PROMPT_RIPRESA | 660 |
| DNA Agent (completo) | 4,250 |
| load_context output | 1,500 |
| **TOTALE** | **~13,585 tokens** |

**NOTA CRITICA:** Questo e SOLO l'injection iniziale!
Non include:
- Il tuo prompt iniziale al task
- Le risposte precedenti nella conversazione
- File letti durante la sessione

---

## TOP 3 COLPEVOLI

### 1. CLAUDE.md (3 file) - 7,175 tokens
**Severita:** CRITICO
**Impatto:** 53% del totale
**Problema:** Tre file CLAUDE.md iniettati automaticamente:
- `~/.claude/COSTITUZIONE.md` (509 righe)
- `~/.claude/CLAUDE.md` (336 righe)  
- `CervellaSwarm/CLAUDE.md` (74 righe)

**Raccomandazione:**
```
CRITICO: Refactor COSTITUZIONE.md + CLAUDE.md

COSTITUZIONE.md (509 righe -> 150 righe)
- Mantenere: Obiettivi, Filosofia, Partnership
- ARCHIVIARE: Storia, Aneddoti, Esempi lunghi
- RIDURRE: Tabelle ripetitive

CLAUDE.md (336 righe -> 200 righe)
- CONSOLIDARE: Sezioni Miracollo (duplicazione)
- SNELLIRE: Tabelle (troppe ripetizioni)
- REFERENZIARE: Link a docs invece di copiare tutto

Target: -50% tokens (7,175 -> 3,500)
```

### 2. DNA Agent (completo) - 4,250 tokens
**Severita:** ALTO
**Impatto:** 31% del totale
**Problema:** Il DNA dell'Ingegnera e estremamente dettagliato.

**Nota:** Questo DNA include anche:
- Regole context-smart (che ironicamente consumano context!)
- Tabelle soglie
- Pattern da cercare
- Protocolli comunicazione swarm

**Raccomandazione:**
```
ALTO: Split DNA in Core + Extended

cervella-ingegnera-core.md (MAX 100 righe)
- Identita base
- Specializzazioni (lista)
- Regole fondamentali
- Output format

cervella-ingegnera-extended.md (referenza)
- Pattern completi
- Esempi dettagliati
- Workflow complessi
- Leggere con Read quando serve

Target: -40% tokens (4,250 -> 2,550)
```

### 3. load_context.py Output - 1,500 tokens
**Severita:** MEDIO
**Impatto:** 11% del totale
**Problema:** Formattazione troppo verbosa.

**Raccomandazione:**
```
MEDIO: Ottimizza format output

ATTUALE:
### 🟡 MEDIUM - Pattern Name
**Trigger:** Long description here...
**Problem:** Long description here...
**Solution:** Long description here...
*Confidence: 95% | Applicata 12x | Score: 85*

OTTIMIZZATO:
[🟡 MEDIUM] Pattern Name (12x, 95%)
→ Problem: Brief desc
→ Solution: Brief desc

Target: -30% tokens (1,500 -> 1,050)
```

---

## RACCOMANDAZIONI CONCRETE

### PRIORITA CRITICA (Fai ORA)

**1. COSTITUZIONE.md Refactor**
```bash
# Backup
cp ~/.claude/COSTITUZIONE.md ~/.claude/COSTITUZIONE_BACKUP.md

# Splitto
~/.claude/COSTITUZIONE.md (150 righe MAX)
  - Obiettivo finale
  - Filosofia core
  - Partnership rules
  - Formula magica (brief)

~/.claude/docs/STORIA_PARTNERSHIP.md
  - Aneddoti
  - Evoluzione
  - Lezioni apprese (narrative)
```

**2. CLAUDE.md Consolidation**
```bash
# Rimuovi duplicazioni Miracollo
# Consolida tabelle
# Usa link invece di copiare
```

**Target immediato:** -3,500 tokens (-26%)

---

### PRIORITA ALTA (Prossima sessione)

**3. DNA Agent Optimization**
```bash
# Split DNA
~/.claude/agents/cervella-ingegnera.md (100 righe MAX)
~/.claude/agents/cervella-ingegnera-extended.md (referenza)

# Aggiorna spawn-workers per iniettare solo core
```

**Target:** -1,700 tokens (-13%)

---

### PRIORITA MEDIA (Quando hai tempo)

**4. load_context Format Optimization**
```python
# Modifica format_lessons_for_agent()
# Usa formato compatto
# Rimuovi emoji ridondanti
# Abbrevia metadata
```

**Target:** -450 tokens (-3%)

---

## TOTALE RISPARMIO POSSIBILE

| Azione | Risparmio |
|--------|-----------|
| COSTITUZIONE + CLAUDE.md refactor | -3,500 tokens |
| DNA Agent split | -1,700 tokens |
| load_context optimization | -450 tokens |
| **TOTALE** | **-5,650 tokens (-42%)** |

**DA:** ~13,585 tokens
**A:** ~8,000 tokens

---

## METRICHE CONFRONTO

### Normal Session (Backend Worker)
- DNA: ~2,000 tokens
- CLAUDE.md: ~7,175 tokens
- PROMPT_RIPRESA: ~660 tokens
- load_context: ~1,500 tokens
- **TOTALE:** ~11,335 tokens

### Ingegnera Session (ATTUALE)
- DNA: ~4,250 tokens (DNA piu grande!)
- CLAUDE.md: ~7,175 tokens
- PROMPT_RIPRESA: ~660 tokens
- load_context: ~1,500 tokens
- **TOTALE:** ~13,585 tokens

**Differenza:** +2,250 tokens (+20%)

**CAUSA PRINCIPALE:** DNA Ingegnera e 2x piu grande del DNA standard!

---

## CONCLUSIONE

Il context usage e alto per 3 motivi:

1. **CLAUDE.md troppo grandi** (53% del problema)
2. **DNA Ingegnera molto dettagliato** (31% del problema)
3. **load_context verboso** (11% del problema)

**Azione immediata:** Refactor COSTITUZIONE + CLAUDE.md
**Risultato atteso:** -42% context usage

---

## NEXT STEPS

**Sessione 307:**
1. [ ] Backup COSTITUZIONE.md
2. [ ] Refactor COSTITUZIONE.md (509 -> 150 righe)
3. [ ] Refactor CLAUDE.md (336 -> 200 righe)
4. [ ] Test injection con session nuova
5. [ ] Verifica context usage

**Sessione 308:**
6. [ ] Split DNA Ingegnera (core + extended)
7. [ ] Ottimizza load_context format
8. [ ] Test completo

---

*Analisi completata: cervella-ingegnera*
*"Il debito tecnico si paga con gli interessi."*
