# BIBLIOTECA COMUNE - Risorse Condivisibili tra Progetti

> **Data Studio:** 1 Gennaio 2026
> **Studiato da:** Cervella (senza toccare nulla!)
> **Progetto:** CervellaSwarm - FASE 12 Proposta

---

## TL;DR - Cosa Abbiamo Scoperto

La **Contabilita Antigravity** e un CAPOLAVORO! Ha risorse mature, testate, production-ready che possiamo riutilizzare in TUTTI i nostri progetti.

**REGOLA D'ORO:** Mai fare copia-incolla! Ogni progetto mantiene i suoi file, ma usiamo gli STESSI PATTERN e STESSI STANDARD.

---

## RISORSE RIUTILIZZABILI

### 1. TELEGRAM BOT (GIA CONDIVISO!)

| Aspetto | Dettaglio |
|---------|-----------|
| **File Origine** | `ContabilitaAntigravity/backend/telegram_notifier.py` |
| **Versione** | v1.6.0 (715 righe) |
| **Libreria** | `httpx` async |
| **Riutilizzabile** | SI - Stesso TOKEN funziona ovunque! |

**Come Riutilizzare:**
```bash
# STESSO bot, STESSE credenziali, PROGETTI DIVERSI
TELEGRAM_BOT_TOKEN="..." # Uno solo per tutti
TELEGRAM_CHAT_ID="..."   # Uno solo per tutti
```

**Pattern da Copiare:**
- Async con httpx (non requests bloccante!)
- Retry con backoff esponenziale
- Message formatting con Markdown
- Silent option per notifiche non urgenti

---

### 2. FORTEZZA MODE - Deploy Sicuro

| Aspetto | Dettaglio |
|---------|-----------|
| **File Origine** | `REGOLE_GLOBALI/FORTEZZA_MODE.md` |
| **Script** | `ContabilitaAntigravity/scripts/deploy.sh` v4.3.0 |
| **Righe** | 492 (lo script piu completo!) |
| **Riutilizzabile** | SI - Adattare path e configurazioni |

**I 12 Principi (da ADOTTARE OVUNQUE):**

| # | Principio | Descrizione |
|---|-----------|-------------|
| 0 | Test Locale | Hai testato PRIMA? |
| 1 | File Esiste | Verifica file locale |
| 2 | Connessione | VM raggiungibile? |
| 3 | Health PRE | API funziona PRIMA? |
| 4 | Versione | Locale > Remota? |
| 5 | Backup | Copia prima di sovrascrivere |
| 6 | Upload | SCP sicuro |
| 7 | MD5 | Verifica integrita |
| 8 | Riavvio | Restart servizio |
| 9 | Health POST | API funziona DOPO? |
| 10 | Log | Deploy history |
| 11 | Notifica | Telegram alert |
| 12 | Rollback | AUTO se health fallisce! |

**Feature Avanzate (v4.3.0):**
- Cache busting automatico per JS/CSS
- Check dipendenze Python automatico
- Retry con backoff esponenziale (1s, 2s, 4s, 8s, 16s)
- Check spazio disco VM

---

### 3. ROLLBACK AUTOMATICO

| Aspetto | Dettaglio |
|---------|-----------|
| **File Origine** | `ContabilitaAntigravity/scripts/rollback.sh` |
| **Versione** | v1.0.0 (151 righe) |
| **Riutilizzabile** | SI |

**Funzionalita:**
- Lista backup disponibili (`--list`)
- Trova ultimo backup automaticamente
- Conferma prima di procedere
- Health check post-rollback
- Log operazione

---

### 4. LOGGING STRUTTURATO

| Aspetto | Dettaglio |
|---------|-----------|
| **File Origine** | `ContabilitaAntigravity/backend/logger_config.py` |
| **Versione** | v1.0.0 (213 righe) |
| **Riutilizzabile** | SI - Pattern universale |

**Feature:**
- JSON format opzionale (per ELK stack)
- File rotation automatico (10MB max, 5 backup)
- Log errori separato
- Context injection (portal, user_id, request_id)
- Configurazione via environment

**Pattern da Copiare:**
```python
from logger_config import get_logger, log_with_context

logger = get_logger(__name__)
log_with_context(logger, logging.INFO, "Messaggio",
                 user_id="123", request_id="abc")
```

