# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 10 Gennaio 2026 - Sessione 147
> **Versione:** v67.0.0 - AUDIT COMPLETO + ROADMAP FAMIGLIA

---

## TL;DR per Prossima Cervella

**Dove siamo:** AUDIT COMPLETO della famiglia! Review 16 DNA, hooks, settings.json, spawn-workers. Tutto OK, configurazioni identiche tra VS Code Insiders e normale.

**Decisione:** PARCHEGGIATO prodotto commerciale. Focus miglioramento famiglia.

**Prossimo step:** Usare famiglia su Miracollo, annotare friction, migliorare.

---

## Sessione 147 - AUDIT COMPLETO FAMIGLIA (10 Gennaio 2026)

### Cosa Fatto
1. Review DNA tutti 16 agenti
2. Analisi hooks (13 file)
3. Analisi settings.json
4. Verifica spawn-workers v3.5.0
5. Creata ROADMAP_MIGLIORAMENTO_FAMIGLIA.md
6. Creata BEST_PRACTICES_FAMIGLIA.md

### Nota su Hook Protezione

I hook `block_edit_non_whitelist.py` e `block_task_for_agents.py` esistono ma sono **DISATTIVATI DI PROPOSITO**.

**Storia:** Erano stati attivati in passato ma hanno causato CAOS, quindi sono stati disattivati intenzionalmente.

**Status attuale:** La Regina può editare file e usare Task - questo è il comportamento VOLUTO.

### Nuovi File
- `.sncp/idee/ROADMAP_MIGLIORAMENTO_FAMIGLIA.md`
- `.sncp/idee/BEST_PRACTICES_FAMIGLIA.md`

### Prossimi Step (Sessione 148)
1. Discutere con Rafa: attivare hook protezione?
2. Se sì, modificare settings.json
3. Usare famiglia su Miracollo
4. Annotare friction, migliorare

---

## Stato Attuale

| Cosa | Stato | Note |
|------|-------|------|
| Ricerca Competitor | DONE | Cursor, Copilot, Windsurf analizzati |
| Decisioni Business | DONE | CLI + BYOK + Tier flat |
| Landing + Marketing | PAUSA | Riprende post-launch |
| Plugin (vecchio) | DEPRECATO | Sostituito da CLI |
| **CLI `cervella`** | **v0.1.0 READY** | 16 agenti, test OK |
| **Pricing Strategy** | **DEFINITO** | $0/$20/$40/$60+ tier flat |
| **BYOK vs Bundled** | **DECISO: BYOK** | Per MVP, zero rischio |
| **Tier System** | **IMPLEMENTATO** | Free/Pro/Team/Enterprise |

---

## Sessione 146 - HARDTEST COMPLETATO (10 Gennaio 2026)

### HARDTEST Risultati: 8/8 PASS
| Test | Risultato |
|------|-----------|
| 1. Spawn Base | ✅ 14 worker disponibili |
| 2. Spawn Headless | ✅ tmux funziona |
| 3. Output Real-Time | ✅ stdbuf unbuffered |
| 4. Researcher Verify | ✅ File scritto e verificato |
| 5. Guardiana Review | ✅ Score 9/10, APPROVE |
| 6. Multi-Worker | ✅ 3 worker paralleli |
| 7. Notifiche macOS | ✅ terminal-notifier |
| 8. Auto-Sveglia | ✅ Watcher attivo |

### Bug Fixati
| Bug | Fix |
|-----|-----|
| DNA Reviewer con Bash refs ma no tool | Sezione "COME LAVORO (Read-Only)" |
| spawn-workers usa API invece di Claude Max | v3.5.0 con `unset ANTHROPIC_API_KEY` |

### Nuovi File
- `.swarm/REPORT_HARDTEST_20260110.md`
- `.sncp/analisi/bug_fixes/20260110_reviewer_bash_error.md`
- `.sncp/analisi/bug_fixes/20260110_spawn_workers_claude_max.md`

### Prossimi Step (Sessione 147)
1. **Ricerche approfondite** su ambiente CervellaSwarm
2. **Code Review di tutti i 🐝** - ogni DNA agente
3. **Analisi hooks e .json** - verificare configurazione
4. **Creare roadmap dedicata** per miglioramento famiglia
5. **Poi** usare famiglia su Miracollo

