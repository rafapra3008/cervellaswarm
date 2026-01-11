# RICERCA: Deploy Best Practices 2025-2026 per Piccoli Team

**Data Ricerca:** 10 Gennaio 2026
**Researcher:** Cervella Researcher
**Contesto:** FastAPI + SQLite + Frontend statico, singola VM Google Cloud con Docker, team 1-2 persone
**Problema:** Script deploy.sh complesso (27KB), deployment instabile, ogni volta qualcosa va storto

---

## TL;DR - RACCOMANDAZIONE FINALE

Per il vostro caso (FastAPI + SQLite, singola VM, 1-2 persone), la raccomandazione è:

🎯 **STRATEGIA: GitHub Actions + Docker Compose + Docker Rollout**

**PERCHÉ:**
- ✅ Costo: **$0** (GitHub Actions free tier 2000 min/mese)
- ✅ Semplicità: Setup in **1-2 giorni**, non settimane
- ✅ Affidabilità: Zero-downtime deployment con health checks
- ✅ Sicurezza: Secrets gestiti da GitHub, backup automatici
- ✅ Rollback: Veloce e sicuro
- ✅ Manutenibilità: Infrastruttura come codice, riproducibile

**ALTERNATIVE CONSIDERATE:**
- Dokploy/Coolify: Ottimi ma aggiungono layer di complessità
- Watchtower: Sconsigliato per production (progetto non mantenuto)
- Script manuali: Quello che avete ora - fonte di errori

---

## 1. PANORAMICA OPZIONI

### 1.1 CI/CD con GitHub Actions (RACCOMANDATO)

**Cosa:** Pipeline automatica che builda, testa e deploya quando pushate su `main`

**Pro:**
- Integrazione nativa con GitHub (già lo usate)
- Free tier generoso (2000 min/mese, più che sufficiente per 1-2 persone)
- Community enorme, migliaia di esempi e actions pronte
- Facilmente estendibile (oggi 1 server, domani scaling)
- Self-hosted runner possibile se servono più minuti

**Contro:**
- Richiede setup iniziale (ma poi zero manutenzione)
- Dipendenza da servizio esterno (ma altamente affidabile)

**Costo:** $0/mese (free tier)

**Complessità:** Media-Bassa (setup 1-2 giorni)

