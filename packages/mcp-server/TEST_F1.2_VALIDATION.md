# F1.2 API Key Validation - Test Manual

## Obiettivo
Verificare che la validazione formato API key avvenga PRIMA della chiamata Anthropic.

## Test Cases

### Test 1: API Key Mancante
```bash
# Rimuovere temporaneamente API key
unset ANTHROPIC_API_KEY
# Chiamare spawn_worker -> dovrebbe fallire con "MISSING_API_KEY"
# Messaggio atteso: "Run: cervellaswarm init or set ANTHROPIC_API_KEY"
```

### Test 2: API Key Formato Sbagliato (prefisso)
```bash
# Impostare key con prefisso sbagliato
export ANTHROPIC_API_KEY="wrongprefix-api-key-123"
# Chiamare spawn_worker -> dovrebbe fallire con "INVALID_API_KEY_FORMAT"
# Messaggio atteso: "API key must start with 'sk-ant-'"
```

### Test 3: API Key Troppo Corta
```bash
# Impostare key troppo corta
export ANTHROPIC_API_KEY="sk-ant-short"
# Chiamare spawn_worker -> dovrebbe fallire con "INVALID_API_KEY_FORMAT"
# Messaggio atteso: "API key seems too short"
```

### Test 4: API Key Formato Valido
```bash
# Impostare key valida (esempio fake ma formato corretto)
export ANTHROPIC_API_KEY="sk-ant-api03-abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
# Chiamare spawn_worker -> dovrebbe procedere alla chiamata API
# (fallirà per key invalida, ma solo DOPO validazione formato)
```

## Acceptance Criteria

✅ Errore PRIMA di ogni chiamata API
✅ Messaggio chiaro con codice errore (MISSING_API_KEY, INVALID_API_KEY_FORMAT)
✅ Suggestion con azione concreta (cervellaswarm init, console.anthropic.com)
✅ Nessuna chiamata Anthropic se formato non valido

## File Modificati

1. `src/config/manager.ts` - Aggiunta `validateApiKeyFormat()`
2. `src/index.ts` - Usa validazione formato in `spawn_worker` tool
3. `src/agents/spawner.ts` - Usa validazione formato in `spawnWorker()`

## Build Verification

```bash
npm run build  # ✅ Compilato senza errori
```
