# MAPPA APP VERA - CervellaSwarm

> **Data:** 9 Gennaio 2026
> **Decisione:** App vera, non plugin. Controllo totale.
> **Motto:** "Quando troviamo il PERCHE, NULLA ci ferma!"

---

## LA VISIONE

```
+==================================================================+
|                                                                  |
|   CervellaSwarm = AI TEAM per Developer Professionali            |
|                                                                  |
|   NON un plugin dipendente da altri                              |
|   NON un wrapper semplice                                        |
|                                                                  |
|   UN PRODOTTO VERO con:                                          |
|   - Controllo totale                                             |
|   - Valore unico                                                 |
|   - Indipendenza                                                 |
|                                                                  |
+==================================================================+
```

---

## COSA ABBIAMO GIA

| Asset | Descrizione | Valore |
|-------|-------------|--------|
| 16 Agenti | Specializzati, testati | ALTO |
| SNCP | Sistema memoria esterna | TRADE SECRET |
| DNA Famiglia | Cultura, filosofia | DIFFERENZIATORE |
| Esperienza | Mesi di uso reale | KNOW-HOW |

---

## OPZIONI ARCHITETTURA

### Opzione A: CLI Propria

```
cervellaswarm init          # Setup progetto
cervellaswarm task "..."    # Delega task
cervellaswarm status        # Stato agenti
cervellaswarm checkpoint    # Salva stato
```

**Pro:**
- Veloce da sviluppare
- Developer-friendly
- Simile a come lavoriamo ora

**Contro:**
- Meno accessibile a non-dev
- Difficile monetizzare CLI

---

### Opzione B: Web App

```
Dashboard web:
- Gestione progetti
- Visualizza agenti
- Task management
- Analytics
```

**Pro:**
- Accessibile a tutti
- Monetizzazione chiara (SaaS)
- Scalabile

**Contro:**
- Più complesso da sviluppare
- Richiede infrastruttura

---

### Opzione C: Hybrid (CLI + Web)

```
CLI per developer     →  Uso quotidiano
Web Dashboard        →  Gestione, analytics
API                  →  Integrazioni
```

**Pro:**
- Best of both worlds
- Developer usano CLI
- Manager usano Web
- API per integrazioni

**Contro:**
- Più lavoro iniziale

---

### Opzione D: VS Code Extension

```
Estensione VS Code con:
- Panel agenti
- Command palette
- Inline suggestions
```

**Pro:**
- Dove i dev già lavorano
- Marketplace distribution
- Familiar UX

**Contro:**
- Dipendenza da VS Code
- Meno controllo che fork

---

## LA MIA RACCOMANDAZIONE

**Opzione C: Hybrid** - Ma in fasi.

```
FASE 1: CLI Solida (MVP)
├── Funziona standalone
├── Usa Claude API direttamente
├── SNCP integrato
└── 16 agenti pronti

FASE 2: Web Dashboard
├── Gestione progetti
├── Analytics uso
├── Team management
└── Billing

FASE 3: Integrazioni
├── VS Code extension
├── GitHub integration
├── Slack/Discord bot
└── API pubblica
```

---

## ARCHITETTURA TECNICA MVP (FASE 1)

```
cervellaswarm/
├── cli/                    # CLI Python
│   ├── __main__.py        # Entry point
│   ├── commands/          # Comandi CLI
│   │   ├── init.py       # cervellaswarm init
│   │   ├── task.py       # cervellaswarm task
│   │   ├── status.py     # cervellaswarm status
│   │   └── checkpoint.py # cervellaswarm checkpoint
│   ├── agents/           # Gestione agenti
│   │   ├── loader.py     # Carica definizioni
│   │   ├── runner.py     # Esegue agenti
│   │   └── definitions/  # 16 agenti
│   ├── sncp/             # Sistema memoria
│   │   ├── manager.py    # CRUD memoria
│   │   └── templates/    # Template SNCP
│   └── api/              # Claude API wrapper
│       ├── client.py     # API calls
│       └── streaming.py  # Streaming response
├── config/
│   ├── default.yaml      # Config default
│   └── agents.yaml       # Config agenti
├── tests/
└── setup.py
```

