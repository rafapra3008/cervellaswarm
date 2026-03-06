# Auto-Handoff Miglioramenti - Research Report
**Data**: 2026-02-18
**Status**: COMPLETA
**Fonti**: 14 consultate
**Autore**: Cervella Researcher - S369

---

## Sintesi Esecutiva

- Autocompact 2026 e migliorato (+12K token usabili, compaction istantanea) ma NON elimina SNCP
- Aprire una nuova finestra per ogni handoff e un antipattern: la community usa STESSA sessione
- SNCP (disco, persistente) e autocompact (RAM, volatile) sono complementari, non alternativi
- Raccomandazione: eliminare apertura nuova finestra, usare handoff "soft" con `/compact` in-session

---

## 1. Stato Autocompact 2026

### 1.1 Il Cambiamento Buffer 45K -> 33K

A inizio 2026 (v2.1.21+) il buffer e stato ridotto da ~45.000 a ~33.000 token:

```
Finestra totale:     200.000 token
Buffer riservato:     33.000 token (16.5%, era 22.5%)
Token usabili:       167.000 token (era ~155.000)
Guadagno:            +12.000 token (+7.7%)
Compaction trigger:  ~83.5% utilizzo (era ~77-78%)
```

### 1.2 Compaction Istantanea (v2.0.64)

Cambio piu importante: da v2.0.64 il compact e ISTANTANEO. Il sistema scrive
summary in background ogni ~5.000 token o ogni 3 tool calls. Quando scatta
il compact, carica il summary gia pronto invece di ricalcolarlo (era fino a 2 minuti).

### 1.3 Session Memory Automatica (v2.1.30-31, Febbraio 2026)

Nuova feature in rollout: session memory automatica. Salva in background in
`~/.claude/projects/<hash>/<session-id>/session-memory/summary.md`. A fine
sessione, alla sessione successiva appare "Recalled N memories". Struttura:
- Session title (auto-generato)
- Current status (items completati + domande aperte)
- Key results (decisioni e pattern)
- Work log (cronologico)

Scrive ogni ~5.000 token o 3 tool calls.

### 1.4 Cosa Rimane Limitato

Nonostante i miglioramenti, autocompact perde:
- Nomi variabili specifici da early session
- Messaggi di errore esatti
- Decisioni sfumate prese ore fa
- Contesto cross-sessione (multi-giorno)
- Tutto cio che e stato compattato piu volte

**Conclusione sezione 1**: Autocompact 2026 e molto migliorato. Sessioni 4-6h
sono piu viabili. Ma NON sostituisce memoria persistente su disco.

---

## 2. Il Problema "Apri Nuova Finestra"

### 2.1 Come Funziona Oggi nel Nostro Sistema

Il sistema CervellaSwarm attuale per l'auto-handoff:
1. Rileva contesto in esaurimento
2. Fa git commit
3. Crea file HANDOFF_*.md con 6 sezioni
4. **Apre una NUOVA finestra Claude Code** (`claude` da terminale)
5. La nuova sessione parte da zero (deve ricaricare tutto il contesto)

Problema: con N task al giorno, si accumulano N finestre. La nuova sessione
non ha il contesto della vecchia. Il SNCP serve proprio a ricostruire quel
contesto, ma e un overhead.

### 2.2 La Community NON Apre Nuove Finestre

Analisi di 5 approcci della community (2025-2026):

| Tool | Approccio | Nuova Finestra? |
|------|-----------|-----------------|
| Smart Handoff | `/compact` custom + WORKING.md, stessa sessione | NO |
| claude-code-handoff | `/handoff` JSON + `/pickup` stessa sessione | NO |
| Continuous Claude v3 | Ledger + `/resume_handoff`, stessa sessione | NO |
| claude-sessions | Slash commands, stessa sessione | NO |
| Context Recovery Hook | PreCompact auto-backup + `/clear` + reload | NO |

**Insight chiave**: NESSUN approccio della community apre una nuova finestra.
Il pattern universale e: salva contesto -> compatta o clears -> ricarica in
STESSA sessione.