### Roadmap Miglioramento Famiglia (DA CREARE)
- [ ] Review DNA tutti 16 agenti
- [ ] Analisi hooks (`~/.claude/hooks/`)
- [ ] Analisi settings.json
- [ ] Verifica spawn-workers scripts
- [ ] Test edge cases
- [ ] Documentare best practices

---

## Sessione 145 - AUDIT FAMIGLIA (10 Gennaio 2026)

### Decisione Strategica
- **PARCHEGGIATO prodotto commerciale** - Prima migliorare la famiglia
- Focus su: test, studi, analisi, log, sessione per sessione
- Obiettivo: 1000000% soddisfatti prima di lanciare

### Audit Completati
1. **Audit Sessioni** (cervella-researcher)
   - 180+ log analizzati
   - 9/16 agenti usati attivamente (56%)
   - Score sistema: 10/10 in sessioni passate
   - Report: `.sncp/analisi/audit_sessioni_famiglia.md`

2. **Audit Agenti** (cervella-ingegnera)
   - Score medio: 7.2/10
   - 3 problemi critici identificati
   - Report: `.sncp/analisi/audit_agenti_famiglia.md`

### Bug Fixati
| Bug | Fix |
|-----|-----|
| Researcher non salva file | Aggiunta regola verifica post-write |
| Overlap Researcher/Scienziata | Documentazione chiara |
| Overlap Guardiana/Reviewer | Workflow sequenziale |

### Nuova Documentazione
| File | Scopo |
|------|-------|
| `docs/guides/GUIDA_RESEARCHER_VS_SCIENZIATA.md` | Quando usare chi |
| `docs/guides/WORKFLOW_GUARDIANA_REVIEWER.md` | Workflow review |
| `docs/protocolli/PROTOCOLLI_BASE.md` | Protocolli condivisi |
| `tests/HARDTEST_FAMIGLIA.md` | Suite test completa |

### Scoperte
- **Ingegnera ESISTE** - audit aveva sbagliato
- **Reviewer senza Write BY DESIGN** - legge, non scrive
- **stdbuf GIA IMPLEMENTATO** - spawn-workers v3.2.0

### Prossimi Step
1. Eseguire HARDTEST famiglia (30-45 min)
2. Usare famiglia su Miracollo
3. Annotare friction, migliorare
4. Ripetere ogni sessione

---

## Sessione 144 - Cosa Fatto

### 1. Decisione BYOK
- **DECISO: BYOK per MVP**
- Zero rischio finanziario, già funzionante
- Pivot a Bundled possibile post-PMF
- Documentato in `.sncp/memoria/decisioni/20260109_BYOK_vs_bundled_da_decidere.md`

### 2. Tier System Implementato
Nuovi file creati:
- `cervella/tier/__init__.py`
- `cervella/tier/tier_manager.py`
- `cervella/cli/commands/upgrade.py`

Modifiche:
- `cervella/cli/commands/status.py` - Mostra tier + usage
- `cervella/cli/commands/task.py` - Check tier prima di eseguire
- `cervella/cli/__init__.py` - Registrato comando upgrade

### 3. Tier Disponibili

| Tier | Agenti | Task/mese | Prezzo |
|------|--------|-----------|--------|
| Free | 3 base | 50 | $0 |
| Pro | 16 tutti | Illimitati | $20 |
| Team | 16 tutti | Illimitati | $40 |
| Enterprise | 16+ | Illimitati | $60+ |

### 4. Nuovi Comandi CLI
```bash
cervella status              # Mostra tier + usage + agenti
cervella upgrade             # Confronto tier
cervella upgrade --set pro   # Dev mode: imposta tier
```

### 5. Persistenza
- Tier e usage salvati in `.sncp/tier.yaml`
- Reset automatico usage ogni mese

---

## Sessione 143 - Cosa Fatto (Precedente)

### 1. Code Review Day (Venerdì)
- cervella-reviewer ha analizzato tutto il CLI
- Score: 7.5/10 → migliorato con fix

