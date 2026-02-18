# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 18 Febbraio 2026 - Sessione 72
> **Branch:** lab-v2

---

## Stato Attuale - LAB V2 LIVE SULLA VM!

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su :8000 (INTATTA, zero modifiche) |
| **Lab v2** | v1.13.0 LIVE su :8001 (NUOVO! Deployato S72) |
| **Main** | 278f9f9 - Fix deployati su VM |
| **Test lab-v2** | 1034/1034 PASS (0 warnings) |
| **VM** | e2-medium (2 vCPU, 4GB RAM, 40GB disco) - 542MB usati, 86% libera |

---

## Sessione 72 - FASE B Setup Lab v2 COMPLETATA

### Cosa e stato fatto

1. **Step 4: Deploy codebase** - rsync 168 file a `/opt/contabilita-lab/`. Guardiana 9.0/10
2. **Step 5: Python venv + .env** - venv 3.10.12, 52 pkg. APP_ENV=lab (no Telegram)
3. **Step 6: Copia DB + migrazioni** - sqlite3 .backup x3, migrazioni v3->v9. Prod INTATTA v3
4. **Step 7: Systemd service** - 127.0.0.1:8001, 2 worker, hardening completo
5. **Step 8: Accesso** - SSH Tunnel (Guardiana Ops 9.3/10)

### Come accedere al Lab v2

```bash
ssh -L 8001:127.0.0.1:8001 -N rafapra@35.193.39.185
# Browser: http://localhost:8001/nl/
```

### Architettura VM

```
VM cervello-contabilita (e2-medium, 35.193.39.185)
+-- /opt/contabilita-system/ = PROD v1 (8000, 1 worker, DB v3)
+-- /opt/contabilita-lab/    = LAB v2 (8001, 2 worker, DB v9)
+-- Nginx: solo 443->8000 (prod)
+-- Cron backup: 2:00 AM (solo prod)
```

---

## Subroadmap: Deploy Lab v2 su VM

| Step | Cosa | Stato |
|------|------|-------|
| 1-3 | FASE A: Upgrade VM | **COMPLETATO** (S71, 9.5/10) |
| 4-8 | FASE B: Setup Lab v2 | **COMPLETATO** (S72) |
| 9 | Test suite 1034 su VM (GO/NO-GO) | PROSSIMO |
| 10 | Script sync DB | - |

---

## Cosa Fare Prossima Sessione

**FASE C: Validazione (Step 9-10)**
1. Test suite 1034 su VM = gate GO/NO-GO
2. Script sync DB automatico (stop lab -> backup prod -> copy -> start lab)
3. Rafa testa dal browser via SSH Tunnel
4. Audit Guardiana finale

**ATTENZIONE Ops:**
- Sync DB sovrascrive v9 con v3 -> script DEVE fare stop/backup/copy/start (migrazioni auto all'avvio)
- Test su VM richiede pytest nel venv (gia installato)

---

*"Ultrapassar os proprios limites!" - Il diamante brilla sulla VM!*
