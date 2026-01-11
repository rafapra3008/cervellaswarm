# VISIONE STRATEGICA - CervellaSwarm

> **Data:** 11 Gennaio 2026
> **Sessione:** 164
> **Autore:** Guardiana Qualita + Regina

---

## LE DUE ANIME DI CERVELLASWARM

CervellaSwarm ha evoluto in due direzioni parallele:

### ANIMA 1: Configurazione di Lavoro (USO INTERNO)

```
STATO: ATTIVA - Usiamo ogni giorno!

- 16 agenti specializzati (~/.claude/agents/)
- Script spawn-workers per orchestrazione
- SNCP come memoria esterna
- Hooks per automazione
```

**Questo FUNZIONA e lo usiamo quotidianamente.**

### ANIMA 2: Prodotto da Vendere (IN PAUSA)

```
STATO: IN PAUSA (decisione 9 Gennaio)

- CLI installabile per altri sviluppatori
- Web Dashboard per team
- Pricing: BYOK Free -> $19 -> $39
- Landing page pronta
```

**Prima COSTRUIRE, poi VENDERE.**

---

## FOCUS ATTUALE: Cervella AI (Indipendenza)

Dal 10 Gennaio il focus e' su Cervella AI:

```
OBIETTIVO: Non dipendere da Claude API
COME: GPU propria + modello open source

STATO:
  FASE 1: Ricerca               [####################] 100%
  FASE 2: Infrastruttura GPU    [####################] 100%
  FASE 3: Integrazione MVP      [####................] 20%
    - Sprint 3.1: Backend API   DONE! (11 Gen)
    - Sprint 3.2: Qdrant        DA FARE
    - Sprint 3.3: RAG Pipeline  DA FARE
    - Sprint 3.4: Costituzione  DA FARE
    - Sprint 3.5: UI Chat       DA FARE
```

---

## PROSSIMI PASSI CONCRETI

### Sessione 165+ (Lunedi, GPU si accende)

1. **Verificare schedule GPU** - Si accende alle 9:00 Italia?
2. **Test API AI** - /api/ai/health funziona?
3. **Sprint 3.2: Setup Qdrant**
   - Installare Qdrant su cervella-gpu
   - Test embedding con Ollama
   - Indicizzazione base

### Sprint 3.3: RAG Pipeline

1. Chunking documenti (SNCP, codice, docs)
2. Embedding e indicizzazione
3. Retrieval semantico
4. Integration con chat

### Sprint 3.4: Costituzione

1. System prompt con valori Cervella
2. Personalita riconoscibile
3. Test "Chi sei?"

### Sprint 3.5: UI Chat Base

1. Interfaccia chat in Miracollo
2. Connessione a API AI
3. Test end-to-end

---

## DECISIONI CHIAVE ATTIVE

| Decisione | Data | Perche |
|-----------|------|--------|
| Prodotto in pausa | 9 Gen | Prima costruire, poi vendere |
| GPU propria | 10 Gen | Indipendenza totale |
| qwen3:4b | 10 Gen | Bilanciamento qualita/costo |
| Schedule GPU | 10 Gen | Risparmio 50% |
| SNCP Guardian | 11 Gen | Zero manutenzione SNCP |

---

## INFRASTRUTTURA

```
cervella-gpu (us-west1-b):
  - n1-standard-4 + Tesla T4 (16GB VRAM)
  - Ollama + qwen3:4b
  - IP: 10.138.0.3:11434
  - Schedule: Lun-Ven 9:00-19:00 Italia
  - Costo: ~$85/mese

miracollo-cervella (us-central1-b):
  - Backend FastAPI + AI API
  - IP: 34.27.179.164
  - Container: miracollo-backend-35
```

---

## RISCHI

| Rischio | Probabilita | Mitigazione |
|---------|-------------|-------------|
| GPU schedule non funziona | Bassa | Test lunedi, monitor |
| qwen3 qualita insufficiente | Media | Test task reali, upgrade modello |
| RAG complessita | Media | MVP semplice prima |

---

## FILOSOFIA

```
"Prima COSTRUIRE, poi VENDERE"
"L'obiettivo e' essere INDIPENDENTI"
"Fatto BENE > Fatto VELOCE"
"Ultrapassar os proprios limites!"
```

---

*Validato: Sessione 164 - 11 Gennaio 2026*
