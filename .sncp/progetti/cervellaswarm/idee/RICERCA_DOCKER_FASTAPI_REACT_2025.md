# Ricerca Docker: FastAPI + React 19 + Vite - Best Practices 2025/2026

**Data**: 13 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Status**: ✅ COMPLETA

---

## TL;DR - Raccomandazioni Chiave

1. **Backend**: Multi-stage build con `python:3.11-slim`, non-root user, layer caching ottimizzato
2. **Frontend**: Multi-stage build con `node:20-alpine` + `nginx:alpine`, hot reload in dev
3. **Cache Busting**: Vite lo fa AUTOMATICAMENTE con hash nei filename (zero config!)
4. **Versioning**: ARG per build-time + ENV per runtime, passato via docker-compose
5. **Dev vs Prod**: Dockerfile separati (`.dev` e `.prod`) o target multi-stage

---

## 1. DOCKERFILE BACKEND (FastAPI + Python 3.11 + SQLite)

### Approccio Consigliato: Multi-Stage Build

```dockerfile
# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching!)
COPY requirements.txt .

# Install dependencies in /install prefix
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================
# Stage 2: Production
# ============================================
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=appuser:appuser ./app ./app

# Switch to non-root user
USER appuser

# Version metadata (ARG -> ENV pattern)
ARG VERSION=unknown
ENV APP_VERSION=$VERSION

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Use exec form for proper signal handling
CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--proxy-headers"]
```

### Alternative: Single-Stage Semplice (OK per progetti piccoli)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy requirements first (layer caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy app
COPY --chown=appuser:appuser ./app ./app

USER appuser

ARG VERSION=unknown
ENV APP_VERSION=$VERSION

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
```

### Development Dockerfile (Dockerfile.dev)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dev dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Hot reload: code mounted via volume in docker-compose
EXPOSE 8000

# Use --reload for hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Best Practices Backend

| Pratica | Motivo | Fonte |
|---------|--------|-------|
| `python:3.11-slim` | 45MB vs 125MB (full) | Better Stack |
| Multi-stage build | Builder + Runtime = ~225MB | FastAPI Docker Comparison |
| Copy requirements FIRST | Layer caching: cambio codice ≠ reinstall deps | Better Stack |
| `pip install --no-cache-dir` | Riduce image size | Docker Best Practices |
| Non-root user | Security hardening | Multiple sources |
| Exec form CMD `["fastapi", "run"]` | Proper signal handling (SIGTERM) | Better Stack |
| `--proxy-headers` | Per reverse proxy (nginx, Caddy) | FastAPI Docs |

---

## 2. DOCKERFILE FRONTEND (React 19 + Vite + TypeScript)

### Production: Multi-Stage con Nginx

```dockerfile
# ============================================
# Stage 1: Builder
# ============================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first (layer caching!)
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production=false

# Copy source
COPY . .

# Build-time environment variables (Vite)
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

ARG VERSION=unknown
ENV VITE_APP_VERSION=$VERSION

# Build for production (output: /app/dist)
RUN npm run build

# ============================================
# Stage 2: Nginx Production
# ============================================
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Version metadata
ARG VERSION=unknown
ENV APP_VERSION=$VERSION

# Expose port
EXPOSE 80

# nginx starts automatically in alpine image
```

### Alternative: nginxinc/nginx-unprivileged (Security++)

```dockerfile
# Stage 2: Use unprivileged nginx
FROM nginxinc/nginx-unprivileged:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080

