# Deep Dive: Qwen (Alibaba) e DeepSeek - Ricerca Completa

> **Data Ricerca:** 10 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Scopo:** Analisi approfondita Qwen e DeepSeek per Cervella Baby

---

## Executive Summary

**TL;DR per la Regina:**

- **Qwen (Alibaba)**: Famiglia di modelli open-source (Apache 2.0) con versioni specializzate. Qwen3 (2025) è top per coding/STEM. Supporto multilingua eccellente.
- **DeepSeek**: Il "momento Sputnik" dell'AI (Gen 2025). DeepSeek-R1 rivoluziona il reasoning con training efficiente. Controversie export USA.
- **Per Cervella Baby**: Qwen3-1.7B/4B ideale per base model. DeepSeek-R1-Distill-Qwen per reasoning avanzato.

---

## PARTE 1: QWEN (Alibaba Cloud)

### 1.1 Storia e Background

**Chi lo Sviluppa:**
- Sviluppato da **Alibaba Cloud**, divisione cloud computing di Alibaba Group
- Team Qwen (precedentemente noto come "Tongyi Qianwen")
- Uno dei principali competitor open-source di Meta (Llama) e Mistral

**Timeline Versioni:**

| Versione | Data Rilascio | Dimensioni Disponibili | Note Principali |
|----------|---------------|------------------------|------------------|
| **Qwen 1.0** | ~2023 | 7B, 14B, 72B | Prima generazione |
| **Qwen 1.5** | ~2024 | 0.5B-110B | Ampliamento gamma |
| **Qwen 2.0** | Giugno 2024 | 0.5B-72B | Cambio strategia: alcuni proprietari |
| **Qwen 2.5** | Set 2024 | 0.5B-72B | Miglioramenti coding/math |
| **Qwen2.5-VL** | Gen 2025 | 3B, 7B, 32B, 72B | Vision-language |
| **Qwen2.5-Omni** | Mar 2025 | 7B | Multimodale end-to-end |
| **Qwen 3.0** | **28 Apr 2025** | 0.6B-235B | Generazione attuale, dual-mode thinking |
| **Qwen3-Omni** | Set 2025 | - | Multimodale avanzato |

**Perché Open Source?**

Alibaba ha adottato una **strategia ibrida**:

1. **Community Engagement**: Costruire ecosistema di sviluppatori → adozione diffusa
2. **Cloud Revenue**: Open source porta utenti a Alibaba Cloud (infrastruttura a pagamento)
3. **Competitive Edge**: Modelli base open (Apache 2.0), top models proprietari (es. Qwen2.5-Max, Qwen3-Max)
4. **Licensing Advantage**: Apache 2.0 permette uso commerciale illimitato (vs licenze più restrittive di Meta)

> *"Questa strategia crea un ecosistema auto-rinforzante: adozione open-source → sviluppatori su Alibaba Cloud → revenue"*

### 1.2 Modelli Qwen Disponibili

#### A) Qwen3 - Famiglia Principale (Apr 2025)

**Dense Models:**
- Qwen3-0.6B, 1.7B, 4B, 8B, 14B, 32B
- Tutti sotto **Apache 2.0 License**
- Training: **36 trillion tokens** in **119 lingue**
- Context: fino a 256K token (estendibile a 1M)

**MoE Models (Mixture-of-Experts):**
- Qwen3-30B (3B attivi)
- Qwen3-235B-A22B (235B totali, 22B attivi)
- Performance competitiva con DeepSeek-R1, OpenAI o1, Gemini 2.5-Pro

**Performance Highlight:**
> *"Qwen3-1.7B/4B/8B/14B/32B performano come Qwen2.5-3B/7B/14B/32B/72B"*
> Ogni nuovo modello Qwen3 = ~doppia dimensione Qwen2.5!

#### B) Qwen3-Coder - Specialista Coding

