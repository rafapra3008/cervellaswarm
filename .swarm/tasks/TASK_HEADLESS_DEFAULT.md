# Task: Rendere --headless il Default

**Assegnato a:** cervella-backend
**Stato:** ready
**Priorità:** ALTA
**Data:** 2026-01-08

## Obiettivo

Modificare spawn-workers per rendere `--headless` il comportamento DEFAULT.

## Perché

"La magia ora è nascosta!" - Headless è meglio, window diventa l'eccezione.

## File da Modificare

`~/.local/bin/spawn-workers`

## Modifiche

### 1. Cambiare default (circa linea 54)

```bash
# PRIMA
HEADLESS_MODE=false

# DOPO
HEADLESS_MODE=true
```

### 2. Aggiornare show_usage()

```bash
# Cambiare le descrizioni:
echo "  --headless             Usa tmux headless (DEFAULT)"
echo "  --window               Apre finestra Terminal (vecchio comportamento)"
```

### 3. Aggiornare messaggio finale

Dove dice "Le finestre Terminal sono aperte!", cambiare in:
```bash
if [ "$HEADLESS_MODE" = true ]; then
    print_info "Worker in background (tmux headless)!"
    print_info "Usa 'tmux list-sessions' per vedere le sessioni"
else
    print_info "Le finestre Terminal sono aperte!"
fi
print_info "I worker stanno cercando task in .swarm/tasks/"
```

### 4. Aggiornare versione

```bash
# Versione: 3.1.0
# CHANGELOG:
# v3.1.0: HEADLESS DEFAULT! --headless è ora il comportamento standard. Usa --window per finestre.
```

## Output

Scrivi conferma in `TASK_HEADLESS_DEFAULT_output.md`

---

*Regina - Sessione 122 - La magia è nascosta!* 🧙
