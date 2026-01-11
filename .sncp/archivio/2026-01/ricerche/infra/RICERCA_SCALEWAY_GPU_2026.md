# RICERCA: Scaleway GPU Cloud per Deploy LLM Inference

**Data Ricerca**: 11 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Contesto**: Deploy Qwen3-4B Q4_K_M (4-6GB VRAM), budget €50-200/mese, 24/7 production

---

## Executive Summary

**Status**: ⚠️ PARZIALMENTE RACCOMANDATO

**TL;DR**: Scaleway offre GPU L4/L40S in Europa con GDPR compliance, ma:
- **Pricing ALTO**: L4 ~€633/mese (fuori budget), L40S €1022/mese (molto fuori budget)
- **Affidabilità MISTA**: Reviews contrastanti, alcuni report di downtime
- **Setup**: Documentazione buona, ma nessun tutorial specifico vLLM
- **Pro**: 100% EU, GDPR native, datacenter Francia/NL/PL

**Raccomandazione**: Scaleway è tecnicamente valido ma COSTOSO per il nostro use case. Meglio per enterprise/public sector. Consiglio valutare alternative (Hetzner, OVHcloud) prima.

---

## 1. GPU Disponibili

### Portfolio GPU Scaleway

| GPU Model | VRAM | Use Case | Disponibilità |
|-----------|------|----------|---------------|
| **NVIDIA L4** | 24GB | Budget-friendly inference, POC, startup | ✅ Disponibile |
| **NVIDIA L40S** | 48GB | Universal GPU, faster than L4, cheaper than H100 | ✅ Disponibile |
| **NVIDIA H100 PCIe** | 80GB | Training, heavy inference, Transformer models | ✅ Disponibile |

### Configurazioni L4

| Instance Type | GPU | VRAM Totale | RAM | Storage | Note |
|---------------|-----|-------------|-----|---------|------|
| L4-1-24G | 1x L4 | 24GB | ~96GB | 1.6TB Scratch | Entry level |
| L4-2-24G | 2x L4 | 48GB | ~96GB | 1.6TB Scratch | - |
| L4-4-24G | 4x L4 | 96GB | ~192GB | 1.6TB Scratch | - |
| L4-8-24G | 8x L4 | 192GB | - | 1.6TB Scratch | - |

### Configurazioni L40S

| Instance Type | GPU | VRAM Totale | RAM | Storage | Note |
|---------------|-----|-------------|-----|---------|------|
| L40S-1-48G | 1x L40S | 48GB | ~96GB | 1.6TB Scratch | Universal |
| L40S-2-48G | 2x L40S | 96GB | - | 1.6TB Scratch | - |
| L40S-4-48G | 4x L40S | 192GB | - | 1.6TB Scratch | - |
| L40S-8-48G | 8x L40S | 384GB | - | 1.6TB Scratch | - |

**Note Configurazione**:
- Pricing include vCPU, RAM, 1.6TB Scratch Storage
- NON include: Block Storage, Flexible IP (€0.004/h extra)
- Savings Plans NON applicabili a L4, L40S, H100

---

## 2. Pricing ESATTO (Gennaio 2026)

### L4 Pricing

| Configurazione | Costo Orario | Costo Mensile 24/7 (730h) | Status Budget |
|----------------|--------------|---------------------------|---------------|
| **L4-1-24G** | $0.88/h (~€0.82/h) | **~€633/mese** | ❌ FUORI BUDGET |
| L4-2-24G | $1.76/h | ~€1,266/mese | ❌ |
| L4-4-24G | $3.52/h | ~€2,532/mese | ❌ |

**Special Pricing**: €0.75/h/GPU (contact experts) → ~€547/mese (ancora fuori budget €50-200)

### L40S Pricing

| Configurazione | Costo Orario | Costo Mensile 24/7 (730h) | Status Budget |
|----------------|--------------|---------------------------|---------------|
| **L40S-1-48G** | **€1.40/h** | **~€1,022/mese** | ❌ MOLTO FUORI BUDGET |
| L40S-2-48G | €2.80/h | ~€2,044/mese | ❌ |
| L40S-4-48G | €5.60/h | ~€4,088/mese | ❌ |
| L40S-8-48G | €11.20/h | ~€8,176/mese | ❌ |