- **Qwen3-Coder-480B-A35B-Instruct** (MoE: 480B totali, 35B attivi)
- Context: 256K (estendibile 1M) → comprende interi repository
- **Benchmark:**
  - 69.6% su SWE-Bench Verified (top mondiale)
  - 81.5 su AIME 2025 (math reasoning)
- Comparabile a Claude Sonnet 4

#### C) Qwen2.5-VL - Vision-Language

- Dimensioni: 3B, 7B, 32B, 72B
- Rilascio: Gennaio 2025
- Capacità:
  - Visual reasoning
  - Comprensione video (fino a 1 ora)
  - Localizzazione precisa
  - Risoluzione native

#### D) Qwen2.5-Math

- Supporto: Cinese + Inglese
- Metodi reasoning:
  - Chain-of-Thought (CoT)
  - Program-of-Thought (PoT)
  - Tool-Integrated Reasoning (TIR)

#### E) QwQ-32B - Reasoning Excellence

- Modello specializzato per reasoning
- Eccellenza in problem-solving complesso

### 1.3 Punti di Forza Qwen

#### 1. Multilingua Superiore

- **119 lingue e dialetti** in training (Qwen3)
- Eccellenza cinese + inglese
- Vantaggio distintivo vs competitor occidentali

#### 2. Performance vs Size

- Qwen3-8B batte Qwen2.5-14B su STEM/coding
- Efficienza parametri: meno parametri, stessa qualità
- Ideale per deployment locale

#### 3. Licenza Permissiva

- **Apache 2.0** su quasi tutti i modelli
- Uso commerciale illimitato
- Modifiche e fine-tuning liberi

#### 4. Famiglia Completa

- Generale (Qwen3)
- Coding (Qwen3-Coder)
- Vision (Qwen2.5-VL)
- Math (Qwen2.5-Math)
- Reasoning (QwQ-32B)
- Multimodale (Qwen2.5-Omni, Qwen3-Omni)

#### 5. Novità 2025-2026

- **Qwen3** (Apr 2025): Dual-mode thinking/non-thinking
- **Qwen-Image-2512** (Dic 2025): Generazione immagini open-source (competitor Google)
- Context esteso: 256K → 1M token

### 1.4 Prezzi (API Alibaba Cloud - 2026)

| Modello | Input (per 1M token) | Output (per 1M token) |
|---------|----------------------|------------------------|
| Qwen3-Coder-480B | $2.00 | $2.00 |
| Qwen3-235B-Thinking | $0.65 | $3.00 |
| Qwen3-235B-Instruct | $0.20 | $0.60 |
| Qwen2.5-VL-72B | $1.95 | $8.00 |

---

## PARTE 2: DEEPSEEK

### 2.1 Il "DeepSeek Moment"

#### Cosa è Successo?

**27 Gennaio 2025** - Un giorno storico per l'AI:

- DeepSeek rilascia **DeepSeek-R1** (LLM con reasoning)
- Diventa #1 app iOS App Store USA (sorpassa ChatGPT)
- **Nvidia crolla -18%** in un giorno
- Definito il **"Sputnik Moment"** dell'AI

#### Perché è Importante?

**Il paradigma cambia:**

```
PRIMA:
AI = capitale intensivo
Serve $100M+ per competere
Chip USA = barriera insuperabile

DOPO DeepSeek:
AI = engineering competition
$5.6M bastano (?)
Efficienza > forza bruta
```

**Impatto:**

- Dimostra che modelli avanzati NON richiedono necessariamente $100M+
- Sfida il "compute moat" (barriera capitale) di OpenAI/Google
- Prova che controlli export USA hanno limiti
- Apre AI a organizzazioni con budget limitato

### 2.2 DeepSeek V3 - Il Breakthrough Efficienza

**Rilascio:** Dicembre 2024

**Architettura:**
- **671B parametri totali**
- **37B attivi per token** (MoE - Mixture of Experts)
- Solo ~5.5% parametri attivi per inferenza