# Runs as non-root by default
```

### Development Dockerfile (Dockerfile.dev)

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Hot reload: source mounted via volume in docker-compose
EXPOSE 5173

# Vite dev server with host 0.0.0.0 for Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### Best Practices Frontend

| Pratica | Motivo | Fonte |
|---------|--------|-------|
| `node:20-alpine` | Smallest Node image (~40MB) | Docker Hub |
| `npm ci` | Reproducible installs, faster | npm docs |
| Multi-stage | Elimina Node.js/tools da prod (~20MB finale) | Multiple sources |
| `nginx:alpine` | Serve statico ottimale (~25MB) | Docker Hub |
| Build args per VITE_* | Vite usa env vars prefissate VITE_ | Vite Docs |
| `--host 0.0.0.0` dev | Vite dev server accessibile fuori container | Vite Docs |

---

## 3. NGINX.CONF (Produzione)

### Configurazione Completa per SPA

```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Security: hide nginx version
    server_tokens off;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_comp_level 6;
    gzip_vary on;
    gzip_min_length 256;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # index.html: NEVER CACHE (must be fresh!)
    location = /index.html {
        add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
        try_files $uri =404;
    }

    # Static assets with hash: CACHE FOREVER (1 year)
    location ~* ^/assets/.*\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, no-transform, immutable";
        try_files $uri =404;
    }

    # SPA client-side routing: fallback to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Block access to hidden files
    location ~ /\. {
        deny all;
    }
}
```

### Nginx per nginxinc/nginx-unprivileged

```nginx
server {
    listen 8080;  # Non-root can't use port 80
    # ... rest is identical
}
```

### Best Practices Nginx

| Pratica | Motivo | Fonte |
|---------|--------|-------|
| `try_files $uri /index.html` | Client-side routing funziona | DEV Community |
| `gzip on` + types | 80-90% riduzione JS/CSS | Multiple sources |
| index.html NO cache | Sempre versione latest | Better Stack |
| /assets cache 1y | Vite usa hash → safe | Vite Docs |
| Security headers | Defense in depth | OWASP |

---

## 4. DOCKER-COMPOSE.YML

### Development (Hot Reload)

```yaml
version: '3.9'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: dev-backend
    volumes:
      # Mount source for hot reload
      - ./backend/app:/app/app
      # Optional: exclude pycache
      - /app/app/__pycache__
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./dev.db
      - ENVIRONMENT=development
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - dev-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: dev-frontend
    volumes:
      # Mount source for hot reload
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
      - ./frontend/index.html:/app/index.html
      - ./frontend/vite.config.ts:/app/vite.config.ts
      # Exclude node_modules from mount
      - /app/node_modules
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
      # Enable polling for Docker Desktop file watch
      - CHOKIDAR_USEPOLLING=true
    depends_on:
      - backend
    networks:
      - dev-network

networks:
  dev-network:
    driver: bridge
