# Output: TASK_HEADLESS_DEFAULT

**Worker:** cervella-backend
**Data:** 2026-01-08
**Stato:** COMPLETATO

## Modifiche Effettuate

### 1. Versione aggiornata a 3.1.0

```bash
# Versione: 3.1.0
# CHANGELOG:
# v3.1.0: HEADLESS DEFAULT! --headless è ora il comportamento standard. Usa --window per finestre.
```

### 2. Default HEADLESS_MODE cambiato a true (linea 58)

```bash
# PRIMA
HEADLESS_MODE=false

# DOPO
HEADLESS_MODE=true
```

### 3. show_usage() aggiornata (linea 724-725)

```bash
# PRIMA
echo "  --headless             Usa tmux headless (no finestre Terminal)"
echo "  --window               Usa Terminal.app (default)"

# DOPO
echo "  --headless             Usa tmux headless (DEFAULT)"
echo "  --window               Apre finestra Terminal (vecchio comportamento)"
```

### 4. Messaggio finale dinamico (linea 911-916)

```bash
if [ "$HEADLESS_MODE" = true ]; then
    print_info "Worker in background (tmux headless)!"
    print_info "Usa 'tmux list-sessions' per vedere le sessioni"
else
    print_info "Le finestre Terminal sono aperte!"
fi
print_info "I worker stanno cercando task in .swarm/tasks/"
```

## Come Usare

```bash
# Ora headless è il DEFAULT!
spawn-workers --backend              # -> tmux headless

# Per aprire finestra Terminal (vecchio comportamento)
spawn-workers --window --backend     # -> finestra Terminal
```

## Verifica

File modificato: `~/.local/bin/spawn-workers`

---

*La magia ora è nascosta!* 🧙
