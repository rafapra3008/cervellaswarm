# RICERCA HETZNER GPU SERVERS 2026

**Data ricerca**: 11 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Obiettivo**: Valutare Hetzner per deploy LLM inference (Qwen3-4B Q4_K_M)

---

## EXECUTIVE SUMMARY

**RACCOMANDAZIONE**: ✅ **Hetzner GEX44 è IDEALE per il nostro use case**

| Criterio | Rating | Note |
|----------|--------|------|
| **Prezzo** | ⭐⭐⭐⭐⭐ | €184/mese - IMBATTIBILE per 24/7 |
| **Performance** | ⭐⭐⭐⭐ | RTX 4000 Ada 20GB - ottima per Qwen 4B-32B |
| **GDPR/Compliance** | ⭐⭐⭐⭐⭐ | ISO 27001:2022, datacenter EU, GDPR native |
| **Reliability** | ⭐⭐⭐⭐ | NO SLA formale, ma feedback utenti positivo |
| **Setup Complexity** | ⭐⭐⭐ | Bare metal, 1-3 giorni provisioning |

**TL;DR**: Per €184/mese (vs ~€1008/mese Scaleway, ~$1145/mese OVH), Hetzner offre RTX 4000 Ada 20GB VRAM in datacenter EU con ISO 27001. Performance verificata: 17 tok/s su Qwen2.5-32B quantizzato. Setup fee €79 una tantum.

---

## 1. GPU DISPONIBILI

Hetzner offre **3 modelli** di GPU dedicated servers (2026):

### GEX44 (ENTRY-LEVEL - IL NOSTRO TARGET)

| Spec | Valore |
|------|--------|
| **GPU** | NVIDIA RTX 4000 SFF Ada Generation |
| **VRAM** | 20 GB GDDR6 ECC |
| **Tensor Cores** | 192 |
| **CPU** | Intel Core i5-13500 (13th gen) - 6P + 8E cores |
| **RAM** | 64 GB DDR4 |
| **Storage** | 2x 1.92 TB NVMe SSD Gen3 (RAID 1) |
| **Network** | 1 Gbit/s (guaranteed, unlimited traffic) |
| **Power** | 33W idle, 187W max |

**Ideale per**: AI inference, LLM API serving (specificatamente progettato per questo)

### GEX131 (HIGH-END)

| Spec | Valore |
|------|--------|
| **GPU** | NVIDIA RTX Pro 6000 Blackwell Max-Q |
| **VRAM** | 96 GB GDDR7 ECC |
| **Prezzo** | €889/mese |

**Uso**: AI training, dataset processing avanzati

### GEX130 (MID-RANGE)

| Spec | Valore |
|------|--------|
| **GPU** | NVIDIA RTX 6000 Ada Generation |
| **VRAM** | 48 GB GDDR6 ECC |
| **Prezzo** | Non specificato pubblicamente |

---

## 2. PRICING ESATTO 2026

### GEX44 - Pricing Dettagliato

| Voce | Costo |
|------|-------|
| **Mensile** | €184.00 - €205.00 |
| **Setup Fee (una tantum)** | €159.00 - €177.00 |
| **Contratto minimo** | NESSUNO |
| **Cancellazione** | Immediata |
| **Traffico** | ILLIMITATO incluso |

**Metodi pagamento**: Bank transfer, Credit Card, PayPal, SEPA Direct Debit

**Costo annuale stimato**:
- Anno 1: (€184 × 12) + €159 setup = **€2,367**
- Anno 2+: €184 × 12 = **€2,208/anno**

### Confronto Pricing Altri Modelli

| Modello | Mensile | Setup | VRAM | €/GB VRAM |
|---------|---------|-------|------|-----------|
| **GEX44** | €184 | €159 | 20 GB | €9.20 |
| GEX131 | €889 | N/A | 96 GB | €9.26 |

**Nota**: Il pricing per GB VRAM è sostanzialmente identico - GEX44 è entry point economico, GEX131 è per scale.