```

### Production (Con versioning)

```yaml
version: '3.9'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      args:
        VERSION: ${VERSION:-latest}
    container_name: prod-backend
    environment:
      - DATABASE_URL=sqlite:///./data/prod.db
      - ENVIRONMENT=production
    volumes:
      # Persist SQLite database
      - backend-data:/app/data
    ports:
      - "8000:8000"
    restart: unless-stopped
    networks:
      - prod-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        VERSION: ${VERSION:-latest}
        VITE_API_URL: ${VITE_API_URL:-http://localhost:8000}
    container_name: prod-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - prod-network

volumes:
  backend-data:

networks:
  prod-network:
    driver: bridge
```

### .env File (per docker-compose)

```bash
# Version
VERSION=1.0.0

# Frontend build-time vars
VITE_API_URL=http://localhost:8000

# Backend runtime vars
DATABASE_URL=sqlite:///./data/prod.db
ENVIRONMENT=production
```

### Best Practices Docker Compose

| Pratica | Motivo | Fonte |
|---------|--------|-------|
| Volume mount src in dev | Hot reload funziona | OneUpTime |
| Exclude node_modules | Keep in container, evita conflitti | Multiple sources |
| CHOKIDAR_USEPOLLING | Docker Desktop file watch fix | GitHub Issues |
| --reload per FastAPI | Hot reload backend | FastAPI Docs |
| depends_on | Ordine startup | Docker Docs |
| healthcheck in prod | Resilienza | Docker Docs |
| restart: unless-stopped | Auto-restart on crash | Docker Docs |

---

## 5. .DOCKERIGNORE

### Backend (Python/FastAPI)

```dockerignore
# Git
.git
.gitignore

# Python
__pycache__
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
venv/
env/
ENV/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.db
*.sqlite3
*.log
.env
.env.*
README.md
docs/
tests/

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore
```

### Frontend (React/Vite)

```dockerignore
# Git
.git
.gitignore

# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Build outputs
dist/
dist-ssr/
build/

# Testing
coverage/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.*
!.env.example

# Project specific
README.md
docs/

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore
```

### Best Practices .dockerignore

| Cosa Escludere | Motivo | Fonte |
|----------------|--------|-------|
| `.git/` | Mai serve in container | Better Stack |
| `node_modules/` | Rebuilt in container | TestDriven.io |
| `__pycache__/` | Python bytecode, rebuilt | Better Stack |
| `*.log`, `.env` | Security + size | Multiple sources |
| `tests/`, `docs/` | Not needed in prod | Multiple sources |
| `Dockerfile*` | Meta-recursion | Common sense |

---

## 6. CACHE BUSTING (Vite)

### Come Funziona (AUTOMATICO!)

**Vite gestisce il cache busting AUTOMATICAMENTE in produzione.**

#### Build Output Example

```bash
npm run build

# Output:
dist/
├── index.html
└── assets/
    ├── index-a1b2c3d4.js      # Hash automatico!
    ├── vendor-e5f6g7h8.js     # Hash automatico!
    └── index-i9j0k1l2.css     # Hash automatico!
```

#### index.html (Generated)

```html
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/assets/index-i9j0k1l2.css">
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/assets/index-a1b2c3d4.js"></script>
  </body>
</html>
```

### Meccanismo

1. **Build**: Vite genera hash basati sul CONTENUTO del file
2. **Cambio codice**: Hash cambia → nuovo filename
3. **Browser**: Vede nuovo filename → download nuovo file
4. **Cache**: Vecchi file con hash diverso → ignorati

### Configurazione (Opzionale)

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // Customizza naming (default va benissimo!)
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  }
})
```

### Nginx Strategy (COMBINATA)

```nginx
# index.html: NO CACHE (sempre fresh per nuovi hash)
location = /index.html {
    add_header Cache-Control "no-store, no-cache, must-revalidate";
}

# /assets/: CACHE FOREVER (hash = immutable)
location ~* ^/assets/.*$ {
    expires 1y;
    add_header Cache-Control "public, no-transform, immutable";
}
```

### Public Folder (Files senza hash)

Files in `public/` NON vengono hashati. Per cache busting manuale:

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    {
      name: 'html-transform',
      transformIndexHtml(html) {
        // Add version query param to non-hashed files
        return html.replace(
          '/config.js',
          `/config.js?v=${process.env.VERSION || Date.now()}`
        )
      }
    }
  ]
})
```

### Best Practices Cache Busting

| Pratica | Motivo | Fonte |
|---------|--------|-------|
| Vite default (hash in filename) | Zero config, bulletproof | Vite Docs |
| index.html NO cache | Entry point must be fresh | Multiple sources |
| /assets cache 1y | Hash = safe to cache forever | Vite Docs |
| `immutable` header | Browser NEVER revalidates | MDN |
| Public folder: manual version | Files senza hash need query param | GitHub Discussions |

---

## 7. VERSIONING (ARG + ENV Pattern)

### Pattern Consigliato

```dockerfile
# Dockerfile (Backend)
ARG VERSION=unknown
ENV APP_VERSION=$VERSION

# Dockerfile (Frontend)
ARG VERSION=unknown
ENV VITE_APP_VERSION=$VERSION
```

### Docker Compose (Passa version)

```yaml
# docker-compose.yml
services:
  backend:
    build:
      context: ./backend
      args:
        VERSION: ${VERSION:-dev}

  frontend:
    build:
      context: ./frontend
      args:
        VERSION: ${VERSION:-dev}
```

### .env File

```bash
VERSION=1.2.3
```

### Comandi

```bash
# Dev (senza version)
docker-compose up --build

# Prod (con version)
VERSION=1.2.3 docker-compose -f docker-compose.prod.yml up --build

# O con .env
echo "VERSION=1.2.3" > .env
docker-compose -f docker-compose.prod.yml up --build
```

### Esporre Version nell'App

#### Backend (FastAPI)

```python
# app/main.py
import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/version")
def get_version():
    return {"version": os.getenv("APP_VERSION", "unknown")}
```

#### Frontend (React)

```typescript
// src/config.ts
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || 'unknown';

