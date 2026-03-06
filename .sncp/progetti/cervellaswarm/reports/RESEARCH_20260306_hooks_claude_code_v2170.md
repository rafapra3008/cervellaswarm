# Claude Code Hooks v2.1.49-2.1.70 - Ricerca
**Data:** 2026-03-06
**Autrice:** Cervella Researcher
**Sessione:** 431
**Status:** COMPLETA
**Fonti:** 8 consultate (docs ufficiali, changelog, GitHub issues, community guides)

---

## SINTESI ESECUTIVA

Tra v2.1.49 e v2.1.70 Claude Code ha introdotto 6 nuove tipologie hook/feature rilevanti per CervellaSwarm:
1. HTTP Hooks (v2.1.63) - alternativa network ai command hooks
2. WorktreeCreate/WorktreeRemove (v2.1.49) - automazione git worktree isolation
3. SubagentStop ampliato (v2.0.42 + v2.1.69) - agent_transcript_path, last_assistant_message, agent_id
4. InstructionsLoaded (v2.1.69) - nuovo hook CLAUDE.md loading
5. ConfigChange (v2.1.49) - monitoring config files
6. Worktree fields nella status line (v2.1.69) - name, path, branch, originalRepoDir

---

## 1. HTTP HOOKS (v2.1.63)

### Come funziona
Alternativa a `"type": "command"`: invece di eseguire uno script shell, Claude Code fa una POST HTTP al tuo endpoint con il JSON dell'evento come body.

