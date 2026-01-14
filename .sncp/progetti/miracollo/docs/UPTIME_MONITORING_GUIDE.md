# UptimeRobot Monitoring Guide - Miracollo

> **Data:** 14 Gennaio 2026
> **Scopo:** Setup monitoraggio uptime per https://miracollo.com
> **Creato da:** Cervella DevOps
> **Status:** Pronto per Rafa

---

## TL;DR

1. Accedi a https://uptimerobot.com (gratis)
2. Crea 2 monitor per gli endpoint health check
3. Configura alert email/Telegram
4. Fatto! Monitora 24/7

**Tempo setup:** ~10 minuti
**Costo:** Gratis (free tier = 50 monitor)

---

## PASSO 1: Creare Account UptimeRobot

### 1.1 Registrazione
- Vai su https://uptimerobot.com
- Clicca **"Sign Up"** (top right)
- Scegli email (consiglio: rafa@cervellaswarm.com)
- Crea password forte
- Verifica email
- Accedi

### 1.2 Dashboard
Una volta loggato:
- Vedrai la dashboard principale
- Clicca **"Add New Monitor"** (pulsante blu grande)

---

## PASSO 2: Aggiungere Monitor #1 - Health Check Principale

### 2.1 Informazioni Base
- **Monitor Type:** HTTP(s)
- **Friendly Name:** `Miracollo - Health Check`
- **URL:** `https://miracollo.com/api/health`

### 2.2 Configurazione Monitoraggio
- **Check Interval:** `5 minutes` (standard)
  - Monitora ogni 5 minuti
  - Consiglio: Non andare sotto 5 min (limite free tier)
- **HTTP Method:** GET
- **Timeout:** `30 seconds` (default OK)

### 2.3 Alert Delay
- **Alert Timeout:** `1` (aspetta 1 check fallito prima di alertare)
  - Evita false alarm
  - Se server va giù, sai in max 10 minuti (2x 5min)

### 2.4 Response Validation
**IMPORTANTE:** Configurare validazione risposta!

Scorri down fino a **"Advanced Settings"**
- Abilita **"Expect Response Status Code"**
  - Campo: `200` (OK)
- Abilita **"Expect Content"** (opzionale ma consigliato)
  - Cerca nel body: `"status":"ok"` oppure `"status":"healthy"`

### 2.5 Salva
- Clicca **"Create Monitor"**
- Vedrai il monitor aggiunto (stato: checking)

**Expected Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-01-14T15:30:45Z"
}
```

---

## PASSO 3: Aggiungere Monitor #2 - Health Check Dettagliato

### 3.1 Informazioni Base
- **Monitor Type:** HTTP(s)
- **Friendly Name:** `Miracollo - Health Detailed`
- **URL:** `https://miracollo.com/api/health/detailed`

### 3.2 Configurazione Monitoraggio
- **Check Interval:** `10 minutes` (meno frequente, più info)
  - Verifica ogni 10 minuti
  - Controlla database, redis, external APIs
- **HTTP Method:** GET
- **Timeout:** `30 seconds`

### 3.3 Alert Delay
- **Alert Timeout:** `2` (aspetta 2 check falliti prima di alertare)
  - Questo endpoint è più sensibile
  - Evita alert per blip momentanei

### 3.4 Response Validation
- Abilita **"Expect Response Status Code"**: `200`
- Abilita **"Expect Content"**:
  - Cerca nel body: `"status":"healthy"` oppure `"database":true`

### 3.5 Salva
- Clicca **"Create Monitor"**

**Expected Response:**
```json
{
  "status": "healthy",
  "database": true,
  "redis": true,
  "external_apis": true,
  "response_time_ms": 45,
  "timestamp": "2026-01-14T15:30:45Z"
}
```

---

## PASSO 4: Configurare Alert

### 4.1 Email Alert (Consigliato)
1. Clicca su uno dei monitor
2. Vai a **"Alert Contacts"** (in basso a sinistra)
3. Clicca **"Add Incident Alert Contact"**
4. Scegli **"Email"**
5. Inserisci: `rafa@cervellaswarm.com`
6. Clicca **"Create Alert Contact"**
7. Spunta il monitor nel popup
8. Done!

### 4.2 Telegram Alert (Opzionale ma comodo!)
1. Vai a https://t.me/uptimerobot_bot
2. Manda `/start` al bot
3. Riceverai un link di verifica
4. Copia il numero di verifica
5. Torna a UptimeRobot
6. Clicca **"Add Incident Alert Contact"**
7. Scegli **"Telegram"**
8. Incolla il numero di verifica
9. Clicca **"Create Alert Contact"**

### 4.3 Quale Usare?
| Canale | Quando | Pro | Contro |
|--------|--------|-----|--------|
| Email | Setup ufficiale | Sempre disponibile | Lento |
| Telegram | Tempo reale | Istantaneo, mobile | Serve account |

**Consiglio:** Setup ENTRAMBI. Email per backup, Telegram per real-time.