// src/App.tsx
import { APP_VERSION } from './config';

function App() {
  return (
    <div>
      <footer>Version: {APP_VERSION}</footer>
    </div>
  );
}
```

### CI/CD Integration

```bash
# GitHub Actions example
VERSION=$(git describe --tags --always)
docker build --build-arg VERSION=$VERSION -t myapp:$VERSION .
```

### Best Practices Versioning

| Pratica | Motivo | Fonte |
|---------|--------|-------|
| ARG for build-time | Baked into image | Docker Docs |
| ENV for runtime | App can read it | Docker Docs |
| `VERSION=${VERSION:-dev}` | Default fallback | Docker Compose Docs |
| SemVer (1.2.3) | Standard versioning | semver.org |
| Git tag/commit in CI | Traceable builds | Industry standard |

---

## 8. COMANDI OPERATIVI

### Development

```bash
# Start dev environment (hot reload)
docker-compose up

# Rebuild after dependency changes
docker-compose up --build

# Stop
docker-compose down

# Clean everything (volumes too)
docker-compose down -v

# Logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Production

```bash
# Build with version
VERSION=1.2.3 docker-compose -f docker-compose.prod.yml build

# Start production
VERSION=1.2.3 docker-compose -f docker-compose.prod.yml up -d

# Check health
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/health

# Stop
docker-compose -f docker-compose.prod.yml down

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Single Container Build

```bash
# Backend
docker build -t myapp-backend:1.2.3 --build-arg VERSION=1.2.3 ./backend

# Frontend
docker build -t myapp-frontend:1.2.3 --build-arg VERSION=1.2.3 --build-arg VITE_API_URL=http://api.example.com ./frontend

# Run
docker run -p 8000:8000 myapp-backend:1.2.3
docker run -p 80:80 myapp-frontend:1.2.3
```

### Debugging

```bash
# Enter running container
docker exec -it prod-backend sh
docker exec -it prod-frontend sh

# Check logs
docker logs prod-backend
docker logs prod-frontend

# Inspect image
docker inspect myapp-backend:1.2.3
```

---

## 9. STRUTTURA PROGETTO CONSIGLIATA

```
project-root/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   └── db/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile              # Production
│   ├── Dockerfile.dev          # Development
│   └── .dockerignore
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── nginx.conf              # For production image
│   ├── Dockerfile              # Production (multi-stage)
│   ├── Dockerfile.dev          # Development
│   └── .dockerignore
│
├── docker-compose.yml          # Development
├── docker-compose.prod.yml     # Production
├── .env.example
└── README.md
```

---

## 10. CHECKLIST PRE-DEPLOY

### Backend

- [ ] `requirements.txt` aggiornato e testato
- [ ] Non-root user nel Dockerfile
- [ ] Health check endpoint `/health` implementato
- [ ] Environment variables documentate
- [ ] `.dockerignore` completo
- [ ] SQLite database in volume persistente
- [ ] Logging configurato
- [ ] `--proxy-headers` se dietro reverse proxy

### Frontend

- [ ] `npm run build` funziona localmente
- [ ] VITE_API_URL corretto per production
- [ ] nginx.conf testato
- [ ] Cache headers verificati
- [ ] Client-side routing funziona
- [ ] `.dockerignore` completo
- [ ] Build args passati correttamente
- [ ] Version visibile nell'app

### Docker Compose

- [ ] Networks configurati
- [ ] Volumes per dati persistenti
- [ ] Health checks definiti
- [ ] Restart policies impostate
- [ ] Port mapping corretto
- [ ] depends_on impostato
- [ ] VERSION in .env

---

## 11. TROUBLESHOOTING COMUNE

### Hot Reload Non Funziona (Dev)

**Problema**: Modifiche al codice non si riflettono in container

**Soluzioni**:

```yaml
# Frontend: aggiungi CHOKIDAR_USEPOLLING
environment:
  - CHOKIDAR_USEPOLLING=true

# Backend: verifica volume mount
volumes:
  - ./backend/app:/app/app  # Path corretto?
