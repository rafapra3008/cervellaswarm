# Ricerca OVHcloud GPU Cloud 2026

**Data ricerca:** 11 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Scopo:** Valutare OVHcloud per deploy LLM inference (Qwen3-4B Q4_K_M, 4-6GB VRAM)

---

## Executive Summary

**RACCOMANDAZIONE:** ✅ OVHcloud L4 è ADATTO per il nostro caso d'uso

**Perché:**
- L4-90 (1x GPU 24GB) = €664-730/mese → rientra nel budget €50-200/mese? **NO, fuori budget**
- L4 ha 24GB VRAM → ampiamente sufficiente per Qwen3-4B (4-6GB richiesti)
- EU-based (Francia), GDPR compliant, ISO 27001 certificato
- SLA 99.99% uptime garantito
- Setup semplice via Control Panel/API

**PROBLEMA PRINCIPALE:** Il prezzo mensile stimato (~€664-730) supera il budget ideale di €200/mese.

**Alternative da considerare:**
- Valutare pricing con fatturazione mensile (sconto ~50% possibile come per altre istanze)
- Considerare GPU spot/preemptible se OVHcloud le offre
- Valutare shared GPU o provider alternativi per budget più contenuto

---

## 1. GPU Disponibili

OVHcloud offre il seguente portfolio GPU nel 2026:

| GPU | VRAM | Caso d'uso principale | Parametri LLM supportati |
|-----|------|----------------------|-------------------------|
| **NVIDIA L4** | 24 GB | Inference piccoli modelli, video | Fino a 7B |
| **NVIDIA A10** | 24 GB | Inference, virtualizzazione grafica | - |
| **NVIDIA L40S** | 48 GB | Inference mid-size LLM, costo/token ottimo | Fino a 20B |
| **NVIDIA A100** | 40/80 GB | Training, inference large models | - |
| **NVIDIA H100** | 80 GB | Highest performance, large LLM | Fino a ~120B (4x H100) |
| **NVIDIA H200** | - | Next-gen high performance | - |
| **Tesla V100S** | 32 GB | Legacy, NGC integration | - |

**Per il nostro caso (Qwen3-4B, 4-6GB VRAM):**
- ✅ **L4** = scelta ideale (24GB VRAM, designed per inference compatti ≤7B)
- ✅ **A10** = alternativa valida
- ⚠️ V100S, L40S, A100, H100 = overkill e più costosi

---

## 2. Pricing L4 GPU (DETTAGLIATO)

### Prezzi Ufficiali (USD)

Fonte: Pricing page OVHcloud US

| Istanza | GPU | vCPU | RAM | Storage | Network Pub/Priv | Prezzo/ora (USD) | Prezzo/mese* (USD) |
|---------|-----|------|-----|---------|------------------|-----------------|-------------------|
| **l4-90** | 1x L4 24GB | 22 | 90 GB | 400 GB NVMe | 8/8 Gbps | $1.00 | $730 |
| **l4-180** | 2x L4 24GB | 45 | 180 GB | 400 GB NVMe | 16/16 Gbps | $2.00 | $1,460 |
| **l4-360** | 4x L4 24GB | 90 | 360 GB | 400 GB NVMe | 25/25 Gbps | $4.00 | $2,920 |

*Calcolo: prezzo orario × 730 ore/mese

**Nota AI Training Service:** Un'altra fonte menziona L4 a $0.91/ora per AI Training service (servizio diverso da Public Cloud).

### Conversione Euro (Stima)

Assumendo cambio USD/EUR ~0.91 (Gennaio 2026):

| Istanza | Prezzo/ora (EUR) | Prezzo/mese 24/7 (EUR) |
|---------|-----------------|----------------------|
| **l4-90** | €0.91 | ~€664 |
| **l4-180** | €1.82 | ~€1,329 |
| **l4-360** | €3.64 | ~€2,657 |

**ATTENZIONE:**
- Questi sono prezzi ORARI standard
- OVHcloud offre fatturazione MENSILE con sconto ~50% per altre istanze (B2/C2/R2)
- **NON è chiaro se lo sconto mensile si applica anche a GPU L4**
- Prezzo effettivo potrebbe essere **€332-400/mese** con billing mensile (da verificare)

