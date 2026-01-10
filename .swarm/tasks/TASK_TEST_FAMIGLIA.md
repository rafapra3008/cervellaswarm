# TASK: Test Funzionalità Famiglia

**Assegnato a:** cervella-tester
**Priorità:** Alta
**Data:** 2026-01-10

---

## Obiettivo

Testare le funzionalità REALI della famiglia per verificare che tutto funzioni.

---

## Test da Eseguire

### 1. Test SNCP
- [ ] Scrivi file in .sncp/test/TEST_SCRITTURA.md
- [ ] Leggi il file per verificare
- [ ] Cancella file test

### 2. Test CLI cervella (se installato)
```bash
cervella --version
cervella status
```

### 3. Test Notifiche macOS
```bash
osascript -e 'display notification "Test Tester" with title "CervellaSwarm" sound name "Glass"'
```

### 4. Test tmux (per spawn-workers headless)
```bash
tmux list-sessions 2>/dev/null || echo "Nessuna sessione tmux"
```

### 5. Test Watcher
- Verifica se watcher-regina.sh esiste
- Verifica se funziona

### 6. Test Context Monitor
- Verifica che statusLine funzioni

---

## Output

Scrivi report in:
`.sncp/test/TEST_FAMIGLIA_20260110.md`

Formato:
```markdown
# Test Famiglia - 10 Gennaio 2026

## Risultati

| Test | Risultato | Note |
|------|-----------|------|
| SNCP Write | PASS/FAIL | |
| CLI cervella | PASS/FAIL | |
| Notifiche | PASS/FAIL | |
| tmux | PASS/FAIL | |
| Watcher | PASS/FAIL | |
| Context Monitor | PASS/FAIL | |

## Issues Trovati
[lista]

## Raccomandazioni
[lista]
```

---

## Verifica Post-Write

DOPO aver scritto il file, LEGGI il file per confermare che è stato salvato!
