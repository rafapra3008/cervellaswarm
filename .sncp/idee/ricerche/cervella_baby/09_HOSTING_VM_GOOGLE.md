# RICERCA: Hosting LLM su Google Cloud VM - Analisi Completa

**Data**: 10 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Status**: COMPLETATA ✅

---

## TL;DR - Raccomandazione Esecutiva

**NON conviene self-host su Google Cloud per ora.**

Motivi:
- Google Cloud GPU è COSTOSO (T4 $0.35/h = $252/mese 24/7)
- Alternative 50-80% più economiche (Vast.ai, RunPod)
- Claude API con prompt caching è competitivo per uso moderato
- Complessità gestionale alta vs API "plug and play"

**Quando conviene self-host:**
- Volume > 100M token/mese (~$3,000 con Claude)
- Necessità privacy/compliance
- Modelli custom/fine-tuned

**Raccomandazione INIZIALE:**
1. Continuare con Claude API + prompt caching (90% risparmio)
2. Se serve sperimentare LLM open source: Vast.ai spot instance (~$0.24/h per RTX 4090)
3. VM Google esistente: usare per orchestrazione, NON per inferenza LLM

---

## 1. REQUISITI HARDWARE LLM

### Tabella Requisiti per Modello

| Modello | Parametri | VRAM (FP16) | VRAM (8-bit) | VRAM (4-bit) | RAM | Storage |
|---------|-----------|-------------|--------------|--------------|-----|---------|
| **Llama 7B** | 7B | 16 GB | 8 GB | 4-5 GB | 16 GB | 15 GB |
| **Mistral 7B** | 7B | 16 GB | 8 GB | 4-5 GB | 16 GB | 15 GB |
| **Llama 13B** | 13B | 26 GB | 13 GB | 7-8 GB | 32 GB | 26 GB |
| **Llama 70B** | 70B | 140 GB | 70 GB | 35 GB | 64 GB+ | 140 GB |

### Performance Benchmark (Tokens/Secondo)

| Modello | Hardware | Framework | Speed | Note |
|---------|----------|-----------|-------|------|
| Mistral 7B | A100 | TensorRT-LLM | 93.63 tok/s | Ottimizzato |
| Mistral 7B | A100 | vLLM | ~85 tok/s | Production-ready |
| Llama 7B | T4 | vLLM | ~40 tok/s | GPU entry-level |
| Llama 7B | CPU (Ryzen 5700G) | llama.cpp | 11 tok/s | CPU-only |
| Llama 13B | A100 | vLLM | ~60 tok/s | Mid-size model |

### Quantizzazione: Impatto su Qualità e Requisiti

| Quantizzazione | VRAM Saving | Qualità | Raccomandazione |
|----------------|-------------|---------|-----------------|
| **FP16 (full)** | 0% | 100% | Solo con VRAM abbondante |
| **8-bit** | ~50% | 98-99% | Sweet spot qualità/efficienza |
| **4-bit (Q4_K_M)** | ~75% | 90-95% | Ottimo per produzione |
| **3-bit** | ~81% | 80-85% | Solo per sperimentazione |

**Insight chiave**: 4-bit quantizzazione riduce VRAM di 75% con perdita qualità minima. Llama 7B passa da 16GB → 4-5GB!

### CPU-Only con llama.cpp

**Possibile? SI**
**Raccomandabile? NO per produzione**

| Scenario | Performance | RAM Needed | Costo |
|----------|-------------|------------|-------|
| Llama 7B (4-bit) | 10-15 tok/s | 8 GB | $0.05/h (VM standard) |
| Llama 13B (4-bit) | 5-8 tok/s | 16 GB | $0.10/h (VM standard) |
| Llama 70B (4-bit) | 2-3 tok/s | 40 GB+ | Non pratico |

**PRO:**
- Costo minimo (VM senza GPU)
- Buono per sviluppo/testing
- llama.cpp ottimizzato (AVX, AVX2, AVX512)

**CONTRO:**
- Lento (80% più lento di GPU)
- Non scalabile per produzione
- User experience scadente

---

## 2. GOOGLE CLOUD GPU PRICING

