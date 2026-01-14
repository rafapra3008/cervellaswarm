# Uptime Monitoring Setup - Miracollo

> **Data:** 14 Gennaio 2026 - Sessione 201
> **Tool:** UptimeRobot (FREE tier)
> **Effort:** 10 minuti

---

## Perché Uptime Monitoring?

```
+================================================================+
|                                                                |
|   SENZA MONITORING:                                            |
|   - Server down? Lo scopri quando clienti si lamentano         |
|   - Weather API fallisce? Non lo sai                           |
|                                                                |
|   CON MONITORING:                                              |
|   - Alert immediato via email/Telegram                         |
|   - Statistiche uptime (99.9%?)                                |
|   - Storico incidenti                                          |
|                                                                |
+================================================================+
```

---

## Setup UptimeRobot (5 minuti)

### Step 1: Registrazione
1. Vai su https://uptimerobot.com
2. Crea account FREE (50 monitors gratuiti!)
3. Conferma email

### Step 2: Crea Monitor Health
1. Click "Add New Monitor"
2. Configura:
   ```
   Monitor Type: HTTP(s)
   Friendly Name: Miracollo Health
   URL: https://miracollo.com/api/health
   Monitoring Interval: 5 minutes
   ```
3. Save

### Step 3: Crea Monitor Weather (opzionale)
```
Monitor Type: HTTP(s)
Friendly Name: Miracollo Weather API
URL: https://miracollo.com/api/weather/status
Monitoring Interval: 15 minutes
```

### Step 4: Crea Monitor Events (opzionale)
```
Monitor Type: HTTP(s)
Friendly Name: Miracollo Events API
URL: https://miracollo.com/api/events/
Monitoring Interval: 15 minutes
```

### Step 5: Configura Alert
1. Settings → Alert Contacts
2. Aggiungi email: rafa@... (o team email)
3. (Opzionale) Aggiungi Telegram bot

---

## Monitors Raccomandati

| Monitor | URL | Intervallo | Priorità |
|---------|-----|------------|----------|
| Health | /api/health | 5 min | CRITICO |
| Weather | /api/weather/status | 15 min | ALTO |
| Events | /api/events/ | 15 min | MEDIO |
| Frontend | https://miracollo.com | 5 min | CRITICO |

---

## Alert Configuration

```
+----------------------------------------------------------------+
|   RACCOMANDATO:                                                |
|                                                                |
|   Down Alert:     Dopo 2 check falliti (10 min)                |
|   Up Alert:       Appena torna online                          |
|                                                                |
|   Canali:                                                      |
|   - Email (sempre)                                             |
|   - Telegram (opzionale, instant)                              |
|   - Webhook (per automazioni future)                           |
+----------------------------------------------------------------+
```

---

## Status Page Pubblica (Bonus)

UptimeRobot offre status page gratuita:
- URL tipo: https://stats.uptimerobot.com/xxxxx
- Mostra uptime % ultimi 30/90 giorni
- Utile per clienti enterprise

---

## Verifica Setup

Dopo configurazione:
1. Attendi 5 minuti
2. Verifica che UptimeRobot mostri "Up"
3. Test alert: ferma container temporaneamente
4. Verifica email ricevuta

---

## Costo

```
FREE TIER:
- 50 monitors
- 5 min interval
- Email alerts
- SMS: 0 (solo paid)

Per Miracollo: FREE è più che sufficiente!
```

---

*Documento creato: 14 Gennaio 2026 - Sessione 201*