---

## 3. LOCATION EU & DATACENTER

### Datacenter Disponibili

| Location | Codice | GEX44 | Note |
|----------|--------|-------|------|
| **Falkenstein, Germany** | FSN1 | ✅ | Disponibile |
| **Nuremberg, Germany** | NBG1 | ✅ | Disponibile |
| **Helsinki, Finland** | HEL1 | ✅ | Disponibile |

### Network Infrastructure

**Backbone**:
- Ring network tra Falkenstein ↔ Nuremberg ↔ Frankfurt
- Multi-redundant uplinks a Internet Exchange
- 1300 Gbit/s verso DE-CIX
- Upgrade 2025: Nokia 7750 SR-1x routers (100G, ready 400G/800G)

**Latency**:
- Ottimale per utenti EU
- Nuremberg ospita N-IX (Internet Exchange locale) → ultra-low latency

**DDoS Protection**: Inclusa gratuitamente

---

## 4. GDPR COMPLIANCE & CERTIFICAZIONI

### ISO 27001:2022 ✅

**Certificato**: ISO/IEC 27001:2022 (Information Security Management System)
**Scope**: Infrastructure, operations, customer support in **TUTTI** i datacenter (Nuremberg, Falkenstein, Helsinki)
**Audit**: SOCOTEC Certification (third-party)
**Validità**: Continua (re-audit periodici obbligatori)

**Link certificato**: https://www.hetzner.com/assets/downloads/ISO-Certificate.pdf

### GDPR Compliance ✅

**Status**: FULL GDPR Compliant (German cloud provider)
**Normativa**: EU GDPR nativa (headquarter Germania)
**Data Processing Agreement**: Disponibile pubblicamente
**Technical & Organizational Measures**: Documentati (Appendix 2 DPA)

**Note importante**: Anche datacenter USA/Singapore sono GDPR-compliant (master data resta con Hetzner Online GmbH, non trasferita a subsidiary).

### Altre Certificazioni

Hetzner ha molteplici certificazioni documentate nella pagina ufficiale:
https://www.hetzner.com/unternehmen/zertifizierung/

---

## 5. RELIABILITY & SLA

### SLA Ufficiale

**STATUS**: ❌ **NO SLA formale**

Hetzner **NON offre** un SLA con uptime garantito contrattualmente. Questo significa:
- ❌ Nessuna garanzia uptime % (es. 99.9%)
- ❌ Nessun rimborso automatico per downtime
- ❌ Non adatto per scenari mission-critical con requisiti SLA contrattuali

### Uptime Storico (Community Feedback)

**Feedback positivi**:
- "Absolutely zero downtime or network issues" (4 mesi)
- "First unexpected outage after 3 years of service"
- "Cheap and reliable provider for many years, only a couple hardware issues resolved promptly"
- "Performance significantly better than competitors for WordPress/VPS"

**Feedback negativi**:
- Account blocking senza spiegazione (casi isolati, 2026)
- Support response time in calo (fino a 2 giorni per email)

**Rating community**:
- WHTop: 3.7/10 (32 reviews) - rating basso ma basato su supporto, non uptime
- TrustPilot: Feedback misti (alcuni eccellenti, altri problematici)

### Mitigazione NO-SLA

Se serve SLA per compliance:
- Usare **managed service provider** su Hetzner infrastructure
- Alcuni MSP offrono SLA su infra Hetzner

**Per il nostro caso (MVP/POC)**:
✅ NO-SLA è accettabile - risparmio €800+/mese giustifica rischio

---

## 6. SETUP & PROVISIONING

### Complessità Setup

**Tipo**: Bare metal dedicated server (NON cloud instance)
**Accesso**: Full root access
**OS supportati**: Ubuntu, CentOS, Linux, Windows (64-bit)

### Processo Provisioning

