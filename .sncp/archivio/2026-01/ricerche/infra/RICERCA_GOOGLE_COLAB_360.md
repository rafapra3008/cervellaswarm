# RICERCA COMPLETA: Google Colab per POC Cervella Baby (2026)

**Data Ricerca**: 10 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Obiettivo**: Setup POC Qwen3-4B con Unsloth su Google Colab

---

## EXECUTIVE SUMMARY

**TL;DR**: Google Colab FREE è sufficiente per il POC iniziale (3 settimane). T4 GPU supporta Qwen3-4B con 4-bit quantization. Limite critico: 12h session + 90min idle timeout.

**Raccomandazione**: Iniziare con FREE tier, backup su Kaggle (30h GPU/settimana). Budget $10-50 se serve estensione.

---

## 1. STATO ATTUALE COLAB (2026)

### Piani Disponibili

| Piano | Prezzo | Compute Units | GPU Access | Session Limit | Best For |
|-------|--------|---------------|------------|---------------|----------|
| **Free** | $0 | Limitati, variabili | T4, occasionalmente P100 | 12h max | POC, sperimentazione |
| **Colab Pro** | $9.99/mese | 100 CU/mese | T4, A100 (priority) | 24h | Progetti continuativi |
| **Colab Pro+** | $49.99/mese | 500 CU/mese | A100, V100 (priority) | 24h | Training intensivo |
| **Pay-as-you-go** | $9.99 per 100 CU | Compri quando serve | T4, A100, V100 | Variabile | Burst workload |
| **Colab Enterprise** | Custom | Custom | Custom + controllo | Custom | Team, produzione |

**Compute Units (CU) Carry-over**: Fino a 90 giorni

### Sistema Compute Units

**Consumption Rates (2026):**
- **T4 GPU**: 1.96 CU/ora (~$0.20/ora)
- **A100 GPU**: 62 CU/ora (~$6.20/ora)
- **100 CU Package**: $9.99 (≈ 51 ore T4)

**Conversione per Piani:**
- Colab Pro (100 CU): ~51 ore T4/mese
- Colab Pro+ (500 CU): ~255 ore T4/mese

### Limiti Critici 2026

| Limite | Free | Pro | Pro+ | Note |
|--------|------|-----|------|------|
| **Session Timeout** | 12h | 24h | 24h | Hard limit, code stop |
| **Idle Timeout** | 90 min | 90 min | 90 min | No user interaction |
| **GPU Availability** | Non garantito | Priority | High Priority | Free può non ottenere GPU in peak hours (US daytime) |
| **Storage** | 10 GB | Include | Include | Runtime temporaneo |
| **Background Execution** | ❌ | ❌ | ❌ | Browser chiuso = stop (diverso da Kaggle) |

**Fair Use Policy**: Free tier soggetto a throttling se uso eccessivo.

---

## 2. GPU E HARDWARE

### T4 GPU - La Nostra Scelta per POC

**Specifiche NVIDIA Tesla T4:**
- **VRAM**: 16 GB (15 GB usabili, 1 GB per ECC)
- **Architettura**: Turing (una generazione dietro Ampere, due dietro Hopper)
- **Memory Bandwidth**: 320 GB/s
- **Power**: 70W (efficiente)
- **Tensor Cores**: Si, ottimizzati per FP16/INT8 inference

**Performance:**
- **Inference**: 40x più veloce di CPU
- **Best Use**: Inference > Training
- **Modelli supportati**: Fino a ~7B parametri full precision, 14B con quantization

**Availability su Colab Free (2026):**
- ✅ T4 disponibile regolarmente su free tier
- ⚠️ Meno disponibile durante US daytime (timezone issue)
- 🔄 Occasionalmente P100 (16GB, leggermente meno performante)

### GPU Alternative su Colab Pro/Pro+

| GPU | VRAM | Performance | CU/ora | Use Case |
|-----|------|-------------|--------|----------|
| **T4** | 16 GB | Baseline | 1.96 | Small LLM inference/fine-tuning |
| **L4** | 24 GB | 2x T4 | ~12 | Medium LLM training |
| **A100 40GB** | 40 GB | 8x T4 | 62 | Large model training |
| **V100** | 16 GB | 4x T4 | ~40 | Older high-performance |

**Per POC Cervella Baby**: T4 è perfetto - Qwen3-4B sta sotto 15GB con margin.

---

## 3. UNSLOTH + QWEN3-4B SU COLAB

### Compatibilità Unsloth (2026)

✅ **Unsloth funziona PERFETTAMENTE su Colab**