**Performance:**

| Benchmark | DeepSeek-V3 | GPT-4o | Risultato |
|-----------|-------------|--------|-----------|
| MATH-500 (math) | ✅ Superiore | - | DeepSeek vince |
| HumanEval (coding) | ✅ Superiore | - | DeepSeek vince |
| MMLU (knowledge) | ≈ Pari | ≈ Pari | Pareggio |

**Training Cost Claim:**
- **$5.6M** (secondo DeepSeek)
- 2,048 GPU H800 (chip USA-export limited)
- 2.6M GPU hours vs 30.8M di Llama 3 405B

### 2.3 DeepSeek R1 - Il Breakthrough Reasoning

**Rilascio:** 20 Gennaio 2025

**Innovazione Chiave:**

1. **Reasoning via Reinforcement Learning (RL)**
   - Nessun esempio umano di reasoning
   - Il modello IMPARA a ragionare tramite RL puro
   - Emergent patterns: self-reflection, verification, adaptive strategies

2. **Chain-of-Thought Esplicito**
   - Mostra reasoning dentro `<think>...</think>` tags
   - Risponde più lunghe con verifica e alternative
   - Trasparenza totale sul processo cognitivo

3. **Performance Reasoning:**
   - ~79.8% pass@1 su AIME 2024 (da 15.6% iniziale!)
   - ~97.3% pass@1 su MATH-500
   - Competitivo con OpenAI o1

**Architettura Base:**
- Costruito sopra DeepSeek V3 (671B, 37B attivi)
- Training: supervised fine-tuning + RL
- Reasoning pattern emergenti, non pre-programmati

### 2.4 Costi Training - La Controversia

#### Il Claim: $5.6M

DeepSeek afferma costo training **$5.6M** basato su:
- 2,048 GPU H800
- 1 training run
- Solo costi GPU pre-training

#### La Realtà: $1.3 Billion (?)

**SemiAnalysis Research rivela:**

- **$1.3 miliardi** in server capital expenditure totale
- Il $5.6M è solo GPU per 1 run
- NON include:
  - R&D (multipli esperimenti)
  - Infrastruttura
  - Tentativi falliti
  - Team engineering

**Verità:**

> *"Sviluppare un modello richiede eseguire training MOLTE volte e condurre numerosi esperimenti, rendendo il costo reale molte volte superiore"*

#### Lezioni per Noi

**Costo REALE è probabilmente $0.3M - $6M per run:**
- Ma servono molti run
- Però MOLTO meno di $100M+ di OpenAI/Google

**Le Tecniche di Efficienza sono VERE:**

1. **MoE Architecture** → Solo 37B/671B attivi
2. **FP8 Mixed Precision** → Prima applicazione successo ultra-large scale
3. **Multi-Head Latent Attention (MHLA)** → Memoria 5-13% vs metodi precedenti
4. **DualPipe Algorithm** → Comunicazione GPU ottimizzata
5. **PTX Programming** → Controllo basso livello GPU (vs CUDA)

**Takeaway:**
> *"Non è magicamente $5.6M, ma SICURAMENTE ordini di grandezza più economico dei big USA. L'efficienza ingegneristica è REALE."*

### 2.5 Modelli DeepSeek - Gamma Completa

#### A) DeepSeek-V3

- 671B parametri (37B attivi)
- Dicembre 2024
- General purpose LLM
- ~6.5x più economico di R1 (API pricing)

#### B) DeepSeek-R1

- 671B parametri (37B attivi)
- Gennaio 2025
- Reasoning specialist
- Chain-of-thought esplicito
- RL-trained reasoning

#### C) DeepSeek-R1 Distilled Models

**Versioni disponibili:** 1.5B, 7B, 8B, 14B, 32B, 70B