| Step | Tempo | Note |
|------|-------|------|
| 1. Ordine via Robot | Immediato | GEX44 reserved for existing customers |
| 2. Provisioning hardware | 1-3 giorni | "Sometimes a few days" |
| 3. OS installation | Automatico | Via rescue system + VNC |
| 4. Setup GPU drivers | Manuale | Nvidia driver install |
| 5. Deploy LLM stack | Manuale | Ollama/vLLM/TensorRT |

**Complessità**: ⭐⭐⭐ (Media)

**Risorse disponibili**:
- ✅ GitHub cheatsheet: https://github.com/stefan-it/hetzner-gpu-server (archived, ma utile)
- ✅ Hetzner Community tutorial: "Running DeepSeek with Ollama"
- ✅ Community tutorial: "Hosting AI chatbot with Ollama and Open WebUI"
- ❌ NO automazione via API (non come cloud VMs)

### Alternative CPU-Only

**Interessante**: Hetzner suggerisce che per modelli moderni, inference CPU è possibile se:
- Server ha RAM sufficiente
- Buona velocità RAM
- SSD veloce e capiente

**Modello suggerito**: AX52 @ €59/mese (no GPU, ma sufficiente per modelli piccoli)

---

## 7. PERFORMANCE LLM INFERENCE

### RTX 4000 Ada - Benchmarks Qwen

**DATO CHIAVE** (dal benchmark ufficiale):

```
Qwen2.5-32B-Instruct-IQ4_XS: 16.93 tokens/second
```

**Interpretazione**:
- ✅ "Fluid experience for many LLM based applications"
- ✅ Sufficiente per utenti singoli/low concurrency
- ⚠️ Non per fleet multi-user ad alta concorrenza

### Performance Generale LLM

| Model Size | Quantization | Performance | Status |
|------------|--------------|-------------|--------|
| **7B-13B** | Q4_K_M | 58.59 tok/s | ✅ Ottima |
| **32B** | IQ4_XS | 16.93 tok/s | ✅ Fluida |
| **>30B** | Non quantized | OOM | ❌ Out of memory |

**VRAM 20GB è sufficiente per**:
- ✅ Qwen3-4B (nostro target) - ABBONDANTE
- ✅ Qwen2.5-7B/14B quantized
- ✅ Qwen2.5-32B quantized (IQ4_XS)
- ❌ Qwen2.5-72B (richiede >20GB anche quantizzato)

### Confronto GPU Class

L'RTX 4000 Ada è classificata come:
- ✅ Professional/Workstation GPU (non consumer)
- ✅ ECC memory (affidabilità)
- ⚠️ NOT datacenter-class (no H100/A100/L40S)
- ⚠️ 70W TDP (efficiente, ma meno raw power di datacenter GPU)

**Raccomandazione uso**:
> "Capable for developer and small-scale production LLM inference (7-13B models) with quantization and TensorRT-LLM/vLLM optimizations. Not a replacement for NVLink-equipped datacenter GPUs for >30B models or multi-user inference fleets."

**Per Qwen3-4B Q4_K_M**: ✅✅✅ PERFETTO

---

## 8. BACKUP & DISASTER RECOVERY

### Opzioni Backup

**Per Dedicated Servers** (categoria GEX44):

#### Storage Box (raccomandato)

| Feature | Dettaglio |
|---------|-----------|
| **Tipo** | Remote storage dedicato |
| **Accesso** | FTP, SFTP, SCP, RSYNC, WebDAV, Samba |
| **Setup** | Manuale (unmanaged) |
| **Costo** | Separato (€3-50/mese a seconda size) |

**Workflow**:
1. Acquistare Storage Box separatamente
2. Configurare backup script (rsync/rclone)
3. Scheduling via cron

#### Snapshots Manuali

**Limitazione**: Le snapshot cloud (20% del prezzo server) sono per **Cloud Servers**, NON dedicated.

Per GEX44 (dedicated):
- ❌ NO snapshot automatiche come cloud
- ✅ Backup manuale verso Storage Box
- ✅ Backup verso S3-compatible storage esterno

### Disaster Recovery

