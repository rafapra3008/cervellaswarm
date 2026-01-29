# PROMPT RIPRESA - CervellaTrading

> **Ultimo aggiornamento:** 28 Gennaio 2026 - Sessione 322
> **STATUS:** PAPER TRADING LIVE! Passive Mode attivo.

---

## COSA È CERVELLATRADING

Sistema di trading **SEMPRE ATTIVO** con obiettivo **20-25% annuo in SICUREZZA**.

**PRIORITÀ SACRE:**
1. PRIMO: Non perdere soldi
2. SECONDO: Guadagnare soldi
3. TERZO: Machine Learning per ottimizzazione

---

## STATO ATTUALE

```
FASE 0: FONDAMENTA         [####################] 100% COMPLETATA!
FASE 1: BACKTEST SYSTEM    [####################] 100% COMPLETATA!
FASE 2: STRATEGIA BASE     [####################] 100% COMPLETATA!
FASE 3: PAPER TRADING      [###                 ] 15%  <-- LIVE!
```

**MERCATO:** FOREX (EUR/USD)
**BROKER:** IG Markets Demo
**STRATEGIA:** MA 15/50 + RSI filter
**SCHEDULE:** Daily 18:00 CET (launchd)

---

## SESSIONE 322 - Email Notifiche

Vedi `archivio/S322_NOTIFICHE_EMAIL.md` per dettagli.

**Risultato:** 97/97 test PASS, Audit 8.5/10, Paper Trading 4gg OK.

---

## DECISIONI PRESE

| Data | Decisione | Perché |
|------|-----------|--------|
| 28/01/2026 | Notifiche email (non Telegram) | Più semplice, zero dipendenze |
| 28/01/2026 | Aspettare 7gg prima di active mode | Dati OOS servono, Guardiana raccomanda |
| 24/01/2026 | FOREX EUR/USD | Più sicuro, priorità #1 |
| 24/01/2026 | IG Markets Demo | API funzionante gratis |
| 24/01/2026 | MA 15/50 + RSI | Walk-Forward PASS (RR 0.32) |
| 24/01/2026 | Paper Trading 60gg | Validazione OOS obbligatoria |

---

## PROSSIMI STEP (Sessione 323)

```
1. [ ] Configurare email in .env (Gmail App Password)
   - EMAIL_ENABLED=true
   - Testare con: python3 -c "from src.notifications... test_connection()"

2. [ ] Monitorare paper trading fino al 31 Gennaio (7 giorni totali)
   - Verificare log giornalieri
   - Aspettare almeno 1 segnale BUY o SELL

3. [ ] Se 7gg OK → valutare active mode (ordini DEMO)
   - Checklist: 7+ run OK, almeno 1 BUY/SELL, connessione stabile
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

## COMANDI UTILI

```bash
# Verifica job attivo
launchctl list | grep cervellatrading

# Test manuale
python3 scripts/run_paper_trading.py --dry-run

# Check segnali
sqlite3 data/signals.db "SELECT * FROM signals ORDER BY timestamp DESC LIMIT 5;"

# Check log oggi
cat ~/Library/Logs/CervellaTrading/paper_trading_$(date +%Y%m%d).log

# Test connessione email
python3 -c "from src.notifications import EmailNotifier; n = EmailNotifier(); n.test_connection()"
```

---

## NOTA: PAPER TRADING SUL MAC

Il paper trading gira sul Mac di Rafa via launchd.
Il Mac deve essere acceso alle 18:00 CET.
Se spento, il segnale del giorno salta (non critico in passive mode).
In futuro (Fase 4+): spostare su server cloud.

---

## MANTRA

> "Prima NON PERDERE. Poi guadagnare." | "Ultrapassar os próprios limites!"

---

*Cervella & Rafa - Sessione 322 - Notifiche Email IMPLEMENTATE!*
