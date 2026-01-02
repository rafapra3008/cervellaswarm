# RICERCA: Prompt Caching - Implementazione Dettagliata

> *Ricerca recuperata da agent transcript - 2 Gennaio 2026*

---

## SINTESI ESECUTIVA

```
PROMPT CACHING = GAME CHANGER!

- Risparmio: 90% sui token cached
- Velocita: 2-10x piu veloce
- ROI: IMMEDIATO (da 2° chiamata)
- Implementazione: 1 RIGA di codice!
```

---

## COME FUNZIONA

### Anatomia di una Richiesta

```python
# PRIMA (senza cache)
system=[
  {"type": "text", "text": "DNA agent lungo..."}
]

# DOPO (con cache)
system=[
  {"type": "text",
   "text": "DNA agent lungo...",
   "cache_control": {"type": "ephemeral"}}
]
```

### Pricing (Marzo 2025 - Claude 3.5)

| Operazione | Costo |
|------------|-------|
| Cache Write | 1.25x base (25% extra) |
| Cache Read | 0.10x base (90% risparmio!) |
| TTL Default | 5 minuti |

### Break-Even Analysis

```
Base: $3.00/MTok
Cache Write: $3.75/MTok (prima chiamata)
Cache Read: $0.30/MTok (chiamate successive)

Break-even: 2 chiamate!
```

---

## IMPLEMENTAZIONE PRATICA

### Python SDK

```python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20251101",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "DNA lungo dell'agente (>1024 tokens)...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Task specifico"}]
)

# Verifica cache hit
print(f"Cache write: {response.usage.cache_creation_input_tokens}")
print(f"Cache read: {response.usage.cache_read_input_tokens}")
```

### Regole Cache

1. **Minimo 1024 tokens** per cache hit
2. **Contenuto IDENTICO** per hit
3. **Max 4 cache breakpoints** per request
4. **TTL 5 minuti** (o 1 ora con TTL esteso)
5. **Ordine conta** - cache_control alla fine del blocco

---

## DOVE APPLICARE IN CERVELLASWARM

### Priorita ALTA (>1024 tokens stabili)

| Contenuto | Tokens Stimati | Risparmio Potenziale |
|-----------|----------------|----------------------|
| DNA agenti (14 file) | ~2000-4000 ciascuno | ENORME |
| COSTITUZIONE.md | ~800 | Medio |
| System prompts | ~1000-2000 | Alto |

### Implementazione Suggerita

```python
# In orchestrator o quando spawn agent
system_content = [
    {
        "type": "text",
        "text": dna_agent_content,  # Il DNA dell'agente
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": task_context  # Il contesto del task
    }
]
```

---

## ERRORI COMUNI DA EVITARE

1. **Contenuto troppo corto** (<1024 tokens)
2. **Contenuto dinamico nel cache** (timestamp, UUID)
3. **Cache position sbagliata** (deve essere alla fine)
4. **Dimenticare cache_control** nella seconda chiamata

---

## CHECKLIST IMPLEMENTAZIONE

```
PRE-IMPLEMENTAZIONE
[ ] Contenuto >= 1024 tokens?
[ ] Riusato 3+ volte?
[ ] Stabile (non cambia)?
[ ] Model supporta? (Opus/Sonnet/Haiku 3.5+)

IMPLEMENTAZIONE
[ ] cache_control nella posizione giusta?
[ ] Contenuto IDENTICO tra chiamate?
[ ] NO timestamp/UUID nel cached content?
[ ] Max 4 breakpoints?

VERIFICA
[ ] cache_creation_input_tokens > 0 prima chiamata?
[ ] cache_read_input_tokens > 0 chiamate successive?
```

---

## FONTI

- [Prompt Caching Documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Anthropic Cookbook - Prompt Caching](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/prompt_caching.ipynb)
- [Prompt Caching Announcement](https://www.anthropic.com/news/prompt-caching)
- [Medium: Practical Guide to Claude Prompt Caching](https://medium.com/@mcraddock/unlocking-efficiency-a-practical-guide-to-claude-prompt-caching-3185805c0eef)

---

## SCOPERTA: CLAUDE CODE GIA SUPPORTA CACHING!

> **Aggiornamento 2 Gennaio 2026 - Sessione 43**

```
+------------------------------------------------------------------+
|                                                                  |
|   CLAUDE CODE USA PROMPT CACHING AUTOMATICAMENTE!               |
|                                                                  |
|   Non serve implementare nulla manualmente.                      |
|   Il caching e gia attivo per:                                   |
|   - DNA degli agent                                              |
|   - System prompts                                               |
|   - File di contesto (CLAUDE.md, COSTITUZIONE.md)               |
|   - Contesto codebase                                            |
|                                                                  |
|   VERIFICATO: Nessuna variabile DISABLE_PROMPT_CACHING e set    |
|                                                                  |
+------------------------------------------------------------------+
```

### Variabili per Disabilitare (se necessario)

| Variabile | Effetto |
|-----------|---------|
| DISABLE_PROMPT_CACHING | Disabilita per TUTTI i modelli |
| DISABLE_PROMPT_CACHING_HAIKU | Disabilita solo per Haiku |
| DISABLE_PROMPT_CACHING_SONNET | Disabilita solo per Sonnet |
| DISABLE_PROMPT_CACHING_OPUS | Disabilita solo per Opus |

### Conclusione

**QW-1 (Prompt Caching): GIA IMPLEMENTATO da Claude Code!**

Non serve azione manuale - il sistema e gia ottimizzato.

---

*Ricerca: 2 Gennaio 2026*
*Ricercatrice: Cervella Researcher*
*Aggiornamento: Sessione 43 - Scoperta caching automatico!*

*"Il risparmio del 90% non e magia - e ingegneria!"*