**Strumenti disponibili**:
- REAR (Relax-and-Recover) per full system backup
- Rescue system (incluso) per recovery
- Kexec per migration

**Limitazione IMPORTANTE**:
> Dedicated servers = responsabilità cliente per backup setup. Nessun backup automatico incluso.

### Raccomandazione

Per production LLM inference:
1. **Code/config**: Git
2. **Model weights**: Storage Box o S3 (Cloudflare R2 free egress)
3. **User data/logs**: Storage Box + rsync daily
4. **Disaster recovery**: Documentare setup in Infrastructure-as-Code (Ansible)

**Costo aggiuntivo stimato**: €10-30/mese per Storage Box adeguato

---

## 9. PRO & CONTRO (ANALISI ONESTA)

### ✅ PRO

1. **PREZZO IMBATTIBILE**
   - €184/mese vs €1008+ competitor
   - 82% risparmio vs Scaleway
   - 84% risparmio vs OVHcloud

2. **COMPLIANCE ECCELLENTE**
   - ISO 27001:2022 certificato
   - GDPR native (German company)
   - Datacenter 100% EU

3. **PERFORMANCE VERIFICATA**
   - RTX 4000 Ada provata su Qwen 16-17 tok/s
   - 20GB VRAM più che sufficiente per Qwen3-4B
   - ECC memory per affidabilità

4. **NETWORK SOLIDO**
   - 1 Gbit/s guaranteed
   - Traffico illimitato (zero costi nascosti)
   - DDoS protection inclusa

5. **FLESSIBILITÀ CONTRATTUALE**
   - NO minimum contract
   - Cancellazione immediata
   - Full root access

6. **EFFICIENZA ENERGETICA**
   - 33W idle, 187W max
   - Costi operativi bassi

### ⚠️ CONTRO

1. **NO SLA FORMALE**
   - Nessuna garanzia uptime contrattuale
   - Nessun rimborso per downtime
   - Rischio per scenari mission-critical

2. **PROVISIONING LENTO**
   - 1-3 giorni per setup
   - NO instant provisioning come cloud
   - NO API provisioning

3. **BARE METAL COMPLEXITY**
   - Setup manuale richiesto
   - Gestione OS/drivers/updates manuale
   - NO managed service

4. **BACKUP NON INCLUSO**
   - Responsabilità cliente
   - Costo aggiuntivo Storage Box
   - Setup manuale

5. **SUPPORTO IN DECLINE** (feedback 2025-2026)
   - Response time fino a 2 giorni
   - Alcuni casi account blocking inspiegabili
   - Community rating misto

6. **LIMITAZIONI GPU**
   - Solo 1 GPU per server (no multi-GPU)
   - RTX series (no H100/A100 datacenter class)
   - Performance limitata per >30B non-quantized

7. **RESERVED FOR EXISTING CUSTOMERS**
   - GEX44 non disponibile per nuovi clienti immediatamente
   - Serve essere existing customer Hetzner

### 🎯 FIT PER IL NOSTRO USE CASE

| Requisito | Hetzner GEX44 | Match |
|-----------|---------------|-------|
| **Budget €50-200/mese** | €184/mese | ✅ Nel range |
| **Qwen3-4B Q4_K_M (4-6GB VRAM)** | 20GB VRAM | ✅ 3x margin |
| **24/7 inference production** | Dedicated | ✅ Perfetto |
| **EU location** | DE/FI | ✅ 100% EU |
| **GDPR compliant** | ISO 27001 | ✅ Certificato |
| **Affidabilità** | NO SLA | ⚠️ Rischio accettabile MVP |

**VERDICT**: ✅ **OTTIMO FIT** per MVP/early production. Per scale futuro, considerare managed alternative.

---

## 10. CONFRONTO COMPETITOR

### HETZNER vs SCALEWAY vs OVHCLOUD

#### Pricing Comparison (24/7 workload)