### 2. Fix Security (2 CRITICAL)
- `api/client.py`: API key ora privata (`__api_key`) + validazione formato
- `cli/commands/checkpoint.py`: Distingue errori git soft/hard

### 3. Fix Quality (4 WARNING)
- Input validation con sanitize + length check
- Modelli configurabili via env vars
- Rollback automatico se init fallisce
- Context manager per API client lifecycle

### 4. Famiglia Completa (16 Agenti)
Aggiunti 8 agenti mancanti:
- **Worker (Sonnet):** data, devops, security, marketing, ingegnera
- **Supervisori (Opus):** guardiana-ops, guardiana-qualita, guardiana-ricerca

### 5. Setup Ambiente
- `cervella` aggiunto al PATH (`~/.zshrc`)
- API key Anthropic configurata
- Test con API reale: FUNZIONA!

### 6. Ricerca Pricing Modulare
- cervella-scienziata ha fatto analisi completa
- Risultato: **NO-GO per a la carte**, tutti i competitor usano tier flat
- Report: `.sncp/idee/RICERCA_PRICING_MODULARE.md`

---

## CLI - Stato Tecnico

### Struttura
```
cervella/
├── pyproject.toml          # Package config
├── README.md               # Documentazione
├── cli/
│   ├── __init__.py
│   ├── __main__.py
│   └── commands/
│       ├── init.py         # cervella init
│       ├── task.py         # cervella task (con sanitize!)
│       ├── status.py       # cervella status
│       └── checkpoint.py   # cervella checkpoint
├── api/
│   └── client.py           # Claude API wrapper (BYOK, secure)
├── sncp/
│   └── manager.py          # Memoria esterna (con rollback!)
├── agents/
│   └── loader.py           # 16 agenti built-in
└── tests/
    ├── test_basic.py
    └── test_structure.py   # 7/7 PASS
```

### Comandi
```bash
cervella --version          # v0.1.0
cervella init               # Crea .sncp/
cervella status             # 16 agenti pronti
cervella status --verbose   # Dettagli agenti
cervella task "..."         # Regina decide agente
cervella task "..." --agent backend  # Specifica agente
cervella task "..." --dry-run        # Preview
cervella checkpoint -m "..."         # Salva stato
cervella checkpoint --git -m "..."   # + git commit
```

### 16 Agenti

**Worker (Sonnet - 12):**
| Agente | Specializzazione |
|--------|------------------|
| backend | Python, FastAPI, DB |
| frontend | React, CSS, UI |
| tester | Testing, QA |
| researcher | Ricerca tecnica |
| scienziata | Ricerca strategica |
| docs | Documentazione |
| reviewer | Code review |
| data | SQL, Analytics |
| devops | Deploy, Docker |
| security | Audit, OWASP |
| marketing | UX Strategy |
| ingegnera | Analisi codebase |

**Supervisori (Opus - 4):**
| Agente | Ruolo |
|--------|-------|
| regina | Orchestratrice principale |
| guardiana-ops | Supervisione operazioni |
| guardiana-qualita | Verifica qualità |
| guardiana-ricerca | Verifica ricerche |

---

## Pricing Strategy (DEFINITO)

### Struttura Tier Flat

| Tier | Prezzo | Agenti | Task | Target |
|------|--------|--------|------|--------|
| Free | $0 | 3 base | 50/mese | Hobby, trial |
| Pro | $20/mese | 16 tutti | Unlimited | Individual dev |
| Team | $40/user | 16 tutti | Unlimited | Team |
| Enterprise | $60+ | 16 + custom | Unlimited | Enterprise |

### Perché Tier Flat
- Tutti i competitor lo usano (Cursor, Copilot, Windsurf)
- -15-20% conversion con a la carte
- Complessità tecnica proibitiva per modulare
- Report completo: `.sncp/idee/RICERCA_PRICING_MODULARE.md`

---

## Decisione Aperta: BYOK vs Bundled

**DA DECIDERE PRIMA DEL LAUNCH**

| Opzione | Pro | Contro |
|---------|-----|--------|
| **BYOK** | Zero costi API, già funziona | Friction onboarding, utente paga 2x |
| **Bundled** | UX semplice, come competitor | Rischio margine, serve capitale |
| **Hybrid** | Flessibilità | Complessità |

**Raccomandazione preliminare:** BYOK per MVP, Bundled post-PMF

**Dettagli:** `.sncp/memoria/decisioni/20260109_BYOK_vs_bundled_da_decidere.md`

---

## Cosa Manca per Launch

### Alta Priorità
| # | Task | Effort | Dipendenze |
|---|------|--------|------------|
| 1 | Decidere BYOK vs Bundled | 1 giorno | - |
| 2 | Implementare tier limits nel CLI | 2-3 giorni | Decisione #1 |
| 3 | User interviews (10-20) | 1-2 sett | - |
| 4 | Billing system (Stripe) | 1 sett | Decisione #1 |
| 5 | Update landing page con pricing | 2-3 giorni | #4 |

### Media Priorità
| # | Task | Effort |
|---|------|--------|
| 6 | Aumentare test coverage (80%+) | 1 sett |
| 7 | PyPI publish | 1 giorno |
| 8 | Documentazione utente | 2-3 giorni |

### Bassa Priorità (Post-Launch)
| # | Task |
|---|------|
| 9 | Web dashboard |
| 10 | Team Packs (add-on opzionale) |
| 11 | Enterprise features (SSO, self-hosted) |

---

## Configurazione Ambiente Rafa

```bash
# ~/.zshrc contiene:
export ANTHROPIC_API_KEY="sk-ant-..."
export PATH="$HOME/Library/Python/3.13/bin:$PATH"

# Per usare:
cd ~/Developer/CervellaSwarm
cervella status
```

---

## Puntatori Importanti

| Cosa | Dove |
|------|------|
| CLI source | `cervella/` |
| README CLI | `cervella/README.md` |
| Code Review Report | `.sncp/reports/CODE_REVIEW_CLI_2026_01_09.md` |
| Ricerca Pricing | `.sncp/idee/RICERCA_PRICING_MODULARE.md` |
| Decisione BYOK | `.sncp/memoria/decisioni/20260109_BYOK_vs_bundled_da_decidere.md` |
| Idea Pricing Modulare | `.sncp/idee/IDEA_PRICING_MODULAR_AGENTS.md` |
| Mappa App Vera | `.sncp/idee/MAPPA_APP_VERA.md` |
| NORD | `NORD.md` |

---

## Git Status

- Branch: main
- Commit pending: Sessione 143 completa
- Da pushare dopo commit

---

## Decisioni Sessione 143

| Cosa | Decisione | Perché |
|------|-----------|--------|
| API key privata | `__api_key` + validazione | Security |
| Modelli config | Via env vars | Future-proofing |
| 16 agenti | Famiglia completa | Copertura task |
| Pricing | Tier flat $0/$20/$40/$60+ | Market standard |
| Modulare | NO-GO | -15-20% conversion |
| BYOK vs Bundled | DA DECIDERE | Business model |

---

## Per la Prossima Sessione

1. **Leggi** questo file + decisione BYOK
2. **Decidi** BYOK vs Bundled con Rafa
3. **Implementa** tier limits nel CLI
4. **Pianifica** user interviews

---

## Filosofia

> "Lavoriamo in PACE! Senza CASINO!"
> "Fatto BENE > Fatto VELOCE"
> "La MAGIA ora è nascosta! Con coscienza!"
> "Ultrapassar os próprios limites!"

---

*Sessione 143: CLI Production Ready + Pricing Definito*
*Con il cuore pieno!*

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

## AUTO-CHECKPOINT: 2026-01-10 11:28 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 8ec0979 - Sessione 147b: Fix alias VS Code Insiders
- **File modificati** (5):
  - swarm/tasks/TASK_TEST_FAQ_v124.done
  - .swarm/tasks/TASK_TEST_FAQ_v124.md
  - .swarm/tasks/TASK_TEST_FAQ_v124.ready
  - .swarm/tasks/TASK_TEST_FAQ_v124_output.md
  - .swarm/tasks/TASK_TEST_HEADLESS.done

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