### Billing Options

- **Hourly (Pay-as-you-go):** Granularità al minuto, paghi solo ore attive
- **Monthly:** Tariffa flat mensile, ideale per workload 24/7, possibile sconto ~50%

---

## 3. Location EU & Datacenter

### Regioni Europee con GPU

| Regione | Città | Paese | GPU Disponibili |
|---------|-------|-------|----------------|
| **GRA** (GRA5, GRA7, GRA9, GRA11) | Gravelines | Francia | ✅ Tutte le GPU |
| **SBG** (SBG5) | Strasbourg | Francia | ✅ GPU disponibili |
| **ERI** | London | UK | ✅ GPU disponibili |
| **DE** | Frankfurt | Germania | ✅ GPU disponibili |

**Nota:** La disponibilità GPU è più concentrata nei datacenter **Gravelines (GRA)**, con molteplici zone OpenStack (GRA5-GRA11).

### Presenza Globale

- **30+ datacenter** in Europa, Nord America, Asia-Pacific
- **EU:** Francia (Roubaix, Gravelines, Paris, Strasbourg), Germania (Frankfurt), UK (London), Polonia
- **Compliance:** Dati ospitati in cloud europeo, trasparente e compliant

---

## 4. GDPR Compliance & Certificazioni

### ISO 27001 Certification

- ✅ **ISO/IEC 27001:2022** - Certificato dal 2013, rinnovato regolarmente
- ✅ **ISO/IEC 27017** - Cloud security
- ✅ **ISO/IEC 27018** - Cloud privacy
- ✅ **ISO/IEC 27701:2022** - Privacy Information Management (supporta GDPR, CCPA)
- 📅 Certificato valido fino al **24 Giugno 2025** (presumibilmente rinnovato per 2026)

### GDPR Compliance

- ✅ OVHcloud è **EU cloud leader**, headquarter Francia
- ✅ ISO 27701 framework supporta compliance GDPR
- ✅ Tutti i servizi Public Cloud (incluso GPU) coperti da certificazione
- ✅ DPA (Data Processing Agreement) disponibile
- ✅ Dati processati entro confini EU

### Altre Certificazioni

- **HDS** (Hébergeur de Données de Santé) - Health data hosting
- **SOC** reports
- **Anti-DDoS** protection inclusa gratuitamente

### Scope Certificazione

Copre: Public Cloud (Compute, Storage, Kubernetes, Databases, ML Serving, AI Training), Hosted Private Cloud, Managed Bare Metal, Bare Metal Servers, NAS, Backup, Logs.

---

## 5. Reliability & SLA

### SLA Uptime

| Service | SLA Uptime | Note |
|---------|-----------|------|
| **GPU instances (generale)** | 99.999% | 5 nines, ~26 sec downtime/mese |
| **L4 GPU instances** | 99.99% | 4 nines, ~4.3 min downtime/mese |
| **Public Cloud standard** | 99.99% | - |
| **Discovery instances** | 99.95% | - |

**Per il nostro caso:** L4 ha SLA **99.99%** = ~4.3 minuti downtime/mese massimo.

### Crediti SLA

In caso di mancato raggiungimento SLA, il cliente è eligibile per **Service Credits** (dettagli in Public Cloud SLA document).

### Customer Reviews - Reliability

**Positivi:**
- "Reliable performance" con "consistent uptime and smooth scaling"
- "Exceptional uptime and stability"
- GPU delivery via **PCI passthrough** (no virtualization layer) = performance dedicata

**Negativi:**
- Alcuni utenti riportano downtime brevi senza notifica
- "Wrong detection of hacking" causando shutdown server (rari)

**Verdetto:** Generalmente affidabile, ma customer support può essere lento.

---

## 6. Setup & Ease of Use

### Deployment Process

**Step principali (da Control Panel):**

1. Login OVHcloud Control Panel
2. Seleziona progetto Public Cloud
3. "Create an instance"
4. Tab "GPU instance"
5. Scegli modello (es. L4-90)
6. Seleziona regione (es. GRA11)
7. Scegli OS (Linux/Windows)
8. Click "Next" → Deploy