### Market Comparison

| Provider | L40S Hourly | L4 Hourly | Note |
|----------|-------------|-----------|------|
| Scaleway | €1.40/h | $0.88/h | 3% off vs avg (L4) |
| Market Average | - | ~$0.91/h | - |
| Market Highest | $2.24/h | ~$0.99/h | - |
| Market Lowest | $0.32/h | - | Spot/preemptible |

**Analisi Pricing**: Scaleway L4 è competitivo vs market, ma TROPPO ALTO per budget €50-200/mese. Nessuna opzione spot/reserved pricing per ridurre costi.

---

## 3. Location EU & Data Centers

### Datacenter Locations

| Location | City | Country | Status |
|----------|------|---------|--------|
| **PAR** | Paris | Francia | ✅ Primary |
| **AMS** | Amsterdam | Olanda | ✅ Secondary |
| **WAW** | Warsaw | Polonia | ✅ Secondary |

**Totale**: 10 datacenter in Europa (4 in Francia)

### Data Sovereignty

- ✅ **100% EU Infrastructure**: Tutti i datacenter in territorio UE
- ✅ **NO Extra-territorial Laws**: Dati fuori portata USA CLOUD Act
- ✅ **Renewable Energy**: Infrastructure powered by renewable energy
- ✅ **French Company**: Provider francese, sotto giurisdizione EU

---

## 4. GDPR Compliance & Certificazioni

### GDPR

| Aspetto | Status | Dettaglio |
|---------|--------|-----------|
| GDPR Compliance | ✅ **Nativo** | GDPR compliant by design |
| Data Residency | ✅ **100% EU** | Tutti i datacenter in UE |
| Extra-territorial Protection | ✅ **Garantito** | Fuori portata USA CLOUD Act |
| DPA Disponibile | ✅ | Data Processing Agreement |

### Certificazioni

| Certificazione | Status | Valido Dal | Note |
|----------------|--------|------------|------|
| **ISO/IEC 27001:2022** | ✅ Certified | - | Information Security |
| **GDPR** | ✅ Compliant | 2018 | By design |
| **HDS** | ✅ Certified | Luglio 2024 | Health Data Host (Francia) |
| **ISO 27001** | ✅ Certified | - | Legacy version |

**Nota HDS**: Certificazione "Hébergeur de Données de Santé" rara, indica standard MOLTO alto per dati sensibili.

---

## 5. Reliability & SLA

### SLA Ufficiale

| Metrica | Valore | Note |
|---------|--------|------|
| **Uptime Guarantee** | **99.9% - 99.99%** | Dipende dal piano |
| Unavailability Period | 4 min continui | Perdita connettività esterna |
| Service Credits | Max 100% | Del costo mensile instance |
| Covered Service | ✅ GPU Instances | Include CPU + GPU instances |

### Customer Reviews Reliability

**Positive**:
- ✅ "Cheap, reliable and very stable - can't remember outages"
- ✅ "Never had it go down except user error"
- ✅ Support risolve issues in ~20 minuti
- ✅ Case study: 200,000 microlearnings "without any downtime"

**Negative**:
- ⚠️ Mixed reviews su TrustPilot (rating inferiore)
- ⚠️ Report di "servers going out of stock" anche per clienti paganti
- ⚠️ Alcuni utenti report "service deactivation without notification"
- ⚠️ "Not being able to launch instance from control panel"
- ⚠️ "Support teams not responding for several months" (isolati)
- ⚠️ Features launched poi suspended per difficoltà scaling

### Analisi Affidabilità

**Verdict**: ⚠️ **MISTA**

- **Enterprise/Production**: SLA 99.9-99.99% è BUONO ma non eccellente (vs 99.99% OVHcloud)
- **Downtime Reports**: Più frequenti di competitors enterprise
- **Support**: Veloce quando risponde, ma alcuni report di non-risposta
- **Stabilità**: OK per workload non mission-critical, RISCHIO per 24/7 critical inference