### 2.3 Perche Aprire Nuove Finestre e un Antipattern

1. **Overhead UI**: ogni nuova finestra e una nuova istanza di Claude Code
2. **Cold start**: la nuova sessione deve leggere PROMPT_RIPRESA, CLAUDE.md, etc.
3. **Perdita contesto recente**: la nuova sessione non sa cosa e stato fatto
   nell'ultima ora (prima del compaction)
4. **Accumulazione**: dopo 4 ore di lavoro -> 3-4 finestre aperte
5. **Confusione**: quale finestra e quella "giusta"?

---

## 3. SNCP vs Autocompact: Complementari

```
+--------------------------------------------------+
|  AUTOCOMPACT (RAM)         |  SNCP (DISCO)        |
|  - Intra-sessione          |  - Cross-sessione    |
|  - Volatile                |  - Persistente       |
|  - Automatico              |  - Controllato       |
|  - Lossy (comprime)        |  - Lossless (tutto)  |
|  - Max 1 sessione          |  - Giorni/settimane  |
|  - Zero config             |  - Richiede gestione |
+--------------------------------------------------+
```

SNCP risolve problemi che autocompact NON puo risolvere:
- "Cosa avevamo deciso la settimana scorsa su X?"
- "Qual e lo stato del progetto dopo 369 sessioni?"
- "Subagent context injection" (hook SubagentStart)
- Condivisione stato tra sessioni parallele (swarm)

Autocompact risolve problemi che SNCP NON puo risolvere:
- Mantenere "flow" durante sessione lunga
- Zero overhead (automatico)
- Contesto immediato degli ultimi 30 minuti

**Sono complementari al 100%. Nessuno rende l'altro obsoleto.**

---

## 4. Tre Opzioni di Miglioramento

### Opzione A: Elimina Finestra, Usa `/compact` In-Session

**Come funziona:**
```
Contesto >70% pieno
  -> PreCompact hook: salva snapshot in .sncp/handoff/
  -> Aggiorna PROMPT_RIPRESA automaticamente (solo campi chiave)
  -> Esegue /compact con custom instructions
  -> STESSA sessione continua compattata
```

**Pro:**
- Zero nuove finestre
- Continuita di flusso
- Contesto recente preservato nel compact summary
- Implementazione semplice (hook PreCompact gia esiste)

**Contro:**
- Compact perde dettagli precisi (ma gia accade oggi con nuova finestra)
- Richiede modifica hook pre_compact_save.py

**Implementazione:**
- Modifica `pre_compact_save.py` per aggiornare PROMPT_RIPRESA
- Aggiungi `/compact` con custom instructions nel trigger
- Rimuovi logica "apri nuova finestra"

---

### Opzione B: Handoff "Soft" - Solo a Fine Sessione

**Come funziona:**
```
DURANTE sessione:
  -> Nessun handoff intermedio
  -> Autocompact gestisce la memoria
  -> PreCompact hook salva snapshot passivo

FINE sessione (trigger "checkpoint" o "chiudiamo"):
  -> Aggiorna PROMPT_RIPRESA
  -> git commit + push
  -> Crea HANDOFF_*.md come archivio storico
  -> NON aprire nuova finestra
```

**Pro:**
- Massima semplicita
- Sessioni 4-6h viabili con autocompact 2026
- HANDOFF diventa archivio storico (non trigger per nuova sessione)
- Allineato con nuova session memory automatica di Claude

**Contro:**
- Se sessione crashs senza checkpoint, stato perso
- Dipende da disciplina "checkpoint" manuale
- Non adatto per sessioni molto lunghe (>6h)

**Implementazione:**
- Nessun auto-handoff intermedio
- Trigger "checkpoint" = aggiorna PROMPT_RIPRESA + git
- Hook PreCompact mantiene snapshot di sicurezza

---

### Opzione C: Sistema Ibrido con Threshold Intelligente

**Come funziona:**
```
< 50% contesto usato:  Nessuna azione
50-70% contesto usato: Warning silenzioso (log)
70-85% contesto usato: PreCompact hook -> snapshot + update PROMPT_RIPRESA
85%+ contesto usato:   /compact automatico con custom instructions
Fine sessione:         checkpoint standard
```

