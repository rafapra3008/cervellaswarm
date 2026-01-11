# RICERCA INFRASTRUTTURA DEFINITIVA 2026 - PARTE 3

> Continua da PARTE2

---

## 5. SELF-HOSTING (OWN HARDWARE)

### 5.1 Consumer GPUs (Entry-Level Self-Hosting)

#### RTX 4090 (24GB)

**Specs:**
- 24GB GDDR6X
- 16,384 CUDA cores
- 450W TDP
- PCIe 4.0 x16

**Pricing 2026:**
- New: $1,600-2,000
- Used: $1,200-1,500 (risk shortage 2026!)

**Performance per Qwen3-4B:**
- ✅ Sufficiente (7-8GB VRAM needed)
- Inference: ~50-80 tokens/sec
- Batch size: medium (fino 4-8 concurrent)

**Electricity Cost:**
```
450W × 24h/day × 30 giorni = 324 kWh/mese
324 kWh × $0.16/kWh (US average) = $51.84/mese
```

**Total Cost of Ownership (1 year):**
```
Hardware: $1,600
Electricity: $51.84 × 12 = $622
TOTALE: $2,222/anno = $185/mese amortized
```

**Break-Even vs Cloud:**
- Vast.ai RTX 4090: $192/mese
- Break-even: ~8.6 mesi
- Dopo 1 anno: $2,222 self vs $2,304 cloud (save $82)

**Pro:**
- Full control
- No latency to cloud
- Privacy (data on-premise)
- Long-term cheaper (dopo break-even)

**Contro:**
- Upfront cost $1,600
- Electricity ongoing ($52/mese)
- Maintenance (hardware failure risk)
- No SLA (se GPU muore, downtime!)
- Single point of failure

**Quando Usarlo:**
- Privacy-critical data
- Long-term (2+ years)
- Budget upfront disponibile
- In-house expertise

---

#### RTX 3090 (24GB) - Budget Option

**Pricing 2026:**
- Used: $600-900

**Specs:**
- 24GB GDDR6X (stesso VRAM di 4090!)
- 10,496 CUDA cores (meno di 4090)
- 350W TDP

**Performance:**
- ~70% performance di RTX 4090
- Ma: VRAM identica! (24GB)
- Inference Qwen3-4B: ~35-50 tokens/sec

**Electricity:**
```
350W × 24h × 30 giorni = 252 kWh/mese
252 kWh × $0.16/kWh = $40.32/mese
```

**TCO (1 year):**
```
Hardware: $750
Electricity: $40.32 × 12 = $484
TOTALE: $1,234/anno = $103/mese amortized
```

**Break-Even vs Cloud:**
- Vast.ai: $192/mese
- Savings: $89/mese (dopo break-even!)
- Break-even: ~4 mesi

**Raccomandazione:**
- ✅ **Best budget self-hosting option!**
- Performance OK per Qwen3-4B
- Fastest break-even (4 mesi)
- Used market availability alta

---

### 5.2 Server GPUs (Enterprise Self-Hosting)

#### NVIDIA A100 40GB (Used)

**Pricing 2026:**
- Used: $6,000-10,000
- New: $15,000-20,000 (se disponibile!)

**Specs:**
- 40GB HBM2e
- 6,912 CUDA cores
- 400W TDP
- Multi-Instance GPU (MIG) support

**Performance:**
- Enterprise-grade
- Inference Qwen3-4B: 100-150 tokens/sec
- Batch size: large (16-32 concurrent)
- MIG: split in 7 instances!

**Electricity:**
```
400W × 24h × 30 giorni = 288 kWh/mese
288 kWh × $0.16/kWh = $46.08/mese
```

**TCO (3 years):**
```
Hardware: $8,000
Electricity: $46.08 × 36 = $1,659
TOTALE: $9,659 / 36 mesi = $268/mese amortized
```

**Break-Even vs Cloud:**
- Lambda Labs A100: $792/mese
- Savings: $524/mese (dopo break-even!)
- Break-even: ~10 mesi

**Pro:**
- Enterprise reliability
- MIG support (multi-tenancy!)
- Performance best-in-class
- Long-term ROI eccellente

**Contro:**
- Upfront $8,000!
- Server infrastructure needed (rack, cooling, network)
- Expertise required
- Warranty risk (used hardware)

**Quando Usarlo:**
- Long-term (2+ years)
- Multiple workloads (MIG!)
- Budget upfront $8-10K disponibile
- In-house datacenter

---

#### NVIDIA A100 80GB (Used) - Overkill ma Future-Proof

**Pricing 2026:**
- Used: $12,000-18,000

**TCO (3 years):**
```
Hardware: $15,000
Electricity: $46.08 × 36 = $1,659
TOTALE: $16,659 / 36 mesi = $463/mese amortized
```

**Break-Even:**
- Lambda Labs A100 80GB: $950/mese
- Savings: $487/mese
- Break-even: ~16 mesi

**Raccomandazione:**
- ⚠️ Overkill per Qwen3-4B!
- OK se planning scaling to 13B+ models
- Future-proofing investment