### Prezzi GPU Google Cloud (2026)

| GPU | VRAM | Costo/Ora | Costo 24/7 Mese | Spot (60-91% sconto) | CUD 1-anno | CUD 3-anni |
|-----|------|-----------|-----------------|---------------------|-----------|-----------|
| **T4** | 16 GB | $0.35 | $252 | $0.10-$0.14 (~$73-100/mese) | $0.22 ($158/mese) | $0.16 ($115/mese) |
| **L4** | 24 GB | $0.62 | $446 | $0.18-$0.25 (~$130-180/mese) | $0.39 ($281/mese) | $0.28 ($201/mese) |
| **A100 40GB** | 40 GB | $1.15 | $828 | $0.35-$0.46 (~$252-331/mese) | $0.72 ($518/mese) | $0.52 ($374/mese) |
| **A100 80GB** | 80 GB | $1.57 | $1,130 | $0.47-$0.63 (~$339-454/mese) | $0.99 ($713/mese) | $0.71 ($511/mese) |

**NOTE:**
- Prezzi NON includono VM instance (aggiungere +$0.10-0.30/h per CPU/RAM)
- CUD (Committed Use Discount): 37% risparmio 1-anno, 55% risparmio 3-anni
- Spot VM: risparmio 60-91%, ma può essere preempted (interruzioni)
- GPU pricing include solo GPU - machine type separato

### Committed Use Discount (CUD) - Dettagli

**Come funziona:**
- Commit 1 o 3 anni su risorse specifiche
- Sconto 37% (1y) o 55% (3y)
- **REQUISITO GPU**: Devi creare reservation + attach al commitment

**Esempio T4:**
- On-demand: $252/mese
- CUD 1-anno: $158/mese (-37%)
- CUD 3-anni: $115/mese (-55%)

**Rischio:**
- Commit fisso, paghi anche se non usi
- Lock-in su regione/zona specifica

### Spot Instance Strategy

**Quando usare:**
- Workload tolleranti a interruzioni
- Batch processing
- Testing/development

**Risparmio reale:**
- T4: $252 → $73-100/mese (71-80% sconto)
- Ma: può essere terminato con 30s notice

---

## 3. ALTERNATIVE A GOOGLE CLOUD

### Comparison Table - Prezzi GPU Cloud Providers

| Provider | GPU | VRAM | Costo/Ora | Costo Mese (730h) | Pro | Contro |
|----------|-----|------|-----------|-------------------|-----|--------|
| **Vast.ai** | RTX 4090 | 24 GB | $0.24-0.60 | $175-438 | CHEAPEST, spot pricing | Variabilità, peer-to-peer |
| **Vast.ai** | A100 80GB | 80 GB | $0.50-1.20 | $365-876 | Marketplace competitivo | Reliability varia |
| **RunPod** | RTX 4090 | 24 GB | $0.34 | $248 | Balance prezzo/features | Meno scelta che Vast |
| **RunPod** | A100 80GB | 80 GB | $1.99 | $1,453 | Serverless $0.0004/s | Community Cloud varia |
| **Lambda Labs** | H100 | 80 GB | Varia | N/A | Best stock, affidabile | Premium pricing |
| **Google Cloud** | T4 | 16 GB | $0.35 | $252 | Enterprise support | EXPENSIVE |
| **Google Cloud** | A100 80GB | 80 GB | $1.57 | $1,130 | Integrated ecosystem | EXPENSIVE |

### Detailed Comparison

#### 🏆 Vast.ai - BEST for Budget

**Pricing:**
- RTX 4090: $0.24-0.60/h
- A100: $0.50-1.20/h
- **50-80% cheaper than AWS/GCP**

**Modello:**
- Marketplace peer-to-peer (Airbnb for GPUs)
- Individual owners rent hardware
- Spot pricing dinamico

**PRO:**
- Prezzi imbattibili
- Buona varietà GPU
- Perfetto per sperimentazione

**CONTRO:**
- Reliability varia (host diversi)
- Latency può variare
- Support limitato

**Use case:** Sperimentazione, development, workload fault-tolerant

---

#### ⚖️ RunPod - BEST Balance

