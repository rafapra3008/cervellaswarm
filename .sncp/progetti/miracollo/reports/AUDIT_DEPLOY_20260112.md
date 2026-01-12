# AUDIT COMPLETO SISTEMA DEPLOY MIRACOLLO

**Data:** 12 Gennaio 2026
**Auditor:** Cervella Guardiana Ops
**Verdetto Globale:** PROBLEMI IDENTIFICATI - AZIONE RICHIESTA

---

## 1. STATO SINCRONIZZAZIONE GIT

### Commit Attuale
| Location | Commit | Status |
|----------|--------|--------|
| Locale | `ba270586d353db0ac3e9fa2e713337c73e495522` | PULITO |
| GitHub | `ba270586d353db0ac3e9fa2e713337c73e495522` | SINCRONIZZATO |
| VM | `ba270586d353db0ac3e9fa2e713337c73e495522` | **PROBLEMI** |

### PROBLEMA CRITICO - VM Git Status Sporco

La VM ha:
- **2 file DELETED** (non committati):
  - `scripts/git-safe-push.sh`
  - `scripts/install-git-hooks.sh`

- **18 file BACKUP orfani** (untracked):
  ```
  backend/data/miracollo.db.backup.20260110_172705
  backend/data/miracollo.db.backup.20260110_182656
  backend/main.py.backup.20260112
  backend/main.py.backup_20260112
  backend/routers/__init__.py.backup.20260112
  docs/roadmap/ROADMAP_SACRA_BACKUP_20251229.md
  frontend/pages/what-if/what-if.css.backup.20260112
  frontend/pages/what-if/what-if.js.backup.20260112
  frontend/pages/what-if/what-if.js.backup.guardiana.20260112_123600
  frontend/pages/what-if/what-if.js.backup_20260112
  frontend/what-if.html.backup.20260112
  ... e altri
  ```

**Gravita:** MEDIO
**Impatto:** Workflow deploy potrebbe comportarsi in modo imprevedibile
**Rischio:** File deleted potrebbero tornare al prossimo pull, creando confusione

---

## 2. STATO VM

### SSH
- Status: FUNZIONANTE
- Connessione: Stabile

### Docker Containers
| Container | Status | Note |
|-----------|--------|------|
| miracollo-backend-13 | UP (healthy) | OK |
| miracollo-nginx | UP 4h (healthy) | OK |
| cervella-ai | Exited (0) 6h ago | ATTENZIONE |

**cervella-ai:** Container AI assistant non attivo. Se non necessario in produzione, OK. Altrimenti da investigare.

### Backend Health
- Internal `/health`: RISPONDE 200 (vedi logs)
- Via Docker network: FUNZIONANTE
- Via localhost:8001: NON RAGGIUNGIBILE (no port mapping - CORRETTO per architettura)

### Nginx
- Config syntax: OK (con warning deprecation)
- Upstream backend: FUNZIONANTE
- SSL: ATTIVO

**Warning Nginx (BASSO):**
- `listen ... http2` directive deprecated (usare `http2` directive)
- `ssl_stapling` ignorato (no OCSP responder URL nel certificato)

### Permessi
- `/app/miracollo`: 755 rafapra:rafapra - OK
- `/app/miracollo/backend`: 755 rafapra:staff - MISMATCH gruppo
- `/app/miracollo/frontend`: 755 rafapra:rafapra - OK

**Gravita:** BASSO (funziona, ma inconsistente)

---

## 3. STATO LOCALE

### Git
- Branch: master
- Working tree: PULITO
- Up to date con origin: SI

### Pre-push Hook
**PROBLEMA CRITICO:** HOOK NON INSTALLATO!

Il locale NON ha il pre-push hook che invece esiste sulla VM.
Questo significa che il push dalla macchina locale NON viene verificato.

**File esistono:**
- `/Users/rafapra/Developer/miracollogeminifocus/scripts/git-safe-push.sh` - ESISTE
- `/Users/rafapra/Developer/miracollogeminifocus/scripts/install-git-hooks.sh` - ESISTE

**Ma NON sono installati in `.git/hooks/`**

**Gravita:** ALTO
**Impatto:** Push senza verifica sincronizzazione = possibili conflitti

---

## 4. STATO WORKFLOW

### GitHub Actions
- Ultimo run: SUCCESS (17s fa)
- Deploy: FUNZIONANTE
- Rollback: CONFIGURATO

### Pre-push Hook (Confronto)

| Location | Hook Installato | Funziona |
|----------|-----------------|----------|
| Locale | NO | - |
| VM | SI | SI |

