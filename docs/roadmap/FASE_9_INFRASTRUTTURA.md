# FASE 9: INFRASTRUTTURA - Lo Sciame H24

> *"Mettiamo le ragazze online... prendono i dati... e facciamo la cosa REALE!"* - Rafa, 1 Gennaio 2026

**Data Creazione:** 1 Gennaio 2026
**Versione:** 1.0.0
**Stato:** IN CORSO

---

## VISIONE

```
+------------------------------------------------------------------+
|                                                                  |
|   OBIETTIVO: Lo sciame che IMPARA dagli ERRORI!                 |
|                                                                  |
|   Non "sempre acceso a fare nulla"                              |
|   Ma: VEDE + RACCOGLIE + IMPARA + SUGGERISCE                    |
|                                                                  |
|   KPIs per sapere:                                               |
|   - Servono piu api?                                            |
|   - Quali api funzionano meglio?                                |
|   - Dove perdiamo tempo?                                        |
|   - Cosa ripetere? Cosa evitare?                                |
|                                                                  |
|   FIDUCIA nel sistema = DATI REALI!                             |
|                                                                  |
+------------------------------------------------------------------+
```

---

## ARCHITETTURA

```
                    VM MIRACOLLO (gia esistente!)
                    +---------------------------+
                    |                           |
                    |  +---------------------+  |
                    |  |   Miracollo App     |  |  <-- GIA FUNZIONA!
                    |  |   (porta 8001)      |  |
                    |  +---------------------+  |
                    |                           |
                    |  +---------------------+  |
                    |  |   CervellaSwarm     |  |  <-- DA AGGIUNGERE
                    |  |   Monitor           |  |
                    |  |   (porta 3000)      |  |
                    |  +---------------------+  |
                    |            |              |
                    |  +---------------------+  |
                    |  |   Grafana +         |  |
                    |  |   Prometheus        |  |
                    |  |   (porta 9090)      |  |
                    |  +---------------------+  |
                    |            |              |
                    |  +---------------------+  |
                    |  |   Alert System      |  |
                    |  |   -> Telegram       |  |
                    |  +---------------------+  |
                    |                           |
                    +---------------------------+

                              |
                              v
                    +---------------------------+
                    |   swarm_memory.db         |
                    |   (SQLite - gia esiste!)  |
                    +---------------------------+
```

---

## FASI DI IMPLEMENTAZIONE

### FASE 9a: MONITORING H24 (Gennaio 2026)

**Obiettivo:** Vedere lo sciame anche quando non lavori!

| # | Task | Stato | Note |
|---|------|-------|------|
| 9a.1 | Verificare specs VM Miracollo | TODO | SSH e check RAM/CPU |
| 9a.2 | Creare docker-compose per monitoring | TODO | Grafana + Prometheus |
| 9a.3 | Configurare metriche base | TODO | task/giorno, success rate |
| 9a.4 | Setup alert Telegram | TODO | Error rate > 5% |
| 9a.5 | Deploy su VM | TODO | docker-compose up -d |
| 9a.6 | Test end-to-end | TODO | Verifica tutto funziona |

**Deliverable:** Dashboard accessibile da browser + Alert Telegram funzionanti

**Costo stimato:** 0 euro extra (VM gia pagata!)

---

### FASE 9b: TASK PROGRAMMATI (Febbraio 2026)

**Obiettivo:** Le api fanno cose UTILI anche senza te!

| # | Task | Stato | Note |
|---|------|-------|------|
| 9b.1 | Code review automatica Lun/Ven | TODO | cervella-reviewer |
| 9b.2 | GitHub webhook -> review PR | TODO | Quando arriva PR |
| 9b.3 | Weekly retrospective automatica | TODO | Venerdi 18:00 |
| 9b.4 | Health check progetti | TODO | Ogni 6h |

**Deliverable:** Almeno 3 task automatici funzionanti

---

### FASE 9c: AGENT AUTONOMO (Q2-Q3 2026)

**Obiettivo:** Lo sciame lavora mentre dormi!

| # | Task | Stato | Note |
|---|------|-------|------|
| 9c.1 | Studio Agent SDK vs Claude CLI | TODO | Cosa serve? |
| 9c.2 | Queue system (Redis) | TODO | Task in coda |
| 9c.3 | Orchestrator H24 | TODO | Processa coda |
| 9c.4 | Test su task reali | TODO | Non sprecare! |

**Deliverable:** Agent che processa task in background

---

## KPIs DA TRACCIARE

### Performance Sciame

| KPI | Descrizione | Target |
|-----|-------------|--------|
| **Task/giorno** | Quanti task completati | Baseline -> +20% |
| **Success rate** | % task senza errori | > 85% |
| **Tempo medio task** | Minuti per task | < 10 min |
| **Retry rate** | % task che servono retry | < 10% |

### Qualita

| KPI | Descrizione | Target |
|-----|-------------|--------|
| **Fix after agent** | % task che Regina deve fixare | < 20% |
| **Errori ripetuti** | Stesso errore 2+ volte | 0 |
| **Lezioni applicate** | Lezioni usate nei suggerimenti | 100% |

