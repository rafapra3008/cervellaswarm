# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 7 Gennaio 2026 - Sessione 112
> **Versione:** v3.0.0 - LA SESSIONE DELLA DIREZIONE E DELLA DASHBOARD!

---

## CARA PROSSIMA CERVELLA

```
+------------------------------------------------------------------+
|                                                                  |
|   Benvenuta! Questo file e' la tua UNICA memoria.               |
|   Leggilo con calma. Qui c'e' tutto quello che devi sapere.     |
|                                                                  |
|   Tu sei la REGINA dello sciame.                                 |
|   Hai 16 agenti pronti a lavorare per te.                       |
|   HAI LA FAMIGLIA!                                               |
|                                                                  |
+------------------------------------------------------------------+
|                                                                  |
|   SESSIONE 112: LA SESSIONE DELLA DIREZIONE!                    |
|                                                                  |
|   ABBIAMO FATTO:                                                 |
|   - Sintetizzato i 6 studi della sessione 111                   |
|   - Confermato strategia DUAL-TRACK (VISUAL first!)             |
|   - COSTRUITO la Dashboard MAPPA (funziona!)                    |
|   - Creato Sistema Memoria Persistente                          |
|   - Documentato DECISIONI_TECNICHE.md                           |
|                                                                  |
+------------------------------------------------------------------+
|                                                                  |
|   IL CLAIM PRINCIPALE:                                           |
|                                                                  |
|   "L'AI NON TI RUBA IL LAVORO. L'AI SALVA IL TUO LAVORO."       |
|                                                                  |
|   LA FRASE SACRA:                                                |
|                                                                  |
|   "L'idea e' fare il mondo meglio                                |
|    su di come riusciamo a fare."                                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

## NOVITA' IMPORTANTE: LEGGI ANCHE LE DECISIONI!

```
+------------------------------------------------------------------+
|                                                                  |
|   PRIMA DI INIZIARE, LEGGI:                                     |
|                                                                  |
|   1. Questo file (PROMPT_RIPRESA.md) - narrativo                |
|   2. docs/decisioni/DECISIONI_TECNICHE.md - strutturato         |
|                                                                  |
|   Il file DECISIONI contiene tutte le scelte tecniche:          |
|   - Porte (8100 = Dashboard, 8000 = Contabilita')               |
|   - Stack (React + FastAPI + SSE)                               |
|   - Strategia (DUAL-TRACK, VISUAL first)                        |
|                                                                  |
|   NON CHIEDERE COSE GIA' DECISE!                                |
|                                                                  |
+------------------------------------------------------------------+
```

---

## COSA E' SUCCESSO NELLA SESSIONE 112

### 1. Sintesi dei 6 Studi (Sessione 111)

Ho letto 3,500+ righe di studi e sintetizzato per Rafa:

| Studio | Insight Chiave |
|--------|----------------|
| Dashboard ARCH | 15+ API, event-driven, schema JSON |
| Dashboard TECH | React + Vite + FastAPI + SSE |
| Dashboard UX | MAPPA = GPS del progetto, 4 momenti WOW |
| Mercato No-Code | $65B mercato, nessuno ha multi-agent |
| OpenAI Swarm | Morto perche' senza visione, noi abbiamo ANIMA |
| Positioning | "L'AI salva il lavoro" funziona per non-tecnici |

### 2. Decisione Strategica: DUAL-TRACK Confermato!

```
+------------------------------------------------------------------+
|                                                                  |
|   DUE MERCATI. STESSO CORE. STESSA FAMIGLIA.                    |
|                                                                  |
|   TRACK 1: CervellaSwarm IDE (Developer)                        |
|   - VS Code Extension                                            |
|   - Mercato: $30B                                                |
|                                                                  |
|   TRACK 2: CervellaSwarm VISUAL (Everyone)                      |
|   - Dashboard web visuale                                        |
|   - Mercato: $65B                                                |
|                                                                  |
|   PRIORITA': VISUAL first!                                       |
|   Perche': Mercato piu' grande, meno competition,               |
|   il claim funziona meglio per non-tecnici,                     |
|   Rafa e' la prova (non programmatore che ha costruito!)        |
|                                                                  |
+------------------------------------------------------------------+
```

### 3. DASHBOARD MAPPA - COSTRUITA E FUNZIONANTE!

Lo sciame ha costruito la Dashboard in ~10 minuti!

**Backend (cervella-backend):**
- 13 endpoints FastAPI
- SSE per real-time
- Parser per markdown
- Porta: 8100 (DEDICATA!)

**Frontend (cervella-frontend):**
- React + Vite + TypeScript
- 5 widget: Layout, Nord, Famiglia, Roadmap, Sessione
- Tailwind con palette UX
- Build funzionante!

**Come lanciare:**
```bash
# Backend (terminale 1)
cd ~/Developer/CervellaSwarm/dashboard/api
./run.sh

# Frontend (terminale 2)
cd ~/Developer/CervellaSwarm/dashboard/frontend
npm run dev

# Oppure tutto insieme:
cd ~/Developer/CervellaSwarm/dashboard
./start-dashboard.sh
```

**URL:**
- Dashboard: http://localhost:5173
- API Docs: http://localhost:8100/docs

### 4. Sistema Memoria Persistente - NUOVO!

Problema scoperto su Miracollo: decisioni tecniche non documentate → doppio lavoro!

**Soluzione creata:**
- Studio: docs/studio/STUDIO_MEMORIA_PERSISTENTE.md
- Template: docs/decisioni/DECISIONI_TECNICHE.md
- Aggiunto alla roadmap: FASE 0.5

**Da applicare anche a:**
- Miracollo (origine del problema)
- Contabilita'

### 5. Infrastruttura Porte Dedicate

```
PORTE CERVELLASWARM:
- 8100 = Dashboard API (FastAPI)
- 5173 = Dashboard Frontend (Vite)

PORTE ALTRI PROGETTI (NON TOCCARE!):
- 8000 = Contabilita' Backend
- 8080 = Miracollo (se attivo)
```

---

## COSA FUNZIONA GIA' (REALE!)

| Cosa | Status |
|------|--------|
| 16 Agents in ~/.claude/agents/ | FUNZIONANTE |
| spawn-workers v3.0.0 | TUTTI i 16 agenti! |
| swarm-global-status | Multi-progetto |
| **Dashboard MAPPA** | **NUOVO! Prototipo funzionante!** |
| **Sistema DECISIONI** | **NUOVO! Template creato!** |
| swarm-logs | Log live worker |
| swarm-status | Stato task |

---

## PROSSIMI STEP

```
+------------------------------------------------------------------+
|                                                                  |
|   PROSSIMA SESSIONE:                                             |
|                                                                  |
|   OPZIONE A: Continuare Dashboard MAPPA                         |
|   - Connettere frontend ai dati reali del backend               |
|   - Widget "Decisioni Attive"                                   |
|   - Test completo                                                |
|                                                                  |
|   OPZIONE B: Sistema Memoria                                    |
|   - Applicare DECISIONI_TECNICHE a Miracollo                    |
|   - Applicare a Contabilita'                                    |
|   - Aggiornare CLAUDE.md globale                                |
|                                                                  |
|   OPZIONE C: Fix Sveglia Regina                                 |
|   - Roadmap: docs/roadmap/ROADMAP_SVEGLIA_REGINA.md             |
|   - Con backend + devops + tester                               |
|                                                                  |
|   CHIEDI A RAFA cosa preferisce!                                |
|                                                                  |
+------------------------------------------------------------------+
```

---

## DOCUMENTI IMPORTANTI

| Documento | Path | Cosa contiene |
|-----------|------|---------------|
| **DECISIONI** | docs/decisioni/DECISIONI_TECNICHE.md | Tutte le scelte tecniche! |
| LA MAPPA v2.0 | docs/strategia/MAPPA_CERVELLASWARM_IDE.md | Step verso liberta' |
| Dashboard Roadmap | docs/roadmap/SUB_ROADMAP_FASE0_DASHBOARD.md | Piano dashboard |
| Memoria | docs/studio/STUDIO_MEMORIA_PERSISTENTE.md | Sistema memoria |
| 6 STUDI | docs/studio/STUDIO_*.md | Tutti gli studi |

---

## LO SCIAME (16 membri)

```
TU SEI LA REGINA (Opus) - Coordina, DELEGA, MAI edit diretti!

3 GUARDIANE (Opus):
- cervella-guardiana-qualita
- cervella-guardiana-ops
- cervella-guardiana-ricerca

12 WORKER (Sonnet):
- frontend, backend, tester
- reviewer, researcher, scienziata, ingegnera
- marketing, devops, docs, data, security

POSIZIONE: ~/.claude/agents/ (GLOBALI!)
```

---

## FILO DEL DISCORSO (Sessioni 110-112)

### Sessione 112: LA SESSIONE DELLA DIREZIONE! (ATTUALE)

**Cosa abbiamo fatto:**
1. Sintetizzato i 6 studi della sessione 111
2. Decisione DUAL-TRACK confermata (VISUAL first!)
3. Dashboard MAPPA costruita! (backend + frontend funzionanti)
4. Sistema Memoria Persistente creato
5. DECISIONI_TECNICHE.md applicato a CervellaSwarm
6. Porte dedicate configurate (8100)

**Insight chiave della sessione:**
- "Rafa NON e' programmatore, eppure ha costruito 2 sistemi" → QUESTO e' il prodotto!
- Il claim "L'AI salva il lavoro" parla a chi ha PAURA dell'AI
- La MAPPA brilla per chi e' PERSO (non-tecnici)
- Problema memoria su Miracollo → soluzione Sistema Decisioni

---

### Sessione 111: LA SESSIONE DEGLI STUDI!

- 6 studi completati dallo sciame
- swarm-global-status implementato
- Nuova visione DUAL-TRACK
- Nuovo positioning "L'AI salva il tuo lavoro"

---

### Sessione 110: IL CLAIM DELLA LIBERTA'

- IL CLAIM scritto
- LA MAPPA creata (1,185 righe!)
- 5 studi iniziali completati

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"L'idea e' fare il mondo meglio su di come riusciamo a fare."

"L'AI NON TI RUBA IL LAVORO. L'AI SALVA IL TUO LAVORO."

"E' il nostro team! La nostra famiglia digitale!"

"Ultrapassar os proprios limites!"

"Prima la MAPPA, poi il VIAGGIO!"

"La comunicazione interna deve essere meglio!" (7 Gen 2026)
```

---

## NOTE IMPORTANTI

```
+------------------------------------------------------------------+
|                                                                  |
|   REGOLA SACRA: PROGETTI SEPARATI!                               |
|                                                                  |
|   - CervellaSwarm ha le sue porte (8100, 5173)                  |
|   - Contabilita' ha le sue (8000)                               |
|   - MAI mischiare!                                               |
|   - Solo MANUALE DIAMANTE e' globale                            |
|                                                                  |
+------------------------------------------------------------------+
|                                                                  |
|   REGOLA SACRA: DOCUMENTARE DECISIONI!                          |
|                                                                  |
|   Quando prendi una decisione tecnica:                          |
|   1. Scrivila in docs/decisioni/DECISIONI_TECNICHE.md           |
|   2. Con data, motivo, alternativa scartata                     |
|   3. Cosi' la prossima sessione SA cosa e' stato deciso         |
|                                                                  |
+------------------------------------------------------------------+
```

---

**VERSIONE:** v3.0.0
**SESSIONE:** 112 - LA SESSIONE DELLA DIREZIONE!
**DATA:** 7 Gennaio 2026

---

*Scritto con CURA, PRECISIONE e AMORE.*

*"L'idea e' fare il mondo meglio su di come riusciamo a fare."*

*"Prima la MAPPA, poi il VIAGGIO!"*

Cervella & Rafa 💙
