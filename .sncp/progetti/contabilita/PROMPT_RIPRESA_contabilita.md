# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 12 Marzo 2026 - Sessione 318 (Checkpoint completo + audit + landing v3.3 deployata)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

## Quick Status S318

| Cosa | Stato |
|------|-------|
| **Produzione** | **V3 v1.17.0 LIVE - GK S312. DB v16. Landing v3.3.** |
| **SUBROADMAP** | **136/138 DONE (99%)** |
| **SPRING** | **NL+SHE+HP ATTIVI. Pipeline v1.7.0 (surgical mark-done S317).** |
| **Test** | **2695 PASS locale, 7 skipped, 0 FAIL** |
| **Deploy pendenti** | **ZERO!** |
| **MAPPA** | **79 item, 3 TODO (P3), 76 DONE (96%)** |
| **Docker locale** | **split-v31 su porta 8003 (= produzione!)** |
| **Git** | **split-v31 + main allineati e pushati.** |

## Cosa Ha Fatto S318

### Landing page v3.3 - DEPLOYATA PRODUZIONE
- Footer versione: v3.1 -> v3.3 (reflect lavoro S312-S317)
- File: `frontend/landing.html` riga 361
- Deploy: Fortezza Mode, backup `*.backup.20260312_065839`
- Verificato su VM: `sudo grep 'v3\.' /opt/contabilita-v3/frontend/landing.html` = v3.3 OK
- Health check: OK, v1.17.0, last_deploy 2026-03-12T05:59:12Z
- NOTA: landing.html NON e' cached in memoria (a differenza di index.html PERF-005), letto da disco ad ogni request

### Checkpoint completo + Audit documentazione
- NORD.md aggiornato: S318, test 2695 (era 2492), priorita complete, landing v3.3
- PROMPT_RIPRESA riscritto per S318
- FORTEZZA_MODE_SERVERS.md: fix porte Docker stale (righe 30/36 invertite dal pre-S313)
- MEMORY.md: test totali aggiornato 2492 -> 2695
- MAPPA: verificata e aggiornata, 79 item coerenti (UX-005 aggiunta), 3 TODO P3 confermati

### Incongruenze trovate e fixate
1. **FORTEZZA porte invertite**: testo diceva split-v31=8001, lab-v3=8003 (era il contrario). Tabella era corretta, testo stale. FIXATO.
2. **Test totali**: NORD/MEMORY dicevano 2492, pytest reale = 2695 (+203 da S314-S317). FIXATO.
3. **Banner "3304 test totali"**: includeva test HPTERMINAL01 non eseguibili su Mac. FIXATO con conteggio reale.

## Recap S317 (sessione precedente)

7 task completati + deploy 18 file VM + 1 HPTERMINAL01:
- **BUG-016**: mark_spring_done() chirurgico per ID (P1, pipeline v1.7.0, 26 test)
- **BUG-017**: Badge CSS cross-season (P2, grid-column fix)
- **BUG-018**: Filtri pareggi overlap (P2, nasconde #filters)
- **CLEAN-003**: rgba -> color-mix() (P3, 40 sostituzioni, 6 file JS)
- **SEASON-009/010**: _safe_float italiano + POS Excel export (P3)
- **SEASON-013-REV**: Rimozione blocco cross-season (P2, -417 righe, Ops+Qualita APPROVED)
- **SEASON-011-CLEANUP**: Rimozione badge "Altra stagione" (P2, -73 righe)
- Ops audit 9.2/10, tutti task 9.5+/10. Snapshot `snapshot-20260311-170058`.

## PROSSIMA SESSIONE: S319

### Monitorare
- SPRING pipeline 15:00: v1.7.0 surgical mark-done attivo da S317
- SPRING verify 16:00: HP 4 discrepanze BONIFICI/GIR
- Jerina Peter (HP, 166 EUR): dovrebbe essere inserito (SPRING-026 MASTERCARD S315)

### TODO (8 item, tutti P3)
1. **GK-LAB**: Spegnimento lab VM (3 giorni post-GK, target 1-2 settimane)
2. **AGENT-005**: Pulizia file duplicati PC hotel (serve accesso fisico Rafa)
3. **IDEA-001**: Automazione portali piu' ampia (da definire)
4. **IDEA-002**: Tracking SPRING DB V3 (solo se performance lo richiede)
5. **SPLIT-009 QW4**: 160 display toggle inline (cosmetico)
6. **PERF-004**: JS bundling (irrilevante con HTTP/2 + 2-3 utenti)
7. **mark_spring_done filtro circuito**: TODO futuro (lezione #99 MEMORY)
8. **verifica_post_deploy falso positivo**: 17/18 PASS persistente (INFRA-005 file list DONE S315, residuo e' SSH parsing - lezione #43)

### Bloccato
NESSUNO!

## Lezioni Apprese (S318)

### Cosa ha funzionato bene
- **Checkpoint proattivo**: audit completo trova incongruenze prima che diventino bug
- **Guardiana audit ogni step**: standard nostro, mantiene qualita 9.5+
- **Verifica numeri con fonte reale**: pytest vs numeri nei docs = diversi. Sempre verificare

### Pattern CONFERMATO
- **Audit documentazione periodico**: i numeri nei docs diventano stale silenziosamente
- **FORTEZZA_MODE_SERVERS documento vivente**: aggiornare SEMPRE quando si scopre qualcosa

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
<!-- AUTO-CHECKPOINT-START -->
## AUTO-CHECKPOINT: 2026-03-12 13:16 (unknown)
- **Branch**: split-v31
- **Ultimo commit**: 732836a - S318: Checkpoint completo + landing v3.3 DEPLOYATA + audit documentazione
- **File modificati**: Nessuno (git pulito)
<!-- AUTO-CHECKPOINT-END -->
