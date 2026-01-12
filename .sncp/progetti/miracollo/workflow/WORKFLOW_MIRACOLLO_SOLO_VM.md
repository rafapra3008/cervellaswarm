# WORKFLOW MIRACOLLO - SOLO VM

> **Data:** 11 Gennaio 2026 - Sessione 166
> **Decisione:** Rafa
> **Status:** ATTIVO

---

## LA REGOLA

```
+================================================================+
|                                                                |
|   MIRACOLLO = SOLO VM                                          |
|                                                                |
|   - Locale NON esiste più (spostato in _OLD)                   |
|   - Docker locale SPENTO                                       |
|   - Lavoriamo SOLO sulla VM                                    |
|   - Backup periodico per sicurezza                             |
|                                                                |
+================================================================+
```

---

## COME LAVORARE

### Per Cervelle

```bash
# Connetti alla VM
ssh miracollo-cervella

# Path del codice
cd /app/miracollo

# Backend
cd /app/miracollo/backend

# Frontend
cd /app/miracollo/frontend

# Database (PRODUZIONE!)
/app/miracollo/backend/data/miracollo.db
```

### Per Rafa

```bash
# Connetti
ssh miracollo-cervella

# Apri in editor (se serve)
code --remote ssh-remote+miracollo-cervella /app/miracollo
```

---

## SICUREZZA

### Triplo Backup

| Layer | Cosa | Dove |
|-------|------|------|
| 1 | Git history | GitHub |
| 2 | Backup periodico | /Users/rafapra/Developer/_BACKUPS_VM/ |
| 3 | VM running | Google Cloud |

### Comando Backup

```bash
# Backup manuale dalla VM
rsync -avz miracollo-cervella:/app/miracollo/ /Users/rafapra/Developer/_BACKUPS_VM/miracollo_$(date +%Y%m%d)/
```

---

## PATHS IMPORTANTI

| Cosa | Path |
|------|------|
| Codice VM | `/app/miracollo/` |
| Backend | `/app/miracollo/backend/` |
| Frontend | `/app/miracollo/frontend/` |
| Database | `/app/miracollo/backend/data/miracollo.db` |
| Logs | `/home/rafapra/logs/` |
| Env produzione | `/home/rafapra/app/.env.production` |

---

## LOCALE (ARCHIVIO)

| Cosa | Path | Status |
|------|------|--------|
| Codice OLD | `_OLD_miracollogeminifocus/` | Archivio |
| Backup VM | `_BACKUPS_VM/` | Backup periodico |

---

## GIT

```bash
# Sulla VM
cd /app/miracollo
git status
git add .
git commit -m "messaggio"
git push
```

**IMPORTANTE:** Il repo sulla VM potrebbe non avere git configurato.
Se serve, configurare:

```bash
cd /app/miracollo
git init  # se non esiste
git remote add origin https://github.com/[repo].git
```

---

## DEPLOY

Il deploy ora è DIRETTO sulla VM:
1. Modifica file sulla VM
2. Restart container se serve: `docker restart miracollo-backend-12`
3. Verifica: `curl https://miracollo.com/health`

---

## RESTART SERVICES

```bash
# Restart backend
docker restart miracollo-backend-12

# Restart nginx
docker restart miracollo-nginx

# Vedi logs
docker logs -f miracollo-backend-12 --tail 50
```

---

## PERCHÉ QUESTA DECISIONE

1. **Confusione eliminata** - Una sola copia = zero dubbi
2. **Errori eliminati** - Mai più "era in locale o VM?"
3. **Deploy immediato** - Modifichi = live
4. **Semplicità** - Meno cose da gestire

---

*"Basta complessità! Una sola fonte di verità!"*

*Sessione 166 - Rafa & Regina*
