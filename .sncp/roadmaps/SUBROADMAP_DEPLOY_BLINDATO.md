# SUBROADMAP: Deploy Blindato

> **Creata:** 18 Gennaio 2026 - Sessione 259
> **Problema:** Stessi errori deploy ripetuti 2 volte in 3 giorni
> **Obiettivo:** Rendere IMPOSSIBILE sbagliare il deploy

---

## IL PROBLEMA ROOT

```
+--------------------------------------------------------------------+
|                                                                    |
|   "Rendere il PATH CORRETTO piu FACILE del path sbagliato"        |
|                                                                    |
|   Oggi:   Comando manuale (5 sec) vs Script (30 sec)              |
|   Dopo:   Comando manuale (BLOCCATO) vs Script (10 sec)           |
|                                                                    |
+--------------------------------------------------------------------+
```

**Pattern identificato:**
```
CREIAMO SCRIPT -> NON LI USIAMO -> CASINO -> FIX -> REPEAT
```

**Causa root:**
- 93 script = troppi da ricordare
- Path manuale piu corto del path corretto
- Nessun enforcement (posso bypassare)
- Checklist passive che non leggiamo

---

## PRINCIPIO GUIDA

```
NON: "Devi usare lo script"
MA:  "Lo script fa in 1 comando quello che manualmente richiede 5"

NON: "Leggi la checklist"
MA:  "La checklist ti chiede interattivamente e BLOCCA se skip"
```

---

## FASE 1: FIX IMMEDIATO (oggi)

**Obiettivo:** Fermare il sanguinamento

| Task | Cosa | Chi | Status |
|------|------|-----|--------|
| 1.1 | Rimuovere container rogue `app-backend-1` | Guardiana Ops | PENDENTE |
| 1.2 | Disabilitare vecchio docker-compose.yml | Guardiana Ops | PENDENTE |
| 1.3 | Verificare 1 solo container backend | Guardiana Ops | PENDENTE |

---

## FASE 2: GUARDRAIL TECNICI (prossima sessione)

**Obiettivo:** Bloccare comandi manuali pericolosi

| Task | Cosa | Effort |
|------|------|--------|
| 2.1 | Wrapper bash su VM che blocca `docker run` | 10 min |
| 2.2 | Pre-flight check nel deploy.sh (conta container) | 15 min |
| 2.3 | Post-deploy health check OBBLIGATORIO | 10 min |
| 2.4 | container_name fisso in docker-compose.yml | 5 min |

**Wrapper da aggiungere a ~/.bashrc sulla VM:**
```bash
docker() {
    if [[ "$1" == "run" ]]; then
        echo "BLOCCATO: Usare docker-compose, non docker run!"
        echo "Comando: cd ~/app && ./deploy.sh"
        return 1
    fi
    command docker "$@"
}
```

---

## FASE 3: UN SOLO ENTRY POINT (sessione successiva)

**Obiettivo:** Da 93 script a 4 comandi

| Comando | Cosa fa |
|---------|---------|
| `cervella start` | Inizio sessione (legge COSTITUZIONE, verifica stato) |
| `cervella check` | Verifica stato attuale (container, DB, etc.) |
| `cervella deploy` | Deploy con TUTTE le verifiche automatiche |
| `cervella end` | Fine sessione (checkpoint completo) |

**Beneficio:** Ricordo 4 comandi invece di 93

---

## FASE 4: WIZARD INTERATTIVO DEPLOY (medio termine)

**Obiettivo:** Non posso saltare step

Invece di checklist passiva:
```
$ cervella deploy

[PRE-FLIGHT CHECK]
[OK] Git pulito
[OK] Test locale passato
[?] Backup DB fatto? (s/n) > s
[?] Guardiana approvato? (s/n) > s

[DEPLOY]
- docker-compose down --remove-orphans
- docker-compose up -d --build
- Health check...

[POST-DEPLOY]
[OK] 1 container backend
[OK] Health check passato
[OK] Planning risponde

DEPLOY COMPLETATO!
```

---

## FASE 5: MONITORAGGIO CONTINUO (lungo termine)

**Obiettivo:** Early warning se qualcosa va storto

| Task | Cosa |
|------|------|
| 5.1 | Cron ogni 5 min che verifica N container |
| 5.2 | Alert se container duplicati |
| 5.3 | Log di tutti i deploy |
| 5.4 | Score settimanale "processi rispettati" |

---

## CHECKLIST COMPLETAMENTO

| Fase | Status | Quando |
|------|--------|--------|
| FASE 1 | PENDENTE | Oggi |
| FASE 2 | PENDENTE | Prossima sessione |
| FASE 3 | PENDENTE | Sessione +1 |
| FASE 4 | PENDENTE | Sessione +2 |
| FASE 5 | PENDENTE | Medio termine |

---

## SUCCESS CRITERIA

```
+--------------------------------------------------------------------+
|                                                                    |
|   SUCCESSO = 0 incidenti deploy per 30 giorni consecutivi         |
|                                                                    |
+--------------------------------------------------------------------+
```

---

## REGOLA D'ORO

```
+--------------------------------------------------------------------+
|                                                                    |
|   MAI COMANDI DOCKER MANUALI SULLA VM!                            |
|                                                                    |
|   SEMPRE: ./deploy.sh                                             |
|                                                                    |
|   Se serve altro: PRIMA aggiorna deploy.sh                        |
|                                                                    |
+--------------------------------------------------------------------+
```

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
