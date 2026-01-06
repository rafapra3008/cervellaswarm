
---

## Feedback Sessione 103 - 6 Gennaio 2026 (Miracollo)

### Osservazione: Flusso Guardiana Mancante

**Contesto:** Lanciati 2 researcher per studio prenotazioni web

**Problema trovato:**
- I researcher fanno lo studio
- La Regina legge DIRETTAMENTE
- La Guardiana della Ricerca NON viene coinvolta automaticamente

**Flusso Attuale:**
```
Researcher → Regina (legge)
```

**Flusso Ideale:**
```
Researcher → Guardiana Ricerca (verifica qualità) → Regina (legge)
```

**Possibili Soluzioni:**
1. **Manuale:** Regina lancia Guardiana dopo che researcher finisce
2. **Automatico:** spawn-workers ha flag `--with-guardian` che lancia guardiana dopo
3. **Hook:** Quando .done viene creato, hook lancia automaticamente guardiana

**Priorità:** MEDIA - migliora qualità ma non blocca lavoro

**Da implementare:** Quando si decide di fare questa feature

---