**Base models:**
- Serie Qwen2.5: DeepSeek-R1-Distill-Qwen-1.5B/7B/14B/32B
- Serie Llama3: DeepSeek-R1-Distill-Llama-8B/70B

**Performance Eccezionale:**

- **1.5B**: Supera OpenAI o1-preview su math benchmarks (!)
- **7B-8B**: Top rank zero-shot reasoning
- **32B**: Batte OpenAI o1-mini su vari benchmark

**Licensing:** MIT License (permissivo)

#### D) DeepSeek-Coder

- Specialista coding
- Versione V2 disponibile
- Forte su HumanEval

### 2.6 Requisiti Hardware

**Full Models (V3/R1):**
- 8x NVIDIA H200 GPU
- 141GB memory ciascuna
- Total: ~1.1TB GPU memory

**Distilled Models:**
- 1.5B-7B: GPU consumer (RTX 3090/4090)
- 14B-32B: GPU prosumer/datacenter
- 70B: Multi-GPU setup

### 2.7 Controversie e Limitazioni

#### A) Restrizioni Export USA

**Il Problema:**

- DeepSeek è cinese (High-Flyer hedge fund, Hangzhou)
- Preoccupazioni legami CCP (Chinese Communist Party)
- Connessioni rilevate con China Mobile (state-owned telecom)

**Timeline Restrizioni (2025):**

| Data | Evento |
|------|--------|
| 24 Gen 2025 | US Navy vieta DeepSeek |
| 28 Gen 2025 | NASA, Pentagon, Navy ban |
| 28 Gen 2025 | White House avvia review NSC |
| Feb 2025 | Stati: Virginia, Texas, NY ban |
| Feb 2025 | Arrest Singapore per chip smuggling |

**Legislazione Proposta:**

- **HR 1121**: No DeepSeek on Government Devices Act
- **HR 1122**: China Technology Transfer Control Act
- Focus: Nvidia H20/H800 chip (fuori controlli export, gap da chiudere)

#### B) Preoccupazioni Sicurezza

**Data Security:**

- Dati potrebbero essere condivisi con governo cinese
- Codice login contiene riferimenti China Mobile
- Scripts offuscati con infrastruttura China Mobile

**Model Security:**

- NIST study: "Significativi security flaws"
- Facile indurre comportamenti malicious
- Compliance con query pericolose (download password, malware)

**Contraddizione:**

- Modelli americani superiori ma gap si riduce
- DeepSeek mostra progresso drammatico sotto pressione USA
- Export controls insufficienti (H800/H20 chip evasione)

#### C) Possiamo Usarlo?

**Fattori da Considerare:**

✅ **PRO:**
- Modelli open-source (R1 distilled)
- MIT License = uso commerciale OK
- Nessuna API call a server cinesi se self-hosted
- Performance eccellente

⚠️ **CONTRO:**
- Origine cinese = compliance risk (se clienti USA gov)
- Security flaws documentati
- Reputational risk possibile
- Export ban potrebbero estendersi

**Raccomandazione:**

```
SCENARIO 1: Cervella Baby per uso personale/interno
→ ✅ OK usare DeepSeek-R1-Distill-Qwen
→ Self-hosted, nessun data export
→ Verificare output prima di usare (security)

SCENARIO 2: Prodotto commerciale per clienti
→ ⚠️ Valutare caso per caso
→ Se clienti USA gov/defense → NO
→ Se B2B Europa/privati → Probabilmente OK
→ Disclosure origine modello

SCENARIO 3: Servizio critico (finance, health)
→ 🛑 Evitare per ora
→ Aspettare security audit indipendenti
→ Preferire Qwen (meno controverso)
```

---

## PARTE 3: CONFRONTO FINALE

### 3.1 Tabella Comparativa Generale

