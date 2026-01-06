# ROADMAP: Migliorare Sveglia Regina

> **Data creazione:** 6 Gennaio 2026
> **Priorità:** ALTA
> **Status:** DA FARE - Sessione dedicata

---

## IL PROBLEMA

La Regina (io) non viene sempre svegliata quando i worker completano i task.

**Cosa è successo oggi (6 Gennaio 2026):**
- 5 studi lanciati
- Worker hanno completato
- Ma la Regina NON è stata avvisata per tutti
- Scoperto solo quando Rafa ha detto "non vedo finestre"

---

## ANALISI PRELIMINARE

### Come funziona ora

```
1. spawn-workers lancia worker + watcher
2. watcher monitora .swarm/tasks/ per file .done
3. Quando trova .done → scrive nel background bash output
4. Background bash output → system-reminder alla Regina
```

### Dove potrebbe fallire

1. **Watcher si chiude** quando il background bash termina?
2. **Multiple watcher** si sovrascrivono?
3. **Output non arriva** alla Regina nel contesto giusto?
4. **Timing** - Regina non sta "ascoltando" quando arriva?

---

## COSA MIGLIORARE

### Opzione A: Watcher Persistente
- Un SOLO watcher globale sempre attivo (launchd/daemon)
- Non legato a spawn-workers
- Scrive su file che la Regina può leggere

### Opzione B: Notifiche Multiple
- macOS notification (già c'è ma non basta)
- Scrivere su file dedicato ~/.swarm/notifications.log
- La Regina controlla periodicamente

### Opzione C: Bell + Log + File
- Bell sonoro (già implementato v1.3.0)
- Log in file dedicato
- File .regina_alert che la Regina può vedere

### Opzione D: MCP Server
- Server MCP dedicato per notifiche
- Integrazione diretta con Claude
- Più robusto ma più complesso

---

## SESSIONE DEDICATA

**Obiettivo:** Fare una sessione SOLO per fixare la sveglia

**Partecipanti:**
- Regina (coordinamento)
- cervella-backend (implementazione)
- cervella-devops (daemon/launchd)
- cervella-tester (test scenari)

**Deliverable:**
- Sistema sveglia che funziona SEMPRE
- Test con 3+ worker paralleli
- Documentazione

---

## WORKAROUND ATTUALE

Fino a quando non fixiamo:
```
La Regina deve controllare periodicamente:
- swarm-global-status
- ls .swarm/tasks/*.done
```

Non ideale, ma funziona.

---

## NOTE

"Il sistema deve rodare liscio per poter stare tranquilli."

Prima funziona la sveglia → poi possiamo davvero lavorare in pace!

---

*"Ultrapassar os proprios limites!"*