### Script Mancanti su VM
I nuovi script della Sessione 177:
- `git-safe-push.sh` - MANCANTE su VM
- `install-git-hooks.sh` - MANCANTE su VM

Il deploy ha portato questi come "deleted" perche esistevano prima e ora sono stati aggiunti di nuovo, ma il `git reset --hard` li ha rimossi.

**SPIEGAZIONE:** Il workflow fa `git reset --hard origin/master` che ripristina i file dal repo. Ma se i file erano stati aggiunti al repo locale e pushati, dovrebbero esserci. Il fatto che siano "deleted" indica un problema di sync precedente.

---

## 5. FILE BACKUP ORFANI (18 totali)

### Backend
- `miracollo.db.backup.20260110_172705`
- `miracollo.db.backup.20260110_182656`
- `miracollo.db.backup_BEFORE_CLEAN_20260106_201123`
- `main.py.backup.20260112`
- `main.py.backup_20260112`
- `routers/__init__.py.backup.20260112`
- `routers/action_tracking_api.py.backup`
- `routers/guest_checkin.py.backup`
- `routers/public.py.backup`
- `routers/email.py.backup`
- `routers/competitors.py.backup`
- `services/email_service.py.backup`
- `database/miracollo.db.backup_20260107_081750`

### Frontend
- `what-if.html.backup.20260112`
- `what-if.js.backup.guardiana.20260112_123600`
- `what-if.js.backup.20260112`
- `what-if.js.backup_20260112`
- `what-if.css.backup.20260112`

### Docs
- `ROADMAP_SACRA_BACKUP_20251229.md`

**Gravita:** BASSO (non impattano funzionamento)
**Raccomandazione:** Pulire per igiene

---

## 6. PROBLEMI IDENTIFICATI - RIEPILOGO

### CRITICO
1. **Pre-push hook NON installato in locale**
   - Rischio: Push senza verifica = conflitti
   - Fix: Eseguire `scripts/install-git-hooks.sh`

### ALTO
2. **Script git mancanti su VM**
   - I file `git-safe-push.sh` e `install-git-hooks.sh` sono "deleted" su VM
   - Fix: `git restore` o attendere prossimo deploy

3. **VM git status sporco**
   - 2 deleted + 18 untracked
   - Rischio: Comportamento imprevedibile su pull/deploy

### MEDIO
4. **cervella-ai container non attivo**
   - Se necessario, riavviare
   - Se non necessario, documentare

### BASSO
5. **Nginx deprecation warnings**
   - `listen ... http2` -> `http2`
   - `ssl_stapling` senza OCSP URL

6. **File backup orfani**
   - 18 file .backup* su VM
   - Pulizia consigliata

7. **Permessi gruppo inconsistenti**
   - backend: staff, altri: rafapra

---

## 7. CHECKLIST FIX

### Immediato (CRITICO)

- [ ] **LOCALE: Installare pre-push hook**
  ```bash
  cd ~/Developer/miracollogeminifocus
  ./scripts/install-git-hooks.sh
  ```

- [ ] **VM: Ripristinare script deleted**
  ```bash
  ssh miracollo-cervella "cd /app/miracollo && git restore scripts/git-safe-push.sh scripts/install-git-hooks.sh"
  ```

### Prossima Sessione (ALTO)

- [ ] **VM: Pulire file backup orfani**
  ```bash
  ssh miracollo-cervella "cd /app/miracollo && find . -name '*.backup*' -type f -delete"
  ```

- [ ] **Verificare cervella-ai necessario**
  - Se si: `docker start cervella-ai`
  - Se no: rimuovere da docker-compose o documentare

### Quando Possibile (BASSO)

- [ ] **Aggiornare nginx.conf**
  - Cambiare `listen 443 ssl http2` in `listen 443 ssl; http2 on;`

- [ ] **Uniformare permessi**
  ```bash
  ssh miracollo-cervella "chown -R rafapra:rafapra /app/miracollo"
  ```

---

## 8. VERDETTO FINALE

| Area | Stato | Urgenza |
|------|-------|---------|
| Sincronizzazione Git | PROBLEMI | ALTO |
| VM Containers | OK | - |
| Backend Health | OK | - |
| Nginx | WARNING | BASSO |
| Hook Pre-push | MANCANTE | CRITICO |
| GitHub Actions | OK | - |
| File Orfani | PRESENTI | BASSO |

**RACCOMANDAZIONE:** Eseguire i fix CRITICO e ALTO prima del prossimo sviluppo.

---

*Report generato da Cervella Guardiana Ops*
*"Una verifica approfondita ora = zero disastri dopo."*