**Fonti:**
- [12 Best CI/CD tools 2025 - Pieces](https://pieces.app/blog/best-ci-cd-tools)
- [14 best CI/CD tools 2025 - Northflank](https://northflank.com/blog/best-ci-cd-tools)

---

### 1.2 Self-Hosted PaaS (Dokploy o Coolify)

**Cosa:** Piattaforme self-hosted che vi danno un'interfaccia web per gestire deploy, simili a Heroku/Railway

**Pro:**
- UI bellissima, tutto in un click
- Gestione integrata di database, backup, monitoring
- Auto-deploy da Git con webhook
- Rollback con un click

**Contro:**
- Layer aggiuntivo da mantenere (il PaaS stesso va aggiornato)
- Consuma risorse sulla VM (1GB RAM + CPU)
- Overkill per 1-2 app semplici
- Curva di apprendimento per debugging

**Costo:** $0/mese (self-hosted)

**Complessità:** Media (setup veloce, ma layer extra da capire)

**Dokploy vs Coolify:**
- **Dokploy:** Più leggero, migliore con Docker Compose, più recente (2024)
- **Coolify:** Più maturo (44k GitHub stars), più database supportati, UI più polita

**Raccomandazione:** Se volete UI, scegliete Dokploy (più efficiente CPU/RAM)

**Fonti:**
- [Coolify vs Dokploy 2025 - Medium](https://girff.medium.com/coolify-vs-dokploy-the-ultimate-comparison-for-self-hosted-in-2025-8c63f1bda088)
- [Dokploy vs Coolify Real-World - Zero One Group](https://blog.zero-one-group.com/dokploy-vs-coolify-real-world-comparison-on-a-fresh-ec2-instance-eab584ceabc6)

---

### 1.3 Webhook-Based Deploy

**Cosa:** Server sulla VM che ascolta webhook da GitHub, esegue `git pull` e restart container

**Pro:**
- Semplicissimo da capire
- Zero dipendenze esterne
- Controllo totale

**Contro:**
- Nessun CI (testing, linting, build prima di deploy)
- Gestione secret e sicurezza manuale
- Nessun rollback automatico
- Deployment diretti senza validazione

**Costo:** $0/mese

**Complessità:** Bassa

**Raccomandazione:** Utile per progetti hobby, **NON per production** seria

**Fonti:**
- [GitHub Webhook Deploy - GitHub](https://github.com/iaincollins/docker-deploy-webhook)
- [Automated Deployments with GitHub Webhooks - Toptal](https://www.toptal.com/devops/deploy-web-applications-automatically-using-github-webhooks)

---

### 1.4 Watchtower (Auto-Update Containers)

**Cosa:** Container che monitora Docker Hub/Registry e auto-aggiorna i container quando trovate nuove immagini

**Pro:**
- Setup semplicissimo (1 container aggiuntivo)
- Completamente automatico

**Contro:**
- ⚠️ **SCONSIGLIATO PER PRODUCTION** (dai maintainer stessi!)
- Progetto non mantenuto (ultimo update 3 anni fa, problemi con Docker 29.x)
- Nessun controllo su quando avvengono gli update
- Nessun testing pre-deploy
- Può rompere production senza preavviso

**Costo:** $0/mese

**Complessità:** Bassissima

**Raccomandazione:** ❌ **NON USARE PER PRODUCTION**

**Alternative migliori:**
- What's Up Docker (WUD) - fork mantenuto
- Renovate Bot - per Infrastructure as Code

**Fonti:**
- [Watchtower Docker Auto Update - Better Stack](https://betterstack.com/community/guides/scaling-docker/watchtower-docker/)
- [What's Up Docker Alternative - Virtualization Howto](https://www.virtualizationhowto.com/2025/11/whats-up-docker-keeps-your-home-lab-containers-updated-automatically/)

---

### 1.5 Script Manuale (Status Quo)

**Cosa:** Script bash/shell che fa build, push, ssh sulla VM, pull, restart

**Pro:**
- Già ce l'avete
- Nessuna dipendenza esterna

**Contro:**
- ❌ Errori frequenti ("ogni volta qualcosa va storto")
- ❌ Non riproducibile (dipende da stato locale)
- ❌ Difficile da debuggare (27KB di bash!)
- ❌ Nessun CI/testing
- ❌ Downtime durante deploy

**Costo:** $0/mese

**Complessità:** Alta (manutenzione continua)

**Raccomandazione:** ❌ **DA SOSTITUIRE**

---

## 2. DEPLOY STRATEGIES - COME FARE IL DEPLOY

### 2.1 Zero-Downtime Deployment

**Problema:** Con `docker-compose up -d`, i container si fermano prima di riavviarsi → downtime

**Soluzione: Docker Rollout**

Tool che implementa rolling update per Docker Compose:

```bash
# Invece di:
docker compose up -d backend

# Usate:
docker rollout backend
```

**Come funziona:**
1. Scala il servizio a 2x istanze (vecchia + nuova)
2. Aspetta che la nuova superi health check
3. Rimuove la vecchia istanza
4. Zero secondi di downtime

**Setup:**
```bash
# Installazione
curl -fsSL https://raw.githubusercontent.com/wowu/docker-rollout/master/install.sh | sh

# Nel docker-compose.yml serve solo health check:
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
```

**Pro:**
- Zero downtime garantito
- Facile integrazione con Docker Compose esistente
- Rollback automatico se health check fallisce

**Contro:**
- Richiede 2x risorse temporaneamente durante deploy
- Solo 1 container per servizio alla volta

**Fonti:**
- [Docker Rollout Zero-Downtime - GitHub](https://github.com/wowu/docker-rollout)
- [Docker Rollout Guide - Virtualization Howto](https://www.virtualizationhowto.com/2025/06/docker-rollout-zero-downtime-deployments-for-docker-compose-made-simple/)

---

### 2.2 Blue-Green Deployment

**Cosa:** Due ambienti identici (blue=vecchio, green=nuovo), switch istantaneo tramite reverse proxy

**Pro:**
- Zero downtime
- Rollback istantaneo (basta switchare il proxy)
- Testing in production con ambiente identico

**Contro:**
- Richiede 2x risorse SEMPRE (non solo durante deploy)
- Complessità maggiore (gestire 2 ambienti)

**Raccomandazione:** Overkill per singola VM, meglio Docker Rollout

**Fonti:**
- [Zero-downtime Docker Compose - Supun.io](https://supun.io/zero-downtime-deployments-docker-compose)
- [Zero Downtime with Nginx Docker - Tines](https://www.tines.com/blog/simple-zero-downtime-deploys-with-nginx-and-docker-compose/)

---

## 3. BEST PRACTICES - SICUREZZA

### 3.1 Gestione Secrets

**❌ MAI FARE:**
```yaml
# docker-compose.yml - NO!
environment:
  DATABASE_PASSWORD: "mysecretpassword"
  API_KEY: "sk-1234567890"
```

**✅ INVECE:**

**Opzione 1: File-based Secrets (Docker Secrets)**
```yaml
# docker-compose.yml
services:
  backend:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

App legge da `/run/secrets/db_password` (in memoria, mai su disco)

**Opzione 2: GitHub Actions Secrets + .env File**
```yaml
# .github/workflows/deploy.yml
- name: Create .env file
  run: |
    echo "DATABASE_PASSWORD=${{ secrets.DB_PASSWORD }}" >> .env
    echo "API_KEY=${{ secrets.API_KEY }}" >> .env

- name: Deploy .env to server
  run: scp .env ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }}:/app/.env
```

**Opzione 3: External Secret Manager (per il futuro)**
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault

**Raccomandazione:** Opzione 2 per iniziare (GitHub Secrets → .env), migrare a Opzione 1 quando scalate

**Fonti:**
- [Docker Secrets Security - GitGuardian](https://blog.gitguardian.com/how-to-handle-secrets-in-docker/)
- [Docker Secrets Best Practices - Spacelift](https://spacelift.io/blog/docker-secrets)
- [Environment Variables Best Practices - Docker Docs](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/)

---

### 3.2 Scan for Secrets in Code

**Problema:** Secret hardcoded per sbaglio in codice/Dockerfile/compose file

**Soluzione:**
- Pre-commit hook con `detect-secrets` o `trufflehog`
- GitHub Actions scan prima di deploy

```yaml
# .github/workflows/security-scan.yml
- name: Scan for secrets
  uses: trufflesecurity/trufflehog@main
```

**Fonti:**
- [Docker Security Best Practices - Better Stack](https://betterstack.com/community/guides/scaling-docker/docker-security-best-practices/)

---

### 3.3 Container Security

**Best Practices:**

1. **Non eseguire come root**
```dockerfile
# Nel Dockerfile
RUN adduser -D appuser
USER appuser
```

2. **Multi-stage builds**
```dockerfile
# Builder stage
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage (molto più piccola)
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["uvicorn", "app.main:app"]
```

3. **Healthchecks obbligatori**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**Fonti:**
- [Modern Docker Best Practices 2025 - Talent500](https://talent500.com/blog/modern-docker-best-practices-2025/)
- [Docker Best Practices 2025 - BenchHub](https://docs.benchhub.co/docs/tutorials/docker/docker-best-practices-2025)

---

## 4. BEST PRACTICES - BACKUP & ROLLBACK

### 4.1 SQLite Backup con Litestream

**Problema:** SQLite è un file, fare backup mentre l'app scrive = corruzione dati

**Soluzione:** Litestream - streaming replication continua su S3/GCS

**Come funziona:**
1. SQLite in WAL mode (Write-Ahead Logging)
2. Litestream monitora il WAL file
3. Replica continua su cloud storage (S3, GCS, Azure Blob)
4. Point-in-time restore

**Setup:**
```yaml
# docker-compose.yml
services:
  backend:
    depends_on:
      - litestream

  litestream:
    image: litestream/litestream
    volumes:
      - ./data:/data
      - ./litestream.yml:/etc/litestream.yml
    environment:
      LITESTREAM_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      LITESTREAM_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
```

```yaml
# litestream.yml
dbs:
  - path: /data/database.db
    replicas:
      - type: s3
        bucket: my-backup-bucket
        path: database
        region: us-east-1
```

**Restore:**
```bash
litestream restore -o /data/database.db s3://my-backup-bucket/database
```

**Pro:**
- Backup continuo (ogni secondo)
- Point-in-time restore
- Costo minimo (S3 costa centesimi)
- Zero downtime durante backup

**Contro:**
- Setup leggermente più complesso
- Dipendenza da cloud storage

**Raccomandazione:** ✅ **FORTEMENTE CONSIGLIATO** per production con SQLite

**Alternative:** Se non volete Litestream, backup giornalieri con cron:
```bash
# Cron job che fa backup giornaliero
0 2 * * * sqlite3 /app/data/db.sqlite3 ".backup /app/backups/db-$(date +\%Y\%m\%d).sqlite3"
```

**Fonti:**
- [FastAPI SQLite Litestream - Medium](https://medium.com/@hadiyolworld007/fastapi-sqlite-wal-with-litestream-cheap-ha-apis-with-point-in-time-restore-8fcf7e368740)

---

### 4.2 Docker Volume Backup

**Cosa backuppare:**
- Database files (SQLite, Postgres data)
- User uploads
- Configuration files
- Logs (se servono)

**Strategia:**

```bash
# Backup manuale
docker run --rm \
  -v myapp_data:/source \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/backup-$(date +%Y%m%d).tar.gz -C /source .

# Restore
docker run --rm \
  -v myapp_data:/target \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/backup-20260110.tar.gz -C /target
```

**Automazione con GitHub Actions:**
```yaml
# .github/workflows/backup.yml
name: Daily Backup
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM ogni giorno

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Backup database
        run: |
          ssh ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} \
            "docker exec backend sqlite3 /app/db.sqlite3 '.backup /tmp/backup.db'"
          scp ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }}:/tmp/backup.db \
            ./backup-$(date +%Y%m%d).db

      - name: Upload to S3
        run: aws s3 cp backup-*.db s3://my-backups/
```

**Fonti:**
- [Docker Container Backup Guide - SimpleBackups](https://simplebackups.com/blog/docker-container-backup-restore-guide)
- [Docker Backup Best Practices - Collabnix](https://collabnix.com/the-importance-of-docker-container-backups-best-practices-and-strategies/)

---

### 4.3 Rollback Strategy

**Opzione 1: Git-based (RACCOMANDATO)**
```bash
# Nel deploy script
git tag v1.2.3
git push --tags

# Rollback
git checkout v1.2.2
docker compose build
docker rollout backend
```

**Opzione 2: Image tags**
```yaml
# Tenere immagini vecchie per N giorni
backend:
  image: myapp:v1.2.3  # Tag specifico, non :latest

# Rollback
sed -i 's/v1.2.3/v1.2.2/' docker-compose.yml
docker rollout backend
```

**Opzione 3: Dokploy Rollback (se usate Dokploy)**
- Click su "Rollback" nella UI
- Scegliete deployment precedente
- Deploy automatico

**Raccomandazione:** Git tags + Docker Rollout = rollback in <2 minuti

**Fonti:**
- [Dokploy Rollbacks - Dokploy v0.24.0](https://dokploy.com/blog/v0-24-0-rollbacks-docker-volume-backups-more)

---

## 5. CONFIGURAZIONE PRODUCTION - FASTAPI

### 5.1 Server Stack

**Raccomandato:** Gunicorn + Uvicorn Workers

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# PRODUCTION: Gunicorn con Uvicorn workers
CMD ["gunicorn", "app.main:app", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

**Workers:** 1 worker per CPU core (VM con 2 CPU = 2 workers)

**max-requests:** Restart worker dopo 1000-1050 request (previene memory leak)

**Fonti:**
- [FastAPI Production Deployment - Render](https://render.com/articles/fastapi-production-deployment-best-practices)
- [FastAPI Deployment Guide 2025 - Zestminds](https://www.zestminds.com/blog/fastapi-deployment-guide/)

---

### 5.2 Environment Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Crash subito se mancano variabili critiche!
    database_url: str  # Required
    api_key: str  # Required

    # Con default per non-critical
    log_level: str = "INFO"
    debug: bool = False  # SEMPRE False in production!

    class Config:
        env_file = ".env"

settings = Settings()

# Questa riga fa crashare l'app se mancano secret
# MEGLIO crash all'avvio che bug in production!
```

**Fonti:**
- [FastAPI Pre-Deployment Checklist - FastroAI](https://fastro.ai/blog/fastapi-deployment-checklist)

---

### 5.3 Reverse Proxy

**Configurazione Nginx (se usate):**

```nginx
# /etc/nginx/sites-available/myapp
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name myapp.com;

    # Redirect HTTP -> HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myapp.com;

    ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    # Static files
    location /static {
        alias /app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to FastAPI
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

**Alternative a Nginx:**
- Caddy (configurazione più semplice, HTTPS automatico)
- Traefik (usato da Dokploy, ottimo per Docker)

**Fonti:**
- [FastAPI Production Deployment - Craft Your Startup](https://craftyourstartup.com/cys-docs/cookbooks/fastapi-production-deployment/)

---

## 6. IMPLEMENTAZIONE RACCOMANDATA - STEP BY STEP

### FASE 1: Setup CI/CD con GitHub Actions (Giorno 1)

**1.1 Preparare Docker Setup**

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    image: ghcr.io/yourusername/myapp-backend:${TAG:-latest}
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    labels:
      - "com.centurylinklabs.watchtower.enable=false"  # No auto-update!

  frontend:
    build: ./frontend
    image: ghcr.io/yourusername/myapp-frontend:${TAG:-latest}
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s

  # (Opzionale ma consigliato) Litestream per backup
  litestream:
    image: litestream/litestream
    restart: unless-stopped
    volumes:
      - ./data:/data
      - ./litestream.yml:/etc/litestream.yml
    env_file: .env.litestream
```

**1.2 GitHub Actions Workflow**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:  # Deploy manuale

env:
  REGISTRY: ghcr.io
  IMAGE_NAME_BACKEND: ${{ github.repository }}/backend
  IMAGE_NAME_FRONTEND: ${{ github.repository }}/frontend

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app tests/

      - name: Lint
        run: |
          pip install ruff
          ruff check backend/app

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta-backend
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}
          tags: |
            type=sha,prefix=,format=short
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta-backend.outputs.tags }}
          labels: ${{ steps.meta-backend.outputs.labels }}

      - name: Build and push frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Create .env file
        run: |
          cat << EOF > .env
          DATABASE_URL=${{ secrets.DATABASE_URL }}
          API_KEY=${{ secrets.API_KEY }}
          TAG=${{ github.sha }}
          EOF

      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H ${{ secrets.SSH_HOST }} >> ~/.ssh/known_hosts

      - name: Deploy to server
        run: |
          # Copia file necessari
          scp .env docker-compose.yml ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }}:/app/

          # Esegui deploy con zero downtime
          ssh ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} << 'ENDSSH'
            cd /app

            # Pull nuove immagini
            docker compose pull

            # Deploy con zero downtime (usa docker-rollout)
            docker rollout backend
            docker rollout frontend

            # Cleanup immagini vecchie
            docker image prune -af --filter "until=72h"
          ENDSSH

      - name: Health check
        run: |
          sleep 10
          curl -f https://myapp.com/health || exit 1

      - name: Notify (opzionale)
        if: always()
        run: |
          # Manda notifica Discord/Slack/Email
          echo "Deploy ${{ job.status }}"
```

**1.3 Setup Secrets in GitHub**

```bash
# Repository Settings > Secrets and variables > Actions
# Aggiungi:
SSH_HOST=35.123.45.67
SSH_USER=deploy
SSH_PRIVATE_KEY=<contenuto chiave privata>
DATABASE_URL=sqlite:///./data/db.sqlite3
API_KEY=<your-api-key>
```

---

### FASE 2: Setup Zero-Downtime Deploy (Giorno 1-2)

**2.1 Installare Docker Rollout sulla VM**

```bash
# SSH sulla VM
ssh deploy@yourserver

# Installa docker-rollout
curl -fsSL https://raw.githubusercontent.com/wowu/docker-rollout/master/install.sh | sh

# Verifica
docker rollout --version
```

**2.2 Aggiungere Health Check Endpoint**

```python
# backend/app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """
    Health check endpoint per Docker.
    Verifica che:
    - App è running
    - Database è accessibile
    - (Opzionale) Altri servizi critici
    """
    try:
        # Test database connection
        # db.execute("SELECT 1")

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Unhealthy: {str(e)}")
```

---

### FASE 3: Setup Backup (Giorno 2)

**Opzione A: Litestream (RACCOMANDATO)**

```yaml
# litestream.yml
dbs:
  - path: /data/database.db
    replicas:
      - type: s3
        bucket: myapp-backups
        path: production/database
        region: us-east-1
        retention: 720h  # 30 giorni
```

```yaml
# .env.litestream
LITESTREAM_ACCESS_KEY_ID=<AWS_KEY>
LITESTREAM_SECRET_ACCESS_KEY=<AWS_SECRET>
```

**Opzione B: Cron Backup Semplice**

```bash
# Sulla VM: crontab -e
# Backup giornaliero alle 2 AM
0 2 * * * docker exec backend sqlite3 /app/data/db.sqlite3 ".backup /app/backups/db-$(date +\%Y\%m\%d).sqlite3"

# Cleanup backups > 7 giorni
0 3 * * * find /app/backups -name "db-*.sqlite3" -mtime +7 -delete
```

---

### FASE 4: Testing (Giorno 2)

**4.1 Test Deploy Manuale**

```bash
# Trigger workflow manualmente da GitHub Actions UI
# oppure
git commit -m "Test deploy" --allow-empty
git push origin main

# Monitora:
# 1. GitHub Actions logs
# 2. Server logs: ssh deploy@server "docker compose logs -f"
# 3. Health check: curl https://myapp.com/health
```

**4.2 Test Rollback**

```bash
# SSH sulla VM
cd /app

# Cambia TAG nel docker-compose.yml a commit precedente
sed -i 's/TAG=abc123/TAG=xyz789/' .env

# Deploy versione vecchia
docker compose pull
docker rollout backend
docker rollout frontend

# Verifica
curl https://myapp.com/health
```

**4.3 Test Backup/Restore**

```bash
# Test Litestream restore
litestream restore -o /tmp/test-restore.db s3://myapp-backups/production/database

# Oppure test backup manuale
docker exec backend sqlite3 /app/data/db.sqlite3 ".backup /tmp/backup.db"
ls -lh /tmp/backup.db
```

---

### FASE 5: Monitoring (Opzionale, Giorno 3+)

**Opzione Semplice: GitHub Actions + Healthcheck**

```yaml
# .github/workflows/health-check.yml
name: Health Check

on:
  schedule:
    - cron: '*/15 * * * *'  # Ogni 15 minuti

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Check API health
        run: |
          response=$(curl -s -o /dev/null -w "%{http_code}" https://myapp.com/health)
          if [ $response != 200 ]; then
            echo "Health check failed: $response"
            # Manda notifica
            exit 1
          fi
```

**Opzione Avanzata: UptimeRobot (Free)**
- https://uptimerobot.com
- Free tier: 50 monitor, check ogni 5 min
- Alert via email/Discord/Slack

---

## 7. CONFRONTO FINALE - COSTI & COMPLESSITÀ

| Opzione | Setup Time | Costo/Mese | Complessità | Affidabilità | Raccomandato |
|---------|-----------|-----------|-------------|--------------|--------------|
| **GitHub Actions + Docker Rollout** | 1-2 giorni | $0 | Media | Alta | ✅ **SI** |
| Dokploy | 3-4 ore | $0 | Media | Alta | ⚠️ Se volete UI |
| Coolify | 3-4 ore | $0 | Media | Alta | ⚠️ Se volete UI |
| Webhook Deploy | 2-3 ore | $0 | Bassa | Media | ❌ Troppo semplice |
| Watchtower | 30 min | $0 | Bassa | Bassa | ❌ Non mantenuto |
| Script Manuale | 0 (già ce l'avete) | $0 | Alta | Bassa | ❌ Da sostituire |

---

## 8. CHECKLIST PRE-DEPLOY

Usate questa checklist prima di ogni deploy in production:

### Codice & Test
- [ ] Tutti i test passano (`pytest`)
- [ ] Linting pulito (`ruff check`)
- [ ] No secret hardcoded (scan con `trufflehog`)
- [ ] Health check endpoint implementato e testato

### Docker
- [ ] Dockerfile usa multi-stage build
- [ ] Container NON esegue come root
- [ ] Healthcheck configurato in docker-compose.yml
- [ ] Immagini taggati con versione/SHA, non solo `latest`

### Sicurezza
- [ ] Secret gestiti tramite GitHub Secrets o file separato (non in repo!)
- [ ] HTTPS configurato (Certbot/Let's Encrypt)
- [ ] Firewall configurato (solo porte 80, 443, SSH aperte)
- [ ] SSH key-only (no password auth)

### Backup
- [ ] Backup automatici configurati (Litestream o cron)
- [ ] Backup testati (restore manuale almeno 1 volta)
- [ ] Retention policy configurata (es: 30 giorni)

### Monitoring
- [ ] Health check endpoint monitora database e servizi critici
- [ ] Uptime monitoring configurato (UptimeRobot/GitHub Actions)
- [ ] Log rotation configurato (Docker logs non crescono all'infinito)

### Rollback
- [ ] Strategia rollback testata manualmente
- [ ] Git tags per ogni release in production
- [ ] Documentazione rollback scritta (README.md)

**Fonti:**
- [FastAPI Production Deployment Checklist - Medium](https://medium.com/@rameshkannanyt0078/fastapi-production-deployment-checklist-e4daa8752016)
- [FastAPI Pre-Deployment Checklist - FastroAI](https://fastro.ai/blog/fastapi-deployment-checklist)

---

## 9. ALTERNATIVE PER IL FUTURO

Quando scalate oltre 1 server, considerate:

### Kubernetes (k8s)
- **Quando:** > 3 server, microservizi, team > 5 persone
- **Pro:** Industry standard, scaling automatico, self-healing
- **Contro:** Complessità elevata, overhead operativo
- **Costo:** GKE Autopilot da ~$70/mese

### Docker Swarm
- **Quando:** 2-5 server, team piccolo, non volete complessità k8s
- **Pro:** Più semplice di Kubernetes, gestione cluster integrata
- **Contro:** Meno feature, community più piccola
- **Costo:** $0 (built-in Docker)

### Managed Platform (Railway, Render, Fly.io)
- **Quando:** Volete zero ops, focus su prodotto
- **Pro:** Zero configurazione, auto-scaling, CI/CD incluso
- **Contro:** Costo più alto, meno controllo
- **Costo:** $5-20/mese/app

**Raccomandazione:** Restate su single server fino a quando avete traffico/revenue che giustifica la complessità. Non scalate prematuramente!

---

## 10. RISORSE UTILI

### Documentazione Ufficiale
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Docker Compose Production](https://docs.docker.com/compose/how-tos/production/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

### Tool & Repository
- [Docker Rollout - GitHub](https://github.com/wowu/docker-rollout)
- [Litestream - litestream.io](https://litestream.io/)
- [FastAPI Best Practices - GitHub](https://github.com/zhanymkanov/fastapi-best-practices)

### Tutorial & Guide
- [Zero-Downtime Docker Compose](https://supun.io/zero-downtime-deployments-docker-compose)
- [Docker Security Best Practices](https://betterstack.com/community/guides/scaling-docker/docker-security-best-practices/)
- [FastAPI Production Setup](https://render.com/articles/fastapi-production-deployment-best-practices)

---

## CONCLUSIONE

Per il vostro caso (FastAPI + SQLite, singola VM, 1-2 persone), la strategia vincente è:

🎯 **GitHub Actions + Docker Compose + Docker Rollout + Litestream**

**Perché funziona:**
1. **Setup una volta, funziona per sempre** - Dopo 1-2 giorni di setup, non ci pensate più
2. **Zero costi** - GitHub Actions free tier è più che sufficiente
3. **Zero downtime** - Docker Rollout garantisce deploy senza interruzioni
4. **Backup sicuri** - Litestream replica continuamente su S3 (costa centesimi)
5. **Rollback veloce** - Git tags + Docker Rollout = rollback in 2 minuti
6. **Scalabile** - Quando crescete, aggiungete server senza riscrivere tutto

**Setup Time:** 1-2 giorni
**Manutenzione:** ~1 ora/mese (aggiornare dipendenze)
**Affidabilità:** 99.9%+ (se fatto bene)

**Step immediati:**
1. Setup Docker Rollout sulla VM (30 min)
2. Aggiungere health check a FastAPI (15 min)
3. Creare GitHub Actions workflow (2-3 ore)
4. Testare deploy + rollback (1 ora)
5. Setup Litestream per backup (1-2 ore)

Dopo questo, ogni push su `main` = deploy automatico, testato, sicuro, zero-downtime. 🚀

---

**Ricerca completata il:** 10 Gennaio 2026
**Tempo ricerca:** ~2 ore
**Fonti consultate:** 40+ articoli, documentazione ufficiale, case study 2025-2026

**Prossimi step suggeriti:**
1. Validare raccomandazione con Rafa
2. Setup ambiente di staging per testare workflow
3. Implementare FASE 1 (GitHub Actions) prima
4. Documentare processo per riferimento futuro

---

## FONTI PRINCIPALI

### CI/CD & Deployment
- [12 Best CI/CD tools 2025 - Pieces](https://pieces.app/blog/best-ci-cd-tools)
- [14 best CI/CD tools 2025 - Northflank](https://northflank.com/blog/best-ci-cd-tools)
- [GitHub Actions Features](https://github.com/features/actions)

### Docker Best Practices
- [Modern Docker Best Practices 2025 - Talent500](https://talent500.com/blog/modern-docker-best-practices-2025/)
- [Docker Best Practices 2025 - BenchHub](https://docs.benchhub.co/docs/tutorials/docker/docker-best-practices-2025)
- [Docker Production Guide - Medium](https://medium.com/@mathur.danduprolu/docker-deep-dive-best-practices-for-using-docker-in-production-part-6-7-dcb8f6f4a057)

### Zero-Downtime Deployment
- [Docker Rollout - GitHub](https://github.com/wowu/docker-rollout)
- [Docker Rollout Guide - Virtualization Howto](https://www.virtualizationhowto.com/2025/06/docker-rollout-zero-downtime-deployments-for-docker-compose-made-simple/)
- [Zero-downtime Docker Compose - Supun.io](https://supun.io/zero-downtime-deployments-docker-compose)
- [Zero Downtime Nginx Docker - Tines](https://www.tines.com/blog/simple-zero-downtime-deploys-with-nginx-and-docker-compose/)

### FastAPI Production
- [FastAPI Deployment Guide 2025 - Zestminds](https://www.zestminds.com/blog/fastapi-deployment-guide/)
- [FastAPI Production Best Practices - Render](https://render.com/articles/fastapi-production-deployment-best-practices)
- [FastAPI Production Checklist - Medium](https://medium.com/@rameshkannanyt0078/fastapi-production-deployment-checklist-e4daa8752016)
- [FastAPI Pre-Deployment Checklist - FastroAI](https://fastro.ai/blog/fastapi-deployment-checklist)

### Security
- [Docker Secrets Security - GitGuardian](https://blog.gitguardian.com/how-to-handle-secrets-in-docker/)
- [Docker Secrets Guide - Spacelift](https://spacelift.io/blog/docker-secrets)
- [Docker Security Best Practices - Better Stack](https://betterstack.com/community/guides/scaling-docker/docker-security-best-practices/)
- [Environment Variables Best Practices - Docker Docs](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/)

### Backup & Rollback
- [FastAPI SQLite Litestream - Medium](https://medium.com/@hadiyolworld007/fastapi-sqlite-wal-with-litestream-cheap-ha-apis-with-point-in-time-restore-8fcf7e368740)
- [Docker Backup Guide - SimpleBackups](https://simplebackups.com/blog/docker-container-backup-restore-guide)
- [Docker Backup Best Practices - Collabnix](https://collabnix.com/the-importance-of-docker-container-backups-best-practices-and-strategies/)
- [Dokploy Rollbacks v0.24.0](https://dokploy.com/blog/v0-24-0-rollbacks-docker-volume-backups-more)

### PaaS Alternatives
- [Coolify vs Dokploy 2025 - Medium](https://girff.medium.com/coolify-vs-dokploy-the-ultimate-comparison-for-self-hosted-in-2025-8c63f1bda088)
- [Dokploy vs Coolify Real-World - Zero One Group](https://blog.zero-one-group.com/dokploy-vs-coolify-real-world-comparison-on-a-fresh-ec2-instance-eab584ceabc6)
- [Coolify vs Dokploy - Hostinger](https://www.hostinger.com/tutorials/coolify-vs-dokploy)
- [Why I Chose Dokploy - Medium](https://medium.com/@shubhthewriter/coolify-vs-dokploy-why-i-chose-dokploy-for-vps-deployment-in-2026-ea935c2fe9b5)

### Watchtower (Sconsigliato)
- [Watchtower Docker Auto Update - Better Stack](https://betterstack.com/community/guides/scaling-docker/watchtower-docker/)
- [Watchtower GitHub](https://github.com/containrrr/watchtower)
- [What's Up Docker Alternative - Virtualization Howto](https://www.virtualizationhowto.com/2025/11/whats-up-docker-keeps-your-home-lab-containers-updated-automatically/)

---

*Fine Report*
