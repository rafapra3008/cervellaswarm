# Task: Test Worker Edit

**Assegnato a:** cervella-backend
**Stato:** ready
**Priorita:** ALTA
**Data:** 2026-01-07

---

## Obiettivo

Verificare che i Worker possano editare file dopo il fix degli hook.

**IMPORTANTE:** Questo e' un test del sistema hook. Se riesci a editare questo file, il fix funziona!

---

## Azione Richiesta

1. Crea un file di test: `.swarm/test/WORKER_CAN_EDIT.txt`
2. Scrivi dentro: "Worker edit test PASSED - [timestamp]"
3. Conferma nel file _output.md

---

## Output Atteso

File `.swarm/test/WORKER_CAN_EDIT.txt` creato con successo.

---

## Note

- Se questo task FALLISCE con "hook blocked", il fix non funziona
- Se questo task PASSA, il sistema Regina/Worker e' OK
