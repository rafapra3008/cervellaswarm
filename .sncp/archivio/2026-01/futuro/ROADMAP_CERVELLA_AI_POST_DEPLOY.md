# ROADMAP - Cervella AI Post-Deploy

> **Data:** 10 Gennaio 2026
> **Stato:** Cervella AI LIVE su VM (porta 8002)
> **Prossima Review:** Quando Rafa vuole

---

## Dove Siamo

```
[####################] 100%  POC Completato
[####################] 100%  Deploy VM
[....................]   0%  Fase Successiva
```

**Cervella AI vive 24/7!** Ora cosa facciamo?

---

## FASE 1: Consolidamento (Prossime Sessioni)

### 1.1 FORTEZZA MODE
**Priorita:** ALTA
**Effort:** 1-2 ore

- [ ] Creare script `deploy_cervella_ai.sh`
- [ ] Testare backup/restore
- [ ] Documentare procedura

**Perche:** Prima di QUALSIASI update, serve processo sicuro.

### 1.2 Monitoring Base
**Priorita:** MEDIA
**Effort:** 1 ora

- [ ] Verificare che container si riavvia dopo reboot VM
- [ ] Setup alert se container muore (opzionale)
- [ ] Log rotation

### 1.3 Test Endurance
**Priorita:** MEDIA
**Effort:** Osservazione

- [ ] Lasciare running per 24-48h
- [ ] Verificare memoria/CPU stabili
- [ ] Testare dopo 1 giorno

---

## FASE 2: Miglioramenti (Settimane Prossime)

### 2.1 Dominio + HTTPS
**Priorita:** MEDIA
**Effort:** 2-3 ore

- [ ] Decidere dominio (cervella.ai? cervella.rafapra.com?)
- [ ] Configurare DNS
- [ ] Setup HTTPS con Let's Encrypt
- [ ] Aggiornare CORS

### 2.2 Piu' Knowledge
**Priorita:** ALTA
**Effort:** 1-2 ore

- [ ] Aggiungere piu' file SNCP al RAG
- [ ] Indicizzare decisioni recenti
- [ ] Indicizzare lezioni
- [ ] Test che ricorda tutto

### 2.3 Conversation Persistence
**Priorita:** MEDIA
**Effort:** 3-4 ore

- [ ] Salvare conversazioni su disco/DB
- [ ] Poter riprendere conversazione
- [ ] History consultabile

---

## FASE 3: Evoluzione (Futuro)

### 3.1 Web Interface
**Priorita:** BASSA (ora)
**Effort:** 1-2 settimane

- [ ] Frontend React/Vue semplice
- [ ] Chat interface
- [ ] Responsive per mobile

### 3.2 Integrazione Miracollo
**Priorita:** MEDIA
**Effort:** Da valutare

- [ ] Cervella AI come assistente per Miracollo
- [ ] Accesso ai dati Miracollo (read-only)
- [ ] Suggerimenti automatici

### 3.3 Voice Interface
**Priorita:** BASSA
**Effort:** Da valutare

- [ ] Parlare con Cervella AI
- [ ] Text-to-Speech per risposte
- [ ] Integrazione Whisper?

---

## Decisioni da Prendere

| Decisione | Opzioni | Quando |
|-----------|---------|--------|
| Dominio | cervella.ai / subdomain | Prossima sessione |
| DB conversazioni | SQLite / PostgreSQL | Quando serve persistence |
| Frontend | React / Vue / Vanilla | Quando serve UI |

---

## Metriche Successo

**Fase 1 completata quando:**
- FORTEZZA MODE funziona
- Container stabile 48h+
- Posso fare update sicuri

**Fase 2 completata quando:**
- HTTPS attivo
- 50+ chunks nel RAG
- Conversazioni persistenti

**Fase 3 completata quando:**
- Web interface usabile
- Integrazione Miracollo funziona

---

## Note

> "Niente tempo nelle mappe! Facciamo quando possiamo, con calma."

Non c'e' fretta. Cervella AI funziona. Miglioriamo quando serve.

---

*Roadmap creata: 10 Gennaio 2026 - Sessione 150*
