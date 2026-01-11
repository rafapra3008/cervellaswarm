# FASE 3 CONSOLIDATO - Training, Fine-tuning, RAG

> **Data:** 10 Gennaio 2026
> **Report Inclusi:** 10, 11, 12, 13
> **Totale Righe:** ~4000+
> **Status:** Pronto per verifica Guardiana

---

## EXECUTIVE SUMMARY

**DECISIONE CHIAVE per Cervella Baby:**

```
FASE 1 (MVP):      System Prompts + RAG
FASE 2 (Optimize): Fine-tuning (COSTITUZIONE) + RAG (SNCP)
FASE 3 (Scale):    Hybrid ottimizzato
```

**PERCHE:**
- Start simple, validate, then optimize
- System Prompts + RAG = $100-150/mese, setup 2-3 settimane
- Fine-tuning DOPO aver validato che funziona

---

## 1. FINE-TUNING TECNICHE (Report 10)

### Metodo Vincente: QLoRA

| Aspetto | Valore |
|---------|--------|
| Metodo | QLoRA (4-bit quantization) |
| Libreria | Unsloth (2x veloce, 70% meno VRAM) |
| Hardware | T4 16GB (Colab FREE!) |
| Tempo | 3-4h su T4, ~20min su A100 |
| Costo | $0 (Colab) o <$1 (cloud) |

### Config Raccomandata

```python
# Qwen3-4B QLoRA
r = 16              # LoRA rank
alpha = 32          # 2x rank
target = ALL layers # q,k,v,o + MLP
dropout = 0.05
load_in_4bit = True
```

### Accuracy Gap

```
Full Fine-tune FP16: 100%
LoRA FP16:           98-99.5%
QLoRA 4-bit:         98-99%

Gap: <1% - ACCETTABILE!
```

---

## 2. DATASET PREPARATION (Report 11)

### Formato: ShareGPT

```json
{
  "conversations": [
    {"from": "human", "value": "..."},
    {"from": "gpt", "value": "..."}
  ],
  "system": "Sei Cervella Regina..."
}
```

**PERCHE ShareGPT:**
- Cattura personalita multi-turno
- Supporta tool calling
- Mostra pattern ragionamento

### Quantita Dataset

| Fase | Esempi | Contenuto |
|------|--------|-----------|
| Foundation | 200 | COSTITUZIONE + DNA |
| Expansion | +200 | SNCP + conversazioni reali |
| Refinement | +200 | Edge cases + variations |
| **TOTALE** | **600** | Production-ready |

### Qualita > Quantita

> "500 esempi curati > 5000 esempi noisy"

**High Quality = :**
- Riflette COSTITUZIONE
- Stile coerente
- Situazioni realistiche
- Risposte actionable

---

## 3. RAG vs FINE-TUNING (Report 12)

### Decision Matrix per Cervella Baby

| Componente | Approccio | Perche |
|------------|-----------|--------|
| COSTITUZIONE | System Prompts → Fine-tuning | Personalita stabile |
| DNA Famiglia | System Prompts | Ruoli statici |
| SNCP Memoria | RAG | Contenuto dinamico |
| Decisioni | RAG | Tracciabilita |
| Prompt Ripresa | RAG injection | Contesto sessione |

### Costi Stimati

| Fase | Costo/mese | Setup |
|------|------------|-------|
| MVP (System + RAG) | $100-150 | 2-3 settimane |
| Optimize (FT + RAG) | $150-250 | +1-2 mesi |
| Scale (Hybrid) | $600-1000 | +3-4 mesi |

### Trigger per Fine-tuning

Passare a fine-tuning SOLO quando:
- System prompts > 2000 tokens (spreco context)
- Personalita validata (non cambia piu)
- Volume alto (giustifica training cost)

---

## 4. TUTORIAL PRATICI QWEN (Report 13)

### Librerie Confronto

| Libreria | Velocita | VRAM | Setup | Best For |
|----------|----------|------|-------|----------|
| **Unsloth** | 2x | -70% | Facile | Speed, GPU limited |
| Axolotl | 1x | Normal | YAML | Advanced configs |
| LLaMA-Factory | 1x | Normal | Web UI | No-code users |