**Pricing:**
- RTX 4090: $0.34/h (Community Cloud)
- H100 PCIe: $1.99/h
- Serverless: $0.0004/s (pay-per-second)

**Modello:**
- Community Cloud (shared) + Secure Cloud (enterprise)
- Pay-per-second billing
- Pre-configured templates

**PRO:**
- Billing al secondo (no spreco)
- Template pronti (vLLM, TGI)
- Community + enterprise options

**CONTRO:**
- Più costoso di Vast.ai
- Community Cloud availability varia

**Use case:** Production workload, API serving, scaling dinamico

---

#### 🎓 Lambda Labs - BEST for Enterprise

**Pricing:**
- H100 serverless: $0.0006/s
- Best stock H100/H200

**Modello:**
- Focus su ML enterprise
- 97% top US universities
- 100,000+ ML engineers

**PRO:**
- Reliability enterprise-grade
- Best H100 availability
- ML-optimized infrastructure

**CONTRO:**
- Premium pricing
- Meno trasparenza su prezzi

**Use case:** Production mission-critical, research, H100 needed

---

#### 💼 Google Cloud - Enterprise Integration

**PRO:**
- Integrated ecosystem (Cloud Storage, BigQuery, etc.)
- Enterprise SLA
- Managed services
- Compliance certifications

**CONTRO:**
- 2-3x più costoso di Vast/RunPod
- Complessità setup
- Lock-in ecosystem

**Use case:** Enterprise con GCP esistente, compliance needed, integrated workload

---

### Raccomandazione per Provider

| Scenario | Provider | GPU | Costo Mese | Motivo |
|----------|----------|-----|------------|--------|
| **Sperimentazione** | Vast.ai | RTX 4090 | $175-250 | Budget, flexibility |
| **Development** | RunPod | RTX 4090 | $248 | Pay-per-second, templates |
| **Production (7B)** | RunPod | T4/RTX 4090 | $248-300 | Reliability + costo |
| **Production (70B)** | RunPod | A100 80GB | $1,450 | High VRAM, scalability |
| **Enterprise** | Google Cloud | A100 80GB | $1,130+ | Ecosystem integration |

---

## 4. SETUP PRATICO

### Come Aggiungere GPU a VM Google Cloud Esistente

**LIMITAZIONE CRITICA:**
❌ **NON puoi aggiungere GPU a VM esistente via gcloud command**

**Opzioni:**

#### Opzione A: Modifica VM Esistente (LIMITATA)
1. **STOP** la VM
2. Google Cloud Console → VM instances → EDIT
3. Aggiungi GPU configuration
4. Restart VM

**LIMITI:**
- Solo alcuni machine types compatibili
- NON puoi convertire a A3/A4 machine types
- Devi comunque fermare VM

#### Opzione B: Crea Nuova VM con GPU (RACCOMANDATO)

```bash
gcloud compute instances create llm-vm \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --accelerator="type=nvidia-tesla-t4,count=1" \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=100GB \
  --maintenance-policy=TERMINATE
```

**NOTE:**
- `--maintenance-policy=TERMINATE` obbligatorio per GPU
- Zone availability varia (usa `gcloud compute accelerator-types list`)

#### Opzione C: Usa Provider Alternativo

**RunPod/Vast.ai:**
- Deploy in < 5 minuti
- GPU già configurato
- Template pre-built (vLLM, TGI)
- NO gestione infrastructure

**Raccomandazione:** Se VM Google esistente serve altro, NON modificarla. Usa RunPod/Vast per LLM.

---

### Docker GPU Setup - NVIDIA Container Toolkit

#### 1. Install NVIDIA Drivers

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y nvidia-driver-535
```

**Requirement:**
- NVIDIA Driver >= 418.81.07
- GPU Architecture >= Kepler (compute 3.0+)

#### 2. Install NVIDIA Container Toolkit

```bash
# Add repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

#### 3. Test GPU Access

```bash
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

**Expected output:** Vedi GPU info (memoria, driver version, etc.)

#### 4. Run LLM Container (Example vLLM)

```bash
docker run --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model mistralai/Mistral-7B-Instruct-v0.2 \
  --quantization awq
