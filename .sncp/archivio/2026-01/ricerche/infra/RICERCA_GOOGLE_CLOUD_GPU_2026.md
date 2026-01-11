# Ricerca Google Cloud GPU per LLM Inference - 2026

**Data Ricerca:** 11 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Contesto:** Deploy Qwen3-4B Q4_K_M (4-6GB VRAM) per inference 24/7 production
**Budget Target:** €50-200/mese
**Requisiti:** EU, GDPR compliant, affidabile, siamo già clienti GCP

---

## TL;DR - Raccomandazione Rapida

**OPZIONE MIGLIORE: G2-Standard-4 con Committed Use Discount (1 anno)**

- GPU: NVIDIA L4 (24GB VRAM) - ideale per inference
- Pricing stimato: **€117-160/mese** (con CUD 1-3 anni)
- Region: europe-west4 (Paesi Bassi) o europe-west1 (Belgio)
- GDPR: Compliant, datacenter EU
- Pro: Già clienti GCP, integrazione immediata, L4 è GPU inference-optimized

**VS HETZNER (€184/mese):**
- GCP più economico con CUD
- GCP ha SLA enterprise, Hetzner è best-effort
- GCP scalabile, Hetzner server dedicato fisso

---

## 1. GPU Disponibili su GCP (2026)

### Entry-Level GPUs per Inference

| GPU | VRAM | Ideale Per | Tipo Machine |
|-----|------|------------|--------------|
| **NVIDIA T4** | 16GB | Inference cost-effective | N1 general-purpose |
| **NVIDIA L4** | 24GB | Inference optimized (2023+) | G2 accelerator-optimized |
| NVIDIA A100 40GB | 40GB | Training/inference pesante | A2 Standard |
| NVIDIA A100 80GB | 80GB | Training large models | A2 Ultra |

**Per Qwen3-4B (4-6GB VRAM):**
- ✅ **T4 (16GB)** - Sufficiente, budget-friendly
- ✅ **L4 (24GB)** - Raccomandato, architettura più recente, inference-optimized

---

## 2. Pricing ESATTO 2026

### NVIDIA T4 Pricing (N1 Machine Types)

| Configurazione | On-Demand | Spot/Preemptible | CUD 1yr | CUD 3yr |
|----------------|-----------|------------------|---------|---------|
| T4 GPU (singola) | $0.35-0.95/h | $0.14-0.29/h | ~$0.16/h | ~$0.16/h |
| **Mensile 24/7** | **$256-694** | **$102-212** | **~$117** | **~$117** |

**Note:**
- Pricing varia per region (iowa cheapest, europe-west leggermente più alto)
- Spot pricing dinamico, può cambiare ogni 30 giorni
- Sustained Use Discounts (SUD) fino a 30% su on-demand (automatico)

**Machine Type Esempio (N1 + T4):**
- n1-standard-4 (4 vCPU, 15GB RAM) + 1x T4 GPU
- Costo totale: GPU + VM + storage

### NVIDIA L4 Pricing (G2 Machine Types)

| Configurazione | On-Demand | Spot | Mensile 24/7 |
|----------------|-----------|------|--------------|
| **g2-standard-4** | $0.71/h | $0.06-0.12/h | **$515-520/mese** |
| (1x L4, 4 vCPU, 16GB RAM) | | | |
| g2-standard-8 | $1.47/h | $0.12-0.24/h | ~$1074/mese |
| (1x L4, 8 vCPU, 32GB RAM) | | | |

**Note:**
- G2 pricing include GPU + vCPU + RAM (all-inclusive)
- L4 è architettura più recente, ottimizzata per inference
- Disponibile in 18+ regions incluse EU

---

## 3. Committed Use Discounts (CUD)

### Come Funzionano

- **Impegno:** 1 anno o 3 anni di utilizzo continuativo
- **Sconto:** Fino a 55% su GPU e machine types
- **Flessibilità:** Puoi attaccare/staccare GPU, ma paghi comunque
- **Riserva GPU:** OBBLIGATORIO per GPU - devi creare reservation

### Calcolo CUD per L4 (g2-standard-4)

| Modalità | Prezzo | Risparmio vs On-Demand |
|----------|--------|------------------------|
| On-Demand | $520/mese | - |
| Spot (dinamico) | $44-88/mese | 83-91% |
| **CUD 1 anno** | **~$286/mese** | **~45%** |
| **CUD 3 anni** | **~$234/mese** | **~55%** |

