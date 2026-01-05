# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 5 Gennaio 2026 - Sessione 98 FINALE

---

## CARA PROSSIMA CERVELLA

```
+------------------------------------------------------------------+
|                                                                  |
|   Benvenuta! Questo file e' la tua UNICA memoria.               |
|   Leggilo con calma. Qui c'e' tutto quello che devi sapere.     |
|                                                                  |
|   Tu sei la REGINA dello sciame.                                 |
|   Hai 16 agenti pronti a lavorare per te.                       |
|                                                                  |
|   SESSIONE 98: TUTTO SALVATO E VERIFICATO!                      |
|                                                                  |
|   L'HANDOFF HA FUNZIONATO!                                       |
|   - Tutti i file sono stati salvati correttamente               |
|   - Hook block_task_for_agents.py ATTIVO                        |
|   - ROADMAP 3 PEZZI MANCANTI creata                             |
|                                                                  |
|   PROSSIMA SESSIONE: ANTI AUTO-COMPACT (Priorita' 1)            |
|                                                                  |
|   "SU CARTA != REALE" - Solo le cose REALI contano!             |
|   "SEMPRE FINESTRE!" - Rafa                                     |
|                                                                  |
+------------------------------------------------------------------+
```

---

## I 3 PEZZI MANCANTI PER IL 100000%!

```
+------------------------------------------------------------------+
|                                                                  |
|   ROADMAP: docs/roadmap/ROADMAP_3_PEZZI_MANCANTI.md             |
|                                                                  |
|   PEZZO 1: ANTI AUTO-COMPACT (Priorita' MASSIMA!)               |
|   - Esiste "su carta" ma NON e' seamless                        |
|   - Da testare in sessione REALE                                |
|   - Da rendere PERFETTO                                          |
|                                                                  |
|   PEZZO 2: SISTEMA FEEDBACK CERVELLE                            |
|   - Idea GENIALE di Rafa                                        |
|   - Ogni Cervella lascia feedback a fine sessione               |
|   - Il sistema IMPARA dai propri errori                         |
|                                                                  |
|   PEZZO 3: ROADMAPS VISUALE                                     |
|   - Multi-progetto automatico                                   |
|   - Un comando, tutti i progetti visibili                       |
|   - DA RICERCARE prima                                          |
|                                                                  |
+------------------------------------------------------------------+
```

---

## COSA FUNZIONA GIA' (REALE!)

| Cosa | Status |
|------|--------|
| 16 Agents in ~/.claude/agents/ | FUNZIONANTE |
| Sistema Memoria SQLite | FUNZIONANTE |
| 11 Hooks globali | FUNZIONANTE |
| block_task_for_agents.py | NUOVO! BLOCCA Task per cervella-* |
| spawn-workers v2.7.0 | AUTO-SVEGLIA SEMPRE! |
| context_check.py v4.3.0 | VS CODE NATIVO! |
| watcher-regina.sh | fswatch + AppleScript |
| TESTO_INIZIO_SESSIONE.md | Template per Rafa |

---

## SESSIONE 98: COSA ABBIAMO FATTO

### Parte 1: Protezione Task Tool

**Il Problema:**
Una Cervella in Miracollo ha usato Task tool invece di spawn-workers.
Risultato: contesto al 6%, TUTTO BLOCCATO, lavoro PERSO!

**La Soluzione (LIVELLO 1 + LIVELLO 2):**

*Livello 1 - Linguaggio forte:*
- cervella-orchestrator.md v1.3.0 - Box VIETATO in cima
- SWARM_RULES.md v1.7.0 - Conseguenze catastrofiche

*Livello 2 - Hook che BLOCCA:*
- block_task_for_agents.py - PreToolUse
- Se contiene "cervella-" -> BLOCCATO!

**HARDTEST Passati:**
- cervella-backend -> BLOCCATO!
- Explore -> Passa (legittimo)
- general-purpose -> Passa (legittimo)

### Parte 2: Recap ONESTO

Rafa ha chiesto recap di CervellaSwarm. Prima risposta troppo ottimista.
Rafa: "rileggi COSTITUZIONE"

Refresh! "SU CARTA != REALE" - Solo le cose REALI contano!

Identificati 3 PEZZI MANCANTI per il 100000%!

### Parte 3: Verifica Handoff

L'auto-compact ha scattato a 72%.
La nuova Cervella ha ripreso e verificato:
- Tutti i file salvati correttamente
- Hook attivo e funzionante
- Roadmap creata

**Lezione:** Mai dire "e' fatto" se non e' REALE!

---

## PROSSIMA SESSIONE

```
INIZIARE DA: ANTI AUTO-COMPACT (Priorita' 1)

1. Testare context_check.py in sessione REALE
2. Vedere se handoff e' SEAMLESS
3. Identificare bug/problemi
4. Fixare
5. HARDTEST end-to-end (10 volte di fila)

"Il vero test e' l'uso!" - Rafa
```

---

## COMANDI UTILI

```bash
# Spawn worker (SEMPRE usare questo per delegare!)
spawn-workers --backend
spawn-workers --frontend
spawn-workers --docs

# Quick task
quick-task "descrizione" --backend

# Health check
swarm-health

# Status
swarm-status
```

---

## LO SCIAME (16 membri)

```
TU SEI LA REGINA (Opus) - Coordina, DELEGA, MAI edit diretti!

3 GUARDIANE (Opus):
- cervella-guardiana-qualita
- cervella-guardiana-ops
- cervella-guardiana-ricerca

12 WORKER (Sonnet):
- frontend, backend, tester
- reviewer, researcher, scienziata, ingegnera
- marketing, devops, docs, data, security

POSIZIONE: ~/.claude/agents/ (GLOBALI!)
```

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"SU CARTA != REALE" - Solo le cose REALI ci portano alla LIBERTA!

"SEMPRE FINESTRE! SEMPRE! SENZA ECCEZIONE!" - Rafa

"E' il nostro team! La nostra famiglia digitale!"

"Ultrapassar os proprios limites!"
```

---

**VERSIONE:** v38.0.0
**SESSIONE:** 98 FINALE
**DATA:** 5 Gennaio 2026

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa
