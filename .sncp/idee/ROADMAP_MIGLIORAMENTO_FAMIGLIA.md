# ROADMAP MIGLIORAMENTO FAMIGLIA - CervellaSwarm

> **Data:** 10 Gennaio 2026 - Sessione 147
> **Autore:** La Regina
> **Versione:** 1.0.0

---

## TL;DR

La famiglia CervellaSwarm è ben strutturata e funzionale. HARDTEST 8/8 passato.
Configurazioni VS Code Insiders e normale sono IDENTICHE. Tutto OK.

---

## AUDIT COMPLETATO

### DNA Agenti (16 totali)

| Categoria | Agenti | Stato |
|-----------|--------|-------|
| **Regina** | cervella-orchestrator | OK |
| **Guardiane (Opus)** | guardiana-qualita, guardiana-ops, guardiana-ricerca | OK |
| **Worker (Sonnet)** | backend, frontend, tester, researcher, reviewer, docs, data, devops, security, marketing, ingegnera, scienziata | OK |

**Punti di forza:**
- Tutti hanno frontmatter YAML coerente
- Struttura DNA uniforme (Costituzione, Regole Context-Smart, Output 150 token)
- Protocolli comunicazione v1.0.0 presenti
- Regola decisione autonoma in tutti
- Tutti parlano al femminile

**Bug già fixati (Sessione 146):**
- cervella-reviewer: sezione "COME LAVORO (Read-Only)"
- spawn-workers: v3.5.0 con `unset ANTHROPIC_API_KEY`

---

### Hooks (13 file)

| Hook | Funzione | Status |
|------|----------|--------|
| pre_compact_save.py | Snapshot JSON + notifica | ATTIVO |
| context_check.py | AUTO-HANDOFF 70% | ATTIVO |
| session_start_scientist.py | Genera prompt ricerca | ATTIVO |
| post_commit_engineer.py | Engineer report post-commit | ATTIVO |
| update_prompt_ripresa.py | Aggiorna PROMPT_RIPRESA | ATTIVO |
| git_reminder.py | Reminder git su Stop | ATTIVO |
| **block_edit_non_whitelist.py** | Blocca edit Regina | **NON ATTIVO** |
| **block_task_for_agents.py** | Blocca Task per cervella-* | **NON ATTIVO** |

---

### Settings.json

| Sezione | Status | Note |
|---------|--------|------|
| Permissions | OK | Tutti tool + MCP Playwright |
| PreCompact | OK | Salva stato + anti-compact |
| SessionEnd | OK | Salva + update PROMPT |
| SessionStart | OK | Notifica + context + scientist |
| PostToolUse | OK | Task logging + engineer |
| UserPromptSubmit | OK | context_check (auto-handoff) |
| **PreToolUse** | **MANCANTE** | Hook di blocco non configurati! |
| MCP | OK | Playwright browser |
| StatusLine | OK | context-monitor.py |

---

### spawn-workers (v3.5.0)

| Feature | Status |
|---------|--------|
| Headless default (tmux) | OK |
| Claude Max (unset API_KEY) | OK |
| Auto-sveglia | OK |
| Max workers (5) | OK |
| Output realtime (stdbuf) | OK |
| Validazione progetto | OK |
| 16 worker supportati | OK |

---

## NOTA STORICA - Hook Protezione

I hook `block_edit_non_whitelist.py` e `block_task_for_agents.py` esistono ma sono **DISATTIVATI DI PROPOSITO**.

**Storia:** Erano stati attivati in passato ma hanno causato CAOS, quindi sono stati disattivati intenzionalmente.

**Status attuale:** La Regina può editare file e usare Task - questo è il comportamento VOLUTO e funziona bene.

---

## ROADMAP MIGLIORAMENTI

### FASE 1: Verifiche

- [x] Verificato: VS Code Insiders = VS Code normale (IDENTICI)
- [x] Verificato: Hook protezione disattivati DI PROPOSITO (storia passata)
- [ ] Verificare che context-monitor.py funzioni correttamente
- [ ] Testare auto-handoff su progetti reali

### FASE 2: Ottimizzazioni

- [ ] Review periodica DNA agenti (mensile)
- [ ] Migliorare differenziazione researcher/scienziata
- [ ] Aggiungere metriche qualità output agenti
- [ ] Creare template task per ogni tipo di agente

### FASE 3: Documentazione

- [ ] Creare BEST_PRACTICES.md per uso famiglia
- [ ] Documentare workflow tipo per task complessi
- [ ] Creare guida "Quando usare quale agente"
- [ ] Documentare recovery da errori comuni

### FASE 4: Monitoraggio

- [ ] Dashboard stato famiglia (chi è attivo, chi ha lavorato)
- [ ] Report automatico fine sessione
- [ ] Alert per agenti che non rispondono
- [ ] Tracking qualità output per agente

---

## BEST PRACTICES IDENTIFICATE

### Per la Regina

1. **MAI editare direttamente** - Usa spawn-workers o quick-task
2. **SEMPRE SNCP** - Scrivi pensieri/decisioni mentre lavori
3. **MAPPA prima di delegare** - Quali task? Ordine? Output dove?
4. **Una cosa alla volta** - Meglio 1 fatto bene che 5 fatti male

### Per i Worker

1. **Leggi Costituzione** - Prima di ogni task
2. **Output max 150 token** - Non sprecare context Regina
3. **Verifica post-write** - Assicurati file salvato
4. **Heartbeat ogni 60s** - La Regina deve sapere che sei vivo

### Per le Guardiane

1. **Verifica risponde al PERCHÉ** - Non solo se codice funziona
2. **Escalation se critico** - Non decidere da sola su cose importanti
3. **Report actionable** - Dire COSA fare, non solo cosa è sbagliato
4. **Spawn solo se urgente** - Max 2 spawn per sessione

---

## CONCLUSIONI

La famiglia CervellaSwarm è matura e funzionale.
Il sistema ha superato HARDTEST 8/8.
Unico problema critico: hook protezione non attivi (da discutere con Rafa).

Prossimo step: Usare la famiglia su progetti reali (Miracollo, Contabilita) e annotare friction.

---

*"Le ragazze nostre! La famiglia!"*