**IMPORTANTE (Aggiornamento 2026):**
- Nuovo modello CUD multiprice dal 21 Gennaio 2026
- Maggiore granularità pricing per SKU
- Migrazione automatica contratti esistenti
- Opt-in disponibile ora per nuovo modello

### Pro/Contro CUD

**PRO:**
- Risparmio significativo (45-55%)
- Prezzo fisso e prevedibile
- Ideale per production 24/7

**CONTRO:**
- Lock-in 1-3 anni
- Paghi anche se non usi
- Richiede previsione capacity

**Per Noi:** Se siamo sicuri di usare GPU 24/7 per almeno 1 anno → CUD è NO-BRAINER.

---

## 4. Spot/Preemptible VMs

### Caratteristiche

- **Sconto:** 60-91% vs on-demand
- **Durata max:** Può essere terminata in qualsiasi momento (30 sec notice)
- **Use case:** Workload fault-tolerant, batch processing

### Pricing Spot GPU

| GPU | Spot Price | Mensile 24/7 | Risparmio |
|-----|------------|--------------|-----------|
| T4 | $0.14/h | $102/mese | ~85% |
| L4 (g2-standard-4) | $0.06-0.12/h | $44-88/mese | ~83-91% |

**PROBLEMA per noi:**
- ❌ Spot VMs possono essere terminate in qualsiasi momento
- ❌ NON adatto per inference 24/7 production critical
- ❌ Serve architettura fault-tolerant (fallback, replica)

**VERDICT:** Spot NO per inference production. Solo per dev/test.

---

## 5. Location EU - Regions Disponibili

### GPU Availability per Region EU

| Region | Location | T4 | L4 | A100 | Note |
|--------|----------|----|----|------|------|
| **europe-west1** | Belgio | ✅ | ✅ | ✅ | St. Ghislain, zones b,c |
| **europe-west4** | Paesi Bassi | ✅ | ✅ | ✅ | Eemshaven, zones a,b,c |
| europe-west2 | UK | ✅ | ✅ | - | Londra |
| europe-west3 | Germania | ✅ | ✅ | - | Francoforte |
| europe-west6 | Svizzera | ✅ | ✅ | - | Zurigo |
| europe-west8 | Italia | - | ✅ | - | Milano |
| europe-west9 | Francia | - | ✅ | - | Parigi |
| europe-west10 | Germania | - | ✅ | - | Berlino |
| europe-north1 | Finlandia | ✅ | ✅ | - | Hamina |
| europe-central2 | Polonia | - | ✅ | - | Varsavia |
| europe-southwest1 | Spagna | - | ✅ | - | Madrid |

**RACCOMANDAZIONE:**
- **europe-west4 (NL)** - Ottima connettività, T4 disponibile in 3 zones
- **europe-west1 (BE)** - Alternativa, leggermente più economica

### GDPR Compliance

✅ Tutti i datacenter EU sono GDPR compliant
✅ Data residency garantito in EU
✅ GCP ha DPA (Data Processing Agreement) standard
✅ Tools avanzati: Cloud DLP, IAM, audit logging

---

## 6. Vertex AI vs Compute Engine

### Compute Engine (IaaS)

**Pro:**
- ✅ Controllo totale su VM e configurazione
- ✅ Pricing più chiaro (solo infra)
- ✅ Flessibilità massima
- ✅ Committed Use Discounts disponibili

**Contro:**
- ❌ Setup manuale (VM, networking, auto-scaling)
- ❌ Manutenzione OS, security patches
- ❌ Autoscaling custom

**Use Case:** Deploy custom LLM server (FastAPI + vLLM/TGI), controllo totale.

### Vertex AI (Managed Service)

**Pro:**
- ✅ Deploy semplificato (upload model, deploy endpoint)
- ✅ Autoscaling automatico
- ✅ Monitoring/logging integrato
- ✅ CUD applicabili anche qui

**Contro:**
- ❌ Management fee (costo aggiuntivo ~20-30%)
- ❌ Meno controllo su configurazione
- ❌ Vendor lock-in

**Use Case:** Deploy rapido, prefer managed solution.

### Confronto Pricing Stimato

| Soluzione | Costo Mensile (stima) | Complexity |
|-----------|------------------------|------------|
| Compute Engine + T4 + CUD 1yr | ~$117-160/mese | Media |
| Compute Engine + L4 (g2-std-4) + CUD 1yr | ~$286/mese | Media |
| Vertex AI + T4 | ~$140-200/mese | Bassa |
| Vertex AI + L4 | ~$340-400/mese | Bassa |

**RACCOMANDAZIONE per noi:**
- **Compute Engine + vLLM/TGI** - Più economico, già sappiamo fare
- Vertex AI - Se vogliamo semplificare ops (ma costa di più)

---

## 7. Free Tier / Credits

### New Customer Credits

✅ **$300 crediti gratuiti** per 90 giorni
✅ Applicabili a QUALSIASI servizio GCP (incluse GPU)
✅ No carta di credito richiesta per free trial

**NOTA IMPORTANTE:**
- ❌ GPU hanno quota di default = 0 su free tier accounts
- ✅ Devi richiedere **quota increase** per GPU
- Path: Console → IAM & Admin → Quotas → Search "GPU" → Select region + GPU type

### Siamo Già Clienti GCP

Se abbiamo già progetti attivi:
- Probabilmente abbiamo già esaurito i $300 free credits
- Ma possiamo richiedere quota GPU immediatamente
- Nessun blocco per nuovi progetti

### Ongoing Free Tier

GCP ha Always Free tier, ma **NON include GPU**.
GPU sono sempre a pagamento.

---

## 8. Pro/Contro vs Hetzner

### Hetzner GPU Server (€184/mese)

**Specifiche (stimate):**
- GPU: RTX 40-series o simile
- Server dedicato
- Datacenter: Germania/Finlandia
- GDPR compliant

**PRO Hetzner:**
- ✅ Prezzo fisso, prevedibile
- ✅ Hardware dedicato (no noisy neighbors)
- ✅ GDPR compliant, EU datacenter
- ✅ Ottimo rapporto qualità/prezzo

**CONTRO Hetzner:**
- ❌ Server dedicato = nessuno scaling
- ❌ SLA best-effort (non enterprise)
- ❌ Setup/manutenzione più manuale
- ❌ No integrazione con GCP ecosystem

### Google Cloud (con CUD)

**PRO GCP:**
- ✅ **Più economico con CUD** (~$117-286/mese = €108-264)
- ✅ SLA enterprise (99.5-99.99%)
- ✅ Scalabilità immediata (add GPU in minuti)
- ✅ Integrazione ecosystem (Cloud Storage, IAM, monitoring)
- ✅ Già clienti, billing centralizzato
- ✅ GPU inference-optimized (L4)
- ✅ Spot per dev/test molto economico

**CONTRO GCP:**
- ❌ Pricing più complesso
- ❌ Vendor lock-in potenziale
- ❌ Spot VMs non affidabili per production

### Confronto Diretto

| Parametro | Hetzner | GCP (CUD 1yr) | Winner |
|-----------|---------|---------------|--------|
| **Prezzo mensile** | €184 | €108-264 (T4-L4) | **GCP (T4)** |
| **GPU Performance** | RTX 40-series | T4/L4 inference-optimized | **GCP (L4)** |
| **SLA** | Best-effort | 99.5-99.99% | **GCP** |
| **Scalabilità** | No (dedicato) | Immediata | **GCP** |
| **GDPR** | ✅ EU | ✅ EU | Pari |
| **Setup Complexity** | Media | Media | Pari |
| **Lock-in** | No | Si (CUD) | **Hetzner** |
| **Ecosystem** | Standalone | GCP integrato | **GCP** |

### VERDICT

**Per Inference 24/7 Production:**

1. **GCP Compute Engine + T4 + CUD 1yr** (~€117-160/mese)
   - Più economico di Hetzner
   - SLA enterprise
   - Scalabile
   - Già clienti GCP

2. **Hetzner GPU** (€184/mese)
   - Se vogliamo evitare lock-in GCP
   - Se preferiamo hardware dedicato
   - Valido backup/failover

3. **GCP L4 + CUD 1yr** (~€286/mese)
   - Se budget permette
   - GPU più recente, inference-optimized
   - Performance superiori

**RACCOMANDAZIONE FINALE:**
Iniziare con **GCP T4 + CUD 1 anno** (€117-160/mese).
Se performance insufficienti → upgrade a L4.
Se vogliamo diversificare → aggiungere Hetzner come backup.

---

## 9. Best Practices per Cost Optimization

### Infrastructure

1. **Right-size GPU:**
   - Per Qwen3-4B Q4_K_M (4-6GB) → T4 (16GB) è sufficiente
   - Non pagare per A100 se non serve

2. **Committed Use Discounts:**
   - Se 24/7 production → CUD 1 anno minimo (45% risparmio)
   - Se sicuri long-term → CUD 3 anni (55% risparmio)

3. **Region Selection:**
   - europe-west4 (NL) o europe-west1 (BE) - buon pricing EU
   - Evitare regions premium (asia, australia)

4. **Machine Type:**
   - T4: n1-standard-4 (4 vCPU, 15GB RAM) sufficiente
   - L4: g2-standard-4 (all-inclusive, già ottimizzato)

### Inference Optimization

1. **Model Optimization:**
   - ✅ Quantization (Q4_K_M già fatto)
   - ✅ vLLM o TGI per serving (paged attention, flash attention)
   - ✅ Batching per throughput

2. **Memory Management:**
   - Paged attention riduce memory fragmentation
   - Flash attention riduce data transfer GPU
   - KV cache optimization

3. **Caching:**
   - Prompt caching per query comuni
   - Warm model cache al boot

4. **Monitoring:**
   - GPU utilization (target 70-90%)
   - Se < 50% → consideriamo T4 invece di L4
   - Se > 95% → aggiungiamo capacity

### Development Workflow

1. **Dev/Test:** Spot VMs (83-91% risparmio)
2. **Staging:** On-Demand (flessibilità)
3. **Production:** CUD (costo ottimizzato)

---

## 10. Setup Raccomandato

### Scenario: Production Inference 24/7

**Configurazione:**
```
Region: europe-west4 (Paesi Bassi)
Machine Type: n1-standard-4 (4 vCPU, 15GB RAM)
GPU: 1x NVIDIA T4 (16GB VRAM)
Storage: 100GB SSD persistent disk
OS: Ubuntu 22.04 LTS
Pricing: CUD 1 anno
```

**Costo Stimato Mensile:**
- GPU T4 (CUD 1yr): ~$90/mese
- n1-standard-4: ~$30/mese
- Storage 100GB SSD: ~$17/mese
- Egress/networking: ~$10-20/mese
- **TOTALE: ~$147-157/mese (€135-145)**

**Software Stack:**
```
- Docker + NVIDIA Container Toolkit
- vLLM o TGI per serving
- FastAPI per REST API
- Prometheus + Grafana per monitoring
- Nginx reverse proxy (opzionale)
```

**Autoscaling:**
- Managed Instance Group con min=1, max=3
- Load balancer per distribuzione traffico
- Autoscale su CPU/GPU utilization

### Alternative: L4 per Performance

**Configurazione:**
```
Machine Type: g2-standard-4 (1x L4, 4 vCPU, 16GB RAM)
Pricing: CUD 1 anno (~$286/mese)
```

**Quando scegliere L4:**
- Servono latenze < 50ms
- Throughput elevato (100+ req/s)
- Budget permette (+$140/mese vs T4)

---

## 11. Prossimi Step

### Immediate Actions

1. **Verifica Quota GPU:**
   - Console GCP → IAM & Admin → Quotas
   - Cerca "NVIDIA T4 GPUs"
   - Region: europe-west4
   - Request increase se = 0

2. **Pricing Exact Check:**
   - GCP Pricing Calculator
   - Region: europe-west4
   - Machine: n1-standard-4 + 1x T4
   - Term: CUD 1 anno
   - Verify exact monthly cost

3. **Free Credit Check:**
   - Se abbiamo ancora crediti → usa per testing
   - Altrimenti, budget previsto OK (~€140/mese)

### Testing Phase

1. **Deploy POC (Spot VM):**
   - Usa Spot VM per test iniziali ($102/mese T4)
   - Deploy Qwen3-4B + vLLM
   - Benchmark performance, latency, throughput

2. **Validate:**
   - T4 sufficiente per use case?
   - vLLM/TGI configuration ottimale?
   - Networking/egress costs realistici?

3. **Go Production:**
   - Se test OK → Purchase CUD 1 anno T4
   - Setup production infra (monitoring, backup, etc.)

### Long Term

1. **Monitor Costs:**
   - GCP Billing dashboard
   - Alert se > budget
   - Quarterly review

2. **Optimize:**
   - Se GPU underutilized → downgrade
   - Se bottleneck → upgrade a L4
   - Se scale-out → add more instances

3. **Consider Hetzner:**
   - Come backup/failover
   - Come multi-cloud strategy
   - Se vogliamo evitare 100% GCP dependency

---

## 12. Fonti & Riferimenti

### Documentazione Ufficiale GCP

- [GPU Pricing](https://cloud.google.com/compute/gpus-pricing)
- [Compute Engine Pricing](https://cloud.google.com/compute/all-pricing)
- [GPU Regions and Zones](https://cloud.google.com/compute/docs/gpus/gpu-regions-zones)
- [Committed Use Discounts](https://docs.cloud.google.com/compute/docs/instances/committed-use-discounts-overview)
- [Spot VMs Pricing](https://cloud.google.com/spot-vms/pricing)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing)
- [Free Tier & Credits](https://cloud.google.com/free)

### Best Practices & Optimization

- [LLM Optimization on GKE](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices/machine-learning/inference/llm-optimization)
- [Cloud Run GPU Best Practices](https://docs.cloud.google.com/run/docs/configuring/services/gpu-best-practices)
- [Vertex AI Compute Configuration](https://cloud.google.com/vertex-ai/docs/predictions/configure-compute)
- [NVIDIA Inference Optimization](https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/)

### Pricing Comparison & Tools

- [CloudPrice.net - GCP GPU Pricing](https://cloudprice.net/gcp/compute)
- [GetDeploying GPU Comparison](https://getdeploying.com/gpus)
- [Economize Cloud - GCP GPU Pricing Chart](https://www.economize.cloud/blog/gcp-gpu-pricing-comparison/)
- [Vantage - GCP Instance Pricing](https://instances.vantage.sh/gcp/)

### Market Analysis

- [Northflank - Cheapest Cloud GPU Providers 2026](https://northflank.com/blog/cheapest-cloud-gpu-providers)
- [RunPod - Top 12 Cloud GPU Providers 2026](https://www.runpod.io/articles/guides/top-cloud-gpu-providers)
- [BentoML - Where to Buy/Rent GPUs for LLM Inference 2026](https://www.bentoml.com/blog/where-to-buy-or-rent-gpus-for-llm-inference)

### GCP vs Competitors

- [GetDeploying - Google Cloud vs Hetzner](https://getdeploying.com/google-cloud-vs-hetzner)
- [VPSBenchmarks - GCE vs Hetzner](https://www.vpsbenchmarks.com/compare/gce_vs_hetzner)
- [Slashdot - GCP vs Hetzner Comparison](https://slashdot.org/software/comparison/Google-Cloud-Platform-vs-Hetzner/)

### Technical Articles

- [NVIDIA T4 GPUs on Google Cloud](https://developer.nvidia.com/blog/nvidia-t4-gpus-now-available-on-google-cloud/)
- [Modal - NVIDIA T4 Cost Analysis](https://modal.com/blog/nvidia-t4-price-article)
- [Modal - NVIDIA L4 Cost Analysis](https://modal.com/blog/nvidia-l4-price-article)
- [Google Cloud - Selecting GPUs for LLM Serving on GKE](https://cloud.google.com/blog/products/ai-machine-learning/selecting-gpus-for-llm-serving-on-gke)

---

## Conclusioni

### La Nostra Strada

**RACCOMANDAZIONE FINALE: Google Cloud T4 + CUD 1 Anno**

**PERCHÉ:**
1. **Budget-friendly:** €135-145/mese (vs €184 Hetzner)
2. **Già clienti GCP:** Integrazione immediata, billing centralizzato
3. **GDPR compliant:** Datacenter EU (europe-west4 NL)
4. **SLA enterprise:** 99.5%+ uptime garantito
5. **Scalabile:** Possiamo aggiungere GPU in minuti se serve
6. **T4 sufficiente:** 16GB VRAM per Qwen3-4B Q4_K_M (4-6GB)

**NEXT STEPS:**
1. Verifica quota GPU in europe-west4
2. Deploy POC con Spot VM (testing economico)
3. Se performance OK → Purchase CUD 1 anno
4. Setup production con vLLM/TGI

**ALTERNATIVE:**
- Se budget permette (+€140/mese) → L4 per performance superiori
- Se vogliamo multi-cloud → Hetzner come backup (€184/mese)
- Se vogliamo zero ops → Vertex AI (+20-30% costo)

**La scelta è chiara: GCP T4 + CUD è il sweet spot per noi.**

---

*Ricerca completata: 11 Gennaio 2026*
*Cervella Researcher - CervellaSwarm*