---

### 5.3 Self-Hosting Additional Costs

**Infrastructure:**
- Server chassis: $500-1,500
- PSU (1200W+ per A100): $200-400
- Cooling (fans/liquid): $100-500
- Networking (10GbE): $100-300
- TOTALE: $900-2,700

**Maintenance:**
- Hardware failure risk: 2-5% per anno
- PSU replacement: $200-400 ogni 3-5 anni
- Downtime cost: variabile

**Space & Cooling:**
- Rack space: $50-200/mese (colo) o $0 (in-house)
- Extra AC: $20-50/mese (if needed)

**Total Hidden Costs:**
```
Setup: $900-2,700 one-time
Maintenance: $50-100/mese ongoing
```

---

### 5.4 Self-Hosting: Break-Even Analysis

| GPU | Upfront | Monthly | Break-Even vs Cloud | ROI Year 1 | ROI Year 3 |
|-----|---------|---------|---------------------|------------|------------|
| RTX 3090 Used | $750 | $40 elec | 4 mesi | +$71/mese | +$89/mese |
| RTX 4090 New | $1,600 | $52 elec | 8-9 mesi | -$7/mese | +$7/mese |
| A100 40GB Used | $8,000 | $46 elec | 10 mesi | +$480/mese | +$524/mese |
| A100 80GB Used | $15,000 | $46 elec | 16 mesi | +$441/mese | +$487/mese |

**Assumptions:**
- Cloud comparison: Vast.ai RTX 4090 $192/mese, Lambda A100 $792-950/mese
- Electricity: $0.16/kWh US average
- No infrastructure extra costs (conservative)

**Key Insight:**
- Consumer GPUs (3090/4090): break-even rapido ma savings limitati
- Server GPUs (A100): break-even lento MA savings enormi long-term

---

### 5.5 Self-Hosting Raccomandazione

**CERVELLA BABY - NO Self-Hosting (per ora)!** ❌

**Perché:**
1. **Volume basso:** 100-1000 req/giorno = cloud più economico
2. **Flexibility:** Scaling up/down impossible con hardware
3. **Risk:** Single point of failure, no SLA
4. **Upfront:** $750-15,000 capital locked
5. **Expertise:** Richiede DevOps in-house

**Quando considerare Self-Hosting:**
- Volume >10K req/giorno costante (break-even accelera!)
- Budget upfront >$8K disponibile
- Long-term commitment (2+ anni)
- Privacy/compliance requirements
- In-house datacenter già esistente

**Alternative Hybrid:**
- Cloud per production + self-host per dev/testing
- Savings: ~30-40% vs full cloud
- Complexity: media

---

## 6. ARCHITETTURA CONSIGLIATA

### 6.1 Entry Level (POC/MVP) - $50-200/mese

**Target:** Validazione idea, 10-100 req/giorno

**STACK:**
```
FRONTEND: Miracollo (existing)
    ↓
API GATEWAY: Cervella AI backend (existing VM)
    ↓
LLM INFERENCE: Google Colab Pro+ (POC) → RunPod Serverless (MVP)
    ↓
VECTOR DB: Chroma (in-memory) → Qdrant Cloud Free
    ↓
STORAGE: Google Cloud Storage (SNCP files)
```

**FASE 1 - POC (Settimane 1-3):** $50/mese
- Colab Pro+: $50
- 100 compute units A100
- Qwen3-4B 4-bit quantized
- Test personalità, RAG, performance

**FASE 2 - MVP (Mesi 1-3):** $100-150/mese
- RunPod Serverless: $6-60/mese (variable traffic!)
- Qdrant Cloud: $0 (Free tier 1GB)
- GCS: $5/mese (SNCP files)
- Monitoring: $10/mese (UptimeRobot, Sentry)

**Scalabilità:** 10 → 100 → 500 req/giorno
**Latency:** 500ms-2s (cold start RunPod)
**Uptime:** 95-98% (no SLA)

**Pro:**
- Costo minimo
- Zero infra management
- Fast iteration
- Risk basso

**Contro:**
- No SLA
- Cold start latency
- Scaling limits (500 req/giorno max)

**Decision Point:** Se traffic >500 req/giorno costante → Growth tier

---

### 6.2 Growth Level (Production) - $300-600/mese

**Target:** Production-ready, 500-5000 req/giorno

**STACK:**
```
FRONTEND: Miracollo
    ↓
API GATEWAY: Cervella AI (load balanced 2× instances)
    ↓
LLM INFERENCE: Vast.ai On-Demand RTX 4090 (always-on) + RunPod (burst)
    ↓
VECTOR DB: Qdrant Cloud Pro ($25/mese)
    ↓
STORAGE: GCS + backup S3
    ↓
MONITORING: Prometheus + Grafana + PagerDuty
```

**Costi:**
- Vast.ai RTX 4090: $192/mese (16h/day) o $288/mese (24h/day)
- RunPod burst: $50/mese (traffic spikes)
- Qdrant Pro: $25/mese
- GCS + S3: $20/mese
- Monitoring: $30/mese (PagerDuty, Grafana Cloud)
- **TOTALE: $317-413/mese**

