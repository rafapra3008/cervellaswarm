# Task: Code Review Settimanale

**Assegnato a:** cervella-reviewer
**Stato:** ready
**Data:** 5 Gennaio 2026
**Tipo:** CODE_REVIEW_WEEKLY

---

## Obiettivo

Esegui una code review settimanale completa del progetto CervellaSwarm.

---

## Cosa Analizzare

### 1. Scripts Bash (scripts/)
- spawn-workers.sh
- swarm-lib.sh
- watcher-regina.sh
- context_check.py (ANTI-COMPACT v5.1.0)

### 2. Hooks Python (~/.claude/hooks/)
- block_task_for_agents.py
- context_check.py

### 3. Agents DNA (~/.claude/agents/)
- Verifica consistenza tra i 16 agenti
- Controlla che le regole siano chiare

### 4. Configurazione
- ~/.swarm/config
- settings.json (hooks)

---

## Focus Particolare

1. **ANTI-COMPACT v5.1.0** - È stato appena implementato, verifica:
   - Logica corretta
   - Edge cases gestiti
   - Errori potenziali

2. **block_task_for_agents.py** - Hook critico:
   - Blocca correttamente cervella-*?
   - Lascia passare Explore/general-purpose?

3. **spawn-workers v2.7.0** - Verifica:
   - AUTO-SVEGLIA funziona?
   - Anti-duplicati watcher ok?

---

## Output Richiesto

Crea il file: `reports/code_review_20260105.md`

Con:
1. **Rating complessivo** (1-10)
2. **Problemi critici** (se ci sono)
3. **Suggerimenti miglioramento**
4. **Cosa funziona bene**

---

## Criteri di Successo

- [ ] Review completata
- [ ] Report scritto in reports/
- [ ] Rating assegnato
- [ ] Problemi documentati (se ci sono)
