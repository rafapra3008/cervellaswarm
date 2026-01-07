# Task: Ricerca Storia Problema Finestre

**Assegnato a:** cervella-researcher
**Stato:** ready
**Priorità:** ALTA
**Data:** 7 Gennaio 2026

---

## Obiettivo

Trovare TUTTI i tentativi precedenti di risolvere il problema:
**"Le Cervelle non lanciano spawn-workers da sole"**

Rafa dice che abbiamo provato 3-4 volte. Devo trovare:
1. Quando abbiamo provato
2. Cosa abbiamo provato
3. Perché non ha funzionato

---

## Dove Cercare

### 1. Git History
```bash
git log --oneline --all | grep -i "spawn\|finestra\|worker\|delega\|auto"
git log --oneline --all --grep="spawn"
git log --oneline --all --grep="worker"
```

### 2. File di Documentazione
- `docs/known-issues/` - problemi noti
- `docs/roadmap/` - roadmap con tentativi
- `PROMPT_RIPRESA.md` - storia sessioni
- `.swarm/` - task precedenti

### 3. DNA Agenti
- `~/.claude/agents/cervella-orchestrator.md` - regole Regina
- `~/.claude/CLAUDE.md` - regole globali

### 4. Report e Studi
- `docs/studio/` - studi fatti
- `reports/` - report generati

---

## Output Richiesto

Crea file: `docs/studio/STUDIO_STORIA_PROBLEMA_FINESTRE.md`

Con:
1. **Timeline** - Quando abbiamo affrontato questo problema
2. **Tentativi** - Cosa abbiamo provato (con dettagli)
3. **Risultati** - Perché ogni tentativo non ha funzionato
4. **Pattern** - Cosa hanno in comune i fallimenti
5. **Insight** - Cosa possiamo imparare

---

## Criteri di Successo

- [ ] Trovati almeno 3 tentativi documentati
- [ ] Capito PERCHÉ non hanno funzionato
- [ ] Identificato pattern comune
- [ ] Proposto direzione diversa

---

*"Nulla è complesso - solo non ancora studiato!"*
