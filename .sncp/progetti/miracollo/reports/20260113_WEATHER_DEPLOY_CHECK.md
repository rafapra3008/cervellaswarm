# Weather API Deploy Check

**Data:** 2026-01-13
**Verificato da:** Cervella Guardiana Ops
**Stato:** ANALISI COMPLETATA

---

## Verdetto

**OK** - Configurazione pronta, manca solo aggiungere la variabile in produzione.

---

## 1. Come Funziona il Deploy di Miracollo

### Architettura

- **VM:** miracollo-cervella (34.27.179.164)
- **Container:** Docker con Nginx reverse proxy
- **Deploy script:** `scripts/deploy_vm.sh` (FORTEZZA MODE v4.1.0)

### Flusso Deploy

1. Il file `.env.production` (locale) contiene le variabili
2. Lo script `deploy_vm.sh` copia `.env.production` come `.env` sulla VM
3. Docker container carica le variabili da `.env`
4. Pydantic Settings legge le variabili in `backend/core/config.py`

### File Coinvolti

| File | Scopo |
|------|-------|
| `.env.production` | Variabili produzione (LOCALE, non committato) |
| `docker-compose.yml` | Definisce env_file: .env |
| `backend/core/config.py` | Settings class con WEATHER_API_KEY |

---

## 2. Stato Attuale WEATHER_API_KEY

### Nel Codice (config.py)

```python
# Weather API (Sessione 188 - External Data Integration)
WEATHER_API_KEY: str = ""  # WeatherAPI.com API key
WEATHER_CACHE_TTL: int = 21600  # 6 hours
WEATHER_DEFAULT_LOCATION: str = "46.5369,12.1389"  # Naturae Lodge
```

**Check weather_enabled:**
```python
@property
def weather_enabled(self) -> bool:
    return bool(self.WEATHER_API_KEY and len(self.WEATHER_API_KEY) > 10)
```

### Nel .env.example

**MANCA!** Il file `.env.example` NON contiene la sezione Weather API.

### Nel docker-compose.yml

Usa `env_file: .env` quindi le variabili vengono passate automaticamente.

---

## 3. Azioni Richieste per Abilitare Weather in Produzione

### Passo 1: Aggiornare .env.example (Best Practice)

Aggiungere al file `.env.example`:

```env
# ============================================
# WEATHER API (Sessione 188)
# ============================================
# WeatherAPI.com API key for weather data integration
# Get your free key: https://www.weatherapi.com/
# Free tier: 1,000,000 calls/month
WEATHER_API_KEY=your-weather-api-key-here
WEATHER_CACHE_TTL=21600
WEATHER_DEFAULT_LOCATION=46.5369,12.1389
```

### Passo 2: Aggiungere a .env.production (LOCALE)

Nel file `.env.production` (che NON e committato su git), aggiungere:

```env
# Weather API
WEATHER_API_KEY=c5add656caef48288d1164756261301
WEATHER_CACHE_TTL=21600
WEATHER_DEFAULT_LOCATION=46.5369,12.1389
```

### Passo 3: Deploy

Eseguire il deploy standard:

```bash
./scripts/deploy_vm.sh
```

Lo script copiera `.env.production` sulla VM come `.env`.

### Passo 4: Verifica

Dopo il deploy, verificare:

```bash
curl https://miracollo.com/api/weather/current
```

Dovrebbe restituire i dati meteo invece di errore 503.

---

## 4. Checklist Sicurezza

| Check | Stato |
|-------|-------|
| API key non in codice | OK - Usa env var |
| API key non in git | OK - .env.production in .gitignore |
| Fallback graceful | OK - weather_enabled property |
| Cache implementato | OK - WEATHER_CACHE_TTL |
| Rate limiting | OK - Free tier ha 1M calls/month |

---

## 5. Note

- La API key fornita (`c5add656caef48288d1164756261301`) e valida per WeatherAPI.com
- Free tier: 1,000,000 calls/month (piu che sufficiente con cache di 6 ore)
- Il servizio degrada gracefully: se la key manca, il frontend non mostra il widget meteo

---

## Riepilogo

**Cosa fare:**

1. Aggiungere `WEATHER_API_KEY=c5add656caef48288d1164756261301` a `.env.production`
2. (Opzionale) Aggiornare `.env.example` per documentazione
3. Eseguire `./scripts/deploy_vm.sh`

**Tempo stimato:** 5 minuti

---

*Cervella Guardiana Ops*
*"La sicurezza e sacra. La qualita e sacra."*