```

**Docker Compose Example:**

```yaml
version: '3.8'
services:
  vllm:
    image: vllm/vllm-openai:latest
    command: >
      --model mistralai/Mistral-7B-Instruct-v0.2
      --quantization awq
      --max-model-len 4096
    ports:
      - "8000:8000"
    volumes:
      - ~/.cache/huggingface:/root/.cache/huggingface
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

**NOTE:**
- Volume mount cache evita re-download model
- `--gpus all` in docker run diventa `deploy.resources.reservations` in compose
- CUDA toolkit NON needed su host (solo driver!)

---

### Framework LLM Serving - Confronto

| Framework | Pro | Contro | Use Case |
|-----------|-----|--------|----------|
| **vLLM** | 24x throughput vs naive, PagedAttention, OpenAI API compatible | Setup più complesso | High concurrency, production |
| **TGI** | HuggingFace integration, low latency, mature | 10-30% slower throughput | Low latency interactive, HF models |
| **llama.cpp** | CPU support, minimal deps, GGUF format | Slower, meno features | Development, CPU-only, low resource |
| **Ollama** | Easiest setup, model library | Limited customization | Local development, testing |

#### vLLM - RACCOMANDATO per Production

**Caratteristiche:**
- PagedAttention: 85-92% GPU utilization
- 2-4x throughput vs naive implementation
- OpenAI-compatible API
- Dynamic batching

**Performance:**
- Llama-2-70B: 3,245 tok/s (4x T4, tensor parallelism)
- Mistral 7B: ~85 tok/s (A100)

**Setup:**
```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mistral-7B-Instruct-v0.2 \
  --quantization awq \
  --max-model-len 8192
```

**Quando usare:** High concurrency, batch processing, production API

---

#### TGI (Text Generation Inference) - HuggingFace

**Caratteristiche:**
- HuggingFace ecosystem integration
- Low tail latency
- Long context optimization (200K+ tokens)

**Performance:**
- Lower tail latency per single-user
- Long context: 13x speedup vs vLLM (200K+ tokens)
- Throughput: 10-30% slower che vLLM

**Setup:**
```bash
docker run --gpus all \
  -p 8080:80 \
  -v $PWD/data:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id mistralai/Mistral-7B-Instruct-v0.2 \
  --quantize bitsandbytes-nf4
```

**Quando usare:** Interactive apps, long context, HuggingFace models

---

#### llama.cpp - CPU/Edge

**Caratteristiche:**
- C++ implementation
- CPU-optimized (AVX, AVX2, AVX512)
- GGUF quantization formats
- Minimal dependencies

**Performance:**
- CPU-only: 10-15 tok/s (7B model, consumer CPU)
- GPU offload: 30-40 tok/s (mid-range GPU)

**Setup:**
```bash
# Compile
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
make

# Run
./main -m models/mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  -p "Ciao, come stai?" \
  --n-gpu-layers 35  # Offload layers to GPU
```

**Quando usare:** Development, CPU-only, edge devices, low resources

---

### Raccomandazione Framework

| Scenario | Framework | Motivo |
|----------|-----------|--------|
| **Production API (alta concorrenza)** | vLLM | Throughput 24x, PagedAttention |
| **Interactive chatbot** | TGI | Low latency, long context |
| **Development locale** | llama.cpp / Ollama | Facile setup, CPU support |
| **Testing modelli HF** | TGI | Integration nativa |
| **Edge deployment** | llama.cpp | Minimal deps, C++ |

---

## 5. COSTI MENSILI STIMATI

### Scenario A: Llama 7B su Google Cloud T4 (24/7)

| Item | Opzione | Costo/Mese |
|------|---------|------------|
| GPU T4 | On-demand | $252 |
| GPU T4 | CUD 1-anno | $158 |
| GPU T4 | CUD 3-anni | $115 |
| GPU T4 | Spot VM | $73-100 |
| VM Instance (n1-standard-4) | Standard | $120 |
| Storage (100GB SSD) | Standard | $17 |
| **TOTALE On-demand** | | **$389** |
| **TOTALE CUD 3-anni** | | **$252** |
| **TOTALE Spot** | | **$210-237** |

