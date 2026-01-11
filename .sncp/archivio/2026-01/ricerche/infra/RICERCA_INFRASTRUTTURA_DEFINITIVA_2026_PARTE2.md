# RICERCA INFRASTRUTTURA DEFINITIVA 2026 - PARTE 2

> Continua da PARTE1

---

### 1.3 Altri Specialized Providers

#### Hyperstack

**Modello:** AI-optimized GPU cloud, pay-per-minute

**GPU Disponibili:**
- RTX A6000 (48GB)
- A100 (40GB/80GB)
- H100 PCIe/SXM (80GB)

**Prezzi:**
- RTX A6000: da $0.50/hour
- A100 80GB: da $0.95/hour
- H100 PCIe: $1.90/hour
- H100 SXM: $2.40/hour

**Entry-level:** Pay-as-you-go da $0.43/hour

**Pro:**
- **75% cheaper than legacy cloud!**
- Pay-per-minute (no minimum commitment)
- Zero egress fees
- Zero bandwidth charges
- High-speed networking (fino 350Gbps per H100 VMs)
- Spot VMs + Reservations
- Transparent pricing

**Contro:**
- Meno conosciuto di AWS/GCP/Azure
- Limited regions
- Community support (non enterprise-grade)

**Quando Usarlo:**
- Budget-conscious startups
- AI/ML workloads standard
- Alternativa economica a hyperscalers

