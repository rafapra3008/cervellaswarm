# RICERCA: Docker Best Practices 2026 - Miracollook

> **Data:** 20 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Progetto:** Miracollook Email Client (Porta 8002)
> **Stack:** Python 3.13 + FastAPI (backend) | React 19 + Vite 7 (frontend)

---

## TL;DR

**RACCOMANDAZIONE:**
- Backend: `python:3.13-slim` (NON alpine)
- Frontend: Multi-stage con `node:20-alpine` + `nginx:1.25-alpine`
- Security: Non-root user, secrets via file/env, healthchecks
- Compose: Version 3.8+, depends_on con service_healthy

**Immagini Base Esatte (2026):**
```
python:3.13-slim-bookworm  # Backend (130MB)
node:20-alpine             # Frontend build stage (57MB)
nginx:1.25-alpine          # Frontend runtime (23MB)
```

---

## 1. BACKEND DOCKERFILE (Python 3.13 + FastAPI)

### Template Multi-Stage Production-Ready

```dockerfile
# =============================================================================
# STAGE 1: Builder - Installa dipendenze
# =============================================================================
FROM python:3.13-slim-bookworm AS builder

# Variabili d'ambiente Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Installa dipendenze di sistema per build (se necessarie)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia SOLO requirements.txt (layer caching!)
COPY requirements.txt .

# Installa dipendenze in una directory separata
RUN pip install --user --no-warn-script-location -r requirements.txt

# =============================================================================
# STAGE 2: Runtime - Immagine finale minimale
# =============================================================================
FROM python:3.13-slim-bookworm

# Variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/appuser/.local/bin:$PATH

WORKDIR /app

# Crea utente non-root
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app

# Copia dipendenze installate dallo stage builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copia il codice dell'applicazione
COPY --chown=appuser:appuser . .

# Crea directory per database SQLite (se necessario)
RUN mkdir -p /app/data && chown appuser:appuser /app/data

# Cambia a utente non-root
USER appuser

# Esponi porta
EXPOSE 8002

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8002/health', timeout=5)" || exit 1

# Comando di avvio (Uvicorn + Gunicorn per produzione)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "2"]
```

### Perché `python:3.13-slim` e NON `alpine`?

**PRO slim:**
- ✅ Usa glibc (compatibilità totale con package Python)
- ✅ Wheel precompilati disponibili (build veloce)
- ✅ Nessun problema con pacchetti C-based
- ✅ 130MB finale (accettabile)

**CONTRO alpine:**
- ❌ Usa musl (incompatibilità con molti package)
- ❌ Build da sorgente = lento + pesante
- ❌ Dimensione finale simile a slim dopo build
- ❌ Problemi noti con cryptography, numpy, pandas

**Fonte:** FastAPI creator raccomanda `slim` per produzione.

---

## 2. FRONTEND DOCKERFILE (React 19 + Vite 7)

### Template Multi-Stage con Nginx

```dockerfile
# =============================================================================
# STAGE 1: Build - Compila React con Vite
# =============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copia package files (layer caching!)
COPY package.json package-lock.json ./

# Installa dipendenze
RUN npm ci --silent

# Copia codice sorgente
COPY . .

# Build produzione
ENV NODE_ENV=production
RUN npm run build

# =============================================================================
# STAGE 2: Runtime - Nginx per servire static files
# =============================================================================
FROM nginx:1.25-alpine

# Copia build da stage precedente
COPY --from=builder /app/dist /usr/share/nginx/html

# Copia configurazione Nginx custom
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Crea utente non-root (nginx usa già 'nginx' user)
# Nginx alpine già configurato per non-root

# Esponi porta
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Nginx parte automaticamente
CMD ["nginx", "-g", "daemon off;"]
```

---

## 3. NGINX CONFIGURATION (nginx.conf)