| Provider | Model | GPU | VRAM | Mensile | Setup | Annuale |
|----------|-------|-----|------|---------|-------|---------|
| **HETZNER** | GEX44 | RTX 4000 Ada | 20GB | €184 | €159 | €2,367¹ |
| **Scaleway** | L40S | L40S | 48GB | ~€1,008² | €0 | €12,096 |
| **OVHcloud** | Scale-GPU-1 | 2x L4 | 48GB³ | $1,145 | N/A | $13,740 |

¹ Anno 1 include setup fee; anno 2+ = €2,208
² Calcolato da €1.4/ora × 720 ore/mese
³ 2 GPU L4 da 24GB ciascuna

#### Feature Comparison

| Feature | Hetzner | Scaleway | OVHcloud |
|---------|---------|----------|----------|
| **Billing** | Monthly | Hourly | Monthly |
| **Contract** | None | None | Varies |
| **Provisioning** | 1-3 days | Instant | Hours-days |
| **SLA** | ❌ None | ✅ Available | ✅ 99.99% |
| **Backup** | Manual | Automated | Automated |
| **API** | ❌ Limited | ✅ Full | ✅ Full |
| **Support** | Basic | Business | Enterprise |
| **Location** | DE/FI | FR | FR/CA/others |
| **GDPR** | ✅ Native | ✅ Yes | ✅ Yes |
| **GPU Type** | RTX Pro | Datacenter | Datacenter |

#### Use Case Fit

**HETZNER** (GEX44):
- ✅ **BEST per**: 24/7 production, budget-conscious, EU-only, long-running inference
- ❌ **WORST per**: Instant scaling, guaranteed SLA, managed service

**SCALEWAY**:
- ✅ **BEST per**: Variable workloads, H100 access, hourly billing, auto-scaling
- ❌ **WORST per**: 24/7 workloads (€1k+/mese), tight budget

**OVHCLOUD**:
- ✅ **BEST per**: Enterprise SLA requirements, multi-GPU, managed service
- ❌ **WORST per**: Budget (>$1k/mese), small workloads

#### Cost Analysis (12 mesi)

```
Scenario: Qwen3-4B inference 24/7

Hetzner:  €2,367 (anno 1) = €197/mese medio
Scaleway: €12,096         = €1,008/mese
OVHcloud: $13,740         = $1,145/mese (~€1,080)

RISPARMIO Hetzner:
vs Scaleway: €9,729/anno (80% saving)
vs OVHcloud: ~€10,000/anno (81% saving)
```

#### Performance Comparison

| Provider | GPU | VRAM | Qwen3-4B Est. | Qwen2.5-32B Q4 |
|----------|-----|------|---------------|----------------|
| **Hetzner** | RTX 4000 Ada | 20GB | ~60 tok/s⁴ | 17 tok/s |
| Scaleway | L40S | 48GB | ~100 tok/s⁴ | ~40 tok/s⁴ |
| OVHcloud | 2x L4 | 48GB | ~80 tok/s⁴ | ~30 tok/s⁴ |

⁴ Stime basate su benchmarks pubblici, variabili con quantization/optimization

**Nota performance**: Per Qwen3-4B, le differenze sono minime in single-user scenario. Multi-GPU/datacenter GPUs vincono in high-concurrency.

---

## 11. RACCOMANDAZIONE FINALE

### Per Qwen3-4B Inference Production

**SCELTA RACCOMANDATA**: 🏆 **Hetzner GEX44**

**Motivazione**:
1. **Budget perfetto**: €184/mese nel nostro range ideale
2. **Performance adeguata**: 20GB VRAM 3x superiore al necessario, margine per scale
3. **Compliance**: ISO 27001 + GDPR = green light per EU
4. **Rischio SLA accettabile**: Per MVP/early prod, feedback community positivo compensa mancanza SLA formale
5. **ROI**: Risparmiamo €800+/mese vs competitor, reinvestibili in development

### Strategia Deployment Consigliata

**FASE 1 - MVP (Mesi 1-3)**:
- ✅ Deploy su Hetzner GEX44
- ✅ Setup monitoring (uptime, performance)
- ✅ Backup manuale → Storage Box
- ✅ Documentare setup per DR