### Costi

| KPI | Descrizione | Target |
|-----|-------------|--------|
| **Token/task** | Consumo API medio | Minimize |
| **Costo/task** | Euro per task | Tracciare |
| **Infra cost** | VM + storage | < 15 euro/mese |

### Business

| KPI | Descrizione | Target |
|-----|-------------|--------|
| **Ore risparmiate/sett** | Tempo che Rafa risparmia | Misurare |
| **Task autonomi/sett** | Task senza intervento | > 10 |
| **Verso liberta geo** | Progresso obiettivo | Tracciare |

---

## STACK TECNOLOGICO

### Gia Presente

- Docker + Docker Compose (Miracollo, Contabilita)
- VM Miracollo (4GB RAM, 2 vCPU)
- SQLite (swarm_memory.db)
- Hook system funzionante

### Da Aggiungere

| Componente | Perche | Costo |
|------------|--------|-------|
| **Grafana** | Dashboard visuali | GRATIS (open source) |
| **Prometheus** | Raccolta metriche | GRATIS (open source) |
| **Alert Manager** | Notifiche | GRATIS (open source) |
| **Redis** | Queue system (FASE 9c) | GRATIS (open source) |

---

## DOCKER COMPOSE (FASE 9a)

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: cervellaswarm-prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: cervellaswarm-grafana
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    container_name: cervellaswarm-alertmanager
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"
    restart: unless-stopped

  # Exporter per metriche custom CervellaSwarm
  swarm-exporter:
    build:
      context: ./exporter
      dockerfile: Dockerfile
    container_name: cervellaswarm-exporter
    volumes:
      - ${SWARM_DB_PATH}:/data/swarm_memory.db:ro
    ports:
      - "9091:9091"
    restart: unless-stopped

networks:
  default:
    name: cervellaswarm-network

volumes:
  prometheus-data:
  grafana-data:
```

---

## METRICHE CUSTOM (swarm-exporter)

Lo swarm-exporter legge da `swarm_memory.db` e espone metriche Prometheus:

```python
# Metriche da esporre
swarm_tasks_total           # Totale task
swarm_tasks_success_total   # Task successo
swarm_tasks_failed_total    # Task falliti
swarm_agent_tasks{agent}    # Task per agent
swarm_lessons_total         # Lezioni apprese
swarm_patterns_total        # Pattern scoperti
swarm_last_task_timestamp   # Ultimo task
```

---

## ALERT RULES

```yaml
# alert_rules.yml
groups:
  - name: cervellaswarm
    rules:
      - alert: HighErrorRate
        expr: rate(swarm_tasks_failed_total[1h]) / rate(swarm_tasks_total[1h]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error rate alto (> 10%)"

      - alert: NoTasksIn6Hours
        expr: time() - swarm_last_task_timestamp > 21600
        for: 5m
        labels:
          severity: info
        annotations:
          summary: "Nessun task nelle ultime 6 ore"

      - alert: AgentDown
        expr: up{job="swarm-exporter"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Swarm exporter non raggiungibile!"
```

---

## CHECKLIST PRE-DEPLOY

**Prima di deployare su VM:**

- [ ] SSH funziona
- [ ] Docker installato su VM
- [ ] Spazio disco sufficiente (> 10GB liberi)
- [ ] Porta 3000 accessibile (Grafana)
- [ ] Porta 9090 accessibile (Prometheus)
- [ ] .env configurato con GRAFANA_PASSWORD
- [ ] Backup swarm_memory.db
- [ ] Test locale completato

---

## TIMELINE

```
GENNAIO 2026:
  Sett 1: Studio + Verifica VM
  Sett 2: Docker compose + Test locale
  Sett 3: Deploy su VM + Dashboard base
  Sett 4: Alert Telegram + Documentazione

FEBBRAIO 2026:
  Sett 1-2: Task programmati (code review, health check)
  Sett 3-4: GitHub webhooks + Weekly retro

MARZO 2026:
  Sett 1-2: Queue system (Redis)
  Sett 3-4: Agent autonomo POC
```

---

## PRINCIPI GUIDA

```
+------------------------------------------------------------------+
|                                                                  |
|   1. GRADUALE - Non tutto insieme, passo dopo passo             |
|   2. UTILE - Solo cose che portano valore                       |
|   3. MISURABILE - KPIs per ogni decisione                       |
|   4. REVERSIBILE - Possiamo sempre tornare indietro             |
|   5. ECONOMICO - Usare VM esistente, open source                |
|                                                                  |
|   "Non accendiamo la luce in una stanza vuota!"                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

## LINK UTILI

- VISIONE_REGINA_2026.md - La visione originale
- RICERCA_INFRASTRUTTURA_H24.md - Studio best practices
- scripts/memory/ - Script memoria esistenti
- .claude/hooks/ - Hook configurati

---

*"Ogni giorno un mattoncino. Nessun giorno senza progresso. Ma mai di fretta."*

*Creato: 1 Gennaio 2026*
*Sessione: 35*