**Per nostro use case (24/7 inference production)**: RISCHIO MODERATO. Non il provider più affidabile.

---

## 6. Setup & Documentation

### Documentazione Ufficiale

| Risorsa | URL | Qualità |
|---------|-----|---------|
| GPU Instances Quickstart | scaleway.com/en/docs/gpu/quickstart/ | ⭐⭐⭐⭐ Buona |
| GPU Instance Concepts | scaleway.com/en/docs/gpu/concepts/ | ⭐⭐⭐⭐ Completa |
| Pricing Calculator | scaleway.com/en/pricing/gpu/ | ⭐⭐⭐ OK |
| Blog: LLM Infrastructure | scaleway.com/en/blog/infrastructures-for-llms-in-the-cloud/ | ⭐⭐⭐⭐ Utile |

### Setup Process

**Facilità**: ⭐⭐⭐⭐ (4/5) - Relativamente facile

1. **OS Image**: Ubuntu Noble GPU OS 13 (NVIDIA) - Drivers + Docker preinstallati
2. **Storage**: Provision Block Storage + Flexible IP manualmente
3. **Networking**: Private links up to 100 Gbps disponibili
4. **Docker**: NVIDIA Docker environment preconfigurato

### vLLM Deployment

**Status**: ⚠️ NESSUN TUTORIAL SPECIFICO SCALEWAY

- ✅ vLLM supporta NVIDIA L4 (compute capability >=7.0)
- ✅ vLLM Docker image disponibile (vllm/vllm-openai)
- ⚠️ Scaleway menziona vLLM nel blog, ma NO step-by-step guide
- ✅ Possibile combinare: Scaleway GPU setup + vLLM Docker deployment

**Workaround**:
1. Launch Scaleway L4 instance (Ubuntu Noble GPU OS 13)
2. Seguire vLLM Docker deployment docs ufficiali
3. Deploy Qwen3-4B con vLLM OpenAI-compatible server

### Managed Inference Alternative

Scaleway offre **Managed Inference**:
- ✅ Model Library con LLM quantizzati
- ✅ Deploy da Hugging Face (incluso Qwen 2.5/3)
- ✅ OpenAI Python client compatible
- ⚠️ Pricing separato (non chiaro se più economico)

**Nota**: Qwen 2.5-Coder-32B già disponibile su Managed Inference (Paris datacenter).

---

## 7. Pro & Contro - Analisi Onesta

### PRO ✅

| Pro | Impatto | Note |
|-----|---------|------|
| **100% EU Infrastructure** | ⭐⭐⭐⭐⭐ | Tutti datacenter in UE, GDPR nativo |
| **GDPR Compliance by Design** | ⭐⭐⭐⭐⭐ | Certificazioni HDS, ISO 27001:2022 |
| **NO USA CLOUD Act** | ⭐⭐⭐⭐⭐ | Data sovereignty garantita |
| **Renewable Energy** | ⭐⭐⭐ | Sostenibilità ambientale |
| **L4 Pricing Competitivo vs Market** | ⭐⭐⭐ | 3% off vs average ($0.88/h) |
| **Documentation Solida** | ⭐⭐⭐⭐ | Quickstart, concepts, blog posts |
| **NVIDIA Drivers Preinstallati** | ⭐⭐⭐⭐ | Ubuntu Noble GPU OS 13 ready |
| **Managed Inference Option** | ⭐⭐⭐ | Alternative a self-hosting |
| **Qwen Models Available** | ⭐⭐⭐ | Qwen 2.5/3 già su piattaforma |

### CONTRO ❌