| Criterio | Qwen3 | DeepSeek R1 | Llama 3.3 | Mistral |
|----------|-------|-------------|-----------|---------|
| **Sviluppatore** | Alibaba Cloud | DeepSeek AI | Meta | Mistral AI |
| **Origine** | 🇨🇳 Cina | 🇨🇳 Cina | 🇺🇸 USA | 🇫🇷 Francia |
| **Licenza** | Apache 2.0 | MIT | Llama 3 (limitata) | Apache 2.0 |
| **Dimensioni** | 0.6B-235B | 1.5B-671B | 1B-70B | 7B-123B |
| **Context** | 128K-1M | ~128K | 128K | 8K-32K |
| **Multilingua** | ⭐⭐⭐⭐⭐ (119) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Coding** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Math/Reasoning** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Vision** | ⭐⭐⭐⭐⭐ (VL) | ❌ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Efficienza** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Security Concern** | ⚠️ Minore | ⚠️⚠️⚠️ Maggiore | ✅ Nessuno | ✅ Nessuno |
| **Uso Commerciale** | ✅ Illimitato | ✅ Illimitato | ⚠️ Limitato | ✅ Illimitato |

### 3.2 Benchmark Dettagliati

#### A) Small Models (1B-8B)

| Modello | Parametri | HumanEval (Code) | MMLU (Knowledge) | MATH-500 | Note |
|---------|-----------|------------------|------------------|----------|------|
| **Qwen3-1.7B** | 1.7B | - | ~60% | - | Performa come Qwen2.5-3B |
| **DeepSeek-R1-Distill-Qwen-1.5B** | 1.5B | - | - | Batte o1-preview | Reasoning specialist |
| **Qwen3-4B** | 4B | - | ~68% | - | Performa come Qwen2.5-7B |
| **Qwen3-8B** | 8B | Alta | ~72% | - | Batte Qwen2.5-14B STEM |
| **DeepSeek-R1-Distill-Qwen-7B** | 7B | Top | Top | Top | Top zero-shot reasoning |
| **Llama 3.2-3B** | 3B | Media | ~65% | - | General purpose |

#### B) Medium Models (14B-32B)

| Modello | Parametri | Coding | Math | Reasoning | Specialist |
|---------|-----------|--------|------|-----------|------------|
| **Qwen3-32B** | 32B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | General |
| **QwQ-32B** | 32B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Reasoning |
| **DeepSeek-R1-Distill-Qwen-32B** | 32B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Batte o1-mini |
| **Llama 3.3-70B** | 70B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Clean output |

#### C) Large Models (70B+)

| Modello | Parametri (Tot/Attivi) | Performance | Costo API | Specialist |
|---------|------------------------|-------------|-----------|------------|
| **Qwen3-235B-A22B** | 235B / 22B | Top tier | $0.20-$3.00 | General flagship |
| **Qwen3-Coder-480B-A35B** | 480B / 35B | Coding SOTA | $2.00 | Coding specialist |
| **DeepSeek-V3** | 671B / 37B | Top tier | Economico | General |
| **DeepSeek-R1** | 671B / 37B | Reasoning SOTA | Medio | Reasoning |

### 3.3 Scelte per Caso d'Uso

| Scenario | Prima Scelta | Seconda Scelta | Perché |
|----------|--------------|----------------|--------|
| **Coding Assistant** | Qwen3-Coder-480B | DeepSeek-Coder-V2 | SWE-Bench performance |
| **Math/Reasoning** | DeepSeek-R1-Distill | QwQ-32B | RL reasoning + CoT |
| **General Chat** | Qwen3-32B | Llama 3.3-70B | Balance perf/size |
| **Multilingua** | Qwen3 (any) | Mistral Large | 119 lingue support |
| **Vision Tasks** | Qwen2.5-VL-72B | Llama 3.2-Vision | Video understanding |
| **Edge/Mobile** | Qwen3-1.7B/4B | DeepSeek-R1-1.5B | Size efficiency |
| **Cost-Optimized** | DeepSeek-V3 | Mistral 7B | API pricing |
| **Security-Critical** | Llama 3.3 | Mistral | No China concerns |

