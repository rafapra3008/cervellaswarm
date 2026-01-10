# Handoff: TASK_HARDTEST_REALTIME_v124

**Da:** cervella-tester
**Per:** Regina
**Data:** 2026-01-10

## Situazione

Il task TASK_HARDTEST_REALTIME_v124 richiede:
1. Esecuzione interattiva di spawn-workers
2. Monitoraggio tmux in tempo reale
3. Checkout git tra versioni diverse (v3.1.0 vs v3.2.0)
4. Stress test con worker multipli
5. Test watcher integration

## Problema

Questo tipo di test NON può essere eseguito automaticamente da un worker perché:
- Richiede sessioni tmux attive
- Richiede osservazione manuale dell'output in tempo reale
- Richiede comparazione tra versioni git
- Richiede coordinamento con altri worker

## Raccomandazione

Questo test deve essere eseguito manualmente da Rafa o dalla Regina in sessione interattiva.

Il file .ready è stato lasciato intatto per decisione futura.

---
cervella-tester
