# TASK: Analisi Funzionalità CervellaSwarm

**Assegnato a:** cervella-ingegnera
**Priorità:** Alta
**Data:** 2026-01-10

---

## Obiettivo

Analizzare TUTTE le funzionalità di CervellaSwarm per verificare:
1. Cosa funziona
2. Cosa è rotto o incompleto
3. Cosa manca
4. Miglioramenti possibili

---

## Cosa Analizzare

### 1. CLI `cervella/`
- Verifica struttura codice
- Trova TODO/FIXME nel codice
- Identifica funzionalità incomplete

### 2. Scripts `scripts/`
- Quali script esistono?
- Sono tutti usati?
- Ci sono script orfani?

### 3. Hooks `~/.claude/hooks/`
- Quali hook esistono?
- Sono tutti attivi?
- Errori o warning nei log?

### 4. spawn-workers
- Verifica script in ~/.local/bin/
- Funzionalità mancanti?
- Edge cases non gestiti?

### 5. Test Suite
- Quali test esistono?
- Coverage?
- Test mancanti?

---

## Output

Scrivi report dettagliato in:
`.sncp/analisi/ANALISI_FUNZIONALITA_20260110.md`

Formato:
```markdown
# Analisi Funzionalità CervellaSwarm

## CLI cervella/
- Status: [OK/INCOMPLETO/ROTTO]
- Issues: [lista]
- TODO trovati: [lista]

## Scripts
- Totale: N script
- Usati: N
- Orfani: [lista]

## Hooks
- Totale: N
- Attivi: N
- Issues: [lista]

## spawn-workers
- Versione: X.X.X
- Issues: [lista]
- Miglioramenti: [lista]

## Test
- Coverage: X%
- Test mancanti: [lista]

## TOP 10 Miglioramenti Prioritari
1. ...
```

---

## Verifica Post-Write

DOPO aver scritto il file, LEGGI il file per confermare che è stato salvato!