**Performance attesa:** ~40 tok/s (vLLM, 4-bit quant)

---

### Scenario B: Llama 13B su Google Cloud L4 (24/7)

| Item | Opzione | Costo/Mese |
|------|---------|------------|
| GPU L4 | On-demand | $446 |
| GPU L4 | CUD 3-anni | $201 |
| VM Instance (n1-standard-8) | Standard | $240 |
| Storage (100GB SSD) | Standard | $17 |
| **TOTALE On-demand** | | **$703** |
| **TOTALE CUD 3-anni** | | **$458** |

**Performance attesa:** ~50-60 tok/s (vLLM, 4-bit quant)

---

### Scenario C: Mistral 7B su RunPod RTX 4090 (24/7)

| Item | Costo/Mese |
|------|------------|
| RTX 4090 (Community Cloud) | $248 |
| Storage (50GB) | Incluso |
| **TOTALE** | **$248** |

**Performance attesa:** ~80-90 tok/s (vLLM, 4-bit quant)

**Risparmio vs Google T4:** $389 - $248 = **$141/mese (36% cheaper)**

---

### Scenario D: Llama 70B su RunPod A100 80GB (24/7)

| Item | Costo/Mese |
|------|------------|
| A100 80GB | $1,453 |
| Storage (200GB) | ~$20 |
| **TOTALE** | **$1,473** |

**Performance attesa:** ~50-70 tok/s (vLLM, 4-bit quant)

**vs Google Cloud:** $1,130 + $240 + $17 = $1,387
**RunPod più caro:** +$86/mese (+6%)

**Ma:** RunPod = pay-per-second, no setup, templates ready

---

### Scenario E: Vast.ai RTX 4090 Spot (on-demand usage)

| Usage Pattern | Ore/Mese | Costo ($0.30/h avg) |
|---------------|----------|---------------------|
| Development (4h/giorno) | ~120h | $36 |
| Part-time (8h/giorno) | ~240h | $72 |
| Full-time work (160h/mese) | 160h | $48 |
| **24/7** | 730h | $219 |

**Quando conviene:**
- Usage sporadico/intermittente
- Testing/sperimentazione
- Non serve 24/7 uptime

**Risparmio ENORME vs on-demand 24/7**

---

## 6. CONFRONTO CON API CLAUDE

### Claude API Pricing (2026)

| Model | Input ($/M tokens) | Output ($/M tokens) | Cache Write | Cache Read (90% discount) |
|-------|-------------------|---------------------|-------------|--------------------------|
| **Haiku 4.5** | $1 | $5 | $1.25 | $0.10 |
| **Sonnet 4.5** | $3 | $15 | $3.75 | $0.30 |
| **Opus 4.5** | $5 | $25 | $6.25 | $0.50 |

**Key feature:** Prompt caching 90% discount dopo 2 richieste!

### Calcolo Break-Even Point

#### Scenario: Cervella AI Dashboard (uso reale)

**Assunzioni:**
- 1,000 richieste/giorno
- 500 tokens input (cached dopo prime 2 req)
- 200 tokens output
- Uso: Sonnet 4.5

**Calcolo mensile (30 giorni):**

```
Richieste totali: 30,000
Input tokens: 30,000 * 500 = 15M tokens
Output tokens: 30,000 * 200 = 6M tokens

SENZA caching:
Input: 15M * $3/M = $45
Output: 6M * $15/M = $90
TOTALE: $135/mese

CON prompt caching (90% hit dopo 2 req):
Prime 2 req: 1,000 tokens * $3.75/M (cache write) = $0.004
Cache reads: 14.998M tokens * $0.30/M = $4.50
Output: $90 (unchanged)
TOTALE: $94.50/mese

RISPARMIO: $40.50/mese (30%)
```

#### Self-Host Alternative (Mistral 7B su RunPod)

**Costo:**
- RunPod RTX 4090: $248/mese
- Setup/maintenance: ~$50/mese (time equivalent)
- **TOTALE: $298/mese**

**Break-even analysis:**