---

## STACK TECNICO

| Componente | Tecnologia | Perche |
|------------|------------|--------|
| CLI | Python + Click | Familiare, veloce |
| API Claude | anthropic SDK | Ufficiale |
| Config | YAML | Leggibile |
| Storage | File system | Semplice, no DB |
| Packaging | PyPI | Distribuzione facile |

---

## USER FLOW MVP

```
1. INSTALL
   pip install cervellaswarm

2. SETUP
   cervellaswarm init
   → Crea .sncp/
   → Configura API key
   → Sceglie agenti

3. USO QUOTIDIANO
   cervellaswarm task "Implementa feature X"
   → Regina analizza
   → Delega ad agente giusto
   → Agente lavora
   → Output salvato in .sncp/

4. CHECKPOINT
   cervellaswarm checkpoint
   → Salva stato
   → Git commit suggerito
```

---

## DIFFERENZIATORI CHIAVE

| Noi | Competitor |
|----|-----------|
| **SNCP** - memoria persistente | Nessuna memoria tra sessioni |
| **16 agenti specializzati** | Agenti generici |
| **Regina che orchestra** | Utente deve coordinare |
| **Filosofia famiglia** | Tool freddo |
| **BYOK** - bring your own key | Vendor lock-in |

---

## PRICING MODEL

| Tier | Prezzo | Cosa Include |
|------|--------|--------------|
| **Free** | $0 | CLI base, BYOK, 3 agenti |
| **Pro** | $19/mese | Tutti agenti, SNCP completo, supporto |
| **Team** | $39/mese/seat | Multi-user, analytics, priority support |

---

## ROADMAP

### Fase 1: CLI MVP (4-6 settimane)
- [ ] Setup progetto Python
- [ ] CLI base (init, task, status)
- [ ] Integrazione Claude API
- [ ] 16 agenti convertiti
- [ ] SNCP integrato
- [ ] Test su progetti reali
- [ ] Documentazione

### Fase 2: Polish + Launch (2-3 settimane)
- [ ] Error handling robusto
- [ ] PyPI publishing
- [ ] Landing page update
- [ ] GitHub repo public
- [ ] Annuncio community

### Fase 3: Web Dashboard (dopo validazione)
- [ ] Backend FastAPI
- [ ] Frontend React
- [ ] Auth + Billing
- [ ] Analytics

---

## RISCHI E MITIGAZIONI

| Rischio | Mitigazione |
|---------|-------------|
| Claude API cambia | Wrapper astratto, facile update |
| Competitor copia | SNCP è trade secret, esperienza conta |
| Nessuno compra | Validare con beta users prima |
| Troppo complesso | MVP minimo, iterate |

---

## PROSSIMI STEP IMMEDIATI

| # | Task | Tempo |
|---|------|-------|
| 1 | Creare repo Python | 1 ora |
| 2 | CLI skeleton | 2 ore |
| 3 | Claude API wrapper | 2 ore |
| 4 | Primo agente funzionante | 2 ore |
| 5 | Test end-to-end | 1 ora |

**TOTALE MVP SKELETON: ~8 ore di lavoro**

Poi iterate.

---

## DECISIONI PRESE (9 Gennaio 2026)

| Domanda | Decisione |
|---------|-----------|
| Nome comando | `cervella` |
| Linguaggio | Python |
| Priorità | CLI first |
| Beta users | Amici, più avanti |

```bash
# Il comando ufficiale
cervella init
cervella task "Implementa feature X"
cervella status
cervella checkpoint
```

---

*"Prima COSTRUIRE, poi VENDERE."*
*"Quando troviamo il PERCHE, NULLA ci ferma!"*

---

*Mappa creata: 9 Gennaio 2026 - Sessione 142*
