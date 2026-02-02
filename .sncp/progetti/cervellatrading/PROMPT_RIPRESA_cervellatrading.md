# PROMPT RIPRESA - CervellaTrading

> **Aggiornamento:** 2 Feb 2026 (consolidato da 120 → 78 righe)
> **STATUS:** PAPER TRADING LIVE - Passive Mode (Fase 3: 15%)

---

## COSA È

Sistema trading **20-25% annuo** con priorità: 1) Non perdere 2) Guadagnare 3) ML ottimizzazione

**SETUP ATTUALE:**
- Mercato: FOREX EUR/USD
- Broker: IG Markets Demo
- Strategia: MA 15/50 + RSI filter (Walk-Forward RR 0.32)
- Schedule: Daily 18:00 CET via launchd (Mac Rafa)

---

## STATO

```
FASE 0-2: FONDAMENTA + BACKTEST + STRATEGIA  [100%] ✅
FASE 3: PAPER TRADING                        [15%]  🔄 LIVE
```

**Sessione 322 (28 Gen):** Email notifiche implementate. Test 97/97 PASS, Audit 8.5/10, 4gg paper trading OK.

---

## DECISIONI ATTIVE

| Cosa | Perché |
|------|--------|
| Email notifiche (no Telegram) | Semplice, zero dipendenze |
| Aspettare 7gg prima active mode | Dati OOS necessari, raccomandazione Guardiana |
| FOREX EUR/USD | Priorità sicurezza |
| Paper Trading 60gg | Validazione OOS obbligatoria |

**Archivio:** `archivio/S322_NOTIFICHE_EMAIL.md`

---

## PROSSIMI STEP

```
1. [ ] Configurare email in .env
   - EMAIL_ENABLED=true
   - Gmail App Password
   - Test: python3 -c "from src.notifications import EmailNotifier; n = EmailNotifier(); n.test_connection()"

2. [ ] Monitorare paper trading fino 31 Gen (7gg totali)
   - Log giornalieri
   - Aspettare almeno 1 segnale BUY/SELL

3. [ ] Se 7gg OK → valutare active mode (ordini DEMO)
   - Checklist: 7+ run OK, 1+ BUY/SELL, connessione stabile
```

---

## FILE CHIAVE

| File | Cosa |
|------|------|
| `src/notifications/email_notifier.py` | Notifiche BUY/SELL |
| `src/strategies/ma_crossover.py` | Strategia MA 15/50 |
| `scripts/run_paper_trading.py` | Main runner |
| `data/signals.db` | Segnali paper trading |

---

## COMANDI

```bash
# Status job
launchctl list | grep cervellatrading

# Test manuale
python3 scripts/run_paper_trading.py --dry-run

# Segnali recenti
sqlite3 data/signals.db "SELECT * FROM signals ORDER BY timestamp DESC LIMIT 5;"

# Log oggi
cat ~/Library/Logs/CervellaTrading/paper_trading_$(date +%Y%m%d).log

# Test email
python3 -c "from src.notifications import EmailNotifier; n = EmailNotifier(); n.test_connection()"
```

---

## NOTE

- Paper trading gira su Mac (launchd). Mac deve essere acceso 18:00 CET.
- Se spento: segnale salta (non critico in passive mode)
- Fase 4+: migrazione server cloud

**Mantra:** *"Prima NON PERDERE. Poi guadagnare."*

---

*Archivio 120 righe → `archivio/2026-02/PROMPT_RIPRESA_cervellatrading_20260202.md`*