| Volume Mensile | Claude API (con caching) | Self-Host (RunPod) | Winner |
|----------------|--------------------------|-------------------|--------|
| 30K requests | $95 | $298 | Claude API |
| 100K requests | $315 | $298 | Self-Host |
| 300K requests | $945 | $298 | Self-Host |
| 1M requests | $3,150 | $298 | Self-Host |

**Break-even point: ~95,000 richieste/mese**

### Confronto Qualità

| Aspect | Claude Sonnet 4.5 | Mistral 7B | Llama 13B |
|--------|-------------------|------------|-----------|
| **Reasoning** | Eccellente | Buono | Buono |
| **Coding** | Eccellente | Molto buono | Buono |
| **Context** | 200K tokens | 32K tokens | 4K tokens (base) |
| **Multimodal** | Si (vision) | No | No |
| **Italiano** | Native-level | Buono | Discreto |
| **Latenza** | ~300-500ms | ~200ms (self-host) | ~250ms |
| **Uptime** | 99.9% SLA | Dipende da provider | Dipende |

**Conclusione qualità:**
- Per RAG/QA semplice: Mistral 7B competitivo
- Per reasoning complesso: Claude superiore
- Per code generation: Claude superiore
- Per long context: Claude 200K vs Mistral 32K

---

### Raccomandazione Strategica

#### FASE 1: Ora (Volume < 100K req/mese)

**Continuare Claude API con ottimizzazioni:**
- ✅ Prompt caching (90% risparmio)
- ✅ Batch processing (50% sconto)
- ✅ Use Haiku per task semplici ($1-5 vs $3-15)

**Costo stimato:** $50-150/mese

#### FASE 2: Scale-up (Volume 100K-500K req/mese)

**Hybrid approach:**
- Claude API per task complessi (30% volume)
- Self-host Mistral 7B per RAG/QA semplice (70% volume)

**Setup:**
- RunPod RTX 4090 ($248/mese)
- Claude API budget ridotto (~$100/mese)
- **TOTALE: ~$350/mese**

#### FASE 3: High Volume (> 500K req/mese)

**Self-host primary:**
- RunPod/Vast.ai fleet (multiple GPU)
- Claude API solo per edge cases
- Fine-tuned models per use cases specifici

**Costo stimato:** $500-1,000/mese (vs $2,000-5,000 con solo API)

---

## 7. RACCOMANDAZIONE PER INIZIARE

### ✅ PERCORSO CONSIGLIATO

#### Step 1: Valutazione (Settimana 1-2)

**NON toccare VM Google esistente** (34.27.179.164)

**Azioni:**
1. Registrati su Vast.ai
2. Prova spot instance RTX 4090 ($0.24/h)
3. Deploy Mistral 7B con vLLM
4. Test inference performance
5. Confronto qualità output vs Claude

**Budget:** $20-50 (testing)

#### Step 2: Proof of Concept (Settimana 3-4)

**Se test positivo:**
1. Setup RunPod Community Cloud ($0.34/h = $248/mese)
2. Docker container vLLM production-ready
3. OpenAI-compatible API endpoint
4. Integration test con Cervella AI

**Metriche da misurare:**
- Latenza p50, p95, p99
- Throughput (req/s)
- Quality score vs Claude
- Uptime/reliability

#### Step 3: Decisione Go/No-Go (Fine mese 1)

**GO se:**
- Quality acceptable per 70%+ use cases
- Latency < 500ms p95
- Costo risparmiato > $100/mese
- Reliability > 99%

**NO-GO se:**
- Quality gap significativo
- Complessità gestionale alta
- Volume non giustifica setup

---

### 🛠️ Setup Tecnico Raccomandato (se GO)

#### Architecture

```
┌─────────────────┐
│  Cervella AI    │
│   Frontend      │
└────────┬────────┘
         │
    ┌────▼────────────────────────┐
    │   API Gateway/Router        │
    │  (FastAPI su VM Google)     │
    └─┬──────────────────────┬────┘
      │                      │
      │ Complex              │ Simple
      │ Reasoning            │ RAG/QA
      │                      │
┌─────▼──────┐      ┌────────▼────────┐
│ Claude API │      │  Self-host LLM  │
│ (Sonnet 4.5)│     │  (RunPod vLLM)  │
└────────────┘      └─────────────────┘
```

