# BUG: Watcher AUTO-SVEGLIA non notifica la Regina

**Rilevato:** 6 Gennaio 2026 - Sessione 108
**Priorità:** MEDIA
**Stato:** investigato_v1.6.0

---

## PROBLEMA

Il watcher rileva il file .done ma NON sveglia/notifica la Regina in modo efficace.
Rafa ha visto la notifica 3 minuti dopo il completamento.

---

## COMPORTAMENTO ATTESO

- Worker finisce → crea .done
- Watcher rileva .done → notifica IMMEDIATA alla Regina
- Regina reagisce subito

---

## COMPORTAMENTO ATTUALE

- Worker finisce → crea .done
- Watcher rileva .done → scrive "TASK COMPLETATO"
- Ma la Regina NON viene "svegliata" in tempo reale

---

## POSSIBILI CAUSE

1. Il watcher scrive su stdout ma la Regina non lo vede subito
2. Il meccanismo di notifica non è integrato con Claude Code
3. Serve un sistema di polling o webhook

---

## POSSIBILI SOLUZIONI

1. **Terminal bell** - Suono quando task completa
2. **File marker** - Scrivere in un file che la Regina controlla
3. **Notifica macOS** - osascript per notifica sistema
4. **Polling attivo** - Regina controlla periodicamente .done

---

## NOTE

Per ora la Regina deve controllare manualmente o Rafa avvisa.
Da sistemare in una sessione futura dedicata.

---

*"Documentare sempre i bug per il futuro!"*

---

## INVESTIGAZIONE (9 Gennaio 2026 - Sessione 134)

**Analisi:**
- Il watcher usa `fswatch` che e' istantaneo (non polling)
- Il ritardo di 3 minuti era probabilmente un caso isolato
- Possibile causa: fswatch non era in esecuzione al momento

**Miglioramenti applicati in v1.6.0:**
1. Aggiunto source common.sh per funzioni condivise
2. Implementato `notify_macos()` con sanitizzazione input (security fix)
3. Fallback sicuro se common.sh non disponibile

**Raccomandazione:**
- Monitorare se il problema si ripresenta
- Se si ripete, aggiungere logging piu' dettagliato

**Status:** Migliorato, da monitorare