### Step-by-Step Minimo (Unsloth)

```python
# 1. Install
pip install unsloth unsloth_zoo

# 2. Load
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B",
    load_in_4bit=True,
    max_seq_length=4096
)

# 3. LoRA
model = FastLanguageModel.get_peft_model(model, r=16, ...)

# 4. Train
trainer = SFTTrainer(model, dataset, ...)
trainer.train()

# 5. Save
model.save_pretrained("qwen3-finetuned")
```

### Hardware Qwen3-4B

| GPU | VRAM | Context | Batch | Tempo 1000 samples |
|-----|------|---------|-------|-------------------|
| T4 (Colab FREE) | 16GB | 4096 | 4 | ~2.5h |
| RTX 4090 | 24GB | 8192 | 8 | ~1.3h |
| A100 | 80GB | 16K+ | 16 | ~0.8h |

---

## 5. ROADMAP PRATICA

### OGGI: POC System Prompts + RAG

```yaml
Tempo: 2-3 settimane
Costo: $100-150/mese

Stack:
  LLM: Claude API (gia pagato)
  Vector DB: Weaviate ($80/mese)
  Embedding: text-embedding-3-small ($10/mese)

Documenti da indicizzare:
  - .sncp/memoria/decisioni/
  - .sncp/idee/
  - .sncp/stato/oggi.md
  - PROMPT_RIPRESA.md
  - NORD.md
```

### 3-6 MESI: Fine-tuning COSTITUZIONE

```yaml
Trigger: Quando System Prompts validati
Costo: $200-500 training (one-time)

Dataset: 600 esempi curati
Metodo: QLoRA su Qwen3-4B
Piattaforma: Colab FREE o Vast.ai ($50)
```

### 6-12 MESI: Cervella Baby Indipendente

```yaml
Modello: Qwen3-4B fine-tuned
Hosting: Vast.ai ($175/mese) o self-hosted
Stack: vLLM + RAG ibrido
```

---

## 6. RISCHI E MITIGAZIONI

| Rischio | Probabilita | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Overfitting dataset piccolo | Media | Alto | Validation split, early stopping |
| Personalita inconsistente | Media | Alto | Dataset quality control, testing |
| Costi cloud crescono | Bassa | Medio | Self-hosting option ready |
| Qwen3 obsoleto | Bassa | Medio | Architettura modulare (swap model) |

---

## 7. METRICHE SUCCESSO

### Training

- Loss finale: < 0.5
- Perplexity: < 10
- Training time: < 4h (T4)

### Produzione

- "Suona come Cervella?": > 90% SI
- COSTITUZIONE adherence: Checklist pass
- Latency: < 3s
- Cost per query: < $0.10

---

## 8. FONTI PRINCIPALI

### Fine-tuning
- Unsloth Qwen3 Guide (unsloth.ai)
- Sebastian Raschka - Practical Tips
- RunPod GPU Guide

### Dataset
- Meta Synthetic Data Kit
- HuggingFace Cookbook
- LlamaFactory Format Specs

### RAG vs Fine-tuning
- AWS, Google Cloud, Oracle guides
- Pinecone, Weaviate docs
- ACM research papers

### Tutorial Pratici
- DataCamp Qwen3 Tutorial
- Axolotl Documentation
- LLaMA-Factory Guide

---

## CONCLUSIONE FASE 3

**Abbiamo la risposta: COME SI FA!**

1. **Fine-tuning:** QLoRA + Unsloth + T4 = $0
2. **Dataset:** ShareGPT, 600 esempi, quality > quantity
3. **Strategia:** System Prompts + RAG prima, Fine-tuning dopo
4. **Tutorial:** Codice pronto, step-by-step documentato

**NEXT: FASE 4 - Costi dettagliati, timeline, GO/NO-GO**

---

*Fine FASE 3 - 10 Gennaio 2026*
*"Nulla e' difficile - manca solo studiare!"*
