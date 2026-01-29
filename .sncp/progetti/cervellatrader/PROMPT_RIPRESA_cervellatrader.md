# PROMPT_RIPRESA - CervellaTrader

> Ultimo aggiornamento: 2026-01-28 (Checkpoint Fase 2 parziale)

---

## STATO ATTUALE

| Aspetto | Status |
|---------|--------|
| **Fase** | 2 - Multi-Asset + Sentiment (60% completata) |
| **Workspace** | `~/Developer/CervellaTrader/` |
| **Git** | 4 commit, no remote |
| **Codice** | ~3500 righe |
| **Test** | 54/54 PASS |

---

## HANDOFF - COSA SA LA PROSSIMA CERVELLA

### Il Progetto
CervellaTrader e un trading bot autonomo con **Self-Learning Loop**. Non segue regole fisse - EVOLVE imparando dai propri trade.

### Cosa Funziona ORA

```bash
cd ~/Developer/CervellaTrader

# Comandi Fase 1 (single asset)
python3 -m src.main signal     # Segnali BTC
python3 -m src.main scan       # Scan + decisione
python3 -m src.main bot        # Bot automatico

# Comandi Fase 2 (NUOVI!)
python3 -m src.main scan-all   # Scansiona BTC + ETH + SOL ranked
python3 -m src.main sentiment  # Fear & Greed Index
python3 -m src.main limits     # Mostra tutti i limiti + asset config
```

### File Chiave (Fase 2)

| File | Cosa Fa |
|------|---------|
| [src/decision/signal_aggregator.py](src/decision/signal_aggregator.py) | Ranking multi-asset |
| [src/data/sentiment.py](src/data/sentiment.py) | Fear & Greed Index API |
| [src/config.py](src/config.py) | AssetConfig + PortfolioLimits |

---

## COSA MANCA (Fase 2 - rimanente)

```
[X] Multi-asset support (BTC, ETH, SOL)
[X] Sentiment analysis (Fear & Greed)
[ ] News feed integration       <-- PROSSIMO
[ ] Learning extraction (LLM)
[ ] Salience tracking automatico
```

---

## DECISIONI PRESE (PERCHE)

| Decisione | Perche |
|-----------|--------|
| 70/20/10 BTC/ETH/SOL allocation | Ricerca VanEck/CoinShares |
| Correlation penalty | BTC-ETH 0.75, SOL 0.55 - evita over-exposure |
| Fear & Greed contrarian | Extreme Fear = BUY, Extreme Greed = SELL |
| Thread-safe cache | Scheduler usa threading |
| Sequential execution | No parallel trades (risk management) |

---

## PORTFOLIO LIMITS (FASE 2)

```python
MAX_TOTAL_EXPOSURE = 0.30        # 30% max
MAX_CORRELATED_EXPOSURE = 0.25   # BTC+ETH max
MAX_SIMULTANEOUS_POSITIONS = 2
MAX_RISK_PER_TRADE = 0.02        # 2%
MAX_DRAWDOWN_PCT = 0.20          # 20%
```

---

## COME CONTINUARE

```
INIZIA SESSIONE -> CervellaTrader

"Continuiamo con News Feed Integration"
```

### Quick Check

```bash
cd ~/Developer/CervellaTrader
python3 -m pytest tests/ -v      # Deve essere 54/54 PASS
python3 -m src.main scan-all     # Deve scansionare 3 asset
python3 -m src.main sentiment    # Deve mostrare Fear & Greed
```

---

## DOCUMENTI DA LEGGERE

| Doc | Quando |
|-----|--------|
| [NORD.md](NORD.md) | Overview progetto |
| [docs/RESEARCH_MULTI_ASSET.md](docs/RESEARCH_MULTI_ASSET.md) | Ricerca multi-asset (800+ righe) |
| [docs/AUDIT_MULTI_ASSET.md](docs/AUDIT_MULTI_ASSET.md) | Audit Guardiana |
| [docs/AUDIT_SENTIMENT.md](docs/AUDIT_SENTIMENT.md) | Audit Guardiana |

---

*"Un trading bot che impara dai propri errori, non li ripete."*

*Checkpoint: 2026-01-28 - Fase 2 parziale (Multi-Asset + Sentiment)*
*Team: Cervella & Rafa*
