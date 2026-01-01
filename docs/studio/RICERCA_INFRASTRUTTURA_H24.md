# RICERCA: Infrastruttura per Agent AI H24

> **Data:** 1 Gennaio 2026
> **Ricercatrice:** cervella-researcher
> **Obiettivo:** Best practices 2025-2026 per hosting agent AI H24

---

## EXECUTIVE SUMMARY

| Aspetto | Raccomandazione | Perche |
|---------|----------------|--------|
| **Hosting** | VM Miracollo (gia esiste!) | Zero costi extra |
| **Deploy** | Docker su VM | Isolamento + portabilita |
| **Monitoring** | Grafana + Prometheus | GRATIS (open source) |
| **Database** | SQLite (gia funziona!) | PostgreSQL quando >1000 req/giorno |
| **Queue** | Redis (FASE 9c) | Semplice, veloce |

**Budget stimato:** ~0-5 euro/mese extra (VM gia pagata!)

---

## 1. HOSTING

### Trend 2025-2026 (Uptime Institute Survey)

- 46% on-premises (controllo diretto)
- 34% colocation
- 14% public cloud

### Per CervellaSwarm

**RACCOMANDAZIONE:** Usare VM Miracollo esistente!

- Gia pagata
- Gia configurata con Docker
- Spazio sufficiente per monitoring
- Zero setup aggiuntivo

---

## 2. MONITORING

### Tool Comparison

| Tool | Costo | Pro | Contro |
|------|-------|-----|--------|
| **Grafana + Prometheus** | GRATIS | Full control, community enorme | Setup iniziale |
| Datadog | $$ | Turnkey | Vendor lock-in |
| New Relic | $$$ | APM completo | Overkill |

### RACCOMANDAZIONE: Grafana + Prometheus

- Zero costi (open source!)
- Industry standard
- Scalabile
- Nessun vendor lock-in

### Metriche Chiave

| Categoria | Metriche |
|-----------|----------|
| Performance | Latency, Throughput, Task/giorno |
| Errors | Error rate, Retry count |
| Resources | CPU, Memory, Disk |
| Business | Success rate, Cost per task |

---

## 3. DATABASE

### SQLite vs PostgreSQL

| Aspetto | SQLite | PostgreSQL |
|---------|--------|------------|
| Setup | Zero | Richiede config |
| Concurrency | 1 write | Centinaia |
| Use case | < 1000 req/giorno | > 1000 req/giorno |

### RACCOMANDAZIONE

- **ORA:** SQLite (gia funziona!)
- **FUTURO:** PostgreSQL quando serve

---

## 4. SECURITY

### Best Practices 2025

| Pratica | Implementazione |
|---------|-----------------|
| API Keys | Environment variables (.env) |
| Mai committare | .gitignore per .env |
| Network | Docker internal networks |

---

## 5. BACKUP

### Regola 3-2-1

- 3 copie dei dati
- 2 tipi storage diversi
- 1 copia off-site

### Per CervellaSwarm

| Cosa | Frequenza | Dove |
|------|-----------|------|
| Database | Ogni 6h | Hetzner + GitHub |
| Code | Ogni commit | GitHub |
| Config | Ogni modifica | Git |

---

## 6. COSTI

### Confronto Provider

| Provider | Config | Costo/mese |
|----------|--------|------------|
| **VM Miracollo** | 4GB RAM, 2 vCPU | **GIA PAGATA** |
| Hetzner CX21 | 4GB RAM, 2 vCPU | 4.90 euro |
| DigitalOcean | 4GB RAM, 2 vCPU | $24 |
| AWS t3.medium | 4GB RAM, 2 vCPU | ~$30 |

**VINCITORE:** VM Miracollo (zero costi extra!)

---

## CONCLUSIONE

Per CervellaSwarm H24, la strategia e:

1. **Usare VM Miracollo** - Gia pagata!
2. **Docker Compose** - Gia presente nei progetti
3. **Grafana + Prometheus** - Gratuito
4. **SQLite** - Gia funziona
5. **Redis** - Solo quando serve (FASE 9c)

**Timeline:** Pronto in GENNAIO 2026!

---

## FONTI

- Uptime Institute AI Infrastructure Survey 2025
- Docker best practices documentation
- Prometheus/Grafana official docs
- Claude Code deployment guides

---

*Ricerca completata: 1 Gennaio 2026*
*"Studiare prima di agire - sempre!"*