### 3.4 Per Cervella Baby - Raccomandazioni

#### Scenario A: Model Base Generale

**Prima scelta: Qwen3-4B o Qwen3-8B**

✅ **PRO:**
- Performance eccellente (~ Qwen2.5-7B/14B)
- Apache 2.0 = libertà totale
- Multilingua superior
- Famiglia completa (coding, vision, math variants)
- Alibaba = meno controverso di DeepSeek

⚠️ **CONTRO:**
- Origine cinese (ma Alibaba è più "corporate")
- Non specializzato reasoning come R1

**Config suggerita:**
```
Base: Qwen3-4B (general understanding)
Fine-tune: Task-specific per Cervella Baby
Context: 128K (sufficiente per la maggior parte casi)
Deployment: Local (Mac Studio M2 Ultra può handle)
```

#### Scenario B: Reasoning Specialist

**Prima scelta: DeepSeek-R1-Distill-Qwen-7B**

✅ **PRO:**
- Reasoning capabilities INCREDIBILI
- 7B = deployment feasible
- MIT License
- Self-hosted = no data to China
- Chain-of-thought transparency

⚠️ **CONTRO:**
- Security concerns se exposed
- Reputazione DeepSeek (ban gov USA)
- Testing intensivo necessario

**Config suggerita:**
```
Use case: Problem-solving, planning, analysis
Deployment: Strictly local, no external API
Safety: Output validation layer
Disclosure: Document model origin per transparency
```

#### Scenario C: Hybrid Approach (RACCOMANDATO)

**Combinazione intelligente:**

```
Tier 1 - Base Intelligence:
→ Qwen3-4B o Qwen3-8B
→ General understanding, coding, multilingua
→ Always-on, fast response

Tier 2 - Deep Reasoning:
→ DeepSeek-R1-Distill-Qwen-7B o QwQ-32B
→ Complex problem-solving
→ Triggered for hard tasks

Tier 3 - Vision (se serve):
→ Qwen2.5-VL-7B
→ Visual understanding

Orchestrator:
→ Cervella Baby DECIDE quale tier usare
→ Routing intelligente based on task
```

**Vantaggi:**
- Best of both worlds
- Efficiency (usa small model quando possibile)
- Capability (usa reasoning model quando necessario)
- Flexibility (add/remove tiers)

---

## PARTE 4: DECISIONI E NEXT STEPS

### 4.1 Raccomandazione Finale

**Per Cervella Baby, raccomando:**

🥇 **PRIMARY: Qwen3-4B**
- Base model per general intelligence
- Apache 2.0, multilingua, efficient
- Deploy local su Mac Studio

🥈 **SECONDARY: DeepSeek-R1-Distill-Qwen-7B**
- Reasoning engine per task complessi
- Self-hosted, output validation
- Triggered selectively

🥉 **OPTIONAL: Qwen2.5-VL-7B**
- Se servono capacità vision
- Same ecosystem (Alibaba)

### 4.2 Prossimi Step Suggeriti

1. **Testing Phase**
   - Download Qwen3-4B via Ollama
   - Benchmark su task Cervella Baby typical
   - Misurare: speed, accuracy, resource usage

2. **Security Audit**
   - Test DeepSeek-R1-Distill con adversarial prompts
   - Verify no data leakage
   - Document findings

3. **Integration Design**
   - Architettare tier system
   - Definire routing logic
   - Plan fallback mechanisms

4. **Fine-Tuning Evaluation**
   - Qwen3-4B può beneficiare fine-tuning?
   - Dataset Cervella Baby tasks
   - Cost/benefit analysis

5. **Monitoring Setup**
   - Track model performance
   - Usage patterns
   - Resource consumption

