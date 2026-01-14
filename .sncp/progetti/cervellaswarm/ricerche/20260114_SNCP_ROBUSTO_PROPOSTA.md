# SNCP ROBUSTO + MAPPA INIZIALE PROGETTO

> **Data:** 14 Gennaio 2026
> **Autore:** Guardiana Ricerca
> **Missione:** Definire SNCP robusto e wizard per nuovi progetti
> **Quality Score:** 8.5/10

---

## EXECUTIVE SUMMARY

```
+================================================================+
|                                                                |
|   SNCP OGGI: Funziona MA e' fragile                            |
|   PROBLEMA #1: Troppa complessita, poca disciplina             |
|   PROBLEMA #2: Nuovi progetti = copia manuale (error-prone)    |
|   PROBLEMA #3: Memoria non sincronizzata con codice            |
|                                                                |
|   SOLUZIONE: Semplificare + Automatizzare + Verificare         |
|                                                                |
+================================================================+
```

---

## 1. STATO ATTUALE SNCP - ANALISI

### Cosa Funziona Bene

| Aspetto | Score | Note |
|---------|-------|------|
| Struttura progetti separati | 8/10 | `.sncp/progetti/{nome}/` chiaro |
| Script manutenzione | 8/10 | health-check, compact, etc. |
| stato.md per tracking | 7/10 | Usato, ma non sempre aggiornato |
| Separazione decisioni/idee | 8/10 | Logica buona |

### Cosa E' Confuso o Ridondante

| Problema | Evidenza | Impatto |
|----------|----------|---------|
| **Troppi file archivio** | 100+ file in `.sncp/archivio/` | Context overload |
| **Naming inconsistente** | `IDEA_20260108_xxx` vs `20260112_xxx` | Difficile trovare file |
| **Sottocartelle profonde** | `moduli/whatif/frontend/` | Navigazione complessa |
| **Duplicazione** | Stesso contenuto in posti diversi | Confusione su fonte di verita |
| **mappa_viva.md obsoleta** | Ultimo update 8 Gennaio | Info stale |

### Cosa Manca

| Gap | Descrizione | Priorita |
|-----|-------------|----------|
| **Wizard nuovo progetto** | Setup manuale = errori | ALTA |
| **Verifica coerenza** | Docs vs codice desync | ALTA |
| **Template standard** | Ogni progetto parte da zero | MEDIA |
| **Checklist chiusura task** | Nessun enforcement | MEDIA |

---

## 2. CONFRONTO CON ALTRI SISTEMI

### Cursor AI (2025-2026)

**Come gestisce contesto:**
- `.cursor/rules/*.mdc` - Regole modulari per progetto
- Memories - Ricorda fatti dalle conversazioni
- Project-level context - Persistente per repo

**Onboarding:**
- Analisi automatica codebase
- Generazione rules iniziali
- "Quartet": MCPs + Rules + Memories + Auto run

**Punti di forza:**
- Rules granulari (per file, per pattern)
- Memory cross-sessione
- Team rules condivise

