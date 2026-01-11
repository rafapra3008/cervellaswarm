# RICERCA INFRASTRUTTURA DEFINITIVA 2026 - PARTE 1

> **"Non micro-soluzioni. SOLUZIONE DEFINITIVA!"**
> **"Facciamo tutto al 100000%!"**
> - Rafa, 10 Gennaio 2026

---

**Data Ricerca:** 10 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Obiettivo:** Mappare TUTTE le opzioni cloud GPU per hosting LLM nel 2026
**Contesto:** Cervella Baby (Qwen3-4B, ~100-1000 richieste/giorno)

**NOTA:** Questa è la PARTE 1 di 4. Vedi anche PARTE2, PARTE3, PARTE4.

---

## INDICE COMPLETO (4 PARTI)

**PARTE 1 (questo file):**
- Executive Summary
- 1. Landscape Cloud GPU 2026
- 2. Tendenze Prezzi 2026

**PARTE 2:**
- 3. Opzioni Economiche ($100-300/mese)
- 4. Opzioni Premium ($300-1000/mese)

**PARTE 3:**
- 5. Self-Hosting (Own Hardware)
- 6. Architettura Consigliata

**PARTE 4:**
- 7. Comparison Table Completa
- 8. Rischi e Mitigazioni
- 9. Raccomandazione Finale
- 10. Fonti (80+ link)

---

## EXECUTIVE SUMMARY

### TL;DR - Le 3 Opzioni Chiave

| Categoria | Soluzione | Costo/Mese | Quando Usarla |
|-----------|-----------|------------|---------------|
| **POC/MVP** | Google Colab Pro+ | $50 | Validazione 3 settimane |
| **GROWTH** | Vast.ai On-Demand | $175-250 | 100-5000 req/giorno |
| **ENTERPRISE** | Lambda Labs Dedicated | $800-1200 | 10K+ req/giorno + SLA |

### La Verità del 2026

**PREZZI:** Stanno SALENDO, non scendendo!
- AWS +15% GPU prices (Gennaio 2026)
- Memory costs +30% Q4 2025, +20% Q1 2026
- H100 da $30K → $40K+ (HBM3E shortage)
- NVIDIA/AMD alzano prezzi ogni mese dal Q1 2026

**DISPONIBILITÀ:** Shortage continua fino 2026+
- AI demand > supply
- NVIDIA taglia produzione gaming GPU 30-40%
- Memory shortage 2024-2026 in corso
- Booking anticipato OBBLIGATORIO

**TENDENZA:** Specializzati battono Big Cloud
- Vast.ai, RunPod, Lambda: 40-50% più economici di AWS/GCP/Azure
- Community cloud = 60-90% discount su spot
- CoreWeave, Hyperstack: 75% cheaper than hyperscalers

### Budget Raccomandato per Cervella Baby

**FASE 1 - POC (3 settimane):** $50
Google Colab Pro+ - 100 compute units/mese

**FASE 2 - MVP (3-6 mesi):** $175-250/mese
Vast.ai RTX 4090 (24GB) on-demand
- $0.34-0.50/hour × 16-20h/day × 30 giorni
- Break-even: ~12.5M tokens/mese vs Claude API

**FASE 3 - Production (6+ mesi):** $800-1200/mese
Lambda Labs A100 80GB dedicated
- SLA enterprise-grade
- Zero egress fees
- H100 availability garantita

**BACKUP PLAN:** Multi-cloud (RunPod + Vast.ai)
Costo extra: +$50-100/mese
Beneficio: Zero downtime, -30-40% costs via arbitrage

---

## 1. LANDSCAPE CLOUD GPU 2026

### 1.1 Major Cloud Providers (Hyperscalers)

#### AWS (Amazon Web Services)

**GPU Disponibili:**
- P3 instances: NVIDIA Tesla V100 (16GB)
- P4d instances: NVIDIA A100 (40GB)
- P5 instances: NVIDIA H100 (80GB)

