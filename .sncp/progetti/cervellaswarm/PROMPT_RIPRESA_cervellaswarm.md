# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-06 - Sessione 437
> **STATUS:** P2 Refactoring completo + Fase E research. FASE D COMPLETA. PyPI v0.3.0.

---

## SESSIONE 437 - Diamante Interno + Ricerca Strategica

### Cosa e successo
P2 refactoring di 4 funzioni grandi, accuracy sweep docs, Fase E research (18 fonti).

### Cambiamenti chiave
- **Refactoring build_symbol_table()**: 116->49 righe (4 helper `_symbol_from_*`)
- **Refactoring tokenize()**: 163->78 righe (2 helper `_check_tabs`, `_tokenize_line_content`)
- **Refactoring _parse_agent()**: 107->94 righe (1 helper `_parse_message_list`)
- **Refactoring _compile_agent()**: 101->72 righe (1 helper `_emit_contract_guards`)
- **create_server() SKIPPED**: rischio alto, beneficio basso (Ingegnera raccomanda)
- **Accuracy sweep**: NORD, README, MAPPA_LINGUAGGIO, SUBROADMAP_D tutti aggiornati (2909/5221/v0.3.0)
- **Fase E research**: report completo in `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260306_FASE_E_INTENTBRIDGE.md`
- **Guardiana S437**: 9.5/10 APPROVED (1 P2 + 6 P3, tutti fixati)

### Numeri
- Suite completa: **5221 test** (9 Python pkg + 4 Node pkg), LU: 2909 in 0.97s
- Guardiana S437: **9.5/10** APPROVED
- Dependabot: **17/20** (invariato da S436)

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE D: L'Ecosistema -- 6/6 DONE = COMPLETA!
    D1-D6 DONE (media 9.5/10)
  PyPI: v0.3.0 (waiting Rafa environment approval)
  P2 Refactoring: 4/5 DONE (create_server skipped)
  Fase E Research: COMPLETA (18 fonti, report scritto)
```

---

## PROSSIMA SESSIONE

### Fase E - IntentBridge (RACCOMANDAZIONE RESEARCHER)
1. Scrivere script "La Nonna con le Ricette" (dialogo esatto parola per parola)
2. IntentBridge MVP su CLI chat: NL -> IntentDraft via B.4 -> spec -> codice
3. Multi-lingua (it/pt/en) PRIMA di voice
4. Report: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260306_FASE_E_INTENTBRIDGE.md`

### TODO Rafa
- Approvare PyPI publish environment su GitHub (Actions -> "Publish lingua-universale" -> approve "pypi")
- Attivare 2FA GitHub (SCADUTO!)
- Ruotare Bedzzle key su MyReception

### BACKLOG
- 3 Dependabot PR rimaste (SKIP tier): #19 stripe 17->20, #14 express 4->5, #11 zod 3->4
- Centralizzare conf versione (core=15, cli/mcp-server=13)
- VS Code Marketplace (publisher account)
- Refactoring P2 residuo: _lsp.create_server() 136 righe (rischio alto, rimandato)

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test totali (13 pkg) | **5221** |
| Test LU | **2909** |
| Audit Guardiana S437 | **9.5/10** |
| PyPI | **v0.3.0** (waiting approval) |
| Dependabot mergiate | **17/20** |

---

## Lezioni Apprese (S437)

### Cosa ha funzionato bene
- **Ingegnera analisi prima di refactoring** -- priorita, rischio, helpers suggeriti = zero sorprese
- **Pattern two-stage (Req2LTL)** -- la ricerca conferma che il nostro B.4 e esattamente il pattern giusto
- **Skip create_server()** -- rischio alto/beneficio basso, decisione CEO giusta

### Cosa non ha funzionato
- **Crash Python SIGSEGV** -- non nostro (CPython 3.13 bug), ma va monitorato

### Pattern candidato
- **"Skip se rischio > beneficio"** -- Evidenza: S437 (create_server rischio ALTO, 5 CC bassa)

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
