# LEZIONE: ANTHROPIC_API_KEY Override Claude Max

> **Data:** 10 Gennaio 2026
> **Sessione:** 146
> **Categoria:** Infrastruttura

---

## Cosa E' Successo

I worker spawnati fallivano con "Credit balance is too low" anche se l'account Claude Max aveva crediti.

---

## Perche' E' Successo

`ANTHROPIC_API_KEY` era settata in `~/.zshrc`. Quando `claude` CLI viene lanciato, usa automaticamente l'API key invece dell'account Claude Max.

```bash
# In ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-..."

# Risultato: claude usa API invece di account Max!
```

---

## Cosa Abbiamo Imparato

> **"Environment variables possono causare comportamenti inaspettati"**

Il CLI di Claude ha questa priorita':
1. ANTHROPIC_API_KEY (se presente) -> Usa API
2. Account Claude Max (se loggato) -> Usa account

Se entrambi presenti, vince l'API key.

---

## Fix Applicato

spawn-workers v3.5.0: Aggiunto `unset ANTHROPIC_API_KEY` prima di lanciare claude.

```bash
# Prima del fix:
claude -p ...  # Usa API key!

# Dopo il fix:
unset ANTHROPIC_API_KEY && claude -p ...  # Usa Claude Max!
```

---

## Come Evitarlo in Futuro

1. **Isolamento ambiente:** Script che devono usare Claude Max devono pulire l'ambiente
2. **Test esplicito:** Verificare quale account viene usato prima di task lunghi
3. **Documentazione:** Specificare chiaramente quale account usa ogni tool

---

*"L'ambiente eredita tutto - a volte troppo"*
