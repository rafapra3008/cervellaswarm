# HARDTESTS ANALYSIS - CervellaSwarm CLI

> **Data:** 15 Gennaio 2026
> **Analisi by:** cervella-ingegnera
> **190+ scenari identificati**

---

## PRIORITA' DA TESTARE SUBITO (CRITICI)

1. Init in directory gia' inizializzata - potrebbe sovrascrivere!
2. Status in progetto non inizializzato
3. Task con command injection (sicurezza)
4. Task con API key invalida
5. Resume senza sessioni

---

## LISTA COMPLETA (dalla cervella-ingegnera)

### 1. INIT COMMAND
- `cervellaswarm init` - Wizard completo interattivo
- `cervellaswarm init -y` - Quick init con defaults
- `cervellaswarm init -y --name test-project` - Quick init con nome custom
- `cervellaswarm init` in directory gia' inizializzata

### 2. STATUS COMMAND
- `cervellaswarm status` - In progetto inizializzato
- `cervellaswarm status` - In progetto NON inizializzato
- `cervellaswarm status -d` - Detailed status

### 3. TASK COMMAND
- Task senza descrizione
- Task con descrizione vuota
- Task con caratteri speciali
- Task con keyword routing
- Task con API key mancante/invalida
- Task con command injection attempt

### 4. RESUME COMMAND
- Resume senza sessioni
- Resume con molte sessioni
- Resume con session corrotta

### 5. EDGE CASES
- Concurrent operations
- File system race conditions
- Large scale (>1000 sessioni)

### 6. ERROR HANDLING
- API errors (401, 403, 429, 500, 503)
- File system errors
- Input validation

### 7. SECURITY
- Command injection prevention
- Path traversal prevention
- API key protection

---

*Report generato per validazione CLI prima di npm publish*