---

## PASSO 5: Monitoraggio Dashboard

### 5.1 Leggere la Dashboard
Una volta creati i 2 monitor, vedrai:

```
Miracollo - Health Check      ✅ UP (last check: 2 min ago)
Miracollo - Health Detailed   ✅ UP (last check: 5 min ago)
```

### 5.2 Statistiche
- **Uptime %:** Percentuale tempo operativo (ultimo mese)
- **Response Time:** Tempo medio risposta (ms)
- **Last Check:** Ultimo controllo

### 5.3 Esportare Dati
- Clicca monitor → **"Statistics"**
- Vedi grafico uptime nel tempo
- Scarica report (opzionale)

---

## TROUBLESHOOTING

### Monitor Dice "DOWN"

**Possibili cause e soluzioni:**

#### 1. Server davvero offline
- SSH in Miracollo VM
- Controlla: `docker ps` - container running?
- Controlla: `docker logs miracollo-pms-production` - errori?
- Riavvia se serve: `docker restart miracollo-pms-production`

#### 2. Endpoint non raggiungibile
- Testa manualmente: `curl https://miracollo.com/api/health`
- Verifica DNS risolve correttamente
- Verifica SSL cert è valido: `openssl s_client -connect miracollo.com:443`

#### 3. Response non contiene testo atteso
- Clicca monitor → **"Response Details"**
- Vedi l'errore specifico
- Aggiusta "Expect Content" in UptimeRobot

#### 4. URL sbagliato
- Verifica che `https://miracollo.com/api/health` è raggiungibile
- Non usare `http://` (deve essere `https://`)

### Alert non Arrivano

#### 1. Email
- Controlla spam/trash
- Verifica indirizzo email è corretto
- Ricrea alert contact

#### 2. Telegram
- Verifica bot è attivo: manda ping a @uptimerobot_bot
- Ricrea link di verifica
- Controlla acceso bot notifiche

---

## BEST PRACTICES

### Interval di Check
| Intervallo | Uso | Pro | Contro |
|-----------|-----|-----|--------|
| 1 min | Business critical | Real-time alerts | Tanti falsi alarm |
| 5 min | Produzione normale | Good balance | Max 10 min lag |
| 10 min | Non-critical | Risparmia richieste | Late detection |

**Per Miracollo:** 5 min per principale, 10 min per detailed = OK!

### Alert Delay
- **Alert Delay 1:** Alert subito dopo 1 fallimento (5 min)
- **Alert Delay 2:** Alert dopo 2 fallimenti (10 min)
- **Alert Delay 3+:** Alert dopo 3+ fallimenti (15+ min)

**Consiglio:** Usa Alert Delay 1 per salute principale, 2 per detailed.

### Response Validation
SEMPRE configurare:
- ✅ Status Code (200)
- ✅ Expected Content (stringa nel body)

Evita false positives (es: errore 500 ma responde comunque)

---

## MONITORING REMOTO

### Vedere Monitor da Mobile
1. Scarica app UptimeRobot
2. Accedi con stesso account
3. Notifiche push automatiche

### Share Status Page (Opzionale)
- UptimeRobot permette creare pagina pubblica
- Mostra status Miracollo ai clienti
- Setup: Dashboard → **"Statuspage"**

---

## NEXT STEPS INFRASTRUTTURA

Una volta UptimeRobot attivo, prossimi miglioramenti:

| Priority | Task | Effort | Benefit |
|----------|------|--------|---------|
| 1 | UptimeRobot setup | 10 min | Sapere quando va giù |
| 2 | Logs aggregation (ELK) | 1 day | Analizzare problem |
| 3 | Performance monitoring (DataDog) | 1 day | Capire bottleneck |
| 4 | Custom metrics | 2 days | Business intelligence |

---

## CHECKLIST SETUP

```
[ ] Account UptimeRobot creato
[ ] Monitor #1 (Health Check) aggiunto
  [ ] URL: https://miracollo.com/api/health
  [ ] Interval: 5 min
  [ ] Status Code: 200
  [ ] Expected Content: "status":"ok"
[ ] Monitor #2 (Health Detailed) aggiunto
  [ ] URL: https://miracollo.com/api/health/detailed
  [ ] Interval: 10 min
  [ ] Status Code: 200
  [ ] Expected Content: "status":"healthy"
[ ] Alert Email configurato
[ ] Alert Telegram configurato (opzionale)
[ ] Entrambi monitor showing ✅ UP
[ ] Prima alert test inviata
```

---

## SUPPORTO

Se qualcosa non funziona:
1. Clicca monitor → **"Response Details"** - vedi errore esatto
2. Verifica endpoint è raggiungibile: `curl https://miracollo.com/api/health`
3. Contatta Cervella DevOps con screenshot dell'errore

---

**Creato:** 14 Gennaio 2026
**Versione:** 1.0
**Ultimo aggiornamento:** Setup guide completa
**Status:** Pronto per implementazione