| Contro | Impatto | Note |
|--------|---------|------|
| **PRICING MOLTO ALTO** | ⭐⭐⭐⭐⭐ | L4 €633/mese (budget €50-200) |
| **NO Spot/Reserved Pricing** | ⭐⭐⭐⭐ | Nessuna opzione risparmio |
| **Affidabilità Mista** | ⭐⭐⭐⭐ | Reviews contrastanti, alcuni downtime |
| **SLA 99.9%** | ⭐⭐⭐ | Inferiore a OVHcloud 99.99% |
| **NO vLLM Tutorial** | ⭐⭐⭐ | Manca guida step-by-step specifica |
| **Support Non Sempre Responsive** | ⭐⭐⭐ | Report isolati di non-risposta |
| **GPU "Out of Stock"** | ⭐⭐ | Alcuni report (raro) |
| **Features Suspended** | ⭐⭐ | Storicamente problemi scaling |
| **NO Savings Plans GPU** | ⭐⭐⭐⭐ | L4/L40S/H100 esclusi |

### Confronto Competitors EU

| Provider | L4/equiv | SLA | GDPR | Reliability | Pricing vs Scaleway |
|----------|----------|-----|------|-------------|---------------------|
| **Scaleway** | $0.88/h | 99.9% | ✅✅✅ | ⚠️ Mista | Baseline |
| **OVHcloud** | L4/L40S | **99.99%** | ✅✅ | ✅ Alta | Competitivo |
| **Hetzner** | RTX 4000/6000 | - | ✅✅ | ✅ Alta | **MOLTO PIÙ BASSO** |

**Winner Affidabilità**: OVHcloud (99.99% SLA)
**Winner Pricing**: Hetzner (budget-friendly)
**Winner GDPR/Sovereignty**: Scaleway (100% focus EU)

---

## 8. Raccomandazione Finale

### Per Nostro Use Case (Qwen3-4B, €50-200/mese, 24/7)

**VERDICT**: ⚠️ **NON RACCOMANDATO** (pricing fuori budget)

#### Analisi Budget

| Opzione | Costo Mensile | Budget Target | Gap |
|---------|---------------|---------------|-----|
| L4-1-24G Standard | €633/mese | €50-200/mese | **+316% OVER** |
| L4-1-24G Special | €547/mese | €50-200/mese | **+173% OVER** |
| Managed Inference | ??? | €50-200/mese | Unknown |

#### Quando Scegliere Scaleway

✅ **SI** se:
- Budget > €600/mese per GPU
- GDPR/EU sovereignty è CRITICO (public sector, health data)
- Requisiti compliance ISO 27001 + HDS
- OK con affidabilità 99.9% (non mission-critical 99.99%)
- Preferenza per provider francese/EU

❌ **NO** se:
- Budget < €300/mese
- Priorità: massima affidabilità (99.99%+)
- Cost optimization è priorità #1
- Need spot/reserved instances per risparmiare

#### Alternative Raccomandate

| Provider | GPU | Costo Stimato | Pro | Contro |
|----------|-----|---------------|-----|--------|
| **Hetzner** | RTX 4000 Ada | **€150-250/mese** | Budget-friendly, EU, affidabile | Meno GPU enterprise-grade |
| **OVHcloud** | L4/L40S | €400-600/mese | 99.99% SLA, EU, affidabile | Più costoso di Hetzner |
| **RunPod Spot** | L4/L40S | €50-150/mese | MOLTO economico, GPU variety | NO SLA, preemptible |

### Next Steps Consigliati

1. **PRIORITÀ 1**: Ricerca **Hetzner GPU** (RTX 4000/6000 Ada)
   - Target: €150-250/mese
   - EU datacenter (Germania/Finlandia)
   - Affidabilità alta

2. **PRIORITÀ 2**: Ricerca **OVHcloud GPU** (L4/L40S)
   - Target: €400-600/mese (se budget aumenta)
   - SLA 99.99%
   - Enterprise-grade

3. **OPZIONE 3**: Valutare **Scaleway Managed Inference**
   - Pricing Qwen models specifico
   - Potrebbe essere più economico di self-hosting

4. **FALLBACK**: Se GDPR è critico assolutamente
   - Considerare Scaleway con budget esteso
   - O attendere special pricing (€0.75/h)

---

## 9. Fonti & Collegamenti

### Documentazione Ufficiale Scaleway