**Schema configurazione:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "http",
        "url": "http://localhost:8080/hooks/pre-tool-use",
        "timeout": 30,
        "headers": {
          "Authorization": "Bearer $MY_TOKEN"
        },
        "allowedEnvVars": ["MY_TOKEN"]
      }]
    }]
  }
}
```

**Campi chiave:**
- `url` (obbligatorio): endpoint che riceve la POST
- `headers` (opzionale): supporta interpolazione `$VAR_NAME`
- `allowedEnvVars` (opzionale): whitelist delle env var espandibili negli headers
- `timeout` (opzionale): default 30 secondi

**Request/Response:**
- Request: POST con `Content-Type: application/json`, body = stesso JSON dei command hooks (da stdin)
- Response: stesso formato JSON output dei command hooks (2xx = success)
- Non-2xx, connection failure, timeout = errori NON-BLOCCANTI (esecuzione continua)
- Per bloccare: rispondere 2xx con `{"decision": "block"}` o `{"hookSpecificOutput": {"permissionDecision": "deny"}}`

**Supporto env var negli headers:** SI, tramite `allowedEnvVars`. Solo le variabili whitelistated vengono espanse.

### Adozione CervellaSwarm
**FUTURO** - Attualmente usiamo solo script Python locali. HTTP hooks richiedono un server in ascolto (locale o remoto). Utile se in futuro vogliamo un "swarm dashboard server" o integrazione con servizi esterni. Per ora overkill.

**Rischio:** Nessun server locale = hook fallisce silenziosamente (non blocca, ma non logga).

---

## 2. WORKTREECREATE / WORKTREEREMOVE (v2.1.49)

### Quando scattano
- `WorktreeCreate`: quando si usa `claude --worktree <nome>` o quando un agente ha `isolation: "worktree"` nel frontmatter
- `WorktreeRemove`: alla rimozione del worktree (cleanup)

### Input JSON
**WorktreeCreate:**
```json
{
  "name": "feature-login"
}
```
Il `name` e un slug identifier (specificato dall'utente o auto-generato).

**WorktreeRemove:**
```json
{
  "worktree_path": "/absolute/path/to/worktree"
}
```

### Output atteso
- `WorktreeCreate`: lo script DEVE stampare su stdout il **percorso assoluto** della directory creata. Qualsiasi altro output deve andare su `/dev/tty` per evitare errori di parsing.
- `WorktreeRemove`: nessun output di decisione - solo side effects. Fallimenti vengono loggati solo in debug mode.

### Tipo supportato
- Solo `"type": "command"` (no HTTP per WorktreeCreate)

### Uso tipico (esempio community)
WorktreeCreate: crea worktree git, copia `.env`, installa dipendenze, assegna porta deterministica via hash del branch name, stampa path.
WorktreeRemove: termina processi sulla porta dev, rimuove worktree e branch.

### Se configurate WorktreeCreate, il comportamento default di git viene SOSTITUITO
Questo e critico: configurare WorktreeCreate significa che ora sei responsabile dell'intera creazione del worktree (incluso `git worktree add`).

### BUG NOTO
Issue GitHub #29716: WorktreeCreate/Remove hooks non vengono chiamati in Claude Desktop (bug confermato). In Claude Code CLI funzionano.

### Adozione CervellaSwarm
**FUTURO** - Interessante per quando usiamo `isolation: "worktree"` negli agenti. Potremmo usarlo per:
- Setup automatico `.env` per ogni agente isolato
- Copia della configurazione `.claude/` corretta per worktree
- Port management se futura dashboard

Al momento non usiamo worktree isolation negli agenti. Da considerare quando arriveremo a D5/D6 o future feature multi-agent avanzate.

---

## 3. SUBAGENT STOP - NUOVI CAMPI (v2.0.42 + v2.1.69)

### Campi input completi aggiornati
```json
{
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "...",
  "stop_hook_active": false,
  "agent_id": "uuid-unico-del-subagente",
  "agent_type": "nome-tipo-agente",
  "agent_transcript_path": "/path/to/agent/conversation.jsonl",
  "last_assistant_message": "Testo completo dell'ultimo messaggio dell'agente"
}
```

### Campi rilevanti per noi

**`agent_transcript_path`**: path al transcript della conversazione del subagente (JSONL). Permette di leggere l'intera conversazione senza fare parsing del transcript principale. Utile per:
- Estrarre il risultato specifico dell'agente senza parsare tutto
- Logging dettagliato per agent

**`last_assistant_message`**: testo dell'ultimo messaggio. Permette di:
- Capire se l'agente ha completato con successo senza leggere il file
- Pattern matching sul risultato (es. "DONE", "ERRORE", "9.5/10")
- Decidere azioni post-agente senza aprire file

**`agent_id`**: UUID unico per run. Permette tracking preciso anche con agenti dello stesso tipo.

**`agent_type`**: nome tipo agente. Anche usato per matcher filtering! Puoi fare:
```json
"matcher": "guardiana-qualita"
```
per hook specifici per certi tipi di agente.

### Impatto sul nostro subagent_stop.py
Il nostro attuale hook ignora questi campi nuovi. Miglioramento concreto disponibile:
- Usare `last_assistant_message` per categorizzare successo/fallimento
- Usare `agent_type` per routing eventi DB (ora scriviamo sempre "subagent" come agent_name)
- Usare `agent_transcript_path` per logging avanzato

### Adozione CervellaSwarm
**SI - ALTA PRIORITA** - Upgrade di `subagent_stop.py` consigliato nella prossima sessione dedicata a infra hooks. Costo basso, beneficio alto per il DB swarm_memory.

---

## 4. INSTRUCTIONSLOADED (v2.1.69)

### Quando scatta
Quando CLAUDE.md o file `.claude/rules/*.md` vengono caricati nel contesto.

### Input JSON
```json
{
  "session_id": "...",
  "files_loaded": ["CLAUDE.md", ".claude/rules/security.md"]
}
```
(schema esatto da confermare - non documentato in dettaglio nelle fonti disponibili)

### Utilizzo possibile
- Audit: loggare quali regole vengono caricate e quando
- Enforcement: verificare che certi file critici siano sempre presenti
- Alerting: se CLAUDE.md mancante, notificare

### Adozione CervellaSwarm
**FUTURO** - Interessante ma non urgente. Potremmo usarlo per verificare che la COSTITUZIONE_OPERATIVA sia sempre disponibile, ma e informativo (non bloccante). Da valutare in una fase di hardening del sistema.

---

## 5. PRETOOLS USE - PERMISSIONDECISION

### Come funziona
Output del hook (command o HTTP) puo includere in `hookSpecificOutput`:

```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow",
    "permissionDecisionReason": "Tool verificato sicuro per questa operazione"
  }
}
```

**Valori permissionDecision:**
- `"allow"`: bypass completo del prompt di permesso, esecuzione automatica
- `"deny"`: blocca l'esecuzione, motivo mostrato a Claude
- `"ask"`: presenta il prompt all'utente (comportamento default)

**Campo aggiuntivo `updatedInput`**: puo modificare i parametri del tool prima dell'esecuzione.
**Campo `additionalContext`**: stringa iniettata nel contesto di Claude prima che il tool venga eseguito.

### Best practices per auto-allow sicuro
- Usare `"allow"` solo per tool read-only verificati (WebFetch, WebSearch, Read)
- Per Bash: auto-allow solo pattern whitelist espliciti (es. `ls`, `cat`, `grep`)
- Mai auto-allow per tool che scrivono file o eseguono codice arbitrario senza validazione
- Loggare ogni auto-allow per audit trail

### BUG v2.1.69
Fix: gli interactive tools (es. `AskUserQuestion`) venivano auto-allowed silenziosamente se listati in `allowed-tools` di uno skill, bypassando il prompt. Questo e stato fixato.

### Adozione CervellaSwarm
**FUTURO** - Non abbiamo PreToolUse hooks attivi. Se vogliamo aggiungere auto-allow per tool specifici (es. Read/Glob sempre allowed per agenti researcher), questo e il meccanismo. Da valutare con Guardiana prima di implementare.

---

## 6. STATUS LINE - WORKTREE FIELDS (v2.1.69)

### Schema JSON aggiornato
La status line (hook che fornisce info al terminale) include ora:
```json
{
  "worktree": {
    "name": "feature-login",
    "path": "/absolute/path/to/worktree",
    "branch": "feature/login",
    "originalRepoDir": "/absolute/path/to/main/repo"
  }
}
```
Il campo `worktree` e presente solo quando si e in una sessione `--worktree`. Altrimenti assente.

### Impatto su context-monitor.py
Il file `context-monitor.py` menzionato nella richiesta NON ESISTE nel nostro sistema. Non c'e nessun file da aggiornare. Se in futuro lo creiamo, dovra gestire il campo `worktree` come opzionale (presente solo in worktree sessions).

### Adozione CervellaSwarm
**FUTURO** - Rilevante solo quando useremo worktree isolation per agenti.

---

## 7. NOVITA MINORI

### /copy picker (v2.1.59)
- Comando `/copy` con picker interattivo per selezionare code block specifici o risposta completa
- Opzione "Always copy full response" per saltare il picker in futuro
- Non impatta i nostri hook ma migliora UX

### Session naming (v2.1.63)
- `/resume` picker ora mostra il prompt piu recente invece del primo
- Sessioni con titoli appaiono correttamente (prima mostravano "(session)")
- `/remote-control` e `claude remote-control` supportano argomento opzionale name per titolo custom

### Ctrl+F per kill background agents (v2.1.49)
- Due-press confirmation per killare agenti in background
- Utile durante sessioni multi-agent per gestire agenti bloccati

### ConfigChange hook (v2.1.49)
- Scatta quando i file di configurazione cambiano durante una sessione
- Pensato per enterprise security auditing
- Puo bloccare modifiche ai settings
- Non prioritario per noi ma interessante per hardening

### Startup performance (v2.1.69)
- SessionStart hook ora eseguito in deferred mode: ~500ms di riduzione al startup
- Nostro `session_start_swarm.py` beneficia automaticamente di questo miglioramento

---

## RIEPILOGO ADOZIONE

| Feature | Versione | Adozione | Priorita | Note |
|---------|----------|----------|----------|------|
| HTTP Hooks | 2.1.63 | FUTURO | Bassa | Richiede server in ascolto |
| WorktreeCreate/Remove | 2.1.49 | FUTURO | Media | Utile con isolamento agenti |
| SubagentStop nuovi campi | 2.0.42+2.1.69 | **SI** | **ALTA** | Upgrade subagent_stop.py |
| InstructionsLoaded | 2.1.69 | FUTURO | Bassa | Audit CLAUDE.md loading |
| permissionDecision | 2.1.49 | FUTURO | Media | Auto-allow tool read-only |
| Status line worktree | 2.1.69 | FUTURO | Bassa | Solo con worktree sessions |
| ConfigChange | 2.1.49 | FUTURO | Bassa | Enterprise hardening |

---

## RACCOMANDAZIONE

**Azione immediata (prossima sessione infra):**
Upgrading di `subagent_stop.py` per sfruttare `agent_type`, `agent_id`, `last_assistant_message`. Sono gia nell'input, vanno solo letti. Costo: 30 minuti. Beneficio: DB swarm_memory molto piu utile con dati reali degli agenti.

**Azione media (D5/D6 o future sessioni):**
Valutare WorktreeCreate/Remove se si adotta `isolation: "worktree"` negli agenti. Da fare DOPO aver definito il pattern di isolamento.

**Azione futura (hardening):**
permissionDecision per auto-allow tool read-only negli agenti Researcher. Richiede approvazione Guardiana Qualita prima di implementare.

**Non fare ora:**
HTTP hooks - overkill senza un server locale dedicato. Aggiunge complessita senza benefici concreti rispetto ai command hooks Python che gia abbiamo.

---

## BREAKING CHANGES

Nessun breaking change identificato tra v2.1.49-2.1.70 per il nostro sistema attuale.

**Nota:** La fix di v2.1.69 su interactive tools auto-allowed in skills non ci impatta (non usiamo `allowed-tools` in skill frontmatter per tool interattivi).

---

*Fonti: [Hooks reference](https://code.claude.com/docs/en/hooks) | [Claude Code Changelog](https://claudefa.st/blog/guide/changelog) | [DeepWiki Hooks](https://deepwiki.com/victor-software-house/claude-code-docs/7.4.5-hooks) | [claude-worktree-hooks](https://github.com/tfriedel/claude-worktree-hooks) | [GitHub Issue #29716](https://github.com/anthropics/claude-code/issues/29716)*