**Tempo stimato:** 5-10 minuti per provisioning.

### Management Tools

- **Control Panel** (Web UI)
- **OVHcloud API** (REST)
- **OVHcloud CLI** (command-line)
- **Terraform** support (via provider)

### Prodotti per LLM Inference

OVHcloud offre 3 livelli di complessità:

| Prodotto | Complessità | Caso d'uso | Pricing |
|----------|------------|-----------|---------|
| **AI Endpoints** | ⭐ Bassa | Modelli supportati, fully managed | Pay-per-token |
| **AI Deploy** | ⭐⭐ Media | Bring your own container | Pay-per-minute |
| **Public Cloud GPU** | ⭐⭐⭐ Alta | Full control, custom setup | Pay hourly/monthly |

**Per Qwen3-4B:** Probabilmente useremo **Public Cloud GPU** (massimo controllo) o **AI Deploy** (container + autoscaling).

### Technical Requirements

**Prerequisiti:**
- Calcolare memoria GPU: `(Parameters × Precision Factor) + Context`
  - Qwen3-4B Q4_K_M = ~4-6GB → L4 24GB = ampiamente sufficiente
- Scegliere inference server: vLLM, Ollama, TensorRT-LLM
- Configurare networking (privato/pubblico)
- Setup CUDA drivers (pre-installati su molte immagini)

