# Dual Repo Strategy - CervellaSwarm

> **SOLUZIONE DEFINITIVA**: Sessione 304+ - Metodo Worktree!
> **v3.0 (S363):** Content scanning aggiunto - verifica pattern sensibili dentro i file.
> Problema risolto dopo 3 tentativi falliti.

---

## Il Problema

```
+================================================================+
|   ATTENZIONE: NON FARE git push public main!                   |
|                                                                |
|   origin (privato)  = 6900+ file (TUTTO)                      |
|   public (pubblico) = ~100 file (SUBSET CURATO)               |
|                                                                |
|   Un push diretto ESPORREBBE:                                  |
|   - .sncp/ (strategie, handoff, stati)                        |
|   - NORD.md (bussola privata)                                 |
|   - docs/studio/ (ricerche interne)                           |
|   - scripts/memory/ (database interno)                        |
+================================================================+
```

---

## La Soluzione Definitiva: Worktree

### Perche Worktree Funziona

1. **Isolamento totale**: Il worktree e una directory SEPARATA
2. **No conflitti**: I file del repo privato NON interferiscono
3. **Whitelist pura**: Solo i file nella lista vanno nel pubblico
4. **Verifica automatica**: Blacklist controllata prima del push

### Come Usare

```bash
# Sempre usare lo script!
./scripts/git/sync-to-public.sh

# Con messaggio custom
./scripts/git/sync-to-public.sh "Release v2.1.0"
```

### Cosa Fa lo Script

```
1. Fetch public/main
2. Crea worktree temporaneo in /tmp/
3. Copia SOLO file pubblici (whitelist)
4. Esclude node_modules e dist
5. Verifica sicurezza (blacklist)
6. Mostra diff e chiede conferma
7. Commit e push
8. Pulisce worktree
```

---

## File Pubblici (Whitelist)

```
packages/           # CLI e MCP Server (NO node_modules)
README.md
CHANGELOG.md
LICENSE
NOTICE
CONTRIBUTING.md
.github/
.gitignore
docs/AGENTS_REFERENCE.md
docs/ARCHITECTURE.md
docs/GETTING_STARTED.md
docs/SNCP_GUIDE.md
docs/SEMANTIC_SEARCH.md
docs/ARCHITECT_PATTERN.md
docs/GIT_ATTRIBUTION.md
docs/DUAL_REPO_STRATEGY.md
CODE_OF_CONDUCT.md
SECURITY.md
```

## File Privati (Blacklist)

```
.sncp/              # Memoria esterna, strategie
NORD.md             # Bussola progetto
COSTITUZIONE.md     # Principi interni
MANIFESTO.md
docs/studio/        # Ricerche interne
scripts/memory/     # Database swarm
scripts/learning/   # Apprendimento interno
scripts/engineer/   # Tool interni
reports/            # Report interni
data/               # Dati locali
PROMPT_RIPRESA*.md
MAPPA_*.md
*_PRIVATO*
*_INTERNO*
```

---

## Tentativi Falliti (per memoria)

### v1 - Checkout + Add (FALLITO)
- Problema: i file tracciati nel privato causavano conflitti durante checkout

### v1.1 - Con verifica sicurezza (FALLITO)
- Problema: pre-commit hook interferiva, git add catturava file non voluti

### v2 - Worktree (SUCCESSO!)
- Soluzione: directory completamente isolata, nessuna interferenza

---

## Errori Comuni

### SBAGLIATO

```bash
# MAI fare questo!
git push public main
git push public HEAD:main
git checkout public/main  # NO! Conflitti!
```

### CORRETTO

```bash
# Sempre usare lo script
./scripts/git/sync-to-public.sh
```

---

## Workflow Release

```
1. Sviluppo su main (origin/privato)
2. Test completi
3. Version bump (npm version patch/minor/major)
4. ./scripts/git/sync-to-public.sh "Release vX.Y.Z"
5. npm publish (se necessario)
6. git tag vX.Y.Z && git push public vX.Y.Z
```

---

*"Fatto BENE > Fatto VELOCE"*
*Sessione 304 - Cervella & Rafa*
*Soluzione definitiva dopo 3 tentativi!*
