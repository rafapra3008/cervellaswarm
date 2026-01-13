# ROADMAP MASTER: RateBoard Diamante

> **Aggiornata:** 13 Gennaio 2026 - Sessione 186 (Post-Audit)
> **Score Attuale:** 8.5/10
> **Target:** 9.5/10

---

## LA VISIONE

```
+================================================================+
|                                                                |
|   RATEBOARD DIAMANTE =                                         |
|                                                                |
|   Native PMS Integration (zero pain)           ✅ FATTO        |
|   + Transparent AI (zero trust issues)         ✅ FATTO        |
|   + Learning AI (impara da TE)                 ✅ FATTO        |
|   + SMB Pricing (zero barriers)                ✅ FATTO        |
|   + Competitor Intelligence (real-time)        ❌ DA FARE      |
|   + Bot Assistant (zero friction)              📋 PIANIFICATO  |
|                                                                |
|   = Primo RMS nel CUORE degli Independent Hotels!              |
|                                                                |
+================================================================+
```

---

## PRIORITA POST-AUDIT (13 Gennaio 2026)

### CRITICO - Q1 2026

| # | Cosa | Effort | Status | Note |
|---|------|--------|--------|------|
| 1 | **Competitor Scraping** | 40-60h | DA FARE | Tutti i competitor lo hanno! |
| 2 | **Test Autopilot Staging** | 8-10h | DA FARE | Codice pronto, mai testato |
| 3 | **Bulk Edit Preview/Undo** | 10h | DA FARE | Safety per utenti |
| 4 | **Split file grossi** | 7h | DA FARE | Tech debt critico |

### ALTO - Q2 2026

| # | Cosa | Effort | Status | Note |
|---|------|--------|--------|------|
| 5 | ML AI Suggestions | 75-95h | SUBROADMAP | Vedere SUBROADMAP_ML |
| 6 | Eventi Esterni API | 30-40h | PIANIFICATO | Concerti, festivita |
| 7 | Alert Competitor | 15-20h | PIANIFICATO | Push quando cambiano |

### MEDIO - Q3/Q4 2026

| # | Cosa | Effort | Status | Note |
|---|------|--------|--------|------|
| 8 | Bot Telegram MVP | 20-30h | PIANIFICATO | Revenue + Chef |
| 9 | Bot WhatsApp | 20-30h | PIANIFICATO | Dopo Telegram |
| 10 | Weather Integration | 10-20h | IDEA | Marketing story |

---

## DOCUMENTI COLLEGATI

| Documento | Cosa Contiene | Path |
|-----------|---------------|------|
| **Audit Completo** | Risultati audit 13 Gen | `reports/20260113_AUDIT_RATEBOARD_COMPLETO.md` |
| **Subroadmap ML** | Piano ML graduale | `roadmaps/SUBROADMAP_ML_AI_SUGGESTIONS.md` |
| **Visione Bot** | Use cases tutti reparti | `idee/20260113_VISIONE_BOT_HOTEL.md` |
| **Ricerca Competitor** | 1640+ righe analisi | `idee/20260113_RICERCA_COMPETITOR_RMS_*.md` |
| **Roadmap Revenue 7-10** | Dettaglio tecnico | `roadmaps/20260112_ROADMAP_REVENUE_7_TO_10.md` |

---

## FEATURES STATUS

### FUNZIONANTI (non toccare!)

| Feature | % | File Principali |
|---------|---|-----------------|
| Heatmap Prezzi | 100% | rateboard-render.js |
| What-If Simulator | 100% | what-if.js, what-if.html |
| Learning Analytics | 100% | learning-dashboard.js |
| YoY Comparison | 90% | rateboard-analytics.py |
| Transparent AI | 80% | rateboard-ai.js |
| AI Suggestions | 85% | rateboard-ai.js (rule-based) |

### DA MIGLIORARE

| Feature | % | Cosa Manca |
|---------|---|------------|
| Bulk Edit | 70% | Preview + Undo |
| Competitor | 60% | Scraping automatico |
| Autopilot | 90% | Test produzione |

---

## TECH DEBT DA RISOLVERE

| File | Righe | Azione | Effort |
|------|-------|--------|--------|
| rateboard.css | 2,426 | Split in 4 file | 2h |
| rateboard-ai.js | 839 | Split in 3 file | 3h |
| autopilot.py | 679 | Estrai in services | 2h |

---

## PROSSIMI STEP CONCRETI

### QUESTA SETTIMANA

1. [ ] **POC Competitor Scraping** - Booking.com test
2. [ ] **Test Autopilot** - Staging con dati reali
3. [ ] **Split rateboard.css** - Tech debt

### PROSSIMO SPRINT

1. [ ] Competitor Scraping MVP completo
2. [ ] Bulk Edit preview
3. [ ] Alert competitor via email

### MESE PROSSIMO

1. [ ] Integrare competitor in AI Suggestions
2. [ ] Iniziare ML-0 (ricerca)
3. [ ] Documentare Autopilot per utenti

---

## VANTAGGI UNICI (da proteggere!)

```
1. NATIVE PMS
   - Solo noi abbiamo dati real-time dal PMS
   - Zero integration pain
   - Setup in minuti, non giorni

2. LEARNING AI
   - Impara dalle decisioni dell'utente
   - FASE 3 completata e funzionante
   - NESSUN competitor lo ha

3. TRANSPARENT AI
   - Mostra PERCHE suggerisce
   - Confidence breakdown
   - Come TakeUp ($11M funding!)

4. SMB-FIRST
   - Pricing accessibile
   - UX semplice
   - Non enterprise castoff
```

---

## GAP VS COMPETITOR (da colmare)

```
+================================================================+
|                                                                |
|   GAP CRITICO: COMPETITOR RATE SHOPPING                        |
|                                                                |
|   IDeaS: ✅ Real-time scraping                                 |
|   Duetto: ✅ Real-time scraping                                |
|   Atomize: ✅ Real-time scraping                               |
|   TakeUp: ✅ Real-time scraping                                |
|   RoomPriceGenie: ✅ Rate shopping                             |
|                                                                |
|   MIRACOLLO: ❌ Dati manuali!                                   |
|                                                                |
|   AZIONE: Priorita #1 per Q1 2026                              |
|                                                                |
+================================================================+
```

---

## OPPORTUNITA MOONSHOT

| Opportunita | Chi Lo Fa | Priorita |
|-------------|-----------|----------|
| Bot Revenue WhatsApp/Telegram | NESSUNO | Q3 2026 |
| Bot Chef (mezza pensione?) | NESSUNO | Q3 2026 |
| Weather Integration | NESSUNO | Q4 2026 |
| AI Planning | NESSUNO | 2027 |

---

## PRINCIPI GUIDA

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"
"Fatto BENE > Fatto VELOCE"
"Una cosa alla volta! Finischi! Fai prova!"
"Non esistono cose difficili, esistono cose non studiate!"
```

---

*Roadmap Master aggiornata post-audit*
*Cervella Regina - 13 Gennaio 2026*