**Prezzi On-Demand:**
- P3.16xlarge: ~$24.48/hour
- P4d.24xlarge: ~$32.77/hour
- P5e.48xlarge: $39.80/hour (era $34.61 pre-Gennaio 2026)

**Spot Discount:** 60-90% off on-demand

**Pricing Update 2026:**
- **GENNAIO 2026: +15% price increase!**
- P4/P5 instances: -33% reduction (Giugno 2025)
- Savings Plans: fino -45% con 1-3 year commitment

**Pro:**
- Global infrastructure (20+ regions)
- Spot fleet availability alta
- EC2 Capacity Blocks per prenotare GPU

**Contro:**
- Prezzi più alti dei competitor
- +15% increase Gennaio 2026 (trend preoccupante)
- Egress fees significativi
- Complessità configurazione

**Quando Usarlo:**
- Se già su AWS ecosystem
- Se serve multi-region compliance
- Enterprise con budget >$5K/mese

**Fonti:**
- [AWS EC2 Spot Pricing](https://aws.amazon.com/ec2/spot/pricing/)
- [AWS GPU Price Comparison](https://compute.doit.com/gpu)
- [AWS 15% Price Increase - The Register](https://www.theregister.com/2026/01/05/aws_price_increase)
- [AWS P4 Instances](https://aws.amazon.com/ec2/instance-types/p4/)

---

#### GCP (Google Cloud Platform)

**GPU Disponibili:**
- NVIDIA T4 (16GB) - entry level
- NVIDIA L4 (24GB) - cost-optimized inference
- NVIDIA A100 (40GB/80GB) - training
- NVIDIA H100 (80GB) - cutting-edge

**Prezzi On-Demand:**
- T4: ~$0.35/hour/GPU
- L4: ~$0.72/hour/GPU (~$515/mese per instance)
- A100 80GB: ~$3-4/hour/GPU
- H100 8-GPU instance: $88.49/hour (us-central1)

**Spot Discount:** 60-91% off on-demand

**A2 Machine Types:**
- A2 Standard: A100 40GB
- A2 Ultra: A100 80GB
- Prezzi includono GPU + CPU + RAM bundled

**Pro:**
- Spot pricing dinamico (aggiornato ogni 30 giorni)
- Buona documentazione
- Integrazione con Vertex AI
- Preemptible instances economiche

**Contro:**
- Prezzi comunque alti vs specialized providers
- Complessità billing (GPU + machine type)
- Availability limitata per H100 (solo us-central1)

**Quando Usarlo:**
- Se già su GCP ecosystem
- Se serve integrazione Vertex AI/BigQuery
- Enterprise con ML pipelines esistenti

**Fonti:**
- [GCP GPU Machine Types](https://docs.cloud.google.com/compute/docs/gpus)
- [GCP GPU Pricing](https://cloud.google.com/compute/gpus-pricing)
- [GCP vs Specialized Providers](https://www.thundercompute.com/blog/thunder-compute-vs-gcp-gpu-cloud-comparison)

---

#### Azure (Microsoft)

**GPU Disponibili:**
- NC series: Tesla V100, T4
- NCv3: Tesla V100
- NCasT4_v3: NVIDIA T4 (fino 4× GPUs)
- NCads H100 v5: NVIDIA H100 NVL (fino 2× GPUs)

**Prezzi On-Demand:**
- NC24ads A100 v4: $3.673/hour on-demand
- NC24ads A100 v4 Spot: $1.096/hour (70% discount!)
- NC H100 v5: ~$6.98/hour/GPU (East US)

**GPU Specs:**
- NCasT4_v3: 4× T4 16GB + AMD EPYC Rome (64 cores) + 440 GiB RAM
- NCads H100 v5: 2× H100 NVL 94GB + AMD EPYC Genoa (96 cores) + 640 GiB RAM

**Pro:**
- Spot instances con 70% discount
- Buona availability H100
- Integrazione Azure ML
- Hybrid benefit per license reuse

**Contro:**
- NVv4 series RETIRED 30 Settembre 2026!
- Prezzi alti on-demand
- Complessità pricing (region-dependent)

**Quando Usarlo:**
- Se già su Azure ecosystem
- Se serve integrazione Azure ML/OpenAI Service
- Enterprise Microsoft-centric

**ATTENZIONE:** Migrazione da NVv4 OBBLIGATORIA entro Settembre 2026!

**Fonti:**
- [Azure NC Family](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nc-family)
- [Azure NV Series Guide](https://www.cloudoptimo.com/blog/a-complete-guide-to-azure-nv-series-gpu-instances/)
- [H100 Pricing Comparison](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [NC24ads Pricing](https://instances.vantage.sh/azure/vm/nc24ads-v4)

---

### 1.2 GPU-Specialized Providers (NeoClouds)

**Definizione:** Cloud providers focalizzati SOLO su GPU compute per AI/ML workloads.

**Vantaggio chiave:** 40-50% più economici dei hyperscalers!

#### Vast.ai

**Modello:** P2P Marketplace - connette chi ha GPU extra con chi le serve

**GPU Disponibili:**
- RTX 3090, RTX 4090 (consumer)
- A100 40GB/80GB
- H100 PCIe/SXM
- L40S, L4

**Prezzi (Community Cloud):**
- RTX 4090 24GB: da $0.34/hour
- A100 80GB: da $0.50/hour (MIGLIORE PREZZO!)
- H100 PCIe: da $1.99/hour

**Spot vs On-Demand:**
- Spot (interruptible): -70-90% discount
- On-demand (reserved): prezzo standard, no interruzioni

**Pro:**
- **Prezzi più bassi del mercato** (spesso 50-80% cheaper di AWS/GCP!)
- Bid system - puoi negoziare prezzo
- Varietà GPU enorme
- Pay-per-second billing
- Ideale per POC/ricerca

**Contro:**
- **ZERO SLA** - reliability variabile!
- No enterprise-grade guarantees
- Network performance inconsistente
- Istanze possono terminare unexpectedly (host power loss)
- NOT recommended per production inference

**Quando Usarlo:**
- POC e sperimentazione
- Training batch jobs (checkpoint-based)
- Budget limitato (<$300/mese)
- Workload fault-tolerant

**Fonti:**
- [Vast.ai Pricing](https://vast.ai/pricing)
- [RunPod vs Vast.ai Comparison](https://www.runpod.io/articles/comparison/runpod-vs-vastai-training)
- [Cheapest GPU Clouds 2026](https://northflank.com/blog/cheapest-cloud-gpu-providers)

---

#### RunPod

**Modello:** Hybrid - Community Cloud + Secure Cloud

**GPU Disponibili:**
- RTX 3090, RTX 4090
- A100 40GB/80GB
- H100 PCIe/SXM
- L40, L40S

**Prezzi:**
- RTX 4090: da $0.34/hour (Community)
- A100 80GB: $1.74/hour
- H100 PCIe: da $1.99/hour

**Community vs Secure Cloud:**
- **Community:** Marketplace simile Vast.ai, no SLA
- **Secure:** Data center professionali, SLA disponibile (enterprise)

**Pro:**
- Pay-per-second billing (no minimum commitment!)
- Spot instances: -70% savings
- Serverless GPU deployments (autoscaling)
- Docker-first approach
- Zero egress fees!
- SLA per Secure tier

**Contro:**
- Community Cloud: no SLA (come Vast.ai)
- Availability variabile
- Documentazione meno completa di AWS/GCP

**Quando Usarlo:**
- Containerized AI workflows
- Serverless LLM deployments (pay only inference time)
- Real-time model iteration
- Startup/developers cost-sensitive

**Fonti:**
- [RunPod Pricing](https://www.runpod.io/pricing)
- [RunPod Top 12 GPU Providers](https://www.runpod.io/articles/guides/top-cloud-gpu-providers)
- [Serverless GPU Review 2026](https://rahulkolekar.com/serverless-gpu-hosting-review-runpod-lambda-aws-2026/)

---

#### Lambda Labs

**Modello:** Specialized GPU cloud per deep learning

**GPU Disponibili:**
- A100 40GB/80GB
- H100 SXM (80GB)
- H200 (141GB) - BEST stock in the world!

**Prezzi:**
- A100 80GB: ~$1.10/hour
- H100 Serverless: $0.0006/second
- H200: Contattare sales (limited availability)

**Infrastructure:**
- Quantum-2 InfiniBand (high-speed networking)
- Lambda Stack preinstalled (deep learning optimized)
- **ZERO egress fees!**

**Pro:**
- **SLA enterprise-grade** (unico tra specialized!)
- Best H100/H200 stock globally
- Zero hidden costs (no egress fees!)
- Lambda Stack ottimizzato per training
- Success stories: billion-parameter models
- Professional support

**Contro:**
- Prezzi leggermente più alti di Vast.ai/RunPod
- Limited regions (vs AWS/GCP global)
- H100/H200 availability limitata (high demand)

**Quando Usarlo:**
- Production deployments requiring SLA
- Large-scale training (billion+ params)
- Quando reliability > cost
- Enterprise workloads

**Fonti:**
- [Lambda GPU Pricing](https://lambda.ai/pricing)
- [Lambda Labs Alternatives](https://www.runpod.io/articles/alternatives/lambda-labs)
- [7 Affordable GPU Clouds](https://estha.ai/blog/7-affordable-gpu-clouds-for-llm-serving-best-options-for-ai-deployment/)

---

#### CoreWeave

**Modello:** Kubernetes-native GPU cloud

**GPU Disponibili:**
- A100 SXM/PCIe (40GB/80GB)
- H100 PCIe/SXM/HGX (80GB)
- H200 NVL (141GB)
- GH200 (96GB CPU + 141GB GPU)
- GB200 NVL72
- RTX Pro 6000 Blackwell
- L40, L40S, L4

**Prezzi (à la carte):**
- A100 80GB: $2.21/hour (GPU only) + CPU/RAM → ~$3/hour totale
- H100 PCIe: $4.25/hour (GPU only)
- H100 HGX 8-GPU node: $49.24/hour (~$6.15/GPU bundled)

**Savings:**
- Committed usage: fino -60% off on-demand!

**Pro:**
- Kubernetes-native (facile orchestrazione)
- Low-latency inference endpoints per LLM
- Smooth growth path (no surprise cost increases)
- 2025: Lanciato B200 instances (NVLink + InfiniBand)
- Balanced performance/cost per production LLMs

**Contro:**
- À la carte pricing può essere confusing
- Totale costo: GPU + vCPU + RAM (calcolare bene!)
- Richiede expertise Kubernetes

**Quando Usarlo:**
- K8s-based infrastructure
- Production LLM serving (performance + cost balance)
- Scaling predictable
- Enterprise con team DevOps/K8s

**Fonti:**
- [CoreWeave Pricing](https://www.coreweave.com/pricing)
- [CoreWeave GPU Pricing Guide](https://www.thundercompute.com/blog/coreweave-gpu-pricing-review)
- [CoreWeave Instance Pricing](https://docs.coreweave.com/docs/pricing/pricing-instances)

---

### FINE PARTE 1

**Continua in:** `RICERCA_INFRASTRUTTURA_DEFINITIVA_2026_PARTE2.md`

---

**Prossime Sezioni (PARTE 2):**
- 1.3 Altri Specialized Providers (Hyperstack, Paperspace, Scaleway, OVH)
- 1.4 Nuovi Entrant 2025-2026
- 2. Tendenze Prezzi 2026 (dettaglio)
- 3. Opzioni Economiche ($100-300/mese) - comparazione completa