**Architettura Resilience:**
1. **Primary:** Vast.ai On-Demand (stable)
2. **Failover:** RunPod Serverless (se Vast.ai down)
3. **Burst:** RunPod autoscale (traffic spikes)

**Scalabilità:** 500 → 5000 req/giorno
**Latency:** 200-500ms (no cold start)
**Uptime:** 98-99% (multi-provider redundancy)

**Pro:**
- Always-on performance
- Multi-cloud resilience
- Cost-optimized
- Autoscaling capability

**Contro:**
- No formal SLA
- Multi-provider complexity
- Manual failover (orchestration needed)

**Migration Path:**
- Da Entry: +$200/mese
- To Enterprise: +$400-800/mese

---

### 6.3 Enterprise Level (Scale + SLA) - $1000-2000/mese

**Target:** High-volume, 10K+ req/giorno, SLA required

**STACK:**
```
FRONTEND: Miracollo (multi-region CDN)
    ↓
API GATEWAY: Cervella AI (K8s cluster, 4× pods)
    ↓
LOAD BALANCER: NGINX Ingress (geo-routing)
    ↓
LLM INFERENCE: Lambda Labs A100 Dedicated (primary) + CoreWeave (DR)
    ↓
VECTOR DB: Qdrant Cloud Enterprise (HA cluster)
    ↓
STORAGE: Multi-cloud (GCS primary, S3 backup, Backblaze archive)
    ↓
MONITORING: Datadog + PagerDuty + On-call
```

**Costi:**
- Lambda A100 80GB: $950/mese (dedicated, SLA)
- CoreWeave A100 (DR standby): $200/mese (commitment discount)
- Qdrant Enterprise: $200/mese (HA cluster)
- K8s cluster (GKE/EKS): $150/mese (3 nodes)
- Storage (multi-cloud): $50/mese
- Monitoring: $100/mese (Datadog)
- CDN (Cloudflare Pro): $20/mese
- **TOTALE: $1,670/mese**

**SLA Target:** 99.9% uptime (43 min downtime/mese max)

**Disaster Recovery:**
1. **Primary:** Lambda Labs (99.9% SLA)
2. **DR:** CoreWeave (failover <5 min)
3. **Backup:** Multi-region storage (RPO <1h, RTO <15 min)

**Scalabilità:** 10K → 100K req/giorno
**Latency:** <200ms (dedicated GPU, geo-routing)
**Uptime:** 99.9% (SLA-backed)

**Pro:**
- Enterprise SLA
- Multi-region DR
- Professional support
- Unlimited scaling potential

**Contro:**
- Costo alto ($1,670/mese)
- Complexity alta (K8s, multi-cloud)
- Richiede team DevOps

**ROI Analysis:**
- 10K req/giorno = ~300K req/mese
- Claude API cost: ~$500-1000/mese (dipende da tokens)
- Self-hosting: $1,670/mese
- Break-even: ~20-30K req/giorno

**Quando Usarlo:**
- Traffic >10K req/giorno
- SLA requirement (business-critical)
- Budget $1,500-2,000/mese disponibile
- Team DevOps in-house

---

### 6.4 Hybrid Strategy (Best of Both Worlds)

**Concept:** Cloud per flexibility + Self-host per baseline

**STACK:**
```
BASELINE LOAD (80%): Self-hosted A100 in colo
    ↓
BURST/SPIKES (20%): Cloud (RunPod/Vast.ai autoscale)
    ↓
DR/BACKUP: Multi-cloud (Lambda/CoreWeave)
```

**Example Sizing:**
- Baseline: 8K req/giorno → A100 self-hosted
- Burst: 2K req/giorno peaks → RunPod autoscale
- Total: 10K req/giorno

**Costi:**
- A100 used: $268/mese (amortized TCO)
- Colo: $100/mese (rack space)
- Cloud burst: $100/mese (RunPod/Vast.ai)
- DR: $200/mese (Lambda standby)
- **TOTALE: $668/mese**

**Savings vs Full Cloud:** $1,670 - $668 = $1,002/mese (60% cheaper!)

**Pro:**
- Best economics (60% savings!)
- Flexibility (cloud burst)
- DR built-in
- Control (self-hosted baseline)

**Contro:**
- Complexity massima
- Upfront $8K (A100)
- Richiede expertise alta
- Orchestration custom

**Quando Usarlo:**
- Budget upfront $8-10K disponibile
- Long-term (2+ anni)
- Volume alto (10K+ req/giorno)
- Team DevOps esperto

---

### FINE PARTE 3

**Continua in:** `RICERCA_INFRASTRUTTURA_DEFINITIVA_2026_PARTE4.md`

---

**Prossime Sezioni (PARTE 4 - FINALE):**
- 7. Comparison Table Completa
- 8. Rischi e Mitigazioni
- 9. Raccomandazione Finale per Cervella Baby
- 10. Fonti Complete (80+ link)
- 11. Timeline di Migrazione