```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "fullscreen=(self)" always;

    # Content Security Policy (adatta ai tuoi CDN)
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' http://localhost:8002;" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # SPA routing - serve index.html per tutte le route non trovate
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (backend su 8002)
    location /api/ {
        proxy_pass http://backend:8002/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 4. DOCKER-COMPOSE.YML (Versione 3.8+)

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: miracollook-backend
    restart: unless-stopped

    ports:
      - "8002:8002"

    environment:
      - PYTHONUNBUFFERED=1
      - DATABASE_PATH=/app/data/miracollook.db
      # Secrets (vedi sezione 5)

    volumes:
      - ./data:/app/data  # SQLite database persistente
      - backend-logs:/app/logs

    networks:
      - miracollook-network

    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8002/health', timeout=5)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

    # Resource limits (produzione)
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 650M
        reservations:
          cpus: '0.25'
          memory: 256M

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: miracollook-frontend
    restart: unless-stopped

    ports:
      - "80:80"

    networks:
      - miracollook-network

    depends_on:
      backend:
        condition: service_healthy

    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 128M
        reservations:
          cpus: '0.1'
          memory: 64M

networks:
  miracollook-network:
    driver: bridge

volumes:
  backend-logs:
```

---

## 5. SECRETS MANAGEMENT

### Opzione 1: Environment Variables (Sviluppo/Test)

```bash
# .env (NON committare in git!)
GMAIL_CLIENT_ID=your-client-id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your-secret
OPENAI_API_KEY=sk-...
```

**docker-compose.yml:**
```yaml
services:
  backend:
    env_file:
      - .env
```

### Opzione 2: Docker Secrets (Produzione con Swarm)

```bash
# Crea secret
echo "sk-..." | docker secret create openai_api_key -

# Leggi secret in Python
with open('/run/secrets/openai_api_key', 'r') as f:
    api_key = f.read().strip()
```

**docker-compose.yml:**
```yaml
services:
  backend:
    secrets:
      - openai_api_key
      - gmail_client_secret

secrets:
  openai_api_key:
    external: true
  gmail_client_secret:
    external: true
```

### Opzione 3: File Secrets (Compose Standalone)

```yaml
services:
  backend:
    secrets:
      - openai_api_key

secrets:
  openai_api_key:
    file: ./secrets/openai_api_key.txt
```

**REGOLA:** MAI secrets in Dockerfile, MAI in git!

---

## 6. .dockerignore (ESSENZIALE!)

### Backend (.dockerignore)

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover

# IDE
.vscode/
.idea/
*.swp
*.swo

# Git
.git/
.gitignore

# Secrets & Config
.env
.env.*
secrets/
*.pem
*.key

# Database (sviluppo)
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
docker-compose.yml
.dockerignore
```

### Frontend (.dockerignore)

```
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build
dist/
build/

# Testing
coverage/

# IDE
.vscode/
.idea/
*.swp

# Git
.git/
.gitignore

# Environment
.env
.env.*

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Misc
README.md
```

---

## 7. COMANDI UTILI

### Build e Run

```bash
# Build singolo servizio
docker-compose build backend
docker-compose build frontend

# Build completo
docker-compose build

# Run con logs
docker-compose up

# Run in background
docker-compose up -d

# Logs in tempo reale
docker-compose logs -f backend

# Stop e rimuovi
docker-compose down

# Stop, rimuovi e pulisci volumi
docker-compose down -v
```

### Debugging

```bash
# Shell nel container
docker-compose exec backend bash
docker-compose exec frontend sh

# Verifica healthcheck
docker inspect --format='{{json .State.Health}}' miracollook-backend

# Network inspect
docker network inspect miracollook_miracollook-network

# Resource usage
docker stats
```

### Security Scan

```bash
# Installa Docker Scout (se non già presente)
docker scout quickview

# Scan immagine
docker scout cves miracollook-backend:latest