- [GPU Instances Pricing](https://www.scaleway.com/en/pricing/gpu/)
- [L4 GPU Instance](https://www.scaleway.com/en/l4-gpu-instance/)
- [L40S GPU Instance](https://www.scaleway.com/en/l40s-gpu-instance/)
- [GPU Instances Available](https://www.scaleway.com/en/gpu-instances/)
- [Instance SLA](https://www.scaleway.com/en/virtual-instances/sla/)
- [Security & Certifications](https://www.scaleway.com/en/security-and-resilience/)
- [GPU Quickstart Documentation](https://www.scaleway.com/en/docs/gpu/quickstart/)
- [Managed Inference](https://www.scaleway.com/en/inference/)
- [Blog: LLM Infrastructure](https://www.scaleway.com/en/blog/infrastructures-for-llms-in-the-cloud/)

### Comparison & Reviews

- [GPU Providers: Scaleway Review](https://gpu-providers.com/reviews/scaleway-review/)
- [Scaleway TrustPilot Reviews](https://www.trustpilot.com/review/scaleway.com)
- [Scaleway HostAdvice Reviews](https://hostadvice.com/hosting-company/scaleway-reviews/)
- [Scaleway GPU Cloud - Shadeform](https://www.shadeform.ai/clouds/scaleway)
- [L40S on Scaleway Specs - Shadeform](https://www.shadeform.ai/instances/scaleway/L40S)

### Market Comparison

- [GPU Price Comparison 2026](https://getdeploying.com/gpus)
- [Cloud GPU Pricing Comparison 2025](https://verda.com/blog/cloud-gpu-pricing-comparison)
- [L4 GPU Pricing Comparison - ComputePrices](https://computeprices.com/gpus/l4)
- [Scaleway GPU Pricing - gpus.io](https://gpus.io/providers/scaleway)
- [Hetzner vs Scaleway - VPSBenchmarks](https://www.vpsbenchmarks.com/compare/hetzner_vs_scaleway)
- [Scaleway Alternatives - Kuberns](https://kuberns.com/blogs/post/scaleway-alternatives/)

### vLLM Resources

- [vLLM Official Documentation](https://docs.vllm.ai/en/stable/)
- [vLLM Docker Deployment](https://docs.vllm.ai/en/stable/deployment/docker/)
- [Deploying vLLM: Step-by-Step - Ploomber](https://ploomber.io/blog/vllm-deploy/)

### GDPR & Compliance

- [Scaleway GDPR - European Tech](https://european-tech.com/service/scaleway/)
- [Public Sector Solutions - Scaleway](https://www.scaleway.com/en/public-sector-solutions/)

---

## 10. Appendice: Calcoli Pricing

### L4-1-24G Breakdown

```
Costo base: $0.88/h
Conversione EUR (1 USD = ~0.93 EUR): €0.82/h

Mensile (730h):
€0.82/h × 730h = €598.60/mese

+ Flexible IP: €0.004/h × 730h = €2.92/mese
+ Block Storage (100GB stima): ~€10/mese

TOTALE STIMATO: ~€611-633/mese
```

### L40S-1-48G Breakdown

```
Costo base: €1.40/h

Mensile (730h):
€1.40/h × 730h = €1,022/mese

+ Flexible IP: €2.92/mese
+ Block Storage: ~€10/mese

TOTALE STIMATO: ~€1,035/mese
```

### Break-Even Analysis

Per rientrare in budget €200/mese:
```
€200 / 730h = €0.27/h massimo accettabile

Scaleway L4: €0.82/h
Gap: €0.55/h (67% troppo alto)

Needed discount: 67% off current price (IRREALISTICO)
```

---

## Conclusione

Scaleway è un provider ECCELLENTE per:
- Enterprise con budget adeguato
- Public sector con requisiti GDPR/HDS stringenti
- Organizzazioni che prioritizzano EU sovereignty

Ma per il nostro use case (Qwen3-4B, €50-200/mese):
- ❌ Pricing TROPPO ALTO (3x budget)
- ⚠️ Affidabilità non best-in-class
- ❌ No opzioni risparmio (spot/reserved)

**Prossimo Step**: Ricerca approfondita **Hetzner GPU** (target €150-250/mese, EU, affidabile).

---

**Fine Ricerca** - Cervella Researcher, 11 Gennaio 2026
