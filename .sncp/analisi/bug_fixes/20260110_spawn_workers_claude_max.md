# Fix: spawn-workers usa account Claude Max

**Data:** 10 Gennaio 2026
**Sessione:** 146
**Versione:** spawn-workers v3.5.0

---

## Problema

Quando `ANTHROPIC_API_KEY` è settata nell'ambiente, `claude` CLI la usa automaticamente invece dell'account Claude Max.

Risultato: "Credit balance is too low" anche se l'account Claude Max ha crediti.

---

## Causa

```bash
# In ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-..."

# Quando spawn-workers lancia claude:
claude -p ...  # Usa API key invece di account Max!
```

---

## Fix

Aggiunto `unset ANTHROPIC_API_KEY` in spawn-workers prima di lanciare claude:

1. **Modalità finestra** (linea 543): Aggiunto nel runner script
2. **Modalità headless** (linea 727): Aggiunto nel comando tmux

---

## Verifica

```bash
# Prima del fix:
spawn-workers --tester
# Log: "Credit balance is too low"

# Dopo il fix:
spawn-workers --tester
# Log: Worker funziona con account Claude Max!
```

---

## Note

- L'API key rimane disponibile per altri usi (es. CLI cervella)
- Solo i worker spawnati usano l'account Claude Max
- Nessun impatto su altri script/tool
