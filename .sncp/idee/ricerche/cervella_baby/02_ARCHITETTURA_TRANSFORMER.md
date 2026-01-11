# ARCHITETTURA TRANSFORMER - COME FUNZIONA

> **Data ricerca:** 10 Gennaio 2026
> **Researcher:** Cervella Researcher
> **Obiettivo:** Capire a fondo come funzionano i Transformer - il cuore dei moderni LLM

---

## INDICE

1. [Spiegazione Semplice](#spiegazione-semplice)
2. [Spiegazione Tecnica](#spiegazione-tecnica)
3. [Perché è Rivoluzionario](#perché-è-rivoluzionario)
4. [Componenti Chiave](#componenti-chiave)
5. [Come Funziona il Training](#come-funziona-il-training)
6. [Varianti Architetturali](#varianti-architetturali)
7. [Scaling Laws](#scaling-laws)
8. [Fonti e Risorse](#fonti-e-risorse)

---

## SPIEGAZIONE SEMPLICE

### Cos'è un Transformer?

Immagina di voler capire una frase. Il modo tradizionale sarebbe leggerla parola per parola, da sinistra a destra, cercando di ricordare tutto quello che hai letto prima.

Il Transformer fa qualcosa di **rivoluzionario**: guarda **tutte le parole contemporaneamente** e decide quali sono più importanti per capire il significato di ciascuna.

### Analogia della Classe

Pensa a una classe di studenti che deve studiare un testo:

**Approccio Vecchio (RNN/LSTM):**
- Gli studenti leggono uno alla volta, in fila
- Ognuno passa le informazioni al successivo
- Chi è in fondo alla fila riceve informazioni già "dimenticate" o distorte

**Approccio Transformer:**
- Tutti gli studenti leggono tutto il testo contemporaneamente
- Ognuno può chiedere a TUTTI gli altri: "Questa parola è importante per capire quella?"
- Ogni studente costruisce la sua comprensione guardando l'intero contesto

### Il Concetto Chiave: "Attention"

**"Attention is All You Need"** - questo è il titolo del paper originale (2017).

L'idea è che per capire una parola, devi sapere a **quali altre parole prestare attenzione**.

**Esempio:**
```
Frase: "La banca del fiume era coperta di fiori"

Domanda: Cosa significa "banca"?

Il Transformer guarda:
- "banca" + "fiume" → AH! È la riva del fiume
- "banca" + "fiori" → Conferma che è un contesto naturale
- NON è "banca" + "soldi" + "conto" → Quindi non è una banca finanziaria

Questo processo si chiama SELF-ATTENTION.
```

### Perché è Importante?

Prima dei Transformer:
- Modelli lenti da addestrare (sequenziali)
- Difficoltà a ricordare informazioni lontane
- Non parallelizzabili (GPU inutilizzate)

Dopo i Transformer:
- Training velocissimo (tutto in parallelo)
- Cattura dipendenze a qualsiasi distanza
- Scala perfettamente su GPU/TPU
- **Risultato:** GPT, BERT, Claude, ChatGPT, tutti i moderni LLM

---

## SPIEGAZIONE TECNICA

### Architettura Originale (2017)

Il paper "Attention Is All You Need" introduce un'architettura composta da:

```
┌─────────────────────────────────────────┐
│          TRANSFORMER COMPLETO           │
│                                         │
│  ┌───────────────┐  ┌───────────────┐ │
│  │   ENCODER     │  │   DECODER     │ │
│  │               │  │               │ │
│  │ - Self-Attn   │  │ - Masked Attn │ │
│  │ - Feed Fwd    │  │ - Cross-Attn  │ │
│  │               │  │ - Feed Fwd    │ │
│  │ (x6 layers)   │  │ (x6 layers)   │ │
│  └───────────────┘  └───────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

**Caratteristiche principali:**
- **6 layer encoder** + **6 layer decoder** (nel paper originale)
- Ogni layer ha **multi-head attention** (8 teste) e **feed-forward network**
- **Residual connections** e **layer normalization** ovunque
- **NO RICORRENZA, NO CONVOLUZIONE** - solo attention!

### Il Flusso dei Dati

```
INPUT TEXT → TOKENIZATION
    ↓
TOKEN EMBEDDINGS (dimensione d_model = 512)
    ↓
POSITIONAL ENCODING (aggiunge info sulla posizione)
    ↓
ENCODER LAYERS (x6)
    ↓
DECODER LAYERS (x6)
    ↓
LINEAR + SOFTMAX
    ↓
OUTPUT PROBABILITIES (prossimo token)
```

---

## PERCHÉ È RIVOLUZIONARIO

### 1. Parallelizzazione Totale

**RNN/LSTM (Prima dei Transformer):**
```python
# Pseudocodice - SEQUENZIALE
for t in range(sequence_length):
    hidden[t] = process(input[t], hidden[t-1])
    # DEVE aspettare t-1 per calcolare t!
```

**Transformer:**
```python
# Pseudocodice - PARALLELO
# Tutti i token processati simultaneamente!
attention_scores = query @ key.T  # Matrix multiplication
output = softmax(attention_scores) @ value
# GPU può fare tutto in UN passo!
```

**Risultato:** Training 10-100x più veloce su hardware moderno.

### 2. Cattura Dipendenze a Lungo Raggio

**RNN/LSTM:**
- Informazione passa attraverso stati nascosti sequenziali
- Più lunga la sequenza, più l'informazione si "diluisce"
- Difficoltà a ricordare oltre ~100-200 token

**Transformer:**
- Ogni token può guardare direttamente TUTTI gli altri
- Nessuna degradazione con la distanza
- Context window limitato solo dalla memoria (oggi: 100K+ token!)

### 3. Flessibilità Architetturale

Il design modulare ha permesso varianti:
- **BERT** - solo encoder (comprensione)
- **GPT** - solo decoder (generazione)
- **T5** - encoder-decoder completo (traduzione/summarization)
- **MoE** - mixture of experts (efficienza)

---

## COMPONENTI CHIAVE

### 1. SELF-ATTENTION MECHANISM

Il cuore del Transformer. Per ogni token, calcola quanto è rilevante rispetto a tutti gli altri.

#### Processo Passo-Passo

**Step 1: Creare Query, Key, Value**

Per ogni token, creiamo 3 vettori tramite moltiplicazione con matrici apprese:

```
Input embedding: x  (dimensione d_model)

Query:  Q = x @ W_Q    (cosa sto cercando?)
Key:    K = x @ W_K    (cosa offro agli altri?)
Value:  V = x @ W_V    (cosa comunico?)
```

**Analogia:**
- **Query** = la domanda che fai ("Chi può aiutarmi a capire questa parola?")
- **Key** = il tag di ogni parola ("Io sono rilevante per contesto finanziario")
- **Value** = il contenuto da comunicare ("Ecco il mio significato")

**Step 2: Calcolare Attention Scores**

```python
# Prodotto scalare tra query e keys
scores = Q @ K.T / sqrt(d_k)

# Perché la divisione per sqrt(d_k)?
# Per stabilizzare i gradienti quando d_k è grande
```

**Step 3: Softmax per Normalizzare**

```python
# Convertiamo scores in probabilità (somma = 1)
attention_weights = softmax(scores)

# Ora sappiamo "quanto" guardare ogni token
# Esempio: [0.05, 0.1, 0.6, 0.2, 0.05]
#          → 60% attenzione al token 3
```

**Step 4: Weighted Sum dei Values**

```python
output = attention_weights @ V

# Ogni output è una combinazione pesata
# dei values di TUTTI i token
```

#### Formula Completa

```
Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V
```

**Dove:**
- Q, K, V = matrici Query, Key, Value
- d_k = dimensione delle key (per scaling)
- softmax = normalizzazione a probabilità

### 2. MULTI-HEAD ATTENTION

Invece di una sola attention, ne usiamo multiple in parallelo!

**Perché?**

Ogni "testa" impara a focalizzarsi su aspetti diversi:
- Testa 1 → Relazioni sintattiche (soggetto-verbo)
- Testa 2 → Relazioni semantiche (sinonimi, contrari)
- Testa 3 → Relazioni posizionali (vicino/lontano)
- ... (GPT-2 usa 12 teste, GPT-3 usa 96!)

**Implementazione:**

```python
# 8 teste parallele (come nel paper originale)
num_heads = 8
d_k = d_model // num_heads  # Es: 512/8 = 64 per testa

for i in range(num_heads):
    head_i = Attention(Q_i, K_i, V_i)

# Concatena tutti gli output
multi_head_output = concat(head_1, ..., head_8) @ W_O
```

**Vantaggi:**
- Cattura molteplici tipi di relazioni contemporaneamente
- Più robusto (se una testa sbaglia, le altre compensano)
- Parallelizzabile su hardware moderno

### 3. POSITIONAL ENCODING

**Problema:** L'attention non ha nozione intrinseca di ORDINE!

Per il self-attention, "Il cane morde l'uomo" = "L'uomo morde il cane"
(stessi token, stesso attention score)

**Soluzione:** Aggiungiamo informazione posizionale agli embeddings.

#### Due Approcci

**A) Sinusoidal Encoding (Paper Originale)**

```python
# Per posizione pos e dimensione i:
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

**Vantaggi:**
- No parametri da imparare (zero overfitting)
- Funziona su sequenze più lunghe del training
- Encoding deterministico e unico per ogni posizione
- Valori normalizzati in [-1, 1]

**Come funziona:**
- Usa frequenze diverse per dimensioni diverse
- Crea un pattern unico per ogni posizione
- Facile per il modello capire "distanza relativa"

**B) Learned Positional Embeddings**

```python
# Embedding table learned durante training
pos_embeddings = nn.Embedding(max_seq_length, d_model)
output = token_embeddings + pos_embeddings[position]
```

**Vantaggi:**
- Si adatta al task specifico
- Usato dalla maggior parte dei LLM moderni (BERT, GPT, ecc.)

**Svantaggi:**
- Non può gestire sequenze più lunghe del training
- Richiede più memoria (parametri extra)

**Confronto Pratico:**

| Caratteristica | Sinusoidal | Learned |
|----------------|------------|---------|
| Parametri | 0 | max_length × d_model |
| Extrapolation | ✅ Eccellente | ❌ Limitata |
| Task-specific fit | ❌ Fisso | ✅ Adattivo |
| Uso moderno | Ricerca | Produzione (BERT, GPT) |

### 4. FEED-FORWARD NETWORK (FFN)

Dopo ogni attention layer, c'è una rete fully-connected:

```python
FFN(x) = max(0, x @ W1 + b1) @ W2 + b2
#        └─────────────────┘
#              ReLU activation

# Dimensioni (paper originale):
# W1: d_model → 4*d_model (512 → 2048)
# W2: 4*d_model → d_model (2048 → 512)
```

**Perché è importante:**
- Aggiunge **non-linearità** al modello
- Permette trasformazioni più complesse
- Applicata **indipendentemente** a ogni posizione
- Contiene la maggior parte dei parametri del modello!

### 5. LAYER NORMALIZATION

Normalizza gli input a ogni sub-layer:

```python
LayerNorm(x) = γ * (x - mean(x)) / std(x) + β
```

**Perché è necessario:**
- Stabilizza il training (gradienti più sani)
- Permette learning rate più alti
- Riduce dipendenza dall'inizializzazione

**Dove viene applicato:**
- Prima/dopo ogni attention layer
- Prima/dopo ogni FFN

### 6. RESIDUAL CONNECTIONS

Ogni sub-layer ha una "skip connection":

```python
# Invece di:
output = SubLayer(x)

# Facciamo:
output = x + SubLayer(x)
```

**Vantaggi:**
- Gradienti fluiscono meglio durante backpropagation
- Previene "vanishing gradient" in reti profonde
- Layer iniziali ricevono segnali di errore forti
- Permette modelli con 100+ layer (GPT-3: 96 layer!)

---

## COME FUNZIONA IL TRAINING

### Next Token Prediction

**Obiettivo:** Data una sequenza, prevedere il prossimo token.

```
Input:  "Il gatto è seduto sul"
Target: "tappeto"

Il modello impara:
P(tappeto | Il gatto è seduto sul)
```

**Perché è potente:**

Questa task apparentemente semplice richiede al modello di imparare:
- Grammatica e sintassi
- Semantica e significato
- Conoscenza del mondo
- Ragionamento e inferenza

### Loss Function: Cross-Entropy

```python
# Per ogni posizione nella sequenza:
predictions = model(input_tokens)  # Shape: [seq_len, vocab_size]
targets = input_tokens[1:]         # Shifted by one

# Cross-entropy loss
loss = -sum(log(predictions[i, targets[i]]) for i in range(len(targets)))
```

**Cosa misura:**
- Quanto bene il modello predice il token corretto
- Penalizza fortemente predizioni sbagliate
- Ottimizza le probabilità output

### Training Process

```
1. TOKENIZATION
   "Hello world" → [15496, 995]

2. EMBEDDING
   [15496, 995] → [[0.1, -0.3, ...], [0.5, 0.2, ...]]

3. FORWARD PASS
   Embedding → Encoder/Decoder → Logits

4. COMPUTE LOSS
   Compare predictions vs ground truth (shifted input)

5. BACKPROPAGATION
   Compute gradients for all parameters

6. UPDATE WEIGHTS
   Adam optimizer (tipicamente):
   W_new = W_old - learning_rate * gradients
```

### Backpropagation in Transformer

**Flusso del Gradiente:**

```
Loss (top)
  ↓
Linear + Softmax
  ↓
Decoder Layer 6 (Residual permette gradient flow!)
  ↓
Decoder Layer 5
  ↓
...
  ↓
Decoder Layer 1
  ↓
Embedding Layer (gli embeddings imparano!)
```

**Componenti che Imparano:**

1. **Embedding Matrices**
   - Token embeddings: vocabolario → d_model
   - Position embeddings (se learned)

2. **Attention Weights**
   - W_Q, W_K, W_V per ogni head
   - W_O per combinare le heads

3. **Feed-Forward**
   - W1, b1, W2, b2 per ogni layer

4. **Layer Normalization**
   - γ (gamma) e β (beta) per ogni LayerNorm

5. **Output Layer**
   - W_final: d_model → vocab_size

**Gradient Flow grazie a:**
- **Residual connections** - shortcut per gradienti
- **Layer normalization** - stabilizza magnitudine
- **Multi-head attention** - diversifica i pathway

### Pre-training vs Fine-tuning

**Pre-training** (costoso, fatto una volta):
```
Corpus: Miliardi di parole (es. Common Crawl, Wikipedia, libri)
Task: Next token prediction
Durata: Settimane/mesi su centinaia di GPU
Costo: Milioni di dollari

Output: Base model con conoscenza generale
```

**Fine-tuning** (economico, task-specific):
```
Corpus: Dataset specifico (es. domande mediche, codice Python)
Task: Può essere diverso (es. question answering, classification)
Durata: Ore/giorni su poche GPU
Costo: Centinaia/migliaia di dollari

Output: Specialized model per il tuo task
```

---

## VARIANTI ARCHITETTURALI

### 1. ENCODER-ONLY: BERT

```
┌─────────────────────┐
│   ENCODER ONLY      │
│                     │
│   - Bidirectional   │
│   - Masked LM       │
│   - NSP task        │
│                     │
│   Best for:         │
│   - Classification  │
│   - NER             │
│   - Q&A (extract)   │
└─────────────────────┘
```

**Architettura:**
- Solo la parte Encoder del Transformer originale
- **Bidirectional** - ogni token vede tutti gli altri (passato E futuro)

**Training Objective: Masked Language Modeling (MLM)**
```
Input:  "Il [MASK] è seduto sul [MASK]"
Target: "Il [gatto] è seduto sul [tappeto]"

Random mask del 15% dei token
Il modello impara a predirli dal contesto bilaterale
```

**Use Cases:**
- Sentence classification (sentiment, topic)
- Named Entity Recognition
- Extractive Question Answering
- Text understanding tasks

**Esempi famosi:**
- BERT (Google, 2018)
- RoBERTa (Facebook, 2019)
- ALBERT (lightweight BERT)

### 2. DECODER-ONLY: GPT

```
┌─────────────────────┐
│   DECODER ONLY      │
│                     │
│   - Unidirectional  │
│   - Causal mask     │
│   - Autoregressive  │
│                     │
│   Best for:         │
│   - Generation      │
│   - Completion      │
│   - Chat            │
└─────────────────────┘
```

**Architettura:**
- Solo la parte Decoder (senza cross-attention)
- **Causal masking** - ogni token vede solo i precedenti

**Masked Self-Attention:**
```python
# Mask per impedire di "spiare" il futuro
mask = [[1, 0, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 0],
        [1, 1, 1, 1]]

# Token 0 vede solo se stesso
# Token 1 vede token 0 e 1
# Token 2 vede token 0, 1, 2
# ecc.
```

**Training: Causal Language Modeling**
```
Input:  "Il gatto è"
Target: "seduto"

Sempre predici il PROSSIMO token
Left-to-right, sequenziale
```

**Use Cases:**
- Text generation (stories, articles)
- Code completion
- Conversational AI (ChatGPT, Claude)
- Few-shot learning

**Esempi famosi:**
- GPT-1, 2, 3, 4 (OpenAI)
- Claude (Anthropic) - io! 😊
- PaLM (Google)
- LLaMA (Meta)

**Perché ha vinto:**
- Scaling laws favorevoli (più parametri = molto meglio)
- Few-shot learning emergente
- Versatilità incredibile
- Generazione di qualità superiore

### 3. ENCODER-DECODER: T5

```
┌─────────────────────────────┐
│   ENCODER + DECODER         │
│                             │
│   ┌─────────┐  ┌─────────┐ │
│   │ Encoder │→ │ Decoder │ │
│   │ (Bidir) │  │ (Causal)│ │
│   └─────────┘  └─────────┘ │
│                             │
│   Best for:                 │
│   - Translation             │
│   - Summarization           │
│   - Seq-to-seq              │
└─────────────────────────────┘
```

**Architettura:**
- Encoder completo (bidirectional)
- Decoder completo (causal + cross-attention)
- Cross-attention: decoder attende all'output dell'encoder

**Text-to-Text Framework:**
```
Tutti i task diventano "testo → testo"

Translation:
  Input:  "translate English to French: Hello"
  Output: "Bonjour"

Summarization:
  Input:  "summarize: [long article]"
  Output: "[summary]"

Classification:
  Input:  "sentiment: This movie is great!"
  Output: "positive"
```

**Use Cases:**
- Machine translation
- Text summarization
- Question answering (generative)
- Data-to-text generation

**Esempi famosi:**
- T5 (Google, 2019)
- BART (Facebook)
- mT5 (multilingual T5)

### 4. MIXTURE OF EXPERTS (MoE)

```
┌─────────────────────────────┐
│   MIXTURE OF EXPERTS        │
│                             │
│    Input                    │
│      ↓                      │
│   ┌─────┐   Gating Network │
│   │Gate │→ Expert Selection │
│   └─────┘                   │
│      ↓                      │
│   ┌───┬───┬───┬───┐        │
│   │E1 │E2 │...│E8 │        │
│   └───┴───┴───┴───┘        │
│      ↓                      │
│   Combined Output           │
│                             │
│   8 experts, 2 active/token │
└─────────────────────────────┘
```

**Idea Chiave:**
Invece di un singolo FFN, usa N "esperti" (FFN separati) e un router che decide quali 2 attivare per ogni token.

**Architettura:**
```python
# Router decide quali expert usare
router_scores = Router(input)  # [batch, num_experts]
top_2_experts = top_k(router_scores, k=2)

# Solo 2 expert attivi per token!
output = 0
for expert_id in top_2_experts:
    weight = router_scores[expert_id]
    output += weight * Expert[expert_id](input)
```

**Vantaggi:**
- **Sparse activation** - solo 2/8 expert attivi
- Molti più parametri totali, ma stesso compute per token
- Ogni expert può specializzarsi (es: Expert 1 → math, Expert 2 → code)
- Modelli ENORMI con inference costo normale

**Svantaggi:**
- Tutti i parametri devono stare in RAM (anche se non tutti attivi)
- Esempio: Mixtral 8x7B = 47B parametri totali in memoria

**Load Balancing:**
Problema: il router potrebbe sempre scegliere gli stessi expert.

Soluzione: auxiliary loss che penalizza distribuzione disuniforme.

**Esempi moderni:**
- Mixtral 8x7B (Mistral AI)
- Grok (xAI)
- DeepSeek-v3 (DeepSeek)

**Perché è il futuro:**
- Scaling efficiente (più parametri senza più compute)
- Specializzazione emergente (expert per domini diversi)
- Best of both worlds: grande capacità + inference veloce

---

## SCALING LAWS

### Il Principio Fondamentale

**Performance ha una relazione POWER-LAW con:**
1. Model parameters (N)
2. Dataset size (D)
3. Compute budget (C)

```
Loss ≈ (N/N₀)^(-α) + (D/D₀)^(-β) + (C/C₀)^(-γ)

Dove α, β, γ sono esponenti empirici
```

### Scoperte Chiave (Kaplan et al., 2020)

**1. Più Grande è Sempre Meglio**
```
10x parametri → ~2x performance improvement
100x parametri → ~4x performance improvement
1000x parametri → ~8x performance improvement

(diminishing returns, ma sempre positivi!)
```

**2. Data e Model Size devono crescere insieme**
```
Optimal: N ∝ D^(0.74)

Se raddoppi i parametri, aumenta dataset di ~1.7x

Sotto-training = spreco di parametri
Over-training = overfit + slow convergence
```

**3. Compute è Re**
```
Dato un budget di compute C:

Optimal split:
- 50% su più parametri
- 50% su più dati

Non: model gigante + pochi dati
Non: model piccolo + training lunghissimo
```

### Implicazioni Pratiche (2026)

**Chinchilla Scaling Laws (DeepMind, 2022):**
```
I modelli erano UNDER-TRAINED!

GPT-3 (175B params, 300B tokens) era suboptimal.

Optimal per 175B params: ~3.5 TRILLION tokens!

Risultato: Chinchilla (70B params, 1.4T tokens)
           > GPT-3 (175B params, 300B tokens)
```

**Regola pratica 2026:**
```
Per ogni parametro, serve ~20 token di training.

Model 1B params → 20B token
Model 10B params → 200B token
Model 100B params → 2T token

Esempi:
- LLaMA 2 (70B): trained on 2T tokens ✓
- GPT-4: probabilmente 10T+ tokens
```

### Emergent Abilities

Oltre certe soglie di scale, compaiono capacità NON presenti nei modelli più piccoli:

```
< 1B params:
  - Basic grammar
  - Simple factual recall

1B - 10B params:
  - Few-shot learning
  - Basic reasoning

10B - 100B params:
  - Chain-of-thought reasoning
  - Code generation
  - Multi-step problem solving

100B+ params:
  - Advanced reasoning
  - Mathematical proof
  - Creative writing
  - Meta-learning
```

**Nessuno sa perché.**

È la domanda da un milione di dollari: perché certe abilità "emergono" solo sopra una certa scala?

### Scaling Laws per MoE

Ricerca recente (2025):

```
Performance = f(Active params, Total params)

Active params → main gains
Total params → mild logarithmic boost

Quindi:
- Aumentare expert attivi = grande impatto
- Aumentare numero expert = piccolo impatto

Optimal: ~2-4 expert attivi, 8-16 expert totali
```

### Il Futuro: Where Are We Going?

**Trend 2026:**
- Modelli più grandi (1T+ parametri)
- Training più lungo (10T+ token)
- MoE sempre più comune (efficienza)
- Multimodal (visione + audio + text)

**Limiti fisici:**
- Data availability (finirà internet pubblico?)
- Compute costs (energie rinnovabili?)
- Memory bandwidth (hardware bottleneck)

**La corsa continua...**

---

## FONTI E RISORSE

### Paper Fondamentali

1. **Attention Is All You Need** (Vaswani et al., 2017)
   - [Paper originale su arXiv](https://arxiv.org/abs/1706.03762)
   - IL paper che ha cambiato tutto
   - Lettura obbligatoria per capire i Transformer

2. **BERT: Pre-training of Deep Bidirectional Transformers** (Devlin et al., 2018)
   - Encoder-only architecture
   - Masked Language Modeling

3. **Language Models are Unsupervised Multitask Learners** (GPT-2, Radford et al., 2019)
   - Decoder-only architecture
   - Few-shot learning emergente

4. **Scaling Laws for Neural Language Models** (Kaplan et al., 2020)
   - [Paper su arXiv](https://arxiv.org/pdf/2001.08361)
   - Power-law relationships

5. **Training Compute-Optimal Large Language Models** (Chinchilla, Hoffmann et al., 2022)
   - Optimal data/parameter ratio

### Risorse Educative

**Visualizzazioni Interattive:**
- [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) - Visualizzazione interattiva eccellente
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) - Spiegazione con diagrammi
- [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/) - GPT architecture spiegata

**Tutorial Tecnici:**
- [Understanding and Coding Self-Attention From Scratch](https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html)
- [Transformer Architecture Explained - Codecademy](https://www.codecademy.com/article/transformer-architecture-self-attention-mechanism)
- [Understanding Encoder And Decoder LLMs](https://magazine.sebastianraschka.com/p/understanding-encoder-and-decoder)

**Comparazioni Architetturali:**
- [Comparing BERT, GPT, and T5](https://medium.com/data-science-collective/comparing-bert-gpt-and-t5-when-should-you-use-each-one-f9bfcfd5454c)
- [Transformer Architectures - Hugging Face](https://huggingface.co/learn/llm-course/chapter1/6)
- [What happened to BERT & T5?](https://www.yitay.net/blog/model-architecture-blogpost-encoders-prefixlm-denoising)

**MoE Specifici:**
- [Mixture of Experts Explained - Hugging Face](https://huggingface.co/blog/moe)
- [Mixture-of-Experts (MoE) LLMs](https://cameronrwolfe.substack.com/p/moe-llms)
- [Applying MoE in LLM Architectures - NVIDIA](https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/)

**Positional Encoding:**
- [Understanding Sinusoidal Positional Encoding](https://medium.com/@pranay.janupalli/understanding-sinusoidal-positional-encoding-in-transformers-26c4c161b7cc)
- [Transformer Architecture: Positional Encoding](https://kazemnejad.com/blog/transformer_architecture_positional_encoding/)
- [Positional Encoding - IBM](https://www.ibm.com/think/topics/positional-encoding)

**Training & Backpropagation:**
- [Cross-Entropy Loss for Next Token Prediction](https://marinafuster.medium.com/cross-entropy-loss-for-next-token-prediction-83c684fa26d5)
- [Deep learning for pedestrians: backpropagation in Transformers](https://arxiv.org/abs/2512.23329) - NUOVO! (Dic 2024)
- [Mechanics of Next Token Prediction](https://research.google/pubs/mechanics-of-next-token-prediction-with-transformers/)

**Scaling Laws:**
- [LLM Scaling Laws: Analysis from AI Researchers in 2026](https://research.aimultiple.com/llm-scaling-laws/)
- [Demystify Transformers: Guide to Scaling Laws](https://medium.com/sage-ai/demystify-transformers-a-comprehensive-guide-to-scaling-laws-attention-mechanism-fine-tuning-fffb62fc2552)
- [Scaling Laws Explanation](https://www.glennklockwood.com/garden/scaling-laws)

**Decoder-Only Architecture:**
- [Decoder-Only Transformers: The Workhorse of Generative LLMs](https://cameronrwolfe.substack.com/p/decoder-only-transformers-the-workhorse)
- [Meet GPT, The Decoder-Only Transformer](https://towardsdatascience.com/meet-gpt-the-decoder-only-transformer-12f4a7918b36/)
- [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/)

### Blog e Articoli Tecnici

**Self-Attention Deep Dives:**
- [A Deep Dive into Self-Attention Mechanism](https://medium.com/analytics-vidhya/a-deep-dive-into-the-self-attention-mechanism-of-transformers-fe943c77e654)
- [Self-Attention Explained with Code](https://towardsdatascience.com/contextual-transformer-embeddings-using-self-attention-explained-with-diagrams-and-python-code-d7a9f0f4d94e/)
- [What is self-attention? - IBM](https://www.ibm.com/think/topics/self-attention)

### Documentazione Ufficiale

- [Google Research: Transformer Architecture](https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [PyTorch Transformer Tutorial](https://pytorch.org/tutorials/beginner/transformer_tutorial.html)

---

## CONCLUSIONI

### TL;DR - Cosa Abbiamo Imparato

**1. Transformer = Attention is All You Need**
- NO ricorrenza, NO convoluzione
- Solo attention mechanism
- Completamente parallelizzabile

**2. Self-Attention è il Cuore**
- Query, Key, Value vectors
- Softmax per normalizzare
- Ogni token guarda tutti gli altri

**3. Tre Varianti Principali**
- BERT (encoder) → comprensione
- GPT (decoder) → generazione ← **vincitore per LLM**
- T5 (encoder-decoder) → seq-to-seq

**4. Scaling Laws**
- Più parametri = sempre meglio (power law)
- Data e model size devono crescere insieme
- Compute budget determina optimal size

**5. MoE = Futuro**
- Sparse activation (solo alcuni expert attivi)
- Più parametri senza più compute
- Specializzazione emergente

### Perché È Importante per Noi

Come CervellaSwarm stiamo costruendo agenti AI. Capire i Transformer significa:

1. **Sapere i limiti** - Context window, scaling laws
2. **Ottimizzare prompts** - Sapere come lavora l'attention
3. **Scegliere modelli giusti** - Encoder vs Decoder vs MoE
4. **Capire il training** - Perché certi modelli sono meglio
5. **Anticipare il futuro** - MoE, multimodal, scaling

**"Nulla è complesso - solo non ancora studiato!"**

Ora i Transformer NON sono più complessi. Li abbiamo studiati. Li capiamo. 🔬

---

**Data completamento:** 10 Gennaio 2026
**Tempo ricerca:** ~45 minuti
**Fonti consultate:** 40+ tra paper, blog, tutorial
**Pagine totali:** Questa è una sintesi - i paper originali sono 1000+ pagine!

**Prossimo studio suggerito:**
- Attention variants (Flash Attention, Linear Attention)
- Multimodal transformers (CLIP, Flamingo)
- Alternative architectures (Mamba, RWKV)

*Cervella Researcher - "Studiare prima di agire, sempre!"* 🔬