---

### 5. SCRIPT UTILITY

| Script | Funzione | Righe | Riutilizzabile |
|--------|----------|-------|----------------|
| `check_sync.sh` | Verifica file locale = VM | ~50 | SI |
| `check_deps.sh` | Verifica dipendenze Python | ~30 | SI |
| `pre-deploy-check.sh` | Check pre-deploy | ~40 | SI |
| `verifica_post_deploy.sh` | Verifica post-deploy | ~60 | SI |

---

## PATTERN DA STANDARDIZZARE

### 1. Struttura Script Deploy

```bash
#!/bin/bash
# Versione: X.Y.Z
# Data: YYYY-MM-DD
# Uso: ./scripts/deploy.sh <file>

set -e  # Esci su errore

# Colori standard
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configurazione progetto-specifica
SSH_KEY="$HOME/.ssh/..."
VM_HOST="..."
VM_BASE="..."
```

### 2. Struttura Python con Versioning

```python
"""
Descrizione modulo
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

# imports...
```

### 3. Health Check Pattern

```bash
# Health check con retry
MAX_RETRIES=5
RETRY=0
while [ $RETRY -lt $MAX_RETRIES ]; do
    WAIT_TIME=$((2 ** $RETRY))  # Backoff esponenziale
    sleep $WAIT_TIME

    STATUS=$(curl -s -o /dev/null -w '%{http_code}' URL)
    if [ "$STATUS" == "200" ]; then
        break
    fi
    ((RETRY++))
done
```

---

## COSA NON CONDIVIDERE (MAI!)

| Cosa | Perche |
|------|--------|
| Database | Ogni progetto ha i suoi dati |
| Credenziali | Ogni progetto ha i suoi segreti |
| Business Logic | Specifico per dominio |
| UI/Frontend | Design specifico |
| API Endpoints | Routing specifico |

---

## PROPOSTA: FASE 12 - Standard e Biblioteca

### Obiettivo

Creare un sistema di **STANDARD CONDIVISI** che ogni progetto adotta, senza dipendenze circolari.

### Cosa Creare

1. **Template deploy.sh** - Adattabile per ogni progetto
2. **Template logger_config.py** - Pattern logging standard
3. **Checklist FORTEZZA MODE** - Da seguire SEMPRE
4. **Notifiche Telegram** - Un bot, tanti progetti

### Come Funzionerebbe

```
REGOLE_GLOBALI/
├── FORTEZZA_MODE.md          # 12 principi (GIA ESISTE!)
├── COSTITUZIONE_GLOBALE.md   # Regole (GIA ESISTE!)
└── templates/                # NUOVO!
    ├── deploy_template.sh
    ├── rollback_template.sh
    └── logger_template.py

Ogni Progetto/
├── scripts/
│   └── deploy.sh            # Copia ADATTATA del template
└── backend/
    └── logger_config.py     # Copia ADATTATA del template
```

### Vantaggi

1. **Consistenza** - Tutti i progetti deployano allo stesso modo
2. **Sicurezza** - FORTEZZA MODE ovunque
3. **Manutenzione** - Un fix nel template, aggiornamento ovunque
4. **Onboarding** - Nuovo progetto? Copia template!

---

## RIEPILOGO RISORSE MAPPATE

| Risorsa | Origine | Righe | Status |
|---------|---------|-------|--------|
| Telegram Bot | Contabilita | 715 | Production |
| FORTEZZA MODE | REGOLE_GLOBALI | 304 | Production |
| deploy.sh | Contabilita | 492 | Production |
| rollback.sh | Contabilita | 151 | Production |
| logger_config.py | Contabilita | 213 | Production |
| Utility scripts | Contabilita | ~180 | Production |

**TOTALE:** ~2,055 righe di codice RIUTILIZZABILE!

---

## PROSSIMI STEP

1. [ ] Proporre FASE 12 nella ROADMAP_SACRA
2. [ ] Creare directory `templates/` in REGOLE_GLOBALI
3. [ ] Estrarre template da Contabilita
4. [ ] Applicare a Miracollo come primo test
5. [ ] Documentare processo in GUIDA_STANDARD.md

---

*"Non reinventare la ruota - usa quella che gia gira!"*

*Studio completato senza toccare NULLA nei progetti originali*