```

### node_modules Conflitti (Frontend Dev)

**Problema**: Errori strani dopo `docker-compose up`

**Soluzione**:

```yaml
volumes:
  - ./frontend/src:/app/src
  - /app/node_modules  # Esclude dal mount!
```

### NGINX 404 su Route React

**Problema**: `/about` funziona in dev, 404 in prod

**Soluzione**:

```nginx
# nginx.conf: aggiungi try_files
location / {
    try_files $uri $uri/ /index.html;  # ← ESSENZIALE per SPA!
}
```

### Permission Denied (SQLite/Volumes)

**Problema**: `PermissionError: [Errno 13]`

**Soluzione**:

```dockerfile
# Dockerfile: crea user e setta ownership
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

USER appuser
```

### Build Args Non Passano

**Problema**: `VERSION=unknown` nell'app

**Soluzione**:

```yaml
# docker-compose.yml: verifica args section
build:
  context: ./backend
  args:
    VERSION: ${VERSION:-dev}  # ← Needs args: block!
```

### Cache Busting Non Funziona

**Problema**: Browser usa vecchio JS dopo deploy

**Verifica**:

1. Vite genera hash? → Check `dist/assets/`
2. index.html ha NO cache header? → Check nginx config
3. Browser fa hard refresh? → Ctrl+Shift+R

---

## 12. RISORSE E FONTI

### Documentazione Ufficiale

- [Docker Best Practices: ARG and ENV](https://www.docker.com/blog/docker-best-practices-using-arg-and-env-in-your-dockerfiles/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [Vite Build Production](https://vitejs.dev/guide/build.html)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

### Guide Recenti (2025-2026)

- [FastAPI Docker Best Practices - Better Stack](https://betterstack.com/community/guides/scaling-python/fastapi-docker-best-practices/)
- [React Vite + Docker + Nginx - Build with Matija](https://www.buildwithmatija.com/blog/production-react-vite-docker-deployment)
- [Docker Hot Reloading - OneUpTime (Jan 2026)](https://oneuptime.com/blog/post/2026-01-06-docker-hot-reloading/view)
- [Guide to Containerizing Modern SPA - DEV Community](https://dev.to/it-wibrc/guide-to-containerizing-a-modern-javascript-spa-vuevitereact-with-a-multi-stage-nginx-build-1lma)

### Best Practices

- [Docker Multi-Stage Builds for Python](https://collabnix.com/docker-multi-stage-builds-for-python-developers-a-complete-guide/)
- [Building Production-Ready Vite Docker Image](https://mahendhiran.medium.com/building-a-production-ready-docker-image-for-a-react-vite-application-using-multi-stage-builds-3a34fe4a1c68)
- [.dockerignore Patterns](https://testdriven.io/tips/6850ab62-9323-4dca-8ddf-8db1d479accc/)

### Cache Busting & Performance

- [Ultimate Guide to Cache-Busting React](https://maxtsh.medium.com/the-ultimate-guide-to-cache-busting-for-react-production-applications-d583e4248f02)
- [Nginx Cache Config for SPAs](https://dev.to/vishwark/part-3-supercharge-your-react-app-with-nginx-caching-compression-load-balancing-2hca)

### Security

- [nginxinc/nginx-unprivileged](https://hub.docker.com/r/nginxinc/nginx-unprivileged)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)

---

## 13. DECISIONE FINALE

### Per Miracollo/Progetti CervellaSwarm

**RACCOMANDAZIONE**:

1. **Backend**: Multi-stage build con `python:3.11-slim`, non-root user
2. **Frontend**: Multi-stage build con `node:20-alpine` + `nginx:alpine`
3. **Dev**: Dockerfiles separati (`.dev`) con hot reload
4. **Prod**: Multi-stage con versioning ARG/ENV
5. **Cache**: Vite default (zero config), nginx headers corretti
6. **Compose**: File separati `docker-compose.yml` (dev) e `.prod.yml` (prod)

**NEXT STEPS**:

1. Creare template Dockerfiles in `.templates/docker/`
2. Testare con progetto Miracollo
3. Documentare in `docs/DOCKER_SETUP.md`

---

**FINE RICERCA**

*Cervella Researcher - 13 Gennaio 2026* 🔬