**Fonti:** [Cursor AI Complete Guide 2025](https://medium.com/@hilalkara.dev/cursor-ai-complete-guide-2025-real-experiences-pro-tips-mcps-rules-context-engineering-6de1a776a8af), [Cursor Changelog 2026](https://blog.promptlayer.com/cursor-changelog-whats-coming-next-in-2026/)

### Claude Code (2025)

**Come gestisce contesto:**
- `CLAUDE.md` in project root
- `.claude/commands/` per workflow
- `/init` per generazione automatica

**Onboarding:**
- `/init` analizza codebase
- Genera CLAUDE.md con stack, comandi, convenzioni
- Progressive disclosure (info on-demand)

**Best Practices:**
- WHAT (tech stack), WHY (purpose), HOW (workflow)
- Conciso (<150 istruzioni)
- Usa linter, non Claude, per formatting

**Punti di forza:**
- Semplicita (un file principale)
- /init automatico
- Hooks per automazioni

**Fonti:** [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices), [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [Using CLAUDE.MD files](https://claude.com/blog/using-claude-md-files)

### Altri Sistemi Memory

**Pieces:**
- OS-level context capture
- Local-first (privacy)
- Resurface snippets quando servono

**Augment Code:**
- Context Engine semantic analysis
- 400k+ file repositories
- Workspace indexing completo

**Problema Universale:**
> "Code agents lose track of which files they're currently editing"

**Fonti:** [Best AI Memory Systems](https://pieces.app/blog/best-ai-memory-systems), [Context-Aware Memory Systems 2025](https://www.tribe.ai/applied-ai/beyond-the-bubble-how-context-aware-memory-systems-are-changing-the-game-in-2025)

---

## 3. SNCP IDEALE - PROPOSTA SEMPLIFICATA

### Principi Guida

```
1. MENO FILE = MEGLIO
   Un file aggiornato > 10 file obsoleti

2. CONVENZIONI RIGIDE
   Se tutti seguono le stesse regole, funziona

3. VERIFICA AUTOMATICA
   Script che controllano coerenza

4. PROGRESSIVE DISCLOSURE
   Info base sempre visibile, dettagli on-demand
```

### Struttura Semplificata (v2.0)

```
.sncp/
|
+-- CONFIG.md                  # Configurazione progetto (NEW!)
|
+-- progetti/
|   +-- {progetto}/
|       +-- stato.md           # UNICA fonte di verita
|       +-- decisioni/         # Solo decisioni IMPORTANTI
|       |   +-- YYYYMMDD_cosa.md
|       +-- roadmaps/          # Piani attivi
|       |   +-- NOME_ROADMAP.md
|       +-- handoff/           # File per sessioni parallele
|           +-- YYYYMMDD_sessione/
|
+-- archivio/                  # Auto-archiviato (>30 giorni)
    +-- YYYY-MM/
```

### Cosa ELIMINO

```
RIMUOVO (o archivio):
- idee/ → merge in stato.md o decisioni/
- reports/ → merge in stato.md
- workflow/ → merge in CONFIG.md
- moduli/ → troppo granulare
- coscienza/ → non usato
- perne/ → non usato
```

### Nuovo CONFIG.md (Ispirato a CLAUDE.md)

```markdown
# CONFIG.md - {Progetto}

## QUICK FACTS
- **Stack**: [tech usate]
- **Repo**: [path]
- **Deploy**: [dove e come]

## CONVENZIONI
- [regole codice]
- [naming]
- [git workflow]

## COMANDI UTILI
- `[comando]`: [cosa fa]

## STRUTTURA CHIAVE
- `path/`: [cosa contiene]

## COSA NON FARE
- [antipattern 1]
- [antipattern 2]
```

---

## 4. WIZARD NUOVO PROGETTO

### Flusso Proposto

```
1. TRIGGER
   $ sncp-init {nome-progetto}

2. ANALISI
   - Legge package.json, requirements.txt, etc.
   - Identifica stack
   - Trova convenzioni esistenti

3. GENERAZIONE
   - Crea .sncp/progetti/{nome}/
   - Genera stato.md template
   - Genera CONFIG.md base
   - Crea decisioni/ e roadmaps/

4. REVIEW
   - Mostra cosa ha creato
   - Chiede conferma/modifiche

5. COMMIT
   - Salva struttura
   - Istruzioni prossimi step
```

### Script sncp-init.sh

```bash
#!/bin/bash
# sncp-init.sh - Wizard nuovo progetto

PROGETTO=$1
BASE=".sncp/progetti/$PROGETTO"

echo "=== SNCP Init: $PROGETTO ==="

# Crea struttura
mkdir -p "$BASE/decisioni"
mkdir -p "$BASE/roadmaps"
mkdir -p "$BASE/handoff"

# Genera stato.md
cat > "$BASE/stato.md" << EOF
# Stato $PROGETTO
> Ultimo aggiornamento: $(date +%Y-%m-%d)
> Score: [X/10]

## TL;DR
[Cosa fa questo progetto in 2 righe]

## STACK
- Backend: [?]
- Frontend: [?]
- Database: [?]

## STATO ATTUALE
[Cosa funziona OGGI]

## PROSSIMI STEP
1. [ ] [step 1]
2. [ ] [step 2]

## DECISIONI CHIAVE
| Data | Decisione | Link |
|------|-----------|------|
EOF

# Genera CONFIG.md
cat > "$BASE/CONFIG.md" << EOF
# CONFIG - $PROGETTO

## Quick Facts
- **Stack**: [da compilare]
- **Repo**: $(pwd)
- **Deploy**: [da compilare]

## Convenzioni
- [da compilare]

## Comandi Utili
- \`npm run dev\`: [?]
- \`npm test\`: [?]
EOF

echo "Creato: $BASE/"
echo "- stato.md"
echo "- CONFIG.md"
echo "- decisioni/"
echo "- roadmaps/"
echo "- handoff/"
echo ""
echo "PROSSIMO: Compila stato.md e CONFIG.md!"
```

---

## 5. VERIFICA COERENZA (Il Problema Memoria)

### Il Problema (gia documentato)

```
Cervella A fa lavoro → NON aggiorna docs
Cervella B legge docs → Pensa sia TODO
TEMPO PERSO!
```

### Soluzione: verify-sync.sh

```bash
#!/bin/bash
# verify-sync.sh - Verifica coerenza docs/codice

echo "=== SNCP Sync Verifier ==="

# Check 1: Files modificati recentemente non documentati
echo "Checking recent changes..."
git log --oneline -10 --name-only | grep -E "\.(py|js|sql)$" > /tmp/recent_changes.txt

# Check 2: Confronta con stato.md
echo "Comparing with stato.md..."
# [logica confronto]

# Check 3: Migrations vs documentate
echo "Checking migrations..."
ls backend/migrations/*.sql 2>/dev/null | while read f; do
    basename "$f"
done > /tmp/real_migrations.txt

grep -o "migration.*\.sql" .sncp/progetti/*/stato.md > /tmp/doc_migrations.txt

# Output discrepanze
echo ""
echo "=== DISCREPANZE ==="
diff /tmp/real_migrations.txt /tmp/doc_migrations.txt || echo "Nessuna discrepanza"
```

### Checklist Chiusura Task (Enforcement)

```markdown
## CHECKLIST TASK COMPLETO

Prima di dire "FATTO":

- [ ] Codice scritto
- [ ] Test passano (o spiegato perche skip)
- [ ] Commit fatto con messaggio chiaro
- [ ] stato.md AGGIORNATO con:
  - [ ] Cosa e' stato fatto
  - [ ] File creati/modificati
  - [ ] Prossimi step aggiornati
- [ ] PROMPT_RIPRESA aggiornato (se fine sessione)

SE MANCA QUALCOSA → Task e' IN_PROGRESS, non DONE!
```

---

## 6. PRIORITA' IMPLEMENTAZIONE

### FASE 1 - Immediato (oggi)

| # | Task | Effort | Impatto |
|---|------|--------|---------|
| 1 | Creare `sncp-init.sh` | 30 min | ALTO |
| 2 | Aggiungere CHECKLIST_TASK a SWARM_RULES | 15 min | ALTO |
| 3 | Aggiornare stato.md Miracollo (sync) | 30 min | ALTO |

### FASE 2 - Questa Settimana

| # | Task | Effort | Impatto |
|---|------|--------|---------|
| 4 | Creare `verify-sync.sh` | 2h | MEDIO |
| 5 | Semplificare struttura (archivio vecchi) | 1h | MEDIO |
| 6 | Creare template CONFIG.md | 30 min | MEDIO |

### FASE 3 - Prossimo Sprint

| # | Task | Effort | Impatto |
|---|------|--------|---------|
| 7 | Hook pre-commit (check docs) | 2h | ALTO |
| 8 | Dashboard stato progetti | 4h | MEDIO |
| 9 | Auto-archive script | 2h | BASSO |

---

## 7. CONFRONTO FINALE

| Aspetto | SNCP Attuale | SNCP Proposto | Cursor | Claude Code |
|---------|--------------|---------------|--------|-------------|
| Setup nuovo progetto | Manuale | Wizard | Auto-rules | /init |
| Complessita struttura | ALTA | BASSA | MEDIA | BASSA |
| Verifica coerenza | NO | SI (script) | Memory | NO |
| Convenzioni | Deboli | Rigide | Strong | Moderate |
| Manutenzione | Manuale | Semi-auto | Auto | Manuale |

---

## 8. CONCLUSIONE

### Il Cuore del Problema

```
SNCP funziona SE viene USATO con DISCIPLINA.
La disciplina manca perche:
1. Troppa complessita → si salta
2. Nessun enforcement → si dimentica
3. Nessuna verifica → si desincronizza
```

### La Soluzione

```
1. SEMPLIFICARE - Meno cartelle, meno file
2. AUTOMATIZZARE - Wizard, script, hook
3. VERIFICARE - Check coerenza automatici
4. ENFORCEMENT - Checklist bloccanti
```

### Il Vantaggio Competitivo

> **"Uno sciame che RICORDA e' uno sciame che SCALA."**

Se CervellaSwarm risolve il problema della memoria persistente:
- Differenziatore vs Cursor, Copilot, altri
- Value proposition chiara per utenti
- Fondamento per "institutional knowledge"

---

## FONTI

- [Cursor AI Complete Guide 2025](https://medium.com/@hilalkara.dev/cursor-ai-complete-guide-2025-real-experiences-pro-tips-mcps-rules-context-engineering-6de1a776a8af)
- [Cursor Changelog 2026](https://blog.promptlayer.com/cursor-changelog-whats-coming-next-in-2026/)
- [Cursor AI Review 2026](https://prismic.io/blog/cursor-ai)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Using CLAUDE.MD files](https://claude.com/blog/using-claude-md-files)
- [Best AI Memory Systems](https://pieces.app/blog/best-ai-memory-systems)
- [Context-Aware Memory Systems 2025](https://www.tribe.ai/applied-ai/beyond-the-bubble-how-context-aware-memory-systems-are-changing-the-game-in-2025)
- [8 Best AI Coding Assistants 2025](https://www.augmentcode.com/tools/8-top-ai-coding-assistants-and-their-best-use-cases)

---

*"Fatto BENE > Fatto VELOCE"*
*"La memoria e' il fondamento dell'intelligenza collettiva."*