**Pro:**
- Granulare e sicuro
- PROMPT_RIPRESA sempre aggiornato
- Compaction al momento ottimale (non troppo presto, non troppo tardi)
- Pattern usato da Context Recovery Hook della community

**Contro:**
- Piu complesso da implementare
- Richiede monitoraggio contesto (fattibile via hook)
- CLAUDE_AUTOCOMPACT_PCT_OVERRIDE necessario per configurare threshold

**Implementazione:**
- Estendi `pre_compact_save.py` per aggiornare PROMPT_RIPRESA
- Configura `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=85`
- Modifica `session_start_swarm.py` per caricare ultimo snapshot se recente

---

## 5. Raccomandazione Finale

**Adotta Opzione B (Handoff Soft) come base + elementi di Opzione C**

Logica:

1. **Con autocompact 2026 (33K buffer, compact istantaneo) le sessioni 4-6h
   sono ora viabili senza handoff intermedi.** Il problema originale che aveva
   motivato l'auto-handoff e significativamente mitigato.

2. **Aprire nuove finestre e antipattern confermato dalla community.** Nessuno
   lo fa. Il pattern standard e: /compact in-session.

3. **SNCP rimane fondamentale** per persistenza cross-sessione. Non si tocca.
   Si toglie solo l'apertura automatica di nuove finestre.

4. **PreCompact hook gia esiste** (`pre_compact_save.py`). Va solo esteso per
   aggiornare PROMPT_RIPRESA prima del compact invece di aprire nuova finestra.

### Implementazione Raccomandata (2 step)

**Step 1 (immediato):** Rimuovi logica "apri nuova finestra" dall'auto-handoff.
Lascia solo: git commit + aggiorna PROMPT_RIPRESA + crea snapshot in archivio.

**Step 2 (miglioramento):** Estendi `pre_compact_save.py` per:
- Aggiornare automaticamente PROMPT_RIPRESA con stato corrente
- Usare custom instructions nel compact (preserva priorita task)
- Configurare `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=85` per threshold ottimale

### KPI di Successo

- Finestre aperte durante sessione: da N a 1
- Overhead per riprendere lavoro dopo compact: < 2 minuti
- PROMPT_RIPRESA sempre aggiornato (check: data modifica < 24h)

---

## Fonti Consultate

1. [Claude Code autocompact mechanics - claudefa.st](https://claudefa.st/blog/guide/mechanics/context-buffer-management)
2. [Claude Code session memory - claudefa.st](https://claudefa.st/blog/guide/mechanics/session-memory)
3. [Context recovery hook - claudefa.st](https://claudefa.st/blog/tools/hooks/context-recovery-hook)
4. [Auto-compact explained - claudelog.com](https://claudelog.com/faqs/what-is-claude-code-auto-compact/)
5. [Smart Handoff for Claude Code](https://blog.skinnyandbald.com/never-lose-your-flow-smart-handoff-for-claude-code/)
6. [claude-code-handoff tool - GitHub](https://github.com/nlashinsky/claude-code-handoff)
7. [Continuous Claude v3 - GitHub](https://github.com/parcadei/Continuous-Claude-v3)
8. [claude-sessions tool - GitHub](https://github.com/iannuttall/claude-sessions)
9. [Claude Code session management - stevekinney.com](https://stevekinney.com/courses/ai-development/claude-code-session-management)
10. [Claude Code compaction - stevekinney.com](https://stevekinney.com/courses/ai-development/claude-code-compaction)
11. [Session handoff feature request - GitHub](https://github.com/anthropics/claude-code/issues/11455)
12. [PreCompact hook feature request - GitHub](https://github.com/anthropics/claude-code/issues/15923)
13. [Session memory - claudefa.st](https://claudefa.st/blog/guide/mechanics/session-memory)
14. [Claude Code hooks reference - code.claude.com](https://code.claude.com/docs/en/hooks)

---

*Report generato da Cervella Researcher - Sessione 369*
*CervellaSwarm - 2026-02-18*