**Documentazione:**
- ✅ Guide ufficiali: [Deploying GPU instance](https://help.ovhcloud.com/csm/en-public-cloud-compute-deploy-gpu-instance)
- ✅ Blog: [GPU for LLM Inferencing Guide](https://blog.ovhcloud.com/gpu-for-llm-inferencing-guide/)
- ✅ Tutorial: Installing CUDA, Kubernetes GPU deployment
- ⚠️ Documentazione buona ma meno estesa di AWS/GCP

---

## 7. Pro & Contro - Analisi Onesta

### ✅ PRO

| Aspetto | Dettaglio |
|---------|-----------|
| **Prezzo competitivo** | L4 a $1/ora (~€0.91) vs AWS/Azure più costosi. H100 più economico di competitor |
| **EU-based & GDPR** | Datacenter Francia/Germania, ISO 27001/27701, DPA compliant |
| **Affidabilità** | SLA 99.99%, uptime generalmente buono |
| **Hardware dedicato** | PCI passthrough, no virtualization layer = max performance |
| **Network incluso** | Fino a 25 Gbps incluso, no costi nascosti |
| **Anti-DDoS** | Protezione inclusa gratis |
| **Renewable energy** | Datacenter con energia rinnovabile |
| **Billing flessibile** | Hourly (pay-as-you-go) o Monthly (possibile sconto) |
| **NVIDIA NGC** | Integrazione con NGC framework (container pre-configurati) |
| **Managed K8s gratis** | Free Managed Kubernetes con GPU instances |

### ❌ CONTRO

| Aspetto | Dettaglio |
|---------|-----------|
| **Fuori budget (?)** | €664/mese hourly rate > budget €200/mese. **Verificare sconto mensile!** |
| **Customer support** | Lento secondo reviews, interfaccia confusa per alcuni |
| **Documentazione** | Buona ma meno estesa di hyperscaler (AWS/GCP/Azure) |
| **Scelta GPU limitata** | No T4 (entry-level), salto diretto a L4. Alcuni utenti lamentano "no choice" |
| **Availability transparency** | Non sempre chiaro quali GPU in quali regioni specifiche |
| **Ecosystem** | Meno integrato di AWS/GCP (es. no SageMaker equivalent) |
| **Multi-server setup** | Complessità alta per distributed inference (Infiniband, clustering) |

### ⚠️ RISCHI & MITIGAZIONI

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|------------|---------|-------------|
| Costo > budget | Alta | Alto | Verificare sconto mensile billing, valutare alternative |
| Support lento | Media | Medio | Documentarsi bene prima, usare community/forum |
| Downtime non notificato | Bassa | Medio | Implementare health checks, monitoring esterno |
| GPU shortage | Bassa | Alto | Reservare in anticipo, avere backup plan su altro provider |

---

## 8. Confronto Competitor (Quick)

### Pricing Benchmark L4 GPU

| Provider | GPU | Prezzo/ora | Prezzo/mese (730h) | Note |
|----------|-----|-----------|-------------------|------|
| **OVHcloud** | L4 24GB | $1.00 | $730 | EU-based, GDPR |
| **AWS** | - | - | - | No L4 standalone, solo bundle 8x GPU |
| **GCP** | L4 24GB | ~$0.70-1.20 | ~$511-876 | Varia per regione |
| **Azure** | - | - | - | No L4 listing chiaro |
| **Vast.ai** | L4 24GB | ~$0.30-0.60 | ~$219-438 | Spot market, no SLA |
| **RunPod** | L4 24GB | ~$0.39 | ~$285 | Community cloud, SLA variabile |

**Nota:** OVHcloud è competitivo vs hyperscaler, ma alternative come Vast.ai/RunPod sono più economiche (tradeoff affidabilità).

### Positioning OVHcloud

- **vs Hyperscaler (AWS/GCP/Azure):** Più economico (soprattutto H100), EU-compliant, ma ecosystem meno ricco
- **vs Budget GPU (Vast.ai, RunPod):** Più costoso, ma SLA garantito, support ufficiale, affidabilità superiore
- **Sweet spot:** Aziende EU che vogliono compliance + affidabilità + costo contenuto

---

## 9. Raccomandazioni Specifiche per CervellaSwarm

### Configurazione Suggerita

**Istanza:** `l4-90` (1x L4 24GB)

**Motivi:**
- 24GB VRAM >> 4-6GB richiesti da Qwen3-4B Q4_K_M (ampio margine)
- 22 vCPU + 90GB RAM = sufficiente per preprocessing, batching
- 400GB NVMe = storage adeguato per modello + cache
- 8 Gbps network = sufficiente per API inference

**Regione:** `GRA11` (Gravelines, Francia)

**Motivi:**
- EU-based, GDPR compliant
- Availability consolidata per GPU
- Latenza bassa per EU users
- Alternative: SBG5 (Strasbourg), DE (Frankfurt)

**Billing:** Monthly (se sconto disponibile)

**Motivi:**
- Workload 24/7 inference = fisso, non spot
- Possibile sconto ~50% → costo target €332-400/mese
- **VERIFICARE con OVHcloud se sconto mensile si applica a L4!**

### Setup Raccomandato

1. **OS:** Ubuntu 22.04 LTS con CUDA pre-installed (immagine OVHcloud)
2. **Inference Server:** vLLM (ottimizzato per Qwen, supporta quantizzazione)
3. **Container:** Docker image custom con vLLM + Qwen3-4B
4. **Deployment:** AI Deploy (container-as-a-service) con autoscaling se load variabile
5. **Monitoring:** OVHcloud Logs + custom health checks
6. **Backup:** Snapshot settimanali configurazione

### Prossimi Step

1. **Contattare OVHcloud Sales:**
   - Confermare pricing Euro per EU region
   - Chiedere sconto monthly billing su L4
   - Verificare disponibilità quota GPU (potrebbero servire giorni per approval)

2. **Proof of Concept (2-3 giorni):**
   - Deploy l4-90 hourly billing (test 24-48h)
   - Setup vLLM + Qwen3-4B
   - Benchmark performance, latenza, throughput
   - Costo PoC: ~€2-4 (2 giorni × €1/ora)

3. **Decisione:**
   - Se PoC OK + pricing mensile OK → Deploy production
   - Se pricing troppo alto → Valutare alternative (Vast.ai, Lambda Labs, etc.)

---

## 10. Alternative da Considerare (se budget issue)

Se OVHcloud L4 rimane fuori budget:

| Provider | GPU | Prezzo/mese stimato | Pro | Contro |
|----------|-----|-------------------|-----|--------|
| **Vast.ai** | L4 | €200-400 | Spot market economico | No SLA, community-hosted |
| **RunPod** | L4 | €250-350 | Billing per-second, buona UI | SLA variabile, meno EU-focused |
| **Lambda Labs** | A10 24GB | €350-500 | ML-optimized, docs eccellenti | US-based, GDPR complesso |
| **Scaleway** | GPU Instance | €400-600 | EU (Francia), renewable energy | Meno GPU options |
| **Hetzner** | Dedicated GPU | €300-500 | EU (Germania), affidabile | Setup più complesso, no managed |

**Raccomandazione:** Se budget è strict (≤€200/mese), considerare **Vast.ai** per PoC/staging, OVHcloud per production.

---

## Fonti

### Pricing & Specifications
- [OVHcloud Public Cloud Prices](https://us.ovhcloud.com/public-cloud/prices/)
- [OVHcloud L4 GPU Instance](https://www.ovhcloud.com/en/public-cloud/gpu/l4/)
- [OVHcloud GPU Portfolio](https://www.ovhcloud.com/en/solutions/nvidia/)
- [OVHcloud Public Cloud Regions Availability](https://www.ovhcloud.com/en/public-cloud/regions-availability/)
- [VPSBenchmarks OVHcloud Instance Types](https://www.vpsbenchmarks.com/instance_types/ovhcloud)

### Compliance & Certifications
- [OVHcloud ISO 27001/27017/27018 Certifications](https://us.ovhcloud.com/compliance/iso-27001-27017-27018/)
- [OVHcloud ISO 27701 Certification](https://us.ovhcloud.com/compliance/iso-27701/)
- [OVHcloud Attestations & Certifications](https://us.ovhcloud.com/compliance/)
- [OVHcloud GDPR Security](https://us.ovhcloud.com/personal-data-protection/security/)
- [OVHcloud ISO Certification Announcement](https://corporate.ovhcloud.com/en/newsroom/news/ovhcloud-extend-iso27001-and-iso27701-cloud-solutions/)

### Reliability & SLA
- [OVHcloud Public Cloud SLA](https://us.ovhcloud.com/legal/sla/public-cloud/)
- [OVHcloud GPU Review - GPU Providers](https://gpu-providers.com/reviews/ovhcloud-review/)
- [OVHcloud Reviews - Trustpilot](https://www.trustpilot.com/review/ovhcloud.com)
- [OVHcloud Reviews - G2](https://www.g2.com/products/ovhcloud/reviews)

### Setup & Documentation
- [Deploying a GPU Instance - OVHcloud Help](https://help.ovhcloud.com/csm/en-public-cloud-compute-deploy-gpu-instance)
- [GPU for LLM Inferencing Guide - OVHcloud Blog](https://blog.ovhcloud.com/gpu-for-llm-inferencing-guide/)
- [OVHcloud Deploying GPU Instance - Support Guide](https://support.us.ovhcloud.com/hc/en-us/articles/23538543708819-Deploying-a-GPU-instance)
- [OVHcloud NVIDIA GPU Cloud](https://www.ovhcloud.com/en/public-cloud/nvidia-gpu-cloud/)

### Infrastructure & Locations
- [OVHcloud Datacenter Regions](https://www.ovhcloud.com/en/about-us/global-infrastructure/regions/)
- [OVHcloud Datacenter Locations](https://www.ovhcloud.com/en/datacenters-ovhcloud/)
- [DataCenterMap - OVH Locations](https://www.datacentermap.com/c/ovh/)

### Comparisons
- [Cloud GPU Pricing Comparison 2025 - Verda](https://verda.com/blog/cloud-gpu-pricing-comparison)
- [Top GPU Cloud Providers 2026 - Hyperstack](https://www.hyperstack.cloud/blog/case-study/top-cloud-gpu-providers)
- [Cloud GPUs Comparison Table - Full Stack DL](https://fullstackdeeplearning.com/cloud-gpus/)
- [GPU Price Comparison 2026 - GetDeploying](https://getdeploying.com/gpus)

---

**Fine ricerca** - 11 Gennaio 2026

*Cervella Researcher - "Non reinventiamo la ruota - la miglioriamo!"* 🔬