**FASE 2 - Production Validation (Mesi 4-6)**:
- ✅ Raccogliere metriche uptime reali
- ✅ Valutare se NO-SLA è problema pratico
- ⚠️ Se downtime inaccettabile → migrate a Scaleway/OVH

**FASE 3 - Scale (Mesi 7+)**:
- Se workload rimane stabile: rimanere Hetzner (risparmio)
- Se serve scaling/SLA: hybrid (Hetzner + Scaleway spot instances)
- Se enterprise critical: migrate OVHcloud con SLA

### Mitigazioni Rischio NO-SLA

1. **Monitoring aggressivo**: UptimeRobot + Prometheus + alerting
2. **Backup automatizzato**: Daily snapshot modello + config su S3
3. **Documentation as Code**: Ansible playbook per rebuild in <2 ore
4. **Failover plan**: Script per switch rapido a Scaleway GPU instance (costo spot)

### Quando NON scegliere Hetzner

❌ **Evitare se**:
- Serve SLA contrattuale (compliance/legale)
- Workload mission-critical con penali downtime
- Serve instant scaling (traffic spikes imprevedibili)
- Team non ha competenze bare metal management
- Budget permette datacenter GPU (€1k+/mese)

---

## 12. NEXT STEPS

**Per procedere con Hetzner GEX44**:

### Immediati (Pre-Ordine)
1. [ ] Verificare se siamo "existing customer" Hetzner
   - Se NO: creare account + ordinare VPS minimo (€3/mese) per qualificare
2. [ ] Scegliere datacenter: FSN1 (Falkenstein) raccomandato
3. [ ] Preparare budget: €184 + €159 setup = €343 primo mese

### Setup (Post-Ordine)
1. [ ] Ordinare GEX44 via Robot
2. [ ] Attendere provisioning (1-3 giorni)
3. [ ] Setup OS: Ubuntu 22.04 LTS
4. [ ] Install NVIDIA drivers + CUDA toolkit
5. [ ] Deploy Ollama/vLLM
6. [ ] Test Qwen3-4B Q4_K_M

### Post-Deployment
1. [ ] Setup monitoring (Prometheus + Grafana)
2. [ ] Configure backup → Storage Box (€10/mese)
3. [ ] Document infrastructure (Ansible)
4. [ ] Create disaster recovery runbook

---

## 13. FONTI