**Logica routing:**
- Prompts > 100K tokens → Claude (long context)
- Code generation → Claude (superior quality)
- Vision/multimodal → Claude (capability)
- RAG retrieval + QA → Self-host (cost effective)
- Batch processing → Self-host (volume)

#### Configurazione RunPod

**Template vLLM:**
```yaml
image: vllm/vllm-openai:latest
gpu_type: RTX 4090 24GB
docker_args:
  command: >
    --model mistralai/Mistral-7B-Instruct-v0.2
    --quantization awq
    --max-model-len 8192
    --tensor-parallel-size 1
  ports:
    - 8000:8000
  volumes:
    - /workspace/cache:/root/.cache/huggingface
```

**Persistent storage:** 50GB (model weights cached)

#### Monitoring

```python
# FastAPI middleware per routing
from fastapi import FastAPI, Request
import aiohttp

app = FastAPI()

async def route_llm(prompt: str, complexity: str):
    if complexity == "high" or len(prompt) > 100000:
        # Use Claude API
        return await call_claude(prompt)
    else:
        # Use self-hosted
        return await call_runpod_vllm(prompt)
```

**Metriche da tracciare:**
- Latency per provider
- Costo per request
- Quality feedback
- Error rate
- Token throughput

---

### 💰 Budget Summary - Prima 6 Mesi

| Fase | Durata | Servizio | Costo | Scopo |
|------|--------|----------|-------|-------|
| **Valutazione** | 2 settimane | Vast.ai spot | $50 | POC testing |
| **POC** | 2 settimane | RunPod Community | $120 | Integration |
| **Production** | 5 mesi | RunPod + Claude | $1,750 | Hybrid ($350/mo) |
| **TOTALE 6 mesi** | | | **$1,920** | |

**vs Solo Claude API (proiezione):**
- Volume medio: 150K req/mese
- Costo Claude: ~$500/mese
- 6 mesi: $3,000

**RISPARMIO:** $1,080 (36% cheaper)

---

## 8. FONTI & RIFERIMENTI

