# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 6 Marzo 2026 - Sessione 293 (SPRING-008b DEPLOYATO + UX-004 fix)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

## Quick Status S293

| Cosa | Stato |
|------|-------|
| **Produzione MAIN** | **V3 LIVE v1.16.1 su contabilitafamigliapra.it** |
| **DEPLOY PENDENTI** | **1: annullamenti.js su VM (UX-004 scroll fix)** |
| **MAPPA** | **`docs/MAPPA_MIGLIORAMENTI_S262.md` - 37 item, 0 TODO, 1 IN_PROGRESS (QC-003), 36 DONE** |
| **Test** | **124/124 spring_insert PASS + 3264 test totali** |
| **SPRING Pipeline** | **NL+SHE+HP TUTTI OK! RegisNumero #1005. Limite 5000. Automazione 15:00 attiva.** |

## Cosa Ha Fatto S293

### 1. SPRING-008b: DEPLOYATO HPTERMINAL01!

**Problema risolto:** Pipeline SHE+HP bloccata - RegisNumero #1001 superava limite 1000.

**Deploy eseguito:**
- Script automatico `deploy_spring_008b.ps1` (backup+sostituzione+pulizia __pycache__+verifica)
- Audit script pre-deploy: corretto falso positivo pattern (commento storico matchava il check)
- Dry-run `--all` OK: NL 0 doc (idempotency), SHE 2, HP 3
- **Run reale: 5 doc committati con successo:**

| Hotel | Tipo | RegisNumero | Totale | Trial Balance |
|-------|------|-------------|--------|---------------|
| SHE | GIR | #1001 | 953.60 | OK |
| SHE | CARTE | #1002 | 1358.40 | OK |
| HP | CARTE | #1003 | 1036.40 | OK |
| HP | BONIFICI | #1004 | 200.00 | OK |
| HP | BONIFICI | #1005 | 80.00 | OK |

- mark-done OK per SHE e HP, Telegram inviate, HC.io ping OK
- Task Scheduler confermato attivo: prossimo run 07/03 15:00
- File su Desktop Mac: `~/Desktop/spring_deploy_S292/` (backup deploy)

### 2. Bug "Collega" - RISOLTO! Era UX, non bug

**Investigazione:** 3 cervelle parallele (Frontend+Reviewer+Data). Scoperto che:
- Backend INTATTO (S291 non ha toccato codice)
- Il pannello SI APRIVA ma `scrollIntoView({ block: 'nearest' })` non scrollava abbastanza
- Il pannello appariva SOTTO la riga, fuori viewport - sembrava non funzionare

**Fix (UX-004):** `annullamenti.js` riga 633 - cambiato a `block: 'center'` con 50ms delay.
- Guardiana 9.7/10 APPROVED (0 P1, 0 P2, 2 P3 cosmetici)
- Testato localmente da Rafa: pannello si apre al centro della pagina
- **Deploy VM pendente** (1 file: `frontend/js/annullamenti.js`)

### 3. Commit e Documentazione

- 3 commit: S292 fix + S293 deploy + S293 UX fix
- MAPPA aggiornata: 37 item, 36 DONE
- NORD.md, PROMPT_RIPRESA, memoria tutti aggiornati

## Deploy Pendente (S294)

```bash
# 1 solo file - Fortezza Mode
./scripts/deploy_v3_files.sh frontend/js/annullamenti.js

# Verifica post-deploy:
curl -s https://contabilitafamigliapra.it/static/js/annullamenti.js | head -4
# Deve mostrare v2.1.0 (versione invariata, solo fix scroll interno)

# Test: aprire NL Caparre, click "Collega" su una cancellazione
# Il pannello deve apparire al CENTRO della pagina
```

## PROSSIMI STEP (S294)

1. **DEPLOY VM**: `annullamenti.js` UX-004 (1 file, Fortezza Mode, procedura sopra)
2. **QC-003**: Code Review split file grandi (IN_PROGRESS, 10/28 DONE)
3. **AGENT-005**: Pulizia file duplicati/vecchi sui PC hotel (TODO P3)

## Bloccato

**NESSUNO!** Pipeline funzionante per tutti e 3 hotel. Automazione attiva.

## Lezioni Apprese (Sessione 293)

### Cosa ha funzionato bene
- **Script PowerShell automatico > procedura manuale**: zero errori umani, backup+verifica inclusi.
- **Audit script ANCHE su codice proprio**: trovato falso positivo (pattern commento storico). Senza audit lo script si sarebbe bloccato su HPTERMINAL01.
- **Dry-run --all**: NL idempotency confermata, SHE+HP preview perfetto. Nessuna sorpresa al run reale.
- **3 cervelle caccia bug = diagnosi completa**: anche se il "bug" era UX, l'investigazione ha confermato che backend e frontend sono integri.
- **Test su hotel diverso (SHE)**: ha dimostrato che non era un bug di codice ma specifico al caso.

### Cosa non ha funzionato
- **Falso allarme bug**: il "bug collega" era in realta' un problema di scroll UX. La caccia con 3 cervelle era overkill per questo caso. Lezione: prima verificare in produzione con DevTools, POI lanciare le cervelle.

### Pattern confermato
- **Script .py/.ps1 per deploy > comandi manuali** (Lezione #23, 5a evidenza).
- **Audit SEMPRE prima di eseguire** (anche su codice proprio).
- **Testare su piu' hotel per isolare il problema** (NL vs SHE ha chiarito subito).

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*

<!-- AUTO-CHECKPOINT-START -->

## AUTO-CHECKPOINT: 2026-03-06 18:50 (unknown)

### Stato Git
- **Branch**: lab-v3
- **Ultimo commit**: e01e999 - S293: Checkpoint finale - MAPPA+NORD aggiornati (UX-004 + deploy pendente)
- **File modificati**: Nessuno (git pulito)

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

<!-- AUTO-CHECKPOINT-END -->