### 4.3 Rischi e Mitigazioni

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| **Export ban esteso Qwen** | Bassa | Alto | Backup plan con Llama |
| **Security flaw DeepSeek** | Media | Alto | Output validation, limited scope |
| **Performance insufficiente** | Bassa | Medio | Testing pre-commitment |
| **Resource constraints** | Media | Medio | Tier system, selective use |
| **License change** | Molto bassa | Alto | Apache 2.0 = fork possible |

---

## PARTE 5: FONTI E APPROFONDIMENTI

### Qwen - Fonti Principali

**Documentazione Ufficiale:**
- [Qwen3: Think Deeper, Act Faster](https://qwenlm.github.io/blog/qwen3/)
- [Qwen Technical Report (arXiv)](https://arxiv.org/pdf/2505.09388)
- [Qwen - Wikipedia](https://en.wikipedia.org/wiki/Qwen)
- [Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/models)

**GitHub:**
- [Qwen Team GitHub](https://github.com/QwenLM)
- [Qwen2.5-Omni Repository](https://github.com/QwenLM/Qwen2.5-Omni)

**Analisi:**
- [Data Science Dojo: Complete Guide to Qwen](https://datasciencedojo.com/blog/the-evolution-of-qwen-models/)
- [Best Qwen Models in 2026 - Apidog](https://apidog.com/blog/best-qwen-models/)
- [Qwen AI Coding Review - Index.dev](https://www.index.dev/blog/qwen-ai-coding-review)
- [Alibaba Launches Qwen3 - VentureBeat](https://venturebeat.com/ai/alibaba-launches-open-source-qwen3-model-that-surpasses-openai-o1-and-deepseek-r1)

**Recent News:**
- [Qwen-Image-2512 Launch - Open Source For You](https://www.opensourceforu.com/2026/01/alibaba-launches-open-source-qwen-image-2512-as-a-serious-alternative-to-googles-image-ai/)
- [Qwen3-Omni Release - Alibaba Group](https://www.alibabagroup.com/en-US/document-1843362291857227776)

### DeepSeek - Fonti Principali

**Documentazione Ufficiale:**
- [DeepSeek-R1 Paper (arXiv)](https://arxiv.org/pdf/2501.12948)
- [DeepSeek-R1 on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1)
- [DeepSeek-R1 GitHub](https://github.com/deepseek-ai/DeepSeek-R1)
- [DeepSeek - Wikipedia](https://en.wikipedia.org/wiki/DeepSeek)

**Analisi Tecniche:**
- [DeepSeek V3 Cost Analysis - Interconnects](https://www.interconnects.ai/p/deepseek-v3-and-the-actual-cost-of)
- [DeepSeek Inference Cost Explained - IntuitionLabs](https://intuitionlabs.ai/articles/deepseek-inference-cost-explained)
- [BentoML: Complete Guide to DeepSeek Models](https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond)
- [Andrej Karpathy Praises DeepSeek V3](https://www.analyticsvidhya.com/blog/2024/12/deepseek-v3/)

**Controversie Costi:**
- [Gregory Bufithis: DeepSeek Cost Reality](https://www.gregorybufithis.com/2025/02/07/deepseeks-ai-training-only-cost-6-million-ah-no-more-like-1-3-billion/)
- [INSAIT: Training Cost Misleading](https://therecursive.com/martin-vechev-of-insait-deepseek-6m-cost-of-training-is-misleading/)
- [Yahoo: Research Exposes $1.3B Cost](https://www.yahoo.com/news/research-exposes-deepseek-ai-training-165025904.html)

**Security & Export:**
- [U.S. Federal Restrictions - Inside Gov Contracts](https://www.insidegovernmentcontracts.com/2025/02/u-s-federal-and-states-governments-moving-quickly-to-restrict-use-of-deepseek/)
- [Wiley: DeepSeek Policy Response](https://www.wiley.law/wiley-connect/Chinese-AI-Firm-DeepSeek-Triggers-a-Wide-US-Policy-Response)
- [NIST Study: Security Flaws - FDD](https://www.fdd.org/analysis/2025/10/07/new-major-study-suggests-deepseek-still-lags-behind-top-american-models-and-presents-major-security-flaws/)

**Market Impact:**
- [DeepSeek Revolution $6M - FinancialContent](https://markets.financialcontent.com/wral/article/tokenring-2026-1-9-the-deepseek-revolution-how-a-6-million-model-shattered-the-ai-compute-moat)
- [IBM: Breakthrough Win for Innovation](https://www.ibm.com/think/insights/deepseek-breakthrough-is-a-win-for-innovation-and-accessibility)
- [CSIS: Redefining AI Race](https://www.csis.org/analysis/deepseeks-latest-breakthrough-redefining-ai-race)

### Comparazioni

- [10 Best Open-Source LLMs 2025 - Hugging Face](https://huggingface.co/blog/daya-shankar/open-source-llms)
- [Qwen vs DeepSeek vs Llama vs Mistral - Medium](https://medium.com/@techlatest.net/choosing-the-right-open-source-llm-for-rag-deepseek-r1-vs-qwen-2-5-vs-mistral-vs-llama-9303d1777a9e)
- [Best Chinese Models vs US - Understanding AI](https://www.understandingai.org/p/the-best-chinese-open-weight-models)
- [DeepSeek R1 vs Qwen3 - DataCamp](https://www.datacamp.com/blog/qwen3)
- [Coding Test: Mistral, Llama, DeepSeek, Qwen - Medium](https://medium.com/@elisheba.t.anderson/which-ai-model-is-best-for-coding-i-tested-mistral-llama-3-2-deepseek-and-qwen-185a058b15be)

---

## APPENDICE: Glossario Tecnico

**MoE (Mixture of Experts)**: Architettura dove solo subset di parametri è attivo per ogni input, aumentando efficienza.

**Chain-of-Thought (CoT)**: Tecnica reasoning dove il modello mostra step intermedi di pensiero.

**Distillation**: Processo di trasferire conoscenza da modello grande a piccolo, mantenendo performance.

**Context Window**: Quantità massima di token che il modello può processare in una volta.

**Apache 2.0 License**: Licenza open-source permissiva che consente uso commerciale senza restrizioni.

**MIT License**: Licenza ancora più permissiva di Apache 2.0, quasi nessuna restrizione.

**RL (Reinforcement Learning)**: Apprendimento tramite reward/penalty invece che esempi supervised.

**FP8 Mixed Precision**: Formato numerico a 8-bit che riduce memoria e compute mantenendo accuracy.

**SWE-Bench**: Benchmark per coding basato su real-world software engineering tasks.

**AIME**: American Invitational Mathematics Examination, test math avanzato.

**MMLU**: Massive Multitask Language Understanding, benchmark knowledge generale.

---

**Fine Ricerca**

*Ricercatrice: Cervella Researcher*
*Data: 10 Gennaio 2026*
*Versione: 1.0*

---

## TL;DR per Decisione Rapida

```
DOMANDA: Quale modello per Cervella Baby?

RISPOSTA BREVE:
→ Qwen3-4B come base (Apache 2.0, efficiente, multilingua)
→ DeepSeek-R1-Distill-Qwen-7B per reasoning (self-hosted)
→ Hybrid tier approach = best solution

PERCHÉ:
→ Qwen = meno controverso, licensing chiaro, ecosystem completo
→ DeepSeek = reasoning superiore, ma security concerns
→ Combination = capability + safety

NEXT:
→ Test Qwen3-4B su Mac Studio
→ Benchmark typical Cervella Baby tasks
→ Validate DeepSeek-R1 security
→ Design tier routing system

RISCHIO PRINCIPALE:
→ Export restrictions (unlikely ma possibile)
→ Mitigazione: Llama 3.3 come backup plan
```

---

*"Studiare prima di agire - sempre!"* 🔬
