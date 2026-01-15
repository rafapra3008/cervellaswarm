# Audit Sistema Deploy Miracollo

**Data:** 15 Gennaio 2026
**Autore:** Cervella Guardiana Ops
**Verdetto:** SISTEMATO

---

## PROBLEMA IDENTIFICATO

Trovati **3 script di deploy diversi** con path e approcci DIVERSI:

| Script | Path VM | Stato |
|--------|---------|-------|
| `deploy.sh` (root) | `~/app/` | CORRETTO - USARE QUESTO |
| `scripts/deploy.sh` | `/app/miracollo/` | DEPRECATO (path sbagliato) |
| `scripts/deploy_vm.sh` | `/opt/miracollo/` | DEPRECATO (path sbagliato) |

## AZIONI ESEGUITE

1. **Verificato architettura reale sulla VM:**
   - Path corretto: `~/app/`
   - Container: `miracollo-nginx` + `miracollo-backend-1`
   - docker-compose.yml in ~/app/

2. **Rinominati script obsoleti:**
   - `scripts/deploy.sh` -> `scripts/deploy.sh.DEPRECATED`
   - `scripts/deploy_vm.sh` -> `scripts/deploy_vm.sh.DEPRECATED`

3. **Creata documentazione definitiva:**
   - `docs/DEPLOY_GUIDE.md` - Guida completa
   - `DEPLOY_VM_README.md` - Quick reference aggiornata

4. **Testato script principale:**
   - `./deploy.sh --help` funziona
   - `./deploy.sh --dry-run --frontend` funziona
   - SSH a miracollo-vm funziona

## SOLUZIONE DEFINITIVA

```bash
# UNICO comando da usare:
./deploy.sh              # Deploy tutto
./deploy.sh --frontend   # Solo frontend
./deploy.sh --backend    # Solo backend
./deploy.sh --dry-run    # Simula
```

## NOTA

Al prossimo deploy REALE, rsync con `--delete` pulira file obsoleti dalla VM (es. `miracallook/backend/venv/` che non dovrebbe essere in frontend/).

## CHECKLIST VERIFICA

- [x] Script `deploy.sh` root ha path corretti
- [x] Script obsoleti rinominati
- [x] Documentazione aggiornata
- [x] SSH funziona
- [x] Dry-run funziona

---

*"Una soluzione che funziona SEMPRE > Dieci soluzioni diverse"*