### Hetzner Ufficiale
- [GEX44 Product Page](https://www.hetzner.com/dedicated-rootserver/gex44/)
- [GEX131 High-End GPU](https://www.hetzner.com/dedicated-rootserver/gex131/)
- [GPU Server Matrix](https://www.hetzner.com/dedicated-rootserver/matrix-gpu/)
- [GPU Server Press Release](https://www.hetzner.com/press-release/new-gpu-server/)
- [Certifications](https://www.hetzner.com/unternehmen/zertifizierung/)
- [ISO Certificate PDF](https://www.hetzner.com/assets/downloads/ISO-Certificate.pdf)
- [Datacenter Info](https://www.hetzner.com/unternehmen/rechenzentrum/)

### Documentazione Tecnica
- [Hetzner Docs - GPU Server Config](https://docs.hetzner.com/robot/dedicated-server/server-lines/gpu-server/)
- [Hetzner Docs - Locations](https://docs.hetzner.com/cloud/general/locations/)
- [Hetzner Docs - Certificates](https://docs.hetzner.com/general/others/certificates/)
- [Hetzner Docs - Technical & Organizational Measures](https://docs.hetzner.com/general/others/technical-and-organizational-measures/)
- [Hetzner Docs - Backups & Snapshots](https://docs.hetzner.com/cloud/servers/backups-snapshots/overview/)

### Benchmarks & Performance
- [RTX 4000 Ada for LLM - Hardware Corner](https://www.hardware-corner.net/guides/rtx-4000-sff-ada-for-llm/)
- [LLM Inference RTX GPU Performance - Puget Systems](https://www.pugetsystems.com/labs/articles/llm-inference-professional-gpu-performance/)
- [RTX 4000 Ada AI Benchmarks - GIGA CHAD LLC](https://gigachadllc.com/nvidia-rtx-4000-ada-generation-ai-benchmarks-breakdown/)
- [Ollama A4000 Benchmark](https://www.databasemart.com/blog/ollama-gpu-benchmark-a4000)
- [Best NVIDIA GPUs for LLM Inference 2025](https://www.databasemart.com/blog/best-nvidia-gpus-for-llm-inference-2025)

### Community & Reviews
- [Hetzner TrustPilot Reviews](https://www.trustpilot.com/review/hetzner.com)
- [Hetzner WHTop Reviews](https://www.whtop.com/review/hetzner.com)
- [Hetzner G2 Reviews](https://www.g2.com/products/hetzner/reviews)
- [Hetzner Cloud Review 2026 - BitDoze](https://www.bitdoze.com/hetzner-cloud-review/)
- [Hacker News - GPU Server Discussion](https://news.ycombinator.com/item?id=41646163)
- [Forum: Better GPU Deal than Hetzner?](https://forumweb.hosting/25757-better-gpu-server-deal-than-hetzner-looking-for-alternatives.html)

### Setup Guides
- [Run LLM on Hetzner - Codref](https://codref.org/rated-d/run-llm-on-hetzner/)
- [GitHub: Hetzner GPU Server Setup Cheatsheet](https://github.com/stefan-it/hetzner-gpu-server)
- [Hetzner Community: AI Chatbot with Ollama](https://community.hetzner.com/tutorials/ai-chatbot-with-ollama-and-deepseek/)
- [Automating Bare Metal with Ansible - Palark](https://palark.com/blog/ansible-hetzner-bare-metal-linux/)

### Competitor Analysis
- [GPU Price Comparison 2026](https://getdeploying.com/gpus)
- [Hetzner vs Scaleway - GetDeploying](https://getdeploying.com/hetzner-vs-scaleway)
- [Scaleway GPU Pricing](https://www.scaleway.com/en/pricing/gpu/)
- [OVHcloud GPU Dedicated Server](https://www.ovhcloud.com/en/bare-metal/gpu-dedicated-server/)
- [Top 5 GPU Server Providers 2026 - Cherry Servers](https://www.cherryservers.com/blog/top-dedicated-server-providers-with-gpu)
- [DigitalOcean vs Hetzner](https://www.digitalocean.com/resources/articles/digitalocean-vs-hetzner)

### SLA & Reliability
- [Hetzner Terms & Conditions](https://www.hetzner.com/legal/terms-and-conditions/)
- [Dedicated Server Service Agreement](https://www.hetzner.com/legal/dedicated-server/)
- [Hetzner Uptime Discussion - WebHostingTalk](https://www.webhostingtalk.com/showthread.php?t=1080100)

---

**Fine Ricerca** - 11 Gennaio 2026
**Prossimo step**: Discussione con Regina per decisione finale deploy strategy

---

## APPENDICE: Quick Decision Matrix

```
SCEGLI HETZNER SE:
✅ Budget < €300/mese
✅ Workload 24/7 stabile
✅ Team può gestire bare metal
✅ NO requirement SLA contrattuale
✅ EU-only deployment OK
✅ Modello < 32B quantized

SCEGLI SCALEWAY SE:
✅ Budget flessibile
✅ Workload variabile (hourly billing)
✅ Serve H100/L40S (datacenter GPU)
✅ Instant scaling requirement
✅ Preferisci managed service

SCEGLI OVHCLOUD SE:
✅ Budget enterprise (€1k+)
✅ Serve SLA 99.99% contrattuale
✅ Multi-GPU requirement
✅ Compliance strict richiede SLA
✅ Preferisci supporto enterprise
```

**Per Qwen3-4B MVP**: 🎯 **HETZNER WINS**
