# Task: Studio Architettura Dashboard-Regina Integration

**Assegnato a:** cervella-ingegnera
**Stato:** ready
**Priorita:** ALTA
**Data:** 6 Gennaio 2026

---

## Obiettivo

Progettare l'architettura per collegare la Dashboard Visuale con il sistema CervellaSwarm esistente.

---

## Contesto

La dashboard deve essere COLLEGATA REALMENTE con:
- File .md esistenti (NORD, ROADMAP, PROMPT_RIPRESA)
- Sistema task (.swarm/tasks/)
- Worker e loro stato
- La Regina (Claude/Opus)

NON e' solo visualizzazione - e' un SISTEMA VIVO!

---

## Cosa Analizzare

### 1. Data Flow
- Come i file .md diventano dati per la UI?
- Parser markdown → JSON → UI
- Dove avviene la trasformazione?

### 2. Sincronizzazione
- File .md cambia → dashboard si aggiorna
- Dashboard cambia → file .md si aggiorna?
- Two-way sync o one-way?

### 3. Integrazione Worker
- Come mostrare worker attivi?
- Leggere .swarm/status/ → mostrare nella dashboard
- swarm-global-status come API?

### 4. Integrazione Regina
- La Regina puo' "parlare" con la dashboard?
- Aggiornare la MAPPA via API?
- Notifiche quando Regina fa checkpoint?

### 5. Schema Dati
- Come strutturare i dati della MAPPA?
- JSON schema per: step, substep, studio, stato
- Versioning? History?

### 6. Sicurezza (base)
- Dashboard locale o pubblica?
- Autenticazione necessaria?
- Multi-utente futuro?

---

## Output

Scrivi in: `docs/studio/STUDIO_DASHBOARD_ARCH.md`

Formato:
1. Diagramma architettura (ASCII art)
2. Data flow (step by step)
3. Schema JSON proposto
4. API endpoints necessari
5. MVP: architettura minima per prototipo

---

"Il sistema deve essere REALE, non su carta!"