# Scan con raccomandazioni
docker scout recommendations miracollook-backend:latest
```

---

## 8. CHECKLIST PRE-PRODUZIONE

- [ ] Dockerfile usa multi-stage build
- [ ] Immagini base specifiche (no `:latest`)
- [ ] Utente non-root (USER 1001)
- [ ] .dockerignore completo
- [ ] Secrets NON in Dockerfile
- [ ] Healthcheck configurato
- [ ] Security headers in nginx
- [ ] Resource limits definiti
- [ ] Logs persistenti (volume)
- [ ] Database persistente (volume)
- [ ] Network isolata
- [ ] depends_on con service_healthy
- [ ] HTTPS in produzione (nginx + Let's Encrypt)
- [ ] Backup strategy per volumi
- [ ] Monitoring (Prometheus/Grafana)

---

## 9. DIFFERENZE DEV vs PROD

### Development

```yaml
services:
  backend:
    build: ./backend
    volumes:
      - ./backend:/app  # Hot reload
    environment:
      - DEBUG=true
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

### Production

```yaml
services:
  backend:
    image: registry.example.com/miracollook-backend:1.0.0
    restart: always
    environment:
      - DEBUG=false
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
```

---

## FONTI

### Python/FastAPI Docker
- [FastAPI Docker Best Practices - Better Stack](https://betterstack.com/community/guides/scaling-python/fastapi-docker-best-practices/)
- [FastAPI Official Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [Docker Multi-Stage Python Builds - Collabnix](https://collabnix.com/docker-multi-stage-builds-for-python-developers-a-complete-guide/)
- [Python Slim vs Alpine - Python Speed](https://pythonspeed.com/articles/base-image-python-docker-images/)

### React/Vite Docker
- [Containerizing JavaScript SPA with Nginx - DEV](https://dev.to/it-wibrc/guide-to-containerizing-a-modern-javascript-spa-vuevitereact-with-a-multi-stage-nginx-build-1lma)
- [React Vite Docker Production - Build with Matija](https://www.buildwithmatija.com/blog/production-react-vite-docker-deployment)
- [Multi-Stage Builds with React and Vite - Medium](https://medium.com/@ryanmambou/optimizing-docker-builds-a-practical-guide-to-multi-stage-builds-with-react-and-vite-c9692414961c)

### Docker Compose & Health Checks
- [Docker Compose Health Checks - Last9](https://last9.io/blog/docker-compose-health-checks/)
- [Docker Compose Services Reference](https://docs.docker.com/reference/compose-file/services/)
- [Control Startup Order - Docker Docs](https://docs.docker.com/compose/how-tos/startup-order/)

### Security
- [Docker Security Best Practices - Vibe App Scanner](https://vibeappscanner.com/docker-security-best-practices/)
- [Docker Security 2025 - Cloud Native Now](https://cloudnativenow.com/topics/cloudnativedevelopment/docker/docker-security-in-2025-best-practices-to-protect-your-containers-from-cyberthreats/)
- [Docker Secrets Management - GitGuardian](https://blog.gitguardian.com/how-to-handle-secrets-in-docker/)
- [Why Non-Root Containers - Broadcom](https://techdocs.broadcom.com/us/en/vmware-tanzu/bitnami-secure-images/bitnami-secure-images/services/bsi-doc/apps-tutorials-why-non-root-containers-are-important-for-security-index.html)

### Nginx Security Headers
- [Nginx Security Headers Setup - Medium](https://medium.com/@oryaacov/how-to-setup-a-secured-http-server-using-nginx-c7d8e85815a4)
- [React Content Security Policy Guide - StackHawk](https://www.stackhawk.com/blog/react-content-security-policy-guide-what-it-is-and-how-to-enable-it/)

---

## PROSSIMI STEP

1. **Creare file struttura:**
   ```
   miracollook/
   ├── backend/
   │   ├── Dockerfile
   │   └── .dockerignore
   ├── frontend/
   │   ├── Dockerfile
   │   ├── .dockerignore
   │   └── nginx.conf
   ├── docker-compose.yml
   ├── docker-compose.dev.yml
   └── .env.example
   ```

2. **Testing locale:**
   - Build e test in ambiente locale
   - Verifica healthcheck funzionanti
   - Test networking backend/frontend

3. **Security scan:**
   - Docker Scout su entrambe le immagini
   - Fix CVE se presenti

4. **Documentazione:**
   - README con istruzioni deploy
   - Guida secrets management
   - Troubleshooting guide

---

*Ricerca completata: 20 Gennaio 2026 - Cervella Researcher* 🔬