**Fonti:**
- [Hyperstack Pricing](https://www.hyperstack.cloud/gpu-pricing)
- [Hyperstack Top GPU Providers](https://www.hyperstack.cloud/blog/case-study/top-cloud-gpu-providers)
- [Hyperstack ComputePrices](https://computeprices.com/providers/hyperstack)

---

#### Paperspace (ora DigitalOcean)

**Modello:** Cloud computing platform per ML, acquisito da DigitalOcean 2024

**GPU Disponibili:**
- A100 40GB/80GB
- H100

**Prezzi On-Demand:**
- A100 40GB: $3.09/hour
- A100 80GB: $3.18/hour
- A100 80GB 2-GPU: $6.36/hour
- H100: $5.95/hour

**Subscription Required:**
- Growth plan: $39/month (richiesto per high-end GPUs)
- A100 $1.15/hour SOLO con 36-month commitment!

**Billing:**
- Per-hour basis
- Storage: $0.29/GB/month extra

**Regions:** 3 datacenter (NY2, CA1, AMS1)

**Pro:**
- Integrazione DigitalOcean ecosystem
- Gradient platform per ML workflows
- Billing chiaro per-hour

**Contro:**
- **Subscription obbligatoria** per A100/H100!
- Prezzi on-demand alti vs competitor
- Long-term commitment per prezzi competitivi
- Limited regions (solo 3!)

**Quando Usarlo:**
- Se già su DigitalOcean
- Se OK con subscription model
- Team piccoli con workflow Gradient

**Fonti:**
- [Paperspace Pricing](https://www.paperspace.com/pricing)
- [Paperspace Alternatives](https://www.thundercompute.com/blog/paperspace-alternative-budget-cloud-gpus-for-ai-in-2025)
- [Paperspace Documentation](https://docs.digitalocean.com/products/paperspace/pricing/)

---

#### Scaleway

**Modello:** European cloud provider (Francia)

**GPU Disponibili:**
- NVIDIA P100
- NVIDIA L4 Tensor Core
- NVIDIA L40S
- NVIDIA H100 Tensor Core
- NVIDIA GH200

**Prezzi:**
- Pay-as-you-go (per-minute billing)
- Pricing varia per instance type
- Unified Snapshot: €0.000044/GB/hour
- Flexible IP: €0.004/hour

**Billing:**
- Per-hour, pausa se power off instance
- Storage/IP continuano billing anche powered off!

**Savings Plans:**
- **NON applicabili** a H100, L40S, L4!

**Pro:**
- European data sovereignty (GDPR compliance)
- Pay-as-you-go flessibile
- Billing pausa su power off

**Contro:**
- Prezzi specifici non pubblici (need console check)
- Savings plans limitati (no H100/L40S/L4!)
- Meno documentazione vs AWS/GCP

**Quando Usarlo:**
- GDPR/EU data residency requirements
- European team/customers
- Budget flessibile (pay-as-you-go)

**Fonti:**
- [Scaleway GPU Pricing](https://www.scaleway.com/en/pricing/gpu/)
- [Scaleway GPU Instances](https://www.scaleway.com/en/gpu-instances/)
- [Scaleway Pricing Guide](https://gpus.io/providers/scaleway)

---

#### OVH Cloud

**Modello:** European cloud provider (Francia)

**GPU Disponibili:**
- NVIDIA Quadro RTX 5000
- NVIDIA A10
- NVIDIA V100S
- NVIDIA L40S
- NVIDIA L4
- NVIDIA H100

**Prezzi:**
- Range: $0.88 - $1.80/hour
- Pay-as-you-go model
- Billing per-minute granularity (displayed as hourly)

**Configurazioni:**
- 1 o 4 GPUs per instance
- Upgradable dopo reboot
- PCI Passthrough (direct hardware access)
- NVMe storage high-performance
- Networking fino 25 Gbps

**AI Services:**
- AI Notebooks: pay-per-running-notebook
- AI Training: pay-per-minute per training task

**Pro:**
- European data sovereignty
- Per-minute billing (come RunPod)
- Prezzi competitivi
- PCI Passthrough performance

**Contro:**
- Prezzi variano per region
- Documentazione meno dettagliata
- Limited global presence (EU-focused)

**Quando Usarlo:**
- EU data residency
- Budget mid-range
- Team europei

**Fonti:**
- [OVH Public Cloud Prices](https://us.ovhcloud.com/public-cloud/prices/)
- [OVH GPU Plans](https://www.vpsbenchmarks.com/gpu_plans/ovhcloud)
- [OVH GPU Provider](https://cloudgpuprices.com/vendors/ovh)

---

### 1.4 Nuovi Entrant 2025-2026

#### Together.ai

**Modello:** AI Native Cloud - serverless + dedicated

**GPU Disponibili:**
- H100 SXM (80GB) - Instant GPU Clusters
- H200
- GB200
- B200 (lanciato 2025!)

**Pricing:**
- Per-minute billing
- Prezzi specifici: contattare sales (non pubblici)

**Service Tiers:**
1. **Instant GPU Clusters:** Spin up/down on-demand, H100 80GB SXM
2. **Custom AI Factories:** 1K-100K+ GPUs, private clusters
3. **Serverless:** 200+ open-source models

**Pro:**
- Cutting-edge hardware (B200!)
- No upfront commitments (instant clusters)
- Serverless option (zero infra management)
- 200+ models supportati

**Contro:**
- Pricing non trasparente (need quote)
- Nuovo player (meno track record)
- Limited public info

**Quando Usarlo:**
- Large-scale AI Factories (1K+ GPUs)
- Serverless inference (no infra management)
- Latest hardware (B200/GB200)

**Fonti:**
- [Together.ai Pricing](https://www.together.ai/pricing)
- [Together GPU Clusters](https://www.together.ai/gpu-clusters)
- [Together.ai Review](https://getdeploying.com/together-ai)

---

### 1.5 Tendenze e Insights 2026

#### Specializzati > Hyperscalers

**Fact:** GPU-specialized providers sono 40-50% più economici!

**Perché:**
- Focus solo AI/ML (no overhead general cloud)
- Community/marketplace model (Vast.ai, RunPod)
- Kubernetes-native efficiency (CoreWeave)
- Zero hidden fees (egress, bandwidth)

**Esempio:**
- AWS H100: $39.80/hour
- CoreWeave H100 HGX: $6.15/hour/GPU (-85%!)
- Vast.ai A100: $0.50/hour vs AWS $32.77 (-98%!)

#### Multi-Cloud = Standard

**2026 Reality:**
- Single-cloud = rischio availability shortage
- Multi-cloud arbitrage: -30-40% costs
- Cross-cloud workload routing per GPU availability

**Strumenti:**
- Kubernetes GPU operators
- Slurm (HPC scheduling)
- Cloud automation platforms

---

## 2. TENDENZE PREZZI 2026

### 2.1 Prezzi STANNO SALENDO! ⚠️

**Gennaio 2026: AWS +15% GPU prices**
- P5e.48xlarge: $34.61 → $39.80/hour
- Effective Gennaio 2026
- Trend preoccupante per tutti cloud providers

**Memory Shortage 2024-2026:**
- +30% Q4 2025
- +20% Q1 2026
- HBM3E shortage spinge prezzi H100/H200

**NVIDIA/AMD Price Hikes:**
- AMD: dal Gennaio 2026 rolling monthly increases
- NVIDIA: dal Febbraio 2026 rolling monthly increases
- H200: $30K → $40K+ (6 stacks HBM3E shortage)
- RTX 5090: potenziale $5,000 (era ~$2,000)

**Structural Drivers:**
- AI demand >> supply (continua fino 2026+)
- Memory shortage (HBM3E, GDDR7, tutto!)
- NVIDIA production cuts: -30-40% GeForce RTX 50 series

**Fonti:**
- [AWS 15% Price Increase](https://www.theregister.com/2026/01/05/aws_price_increase)
- [GPU Pricing Trends 2026](https://www.silicondata.com/blog/gpu-pricing-trends-2026-what-to-expect-in-the-year-ahead)
- [NVIDIA AMD Price Hikes](https://www.trendforce.com/news/2026/01/05/news-nvidia-amd-reportedly-plan-price-hikes-starting-1q26-geforce-rtx-5090-may-reach-5000/)
- [Memory Supply Shortage](https://en.wikipedia.org/wiki/2024–2026_global_memory_supply_shortage)

---

### 2.2 Ma C'è Speranza! 📈

**Competitive Pressure:**
- Specialized providers NON alzano prezzi (ancora)
- Vast.ai, RunPod: stessi prezzi 2025 → 2026
- Competition keeps prices in check (per ora)

**Efficiency Gains:**
- H100 vLLM: 0.39 joules/token (Llama-3.3-70B FP8)
- Quantization: 4B model da 14GB → 7GB VRAM (4-bit)
- Inference optimization continua

**Alternative Hardware:**
- AMD MI300X (competitor H100)
- Google TPU v5/v6
- Intel Gaudi 3

**Prediction 2026:**
- Hyperscalers: +10-20% entro fine 2026
- Specialized: +0-10% (resistenza competitiva)
- Community clouds: stabili (marketplace dynamics)

---

## 3. OPZIONI ECONOMICHE ($100-300/mese)

### 3.1 Google Colab (POC/Experimentation)

#### Colab Free
**Costo:** $0

**GPU:**
- Tesla T4 (15GB) - standard
- Occasionalmente P100, V100

**Limiti:**
- 12 hours session timeout
- No persistence (files deleted)
- Availability non garantita
- Interruzioni frequenti

**Quando Usarlo:**
- Quick experiments
- Learning/tutorials
- Zero budget

---

#### Colab Pro
**Costo:** ~$10/month

**GPU:**
- Tesla T4 garantita
- Occasionalmente V100, A100

**Limiti:**
- 24 hours session
- Background execution
- Priority access

**Quando Usarlo:**
- POC projects
- Occasional training
- Budget minimo

---

#### Colab Pro+
**Costo:** ~$50/month

**GPU:**
- A100 40GB (priorità più alta)
- 100 compute units/month

**Limiti:**
- Longer sessions (fino 24h+)
- More RAM
- Better availability

**Quando Usarlo:**
- **CERVELLA BABY POC!** ✅
- 3 settimane validation
- Before committing to dedicated GPU
- Budget: $50

**ROI per Cervella Baby:**
- 100 compute units = ~50-80 hours A100
- Sufficiente per testare Qwen3-4B
- Validare personalità, RAG, performance
- Decision GO/NO-GO entro 3 settimane

**Fonti:**
- [Google Colab Pricing](https://colab.research.google.com/signup)
- [Colab Pro Features](https://colab.research.google.com/notebooks/pro.ipynb)

---

### 3.2 Vast.ai Spot/On-Demand

**Budget Target:** $100-250/month

#### Setup Consigliato per Qwen3-4B

**GPU:** RTX 4090 24GB
**VRAM Needed:** 7-8GB (4-bit quantization)
**Headroom:** 16GB extra per batch inference

**Pricing:**
- Spot (interruptible): da $0.20/hour
- On-Demand: $0.34-0.50/hour

**Calcolo Budget:**

**Scenario A - Spot (Risk-tolerant):**
```
$0.20/hour × 16 hours/day × 30 giorni = $96/mese
```
- Pro: Cheapest option
- Contro: Interruptions possibili

**Scenario B - On-Demand (Stable):**
```
$0.40/hour × 16 hours/day × 30 giorni = $192/mese
```
- Pro: Nessuna interruption
- Contro: +100% vs spot

**Scenario C - Hybrid (Recommended!):**
```
Spot: $0.20/hour × 12h/day × 30 giorni = $72
On-Demand: $0.40/hour × 4h/day × 30 giorni = $48
TOTALE = $120/mese
```
- Pro: Balance costo/stabilità
- 12h spot (notte/off-peak) + 4h on-demand (peak)

**Setup:**
1. Docker container con Qwen3-4B + vLLM
2. Persistent storage per model weights (~4GB)
3. Auto-restart script per spot interruptions
4. Health check + monitoring

**Quando Usarlo:**
- **CERVELLA BABY MVP!** ✅
- Dopo POC positivo
- 100-1000 req/giorno
- Budget $100-200/mese

**Fonti:**
- [Vast.ai Pricing](https://vast.ai/pricing)
- [Vast.ai Marketplace](https://vast.ai/console/create/)

---

### 3.3 RunPod Community Cloud

**Budget Target:** $120-250/month

#### Setup Consigliato

**GPU:** RTX 4090 24GB
**Pricing:** $0.34/hour (community), $0.50/hour (secure)

**Serverless Option:**
- Pay ONLY per inference time
- Autoscaling (0 → N instances)
- Cold start: ~10-30 seconds

**Calcolo Budget:**

**Scenario A - Always-On:**
```
$0.34/hour × 20 hours/day × 30 giorni = $204/mese
```

**Scenario B - Serverless (100 req/giorno):**
```
Assume: 2 sec/request, $0.34/hour
100 req × 2 sec = 200 sec/giorno = 0.055 hour/giorno
$0.34/hour × 0.055 hour × 30 giorni = $0.56/mese
```
- Pro: Cheapest per LOW volume!
- Contro: Cold start latency

**Scenario C - Serverless (1000 req/giorno):**
```
1000 req × 2 sec = 2000 sec/giorno = 0.55 hour/giorno
$0.34/hour × 0.55 hour × 30 giorni = $5.6/mese
```
- Pro: Still cheap!
- Contro: Cold start ogni N minuti idle

**Quando Usarlo:**
- Variable traffic (serverless shines!)
- Docker-first teams
- Cost-optimization critical
- OK con cold start latency

**Fonti:**
- [RunPod Pricing](https://www.runpod.io/pricing)
- [RunPod Serverless Guide](https://www.runpod.io/articles/guides/deploy-llm-docker)

---

### 3.4 Comparison: Opzioni Economiche

| Provider | GPU | Costo/Mese | Uptime | SLA | Use Case |
|----------|-----|------------|--------|-----|----------|
| Colab Pro+ | A100 40GB | $50 | Medium | ❌ | POC 3 settimane |
| Vast.ai Spot | RTX 4090 | $96-120 | Low | ❌ | MVP fault-tolerant |
| Vast.ai On-Demand | RTX 4090 | $192-250 | Medium | ❌ | MVP stable |
| RunPod Community | RTX 4090 | $204 | Medium | ❌ | MVP always-on |
| RunPod Serverless | RTX 4090 | $6-60 | High | ❌ | MVP variable traffic |

**Raccomandazione per Cervella Baby:**

**FASE 1 (Settimane 1-3):** Colab Pro+ $50
- Validazione rapida
- Zero infra setup
- GO/NO-GO decision

**FASE 2 (Mesi 1-3):** RunPod Serverless o Vast.ai Hybrid
- RunPod se traffic variabile → $6-60/mese
- Vast.ai se traffic stabile → $120/mese
- Break-even: 100-1000 req/giorno

---

## 4. OPZIONI PREMIUM ($300-1000/mese)

### 4.1 Lambda Labs Dedicated

**Budget Target:** $800-1200/month

#### GPU Disponibili

**A100 80GB:**
- On-Demand: $1.10/hour
- Reserved (1 month): ~$750/month
- Reserved (1 year): ~$650/month

**H100 80GB:**
- Serverless: $0.0006/second = $2.16/hour
- Dedicated: Contact sales (~$3-4/hour estimate)

**Calcolo Budget:**

**A100 80GB Always-On:**
```
$1.10/hour × 24 hours × 30 giorni = $792/mese
```

**A100 80GB Reserved (1 month):**
```
~$750/mese flat
```

**H100 Serverless (1000 req/giorno, 2 sec each):**
```
1000 × 2 sec × 30 giorni = 60,000 sec = 16.6 hours
$2.16/hour × 16.6 hours = $36/mese
```
- Ma: cold start issues!

**Pro:**
- ✅ **SLA enterprise-grade** (unico specialized!)
- ✅ Zero egress fees
- ✅ Lambda Stack ottimizzato
- ✅ Best H100/H200 stock globally
- ✅ Professional support

**Contro:**
- Prezzi più alti vs Vast.ai/RunPod
- Limited regions
- H100 availability limitata

**Quando Usarlo:**
- **CERVELLA BABY PRODUCTION!** ✅
- Serve SLA (uptime garantito)
- Traffic costante (always-on economics)
- Budget $800-1200 OK

**Fonti:**
- [Lambda Pricing](https://lambda.ai/pricing)
- [Lambda GPU Comparison](https://estha.ai/blog/7-affordable-gpu-clouds-for-llm-serving-best-options-for-ai-deployment/)

---

### 4.2 RunPod Secure Cloud

**Budget Target:** $400-800/month

**Differenza vs Community:**
- Professional data centers
- **SLA disponibile** (enterprise tier)
- Better network performance
- More reliable availability

**Pricing:**
- RTX 4090: ~$0.50-0.70/hour
- A100 80GB: ~$2.00-2.50/hour

**Calcolo Budget:**

**RTX 4090 Secure 24/7:**
```
$0.60/hour × 24 hours × 30 giorni = $432/mese
```

**A100 80GB Secure 24/7:**
```
$2.25/hour × 24 hours × 30 giorni = $1,620/mese
```
- Troppo per budget $300-1000!

**Quando Usarlo:**
- Need SLA ma budget limitato
- RTX 4090 sufficient per workload
- Prefer RunPod ecosystem

---

### 4.3 CoreWeave Committed

**Budget Target:** $600-1000/month (con commitment)

**Pricing con -60% Committed Discount:**

**A100 80GB:**
- On-Demand: $3/hour totale
- Committed (-60%): $1.20/hour

**Calcolo Budget:**
```
$1.20/hour × 24 hours × 30 giorni = $864/mese
```

**Pro:**
- Kubernetes-native
- Low-latency inference
- Smooth scaling
- Good balance performance/cost

**Contro:**
- Richiede commitment (lock-in!)
- Expertise K8s necessaria

**Quando Usarlo:**
- K8s infrastructure
- Long-term commitment OK
- Team DevOps

**Fonti:**
- [CoreWeave Pricing](https://www.coreweave.com/pricing)

---

### 4.4 Comparison: Opzioni Premium

| Provider | GPU | Costo/Mese | Uptime | SLA | Support |
|----------|-----|------------|--------|-----|---------|
| Lambda A100 | 80GB | $792-950 | 99.9%+ | ✅ Yes | Professional |
| RunPod Secure RTX 4090 | 24GB | $432 | 99%+ | ✅ Enterprise | Standard |
| CoreWeave A100 (committed) | 80GB | $864 | 99.5%+ | ⚠️ Custom | Standard |
| Hyperstack A100 | 80GB | $684 | 99%+ | ❌ No | Community |

**Raccomandazione per Cervella Baby Production:**

**Opzione A - Lambda Labs A100** ✅
- SLA garantito
- Zero egress fees
- $800/mese
- Best per production-ready

**Opzione B - RunPod Secure RTX 4090**
- SLA enterprise tier
- $432/mese
- Sufficient per Qwen3-4B
- Best bang-for-buck premium

---

### FINE PARTE 2

**Continua in:** `RICERCA_INFRASTRUTTURA_DEFINITIVA_2026_PARTE3.md`

---

**Prossime Sezioni (PARTE 3):**
- 5. Self-Hosting (Own Hardware)
- 6. Architettura Consigliata (Entry/Growth/Enterprise)