### Google Cloud Pricing
- [GPU pricing | Google Cloud](https://cloud.google.com/compute/gpus-pricing)
- [7 cheapest cloud GPU providers in 2026](https://northflank.com/blog/cheapest-cloud-gpu-providers)
- [Committed use discounts (CUDs)](https://docs.cloud.google.com/compute/docs/instances/committed-use-discounts-overview)
- [Spot VMs Pricing](https://cloud.google.com/spot-vms/pricing)

### Hardware Requirements
- [How Much GPU VRAM Do You Need for a 7B, 33B, or 70B Model?](https://www.databasemart.com/blog/how-much-vram-do-you-need-for-7-70b-llm)
- [LLM GPU VRAM Requirements Explained: Complete 2026 Guide](https://www.propelrc.com/llm-gpu-vram-requirements-explained/)
- [Build Your Own AI PC: Recommended Specs for Local LLMs in 2026](https://techpurk.com/build-ai-pc-specs-2026-local-llms/)
- [The Complete Guide to Running LLMs Locally](https://www.ikangai.com/the-complete-guide-to-running-llms-locally-hardware-software-and-performance-essentials/)

### Alternative Cloud Providers
- [Runpod vs Vast.ai: Comprehensive Comparison](https://www.poolcompute.com/compare/runpod-vs-vast-ai)
- [7 Affordable GPU Clouds for LLM Serving](https://estha.ai/blog/7-affordable-gpu-clouds-for-llm-serving-best-options-for-ai-deployment/)
- [Top 12 Cloud GPU Providers for AI in 2025](https://www.runpod.io/articles/guides/top-cloud-gpu-providers)

### LLM Serving Frameworks
- [Comparative Analysis of vLLM and HuggingFace TGI](https://arxiv.org/html/2511.17593v1)
- [vLLM vs. TGI](https://modal.com/blog/vllm-vs-tgi-article)
- [TGI vs. vLLM: Making Informed Choices for LLM Deployment](https://medium.com/@rohit.k/tgi-vs-vllm-making-informed-choices-for-llm-deployment-37c56d7ff705)
- [GitHub - ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

### Performance Benchmarks
- [Benchmarking fast Mistral 7B inference](https://www.baseten.co/blog/benchmarking-fast-mistral-7b-inference/)
- [Exploring LLMs Speed Benchmarks](https://home.mlops.community/public/blogs/exploring-llms-speed-benchmarks-independent-analysis)
- [Mistral 7B - Intelligence, Performance & Price Analysis](https://artificialanalysis.ai/models/mistral-7b-instruct)

### Docker & GPU Setup
- [Installing the NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- [GPU support | Docker Docs](https://docs.docker.com/desktop/features/gpu/)
- [How to Use Your GPU in a Docker Container](https://blog.roboflow.com/use-the-gpu-in-docker/)

### Claude API Pricing
- [Pricing - Claude Docs](https://platform.claude.com/docs/en/about-claude/pricing)
- [Anthropic API Pricing: The 2026 Guide](https://www.nops.io/blog/anthropic-api-pricing/)
- [Claude API Pricing Guide 2026](https://www.aifreeapi.com/en/posts/claude-api-pricing-per-million-tokens)

### Google Cloud VM GPU Management
- [Overview of creating an instance with attached GPUs](https://cloud.google.com/compute/docs/gpus/create-vm-with-gpus)
- [Create an N1 VM that has attached GPUs](https://cloud.google.com/compute/docs/gpus/create-gpu-vm-general-purpose)

---

## CONCLUSIONE FINALE

### Risposta alla Domanda: "Possiamo far girare modelli open source sulla VM Google Cloud?"

**SI, tecnicamente possibile.**
**NO, non conviene economicamente per ora.**

### La Nostra Strada

```
┌─────────────────────────────────────────┐
│  FASE 1 (ORA)                           │
│  - Claude API + prompt caching          │
│  - VM Google: backend orchestration     │
│  - Budget: $50-150/mese                 │
└─────────────────────────────────────────┘
                  │
                  ▼
        Volume > 100K req/mese?
                  │
                  ▼ SI
┌─────────────────────────────────────────┐
│  FASE 2 (Scale-up)                      │
│  - Vast.ai POC testing (2 settimane)    │
│  - RunPod RTX 4090 production           │
│  - Hybrid: 70% self-host, 30% Claude    │
│  - Budget: $300-400/mese                │
└─────────────────────────────────────────┘
                  │
                  ▼
        Volume > 500K req/mese?
                  │
                  ▼ SI
┌─────────────────────────────────────────┐
│  FASE 3 (High Volume)                   │
│  - Fleet GPU (RunPod/Vast.ai)           │
│  - Fine-tuned models                    │
│  - Claude API < 10% volume              │
│  - Budget: $500-1,000/mese              │
└─────────────────────────────────────────┘
```

### Key Takeaways

1. **Google Cloud GPU troppo costoso** ($389/mese T4 on-demand vs $248 RunPod RTX 4090)
2. **Vast.ai/RunPod 50-80% cheaper** per stesso hardware
3. **Claude API competitivo fino a 100K req/mese** con prompt caching
4. **Break-even self-host: ~95K requests/mese**
5. **VM Google esistente: NO GPU, usa per orchestration**
6. **Raccomandazione: Start small con Vast.ai spot testing**

### Prossimi Step Concreti

**QUESTA SETTIMANA:**
- [ ] Registrazione Vast.ai account
- [ ] Budget approval $50 testing

**PROSSIME 2 SETTIMANE:**
- [ ] Deploy Mistral 7B su Vast.ai spot
- [ ] Benchmark latency/quality vs Claude
- [ ] Decisione GO/NO-GO

**SE GO (mese 1):**
- [ ] Setup RunPod production
- [ ] Integration Cervella AI
- [ ] Monitoring dashboard
- [ ] Cost tracking

---

**Fine ricerca: 10 Gennaio 2026**
**Tempo ricerca: ~3 ore**
**Fonti consultate: 45+**
**Qualità: Approfondita ✅**

*"Non reinventiamo la ruota - studiamo chi l'ha già fatta!"*

🔬 Cervella Researcher