**Repository Ufficiale**: [unslothai/notebooks](https://github.com/unslothai/notebooks)

**Notebook Disponibili per Qwen3-4B:**
1. **Qwen3_(4B)-Instruct.ipynb** - Fine-tuning base
2. **Qwen3_(4B)-GRPO.ipynb** - Reinforcement learning avanzato
3. Direct Colab link: `https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_(4B)-Instruct.ipynb`

### Qwen3-4B Specifiche

**Model Architecture:**
- **Parametri**: 4.0 miliardi
- **Layers**: 36 transformer layers
- **Attention**: Grouped Query Attention (GQA) - 32 query heads, 8 KV heads
- **Context Length**: 32,768 tokens nativo

**VRAM Requirements:**

| Precision | Model Weights | KV Cache (2K ctx) | KV Cache (32K ctx) | Total (2K) | Total (32K) |
|-----------|---------------|-------------------|---------------------|------------|-------------|
| **FP16 Full** | 3.9 GB | 0.2 GB | 3.0 GB | ~4.1 GB | ~6.9 GB |
| **4-bit Quant** | ~2.0 GB | 0.2 GB | 3.0 GB | ~2.2 GB | ~5.0 GB |

**⚠️ IMPORTANTE**: KV cache scala con context length! 32K context → +3GB VRAM.

### Setup Qwen3-4B con Unsloth

**One-Click Setup (Colab Notebook):**
```python
# Click Runtime → Run All
# Settings automatiche già configurate

# Configurazione base
model_name = 'unsloth/Qwen3-4B-unsloth-bnb-4bit'  # Pre-quantized!
load_in_4bit = True  # Riduce VRAM 4x
```

**Dependencies Auto-Install:**
- Unsloth library (auto-update)
- PyTorch compatibile (CUDA 11.8/12.1+)
- Transformers, TRL, datasets

**Tempo Setup**: ~5 minuti primo run (installazione), ~30 secondi successive.

### Performance su T4 GPU

**Training (Fine-tuning):**
- **Speed**: 2x più veloce vs standard (Unsloth optimization)
- **VRAM Usage**: 70% meno vs standard
- **Qwen3-4B 4-bit**: ~2-4 GB VRAM durante training (fit comodamente in T4)
- **Qwen3-14B 4-bit**: ~8-10 GB VRAM (fit anche questo!)

**Inference:**
- **Latency**: ~3.8 tokens/secondo su T4 (Qwen family benchmark)
- **Batch Size**: 1-4 samples su T4 16GB
- **Note**: Per production serve GPU migliore, ma per POC testing è OK

**Esempio Tempo Inference:**
- Prompt 100 token + generazione 200 token → ~53 secondi (3.8 tok/s)
- Conversational turn (50 in + 50 out) → ~26 secondi

**Per POC**: Latenza accettabile, non real-time ma interattivo.

### Problemi Noti / Workaround

**Issue #1: Memory Spike durante Load**
- **Problema**: Primo load modello può spike a 12-14GB VRAM
- **Workaround**: Chiudi altri processi, riavvia runtime se OOM
- **Soluzione**: `max_memory = {"cuda:0": "14GB"}` nel from_pretrained

**Issue #2: Torch Compile Warning**
- **Problema**: Warning su torch.compile con alcune versioni PyTorch
- **Workaround**: Ignora o disabilita compile (non critico)

**Issue #3: KV Cache con Long Context**
- **Problema**: 32K context → +3GB VRAM, risk OOM su T4
- **Workaround**: Limita max_seq_length a 8K-16K per POC
- **Codice**: `max_seq_length = 8192  # vs default 32768`

**Issue #4: Slow Inference on T4**
- **Problema**: 3.8 tok/s è lento vs GPU moderne
- **Workaround**: Batch requests, use async pattern
- **Nota**: Sufficiente per POC, non per prod scale

---

## 4. LIMITAZIONI IMPORTANTI

### Session Timeout (CRITICO)

**12 ore massime (Free), 24 ore (Pro/Pro+)**

**Impatto POC:**
- ❌ Training overnight non fattibile su Free
- ✅ Fine-tuning epochs 2-4h OK
- ⚠️ Devi salvare checkpoint ogni 30-60 min

**Workaround Best Practices:**
1. **Checkpoint frequenti** a Google Drive
2. **Resume automatico** da ultimo checkpoint
3. **Monitor training** ogni 2-3h se run lungo

### Idle Disconnect (CRITICO)

**90 minuti senza interazione → disconnect**

**Cosa Conta come "Interaction":**
- Click nel notebook
- Typing in celle
- Scroll della pagina
- **NON** conta: GPU al 100%, code running

**Workaround JavaScript (console browser):**
```javascript
// Keep-alive - evita idle timeout
function KeepClicking(){
   console.log("Clicking");
   document.querySelector("colab-toolbar-button#connect").click();
}
setInterval(KeepClicking, 60000);  // Ogni 60s
```

**⚠️ Attenzione**: Uso eccessivo keep-alive può triggare CAPTCHA o rate limiting.

**Raccomandazione**:
- ✅ Checkpoint solidi > keep-alive tricks
- ✅ Monitoring manuale ogni 1-2h
- ❌ Evitare interval < 60s (troppo aggressivo)

### Storage Persistente

**Runtime Storage: TEMPORANEO**
- Ogni disconnect → tutto perso
- `/content/` viene wipato

**Soluzione: Google Drive Mount**

```python
from google.colab import drive
drive.mount('/content/gdrive')

# Salva modelli/checkpoint su Drive
save_dir = '/content/gdrive/MyDrive/cervella_baby/checkpoints/'
```

**File Structure Consigliata:**
```
MyDrive/
├── cervella_baby/
│   ├── checkpoints/        # Model weights ogni epoch
│   ├── logs/               # Training logs
│   ├── outputs/            # Inference results
│   └── datasets/           # Training data
```

**Limiti Google Drive Free**: 15 GB (condivisi Gmail+Photos+Drive)

**Tip**: Cancella checkpoint vecchi, tieni solo best + ultimo.

### Networking Restrictions

**Allowed:**
- ✅ API calls esterni (OpenAI, HuggingFace, etc)
- ✅ Download datasets/models da web
- ✅ Git clone repositories
- ✅ pip install da PyPI

**Disallowed (Free Tier Abuse Prevention):**
- ❌ File hosting / media serving
- ❌ Torrents / P2P file sharing
- ❌ Cryptomining
- ❌ DDoS / scraping aggressivo

**Per POC**: Nessun problema, use case standard.

### CUDA e PyTorch Versioni (2026)

**Environment Colab Corrente:**
- **CUDA**: 12.1 / 12.4 (aggiornato da 11.8)
- **cuDNN**: 8.7.0+
- **PyTorch**: 2.4.0+ (compatibile CUDA 12.1/12.4)
- **Python**: 3.10.x

**Unsloth Compatibility**: ✅ Funziona out-of-the-box

**Custom Version Install (se necessario):**
```bash
# Nightly build
!pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

# Versione specifica
!pip install torch==2.4.0+cu121 -f https://download.pytorch.org/whl/torch_stable.html
```

---

## 5. ALTERNATIVE A COLAB

### Kaggle Notebooks ⭐ (TOP ALTERNATIVA)

**Vantaggi:**
- ✅ **30 GPU hours/settimana** GRATIS (vs Colab variabile)
- ✅ **9 ore session** (vs 12h Colab)
- ✅ **Background execution** (chiudi browser, continua training!)
- ✅ **2x T4 disponibili** (usa 1, Unsloth 5x più veloce per overhead evitato)
- ✅ **Predictable access** (meno contention vs Colab)
- ✅ **Dataset library** integrata

**Svantaggi:**
- ⚠️ Quota settimanale (30h) vs giornaliera variabile Colab
- ⚠️ Meno integrazioni vs Colab

**Ideal Use**: Training settimanali programmati, complementare a Colab per iterazione rapida.

### Lightning.ai

**Piano Free:**
- **GPU Hours**: ~30h/settimana
- **GPU Type**: Non specificato (mid-range)
- **Storage**: Persistent home drives (!)
- **RAM**: 32 GB
- **Session**: Variabile

**Vantaggi:**
- ✅ VSCode integration
- ✅ Persistent storage nativo
- ✅ Team collaboration features
- ✅ Auto CPU/GPU switching

**Svantaggi:**
- ⚠️ Approval manuale account (~24h wait)
- ⚠️ GPU hours limitati per task intensivi
- ⚠️ Meno documentazione community vs Colab

**Ideal Use**: Progetti team, sviluppo iterativo con storage persistente.

### Paperspace Gradient

**Piano Free (Community Notebooks):**
- **GPU**: Quadro M4000 (8GB VRAM)
- **Session**: 6 ore max
- **Quota**: Unlimited sessions
- **Storage**: Versioning incluso

**Vantaggi:**
- ✅ Sessions unlimited (6h ciascuna)
- ✅ UI pulita, notebook versioning
- ✅ Nessun quota giornaliero/settimanale

**Svantaggi:**
- ⚠️ **M4000 è vecchia** (Pascal architecture, 8GB solo)
- ⚠️ **Notebooks pubblici di default** (no privacy)
- ⚠️ Performance inferiore a T4

**Ideal Use**: Modelli small (<7B), sperimentazione pubblica, tutorial.

### Amazon SageMaker Studio Lab

**Piano Free:**
- **GPU**: T4
- **Session**: 4 ore max
- **Quota**: 4 GPU hours / 24h window

**Vantaggi:**
- ✅ T4 GPU gratuita
- ✅ Ambiente AWS-native

**Svantaggi:**
- ⚠️ **Solo 4h/giorno** (molto limitato)
- ⚠️ Session brevi (4h)
- ⚠️ Meno flessibile di Colab

**Ideal Use**: Quick experiments, AWS workflow testing.

### RunPod, Thunder Compute (PAID, LOW COST)

**Pricing T4:**
- **RunPod**: $0.40/ora
- **Thunder Compute**: $0.29/ora (CHEAPEST!)
- **Google Colab Pro** (implicit): ~$0.20/ora (ma subscription required)

**Vantaggi:**
- ✅ Pay-per-minute (no subscription)
- ✅ No timeout limits
- ✅ Spot pricing available
- ✅ Più GPU options (RTX 3090 @ $0.20/h)

**Svantaggi:**
- ⚠️ Costa denaro (vs free tier alternatives)
- ⚠️ Meno integrato di Colab

**Ideal Use**: Backup se free tier esaurito, production scale testing.

### Confronto Rapido

| Servizio | GPU Free | Quota | Session | Background | Best For |
|----------|----------|-------|---------|------------|----------|
| **Colab Free** | T4 | Variabile | 12h | ❌ | Iterazione rapida |
| **Kaggle** | 2x T4 | 30h/week | 9h | ✅ | Training scheduled |
| **Lightning.ai** | Mid-range | 30h/week | Var | ✅ | Team projects |
| **Paperspace** | M4000 | Unlimited | 6h | ❌ | Small models |
| **SageMaker Lab** | T4 | 4h/day | 4h | ❌ | AWS testing |
| **Thunder Compute** | - | Pay | Unlimited | ✅ | Backup paid |

---

## 6. SETUP CONSIGLIATO PER POC

### Piano Raccomandato: FREE + Backup Strategy

**Primary: Google Colab FREE**
- Iterazione rapida sviluppo
- Testing inference
- Fine-tuning short epochs (2-4h)

**Backup: Kaggle Notebooks**
- Training overnight (background exec)
- Utilizzo quota 30h/settimana per sessioni lunghe

**Emergency: Thunder Compute** ($0.29/h T4)
- Se quote esaurite e serve urgenza
- Budget backup: $10-20 per emergenze

### Notebook Template POC

```python
"""
CERVELLA BABY POC - Google Colab Setup
Qwen3-4B + Unsloth Fine-tuning
"""

# ============================================
# 1. SETUP AMBIENTE
# ============================================

# Mount Google Drive (persistenza)
from google.colab import drive
drive.mount('/content/gdrive')

# Crea directory progetto
import os
project_dir = '/content/gdrive/MyDrive/cervella_baby'
os.makedirs(f"{project_dir}/checkpoints", exist_ok=True)
os.makedirs(f"{project_dir}/logs", exist_ok=True)
os.makedirs(f"{project_dir}/outputs", exist_ok=True)

# ============================================
# 2. INSTALL DEPENDENCIES
# ============================================

# Unsloth (auto-aggiorna se già installato)
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

# Check GPU
!nvidia-smi

# ============================================
# 3. LOAD MODEL (4-bit Quantization)
# ============================================

from unsloth import FastLanguageModel
import torch

max_seq_length = 8192  # 8K context (vs 32K max) - risparmia VRAM
dtype = None  # Auto-detect
load_in_4bit = True  # OBBLIGATORIO per T4

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen3-4B-unsloth-bnb-4bit",  # Pre-quantized!
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    # Memory optimization per T4
    max_memory = {"cuda:0": "14GB"},  # Evita spike OOM
)

print("✅ Model loaded successfully!")
print(f"VRAM used: {torch.cuda.memory_allocated()/1024**3:.2f} GB")

# ============================================
# 4. CONFIGURE PEFT (LoRA)
# ============================================

model = FastLanguageModel.get_peft_model(
    model,
    r = 16,  # LoRA rank
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",  # 70% VRAM saving
    random_state = 3407,
)

# ============================================
# 5. PREPARE DATASET
# ============================================

from datasets import load_dataset

# Esempio: usa il tuo dataset
dataset = load_dataset("your-dataset", split="train[:1000]")  # Subset POC

# Format prompt (esempio)
def format_prompts(examples):
    texts = []
    for instruction, output in zip(examples["instruction"], examples["output"]):
        text = f"""Below is an instruction. Write a response.

### Instruction:
{instruction}

### Response:
{output}"""
        texts.append(text)
    return {"text": texts}

dataset = dataset.map(format_prompts, batched=True)

# ============================================
# 6. TRAINING CONFIG (con CHECKPOINT!)
# ============================================

from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,  # Effective batch = 8
        warmup_steps = 10,
        max_steps = 100,  # POC veloce
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 10,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        # ⚠️ CHECKPOINT CONFIG (CRITICO!)
        output_dir = f"{project_dir}/checkpoints",
        save_strategy = "steps",
        save_steps = 25,  # Ogni 25 steps
        save_total_limit = 3,  # Tieni solo ultimi 3
    ),
)

# ============================================
# 7. TRAIN (con Progress Monitor)
# ============================================

print("🚀 Starting training...")
print(f"Checkpoints saved to: {project_dir}/checkpoints")

trainer_stats = trainer.train()

print("✅ Training completed!")
print(trainer_stats)

# ============================================
# 8. SAVE FINAL MODEL
# ============================================

model.save_pretrained(f"{project_dir}/checkpoints/final_model")
tokenizer.save_pretrained(f"{project_dir}/checkpoints/final_model")

print(f"✅ Model saved to Drive: {project_dir}/checkpoints/final_model")

# ============================================
# 9. INFERENCE TEST
# ============================================

# Switch to inference mode
FastLanguageModel.for_inference(model)

# Test generation
inputs = tokenizer(
    "Below is an instruction. Write a response.\n\n### Instruction:\nWhat is machine learning?\n\n### Response:\n",
    return_tensors="pt"
).to("cuda")

outputs = model.generate(**inputs, max_new_tokens=128)
print("\n🔬 INFERENCE TEST:")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# ============================================
# 10. CLEANUP (opzionale)
# ============================================

# Libera VRAM se serve
import gc
del model
del trainer
gc.collect()
torch.cuda.empty_cache()

print("✅ POC Completato!")
```

### Best Practices Implementate

1. ✅ **Google Drive mount** → persistenza garantita
2. ✅ **4-bit quantization** → fit in T4 16GB
3. ✅ **Checkpoint ogni 25 steps** → protezione da disconnect
4. ✅ **8K context** (vs 32K) → VRAM ottimizzato
5. ✅ **Gradient checkpointing** → 70% VRAM saving
6. ✅ **Memory limit** 14GB → evita OOM spike
7. ✅ **Save total limit 3** → Drive space management

### Monitoring Durante Training

**Terminal Tab:**
```bash
# Monitor GPU usage
watch -n 2 nvidia-smi
```

**Notebook Cell (run parallel):**
```python
# Keep-alive heartbeat
import time
from IPython.display import clear_output

while True:
    clear_output(wait=True)
    print(f"✅ Training running... {time.strftime('%H:%M:%S')}")
    time.sleep(60)
```

---

## 7. COSTI STIMATI POC 3 SETTIMANE

### Scenario OTTIMISTICO (Free Tier Only)

**Assumptions:**
- Colab Free per sviluppo/testing (8h/giorno)
- Kaggle per training overnight (2 sessioni/week, 8h ciascuna)

**Costi:**
- **Colab Free**: $0
- **Kaggle Free**: $0 (16h/21 quota 30h)
- **Google Drive**: $0 (usa < 15GB)

**Total**: **$0** 🎉

**Effort Required:**
- Manual monitoring Colab ogni 2-3h (idle timeout)
- Checkpoint management
- Switching Colab↔Kaggle per long runs

**Feasibility**: ✅ ALTA se workflow organizzato

### Scenario REALISTICO (Free + Minimal Paid)

**Assumptions:**
- Colab Free per sviluppo (6h/giorno)
- Kaggle quota esaurita week 2
- Backup Thunder Compute 10h @ $0.29/h

**Costi:**
- **Colab Free**: $0
- **Kaggle Free**: $0
- **Thunder Compute**: 10h × $0.29 = **$2.90**

**Total**: **~$3** 💰

**Feasibility**: ✅ MOLTO ALTA

### Scenario PESSIMISTICO (Interruzioni + Premium)

**Assumptions:**
- Free tier unreliable (peak hours)
- Acquisto Colab Pro month 1 ($9.99)
- Uso 50 CU (25h T4)
- Backup Thunder Compute 15h ($4.35)

**Costi:**
- **Colab Pro**: $9.99 (100 CU, uso 50)
- **Thunder Compute**: 15h × $0.29 = $4.35
- **Google Drive** (se serve 100GB): $1.99/mese

**Total**: **~$16** 💸

**Feasibility**: ✅ Budget-friendly anche worst case

### Scenario COMFORT (Best Experience)

**Assumptions:**
- Colab Pro+ ($49.99) per zero friction
- 100 CU usage (~51h T4)
- No monitoring stress

**Costi:**
- **Colab Pro+**: $49.99

**Total**: **$50** 🚀

**Feasibility**: ✅ Se valore tempo > $50

### Backup Plan: Quota Esaurite

**Se tutti free tier esauriti + Pro non sufficiente:**

1. **Thunder Compute Burst** - $0.29/h T4
   - 40h training intensivo = $11.60
   - Pay-per-minute, no subscription

2. **RunPod Spot** - $0.20-0.30/h RTX 3090
   - Performance migliore, costo simile
   - Spot instance (può essere interrotta)

3. **Pause POC** - Aspetta reset quota
   - Kaggle reset ogni lunedì
   - Colab Free quota reset variabile

**Raccomandazione**: Scenario Realistico ($3) è sweet spot effort/costo.

---

## 8. ALTERNATIVE DEEP DIVE

### Kaggle Notebooks - Guida Setup

**Come Iniziare:**

1. **Account**: Kaggle.com → verifica telefono (richiesto per GPU)
2. **Create Notebook**: New Notebook → Settings → Accelerator → GPU T4 x2
3. **Internet ON**: Settings → Internet → ON (per pip install)

**Template Kaggle:**
```python
# Kaggle monta automaticamente datasets, non serve Drive
# Ma puoi usare Kaggle Datasets per persistenza

# Import dataset
!kaggle datasets download your-username/cervella-baby-data
!unzip cervella-baby-data.zip

# Save output come Kaggle Dataset (persistenza)
!kaggle datasets version -p /kaggle/working/checkpoints -m "Training epoch 10"
```

**Vantaggi Specifici:**
- Background execution: chiudi tab, continua
- 2x T4: puoi usare DDP (distributed) se serve
- Dataset library: versioning nativo

**Quando Usare Kaggle:**
- ✅ Training overnight (background!)
- ✅ Iterazioni complete fine-tuning
- ✅ Benchmark riproducibili (public notebooks)

### Lightning.ai - Guida Setup

**Come Iniziare:**

1. **Account**: lightning.ai → Sign up → wait approval (24h)
2. **Create Studio**: New Studio → GPU instance
3. **VSCode Integration**: Open in VSCode (seamless!)

**Template Lightning:**
```python
# Lightning ha storage persistente nativo
# /teamspace/studios/this_studio/ → persiste tra sessioni

project_dir = '/teamspace/studios/this_studio/cervella_baby'

# Resto identico a setup Colab
```

**Vantaggi Specifici:**
- Persistent home drives (no need Drive mount!)
- Team collaboration (share studio)
- VSCode nativo (miglior dev experience)

**Quando Usare Lightning:**
- ✅ Team development
- ✅ Progetti con persistent data/models
- ✅ Workflow complessi (VSCode debugger, etc)

### Quando Scegliere PAID Alternative

**Considera Thunder Compute / RunPod SE:**

1. **Free quota esaurite** ripetutamente
2. **Time-sensitive deadline** (non puoi aspettare reset quota)
3. **Production testing** (serve availability guarantee)
4. **Scaling test** (GPU multiple, benchmarking)

**Non Serve PAID SE:**
- POC initial development (free tier basta)
- Learning/experimentation
- Timeline flessibile (puoi aspettare quota)

---

## 9. PROBLEMI CONOSCIUTI & SOLUZIONI

### Problema: OOM (Out Of Memory) durante Model Load

**Sintomi:**
```
RuntimeError: CUDA out of memory. Tried to allocate 14.00 GiB
```

**Cause:**
- Spike VRAM durante from_pretrained
- Altri processi usano GPU
- Context length troppo alto

**Soluzioni:**
```python
# 1. Limit max memory
model, tokenizer = FastLanguageModel.from_pretrained(
    ...,
    max_memory = {"cuda:0": "14GB"},  # Force limit
)

# 2. Clear cache prima di load
import torch
torch.cuda.empty_cache()

# 3. Restart runtime (Factory reset GPU)
# Runtime → Factory reset runtime

# 4. Riduci max_seq_length
max_seq_length = 4096  # Instead of 8192
```

### Problema: Slow Inference (>1min per response)

**Sintomi:**
- Generating 100 tokens richiede >30s
- Real-time chat impossibile

**Cause:**
- T4 inference naturalmente slow (3.8 tok/s)
- Batch size 1
- Long context KV cache

**Soluzioni:**
```python
# 1. Use generation config ottimizzato
generation_config = GenerationConfig(
    max_new_tokens=128,  # Limita output
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1,
    pad_token_id=tokenizer.eos_token_id,
)

# 2. Batch inference (se multiple queries)
inputs = tokenizer(prompts_list, return_tensors="pt", padding=True)
outputs = model.generate(**inputs, generation_config=generation_config)

# 3. Async pattern (user perspective)
# Show "typing..." indicator durante generation
```

**Acceptance**: Per POC, 30-60s latency è OK. Production serve GPU migliore.

### Problema: Session Timeout Durante Training

**Sintomi:**
- Training a 80%, disconnect, perso tutto
- No checkpoint saved

**Cause:**
- Idle timeout 90min
- Forgot keep-alive
- Checkpoint save_steps troppo alto

**Soluzioni:**
```python
# 1. Checkpoint FREQUENTI
args = TrainingArguments(
    ...,
    save_steps = 10,  # Ogni 10 steps! (vs 50-100)
    save_total_limit = 5,
)

# 2. Resume da checkpoint
trainer = SFTTrainer(
    ...,
    args = args,
)

# Resume se esiste checkpoint
checkpoint_dir = f"{project_dir}/checkpoints"
if os.path.exists(checkpoint_dir) and os.listdir(checkpoint_dir):
    print("📂 Resuming from checkpoint...")
    trainer.train(resume_from_checkpoint=True)
else:
    print("🚀 Starting fresh training...")
    trainer.train()

# 3. Keep-alive + monitoring
# Vedi sezione 6 (template notebook)
```

### Problema: Google Drive Quota Exceeded

**Sintomi:**
```
ERROR: No space left on device
```

**Cause:**
- Checkpoint ogni epoch (model 4GB × 10 epochs = 40GB)
- Google Drive free = 15GB

**Soluzioni:**
```python
# 1. Save solo LORA adapters (non full model)
model.save_pretrained_merged(
    save_directory,
    save_method = "lora",  # Solo adapter ~10MB vs full 4GB!
)

# 2. Delete old checkpoints auto
args = TrainingArguments(
    ...,
    save_total_limit = 2,  # Solo best + latest
)

# 3. Manual cleanup
import shutil
old_checkpoints = glob.glob(f"{checkpoint_dir}/checkpoint-*")
old_checkpoints.sort(key=os.path.getmtime)
for ckpt in old_checkpoints[:-3]:  # Delete all except last 3
    shutil.rmtree(ckpt)

# 4. Upgrade Google Drive ($1.99/mese → 100GB)
```

### Problema: Kaggle Kernel Timeout (9h)

**Sintomi:**
- Training richiede 12h, Kaggle stoppa a 9h

**Soluzioni:**
```python
# 1. Resume training (Kaggle supporta checkpoint)
# Stesso codice resume di Colab funziona

# 2. Split training in sessioni multiple
# Day 1: Train 100 steps → save
# Day 2: Resume, train altri 100 steps

# 3. Optimize training speed
# - Reduce dataset size (sample 50%)
# - Increase batch size (se VRAM permette)
# - Fewer epochs (3 vs 10)
```

---

## 10. CHECKLIST FINALE POC

### Pre-POC Setup ✅

- [ ] Account Google con Drive (15GB free)
- [ ] Account Kaggle (verified phone per GPU)
- [ ] Account Lightning.ai (optional, approval 24h)
- [ ] Account Thunder Compute (optional backup, $10 credit)
- [ ] Install VSCode (optional, per Lightning.ai)

### Week 1: Setup & Baseline

- [ ] Clone Unsloth Qwen3-4B notebook su Colab
- [ ] Test inference baseline (latency, VRAM usage)
- [ ] Prepare dataset (upload Drive, format prompts)
- [ ] Run 1 epoch fine-tuning test (verify checkpoint works)
- [ ] Document baseline metrics (loss, perplexity, sample outputs)

### Week 2: Fine-tuning Iterazioni

- [ ] Fine-tune 3-5 epochs su dataset full
- [ ] Kaggle overnight training (background exec)
- [ ] A/B test: baseline vs fine-tuned
- [ ] Collect failure cases, iterate prompts
- [ ] Monitor quota usage (Colab, Kaggle)

### Week 3: Evaluation & Scale Test

- [ ] Benchmark inference speed (tokens/s, latency p50/p99)
- [ ] Test edge cases (long context, multi-turn)
- [ ] Cost analysis: actual usage vs estimate
- [ ] Document findings (what works, what doesn't)
- [ ] Decisione: scale to production GPU or optimize further?

### Deliverables POC

1. **Notebook funzionante** (Colab + Kaggle)
2. **Model checkpoint** fine-tuned (Drive)
3. **Benchmark report** (inference speed, accuracy)
4. **Cost analysis** (actual spend vs estimate)
5. **Lessons learned** (limitations, next steps)

---

## FONTI & RIFERIMENTI

### Google Colab Official

- [Colab Pricing](https://cloud.google.com/colab/pricing)
- [Colab FAQ](https://research.google.com/colaboratory/faq.html)
- [Colab Enterprise Quotas](https://docs.cloud.google.com/colab/docs/quotas)

### Unsloth + Qwen3

- [Unsloth Notebooks Repository](https://github.com/unslothai/notebooks)
- [Unsloth Documentation](https://docs.unsloth.ai/get-started/unsloth-notebooks)
- [Qwen3 Official](https://qwenlm.github.io/blog/qwen3/)
- [Qwen3 Unsloth Guide](https://docs.unsloth.ai/models/qwen3-how-to-run-and-fine-tune)
- [Qwen Hardware Requirements](https://www.hardware-corner.net/llm-database/Qwen/)

### GPU & Pricing

- [Colab GPUs Features & Pricing](http://mccormickml.com/2024/04/23/colab-gpus-features-and-pricing/)
- [NVIDIA T4 Specs & Pricing](https://www.fluence.network/blog/nvidia-t4/)
- [Cheapest Cloud GPU Providers 2025](https://www.thundercompute.com/blog/cheapest-cloud-gpu-providers-in-2025)
- [RunPod Pricing](https://www.runpod.io/pricing)

### Alternatives Comparison

- [Top Colab Alternatives December 2025](https://www.thundercompute.com/blog/colab-alternatives-for-cheap-deep-learning-in-2025)
- [Free Cloud GPUs for Students 2026](https://freerdps.com/blog/free-cloud-gpus-for-students/)
- [Free Cloud GPU Comparison 2026](https://research.aimultiple.com/free-cloud-gpu/)
- [RunPod vs Colab vs Kaggle](https://www.runpod.io/articles/comparison/runpod-vs-colab-vs-kaggle-best-cloud-jupyter-notebooks)

### Best Practices

- [Prevent Colab Disconnection 2025](https://apatero.com/blog/keep-google-colab-disconnecting-training-guide-2025)
- [Colab Persistent Storage with Drive](https://medium.com/@prajwal.prashanth22/google-colab-drive-as-persistent-storage-for-long-training-runs-cb82bc1d5b71)
- [How to Connect Colab with Drive 2025](https://www.marktechpost.com/2025/07/12/how-to-connect-google-colab-with-google-drive/)

### Benchmarks

- [Benchmarking Qwen Models T4/L4/H100](https://medium.com/@wltsankalpa/benchmarking-qwen-models-across-nvidia-gpus-t4-l4-h100-architectures-finding-your-sweet-spot-a59a0adf9043)
- [Qwen Speed Benchmark](https://qwen.readthedocs.io/en/latest/getting_started/speed_benchmark.html)
- [Unsloth 4-bit Quantization](https://unsloth.ai/blog/dynamic-4bit)

---

## CONCLUSIONI & RACCOMANDAZIONI

### TL;DR Finale

✅ **Google Colab FREE è sufficiente per POC Cervella Baby (3 settimane)**

**Setup Raccomandato:**
1. **Primary**: Colab Free (sviluppo + test)
2. **Backup**: Kaggle Notebooks (training overnight)
3. **Emergency**: Thunder Compute ($0.29/h se quota esaurite)

**Budget Previsto**: $0-5 (scenario realistico)

**GPU**: T4 16GB supporta Qwen3-4B con 4-bit quantization comodamente

**Limitation Critica**: Idle timeout 90min + session 12h → checkpoint ogni 25-50 steps OBBLIGATORIO

### Next Steps Immediati

1. **Setup Account Kaggle** (verification phone richiede 24-48h)
2. **Clone Unsloth Notebook** da repo ufficiale
3. **Test Baseline** inference Qwen3-4B su Colab Free
4. **Prepare Dataset** e upload Google Drive
5. **First Fine-tuning Run** (1 epoch, verify checkpoint)

### Red Flags da Monitorare

⚠️ **Se Colab Free GPU non disponibile >50% tentativi**
→ Considera Colab Pro ($9.99) o switch primario a Kaggle

⚠️ **Se training richiede >8h continuous**
→ Usa Kaggle background execution, non Colab

⚠️ **Se VRAM spike >15GB**
→ Riduci max_seq_length a 4096 o lower

⚠️ **Se Drive quota >10GB**
→ Save solo LoRA adapters, non full model

### Quando Scale Beyond POC

**Se POC success + serve production:**

1. **Inference speed**: T4 3.8 tok/s troppo slow
   → Migrate to L4 ($0.71/h) o A100 spot
   → Consider vLLM + quantization optimizations

2. **Availability**: Free tier unreliable
   → Colab Pro+ ($49.99) o dedicated GPU cloud
   → RunPod / Lambda Labs per production

3. **Cost optimization**: $0.20-0.40/h sostenibile?
   → Calculate monthly cost (24/7 inference)
   → Compare cloud vs self-hosted GPU

**Ma per POC ora**: Free tier è perfetto! 🚀

---

**Fine Ricerca - 10 Gennaio 2026**

*Cervella Researcher*

"Ultrapassar os próprios limites!" 💪
