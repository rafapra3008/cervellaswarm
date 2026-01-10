# Setup Multi-Account Claude Code

> **Data:** 10 Gennaio 2026 - Sessione 147
> **Scopo:** Documentare come installare CervellaSwarm su account Claude diversi

---

## Problema

Claude Code usa `~/.claude/` come cartella config globale.
Se cambi account, influenza TUTTE le istanze (VS Code, VS Code Insiders, CLI).

## Soluzione

Usare `CLAUDE_CONFIG_DIR` per avere configurazioni separate.

---

## Procedura Completa

### 1. Creare Struttura Nuova Config

```bash
mkdir -p ~/.claude-NOME/{agents,hooks,scripts,docs,cache,data}
```

### 2. Copiare File Essenziali

**Documentazione:**
```bash
cp ~/.claude/CLAUDE.md ~/.claude-NOME/
cp ~/.claude/COSTITUZIONE.md ~/.claude-NOME/
cp ~/.claude/CHECKLIST_AZIONE.md ~/.claude-NOME/
cp ~/.claude/MANUALE_DIAMANTE.md ~/.claude-NOME/
```

**Settings:**
```bash
cp ~/.claude/settings.json ~/.claude-NOME/
cp ~/.claude/settings.local.json ~/.claude-NOME/
```

**Agenti (DNA Famiglia):**
```bash
cp -r ~/.claude/agents/* ~/.claude-NOME/agents/
```

**Hooks e Scripts:**
```bash
cp -r ~/.claude/hooks/* ~/.claude-NOME/hooks/
cp -r ~/.claude/scripts/* ~/.claude-NOME/scripts/
cp -r ~/.claude/docs/* ~/.claude-NOME/docs/
```

### 3. Login con Nuovo Account

```bash
CLAUDE_CONFIG_DIR=~/.claude-NOME claude logout
CLAUDE_CONFIG_DIR=~/.claude-NOME claude login
```

### 4. Setup Alias (Opzionale)

In `~/.zshrc`:
```bash
alias claude-main="CLAUDE_CONFIG_DIR=~/.claude claude"
alias claude-insiders="CLAUDE_CONFIG_DIR=~/.claude-insiders claude"
```

### 5. Per VS Code / VS Code Insiders

L'estensione Claude deve sapere quale config usare.
Opzioni:
- Settare `CLAUDE_CONFIG_DIR` nel profilo VS Code
- Usare settings.json del workspace

---

## File Copiati (Sessione 147)

| Categoria | File/Cartella | Quantità |
|-----------|---------------|----------|
| Docs | CLAUDE.md, COSTITUZIONE.md, CHECKLIST, MANUALE | 4 |
| Settings | settings.json, settings.local.json | 2 |
| Agents | ~/.claude-insiders/agents/ | 16 |
| Hooks | ~/.claude-insiders/hooks/ | 14 |
| Scripts | ~/.claude-insiders/scripts/ | 13 |
| Docs extra | ~/.claude-insiders/docs/ | 1 |

---

## Note per Prodotto Futuro

Questo processo è il **prototipo di onboarding** per CervellaSwarm:

1. **Setup automatico** - Script che copia tutto
2. **Verifica** - Check che tutti i file siano presenti
3. **Login guidato** - Wizard per autenticazione
4. **Test** - Verifica che hooks funzionino

### Possibile comando futuro:
```bash
cervella setup --config-dir ~/.claude-NOME
```

---

## Troubleshooting

### CRITICO: "Credit balance is too low" con subscription attiva

**Sintomo:** Hai usage disponibile sulla subscription ma Claude dice "Credit balance is too low"

**Causa:** C'è una `ANTHROPIC_API_KEY` settata nell'ambiente che forza Claude a usare l'API invece della subscription.

**Diagnosi:**
```bash
env | grep ANTHROPIC
```

Se vedi `ANTHROPIC_API_KEY=sk-ant-...` questo è il problema!

**Soluzione:**
1. Trova dove è definita:
```bash
grep -l "ANTHROPIC_API_KEY" ~/.zshrc ~/.bashrc ~/.zprofile 2>/dev/null
```

2. Commenta o rimuovi la riga nel file trovato:
```bash
# export ANTHROPIC_API_KEY="sk-ant-..."  # commentata per usare subscription
```

3. Apri un nuovo terminale (o `unset ANTHROPIC_API_KEY`)

4. Rilancia Claude

**Nota per prodotto:** Questo sarà un check automatico nel setup wizard!

---

### Hooks non funzionano
I path negli hooks sono hardcoded a `~/.claude/`.
Bisogna sostituirli con path relativi o dinamici.

**Esempio problema in settings.json:**
```json
"command": "python3 /Users/rafapra/.claude/hooks/pre_compact_save.py"
```

**Soluzione:** Usare `$CLAUDE_CONFIG_DIR` o path relativo.

### VS Code non usa il config giusto
Verificare che l'estensione Claude rispetti `CLAUDE_CONFIG_DIR`.
Potrebbe servire settarlo nelle env del profilo VS Code.

### `code-insiders` comando non trovato

**Sintomo:** Alias come `swarm-insiders="code-insiders ~/path"` non funziona

**Causa:** VS Code Insiders ha il comando `code` (non `code-insiders`) nella sua cartella bin

**Diagnosi:**
```bash
which code-insiders  # Non trovato
ls -la "/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/"
# Mostra: code, code-tunnel-insiders (NON code-insiders!)
```

**Soluzione:** Usare path completo negli alias:
```bash
alias swarm-insiders='"/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/code" ~/Developer/CervellaSwarm'
```

**Lezione:** Quando un comando non funziona:
1. `which nome-comando` - verifica se esiste nel PATH
2. `ls -la /path/al/bin/` - guarda come si chiama l'eseguibile reale

---

*Documentato durante Sessione 147 - primo test multi-account*
*Aggiornato Sessione 147b - fix alias code-insiders*
