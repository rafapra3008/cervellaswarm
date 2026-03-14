# Auto-Compact in Claude Code -- Ricerca Completa
**Data**: 2026-03-14
**Status**: COMPLETA
**Fonti**: 12 consultate (docs ufficiali Anthropic, GitHub issues, blog tecnici, source code)
**Versione Claude Code**: 2.1.75 (Marzo 2026)

---

## 1. COME FUNZIONA AUTO-COMPACT

### Trigger: a che percentuale si attiva?

Con finestra da **1M token** (Opus 4.6 / Sonnet 4.6), il compact si attiva a circa **83.5% di utilizzo**.

La formula nel codice sorgente Claude Code:
```javascript
threshold = Math.min(userOverride, effectiveWindow - 13000)
// con 1M window: Math.min(override, ~987K) => trigger a ~987K token
```

Con la finestra da **200K** (modelli non-1M), il trigger era:
- Buffer riservato: ~33K token (16.5% della finestra)
- Trigger: ~83.5% = ~167K token usati

Nota importante: con 1M context, il compact e molto meno frequente. Anthropic ha misurato un **-15% di eventi compact** dopo il passaggio a 1M.

### Il processo passo-passo

1. Claude Code rileva che i token di input superano la soglia configurata
2. Genera un summary della conversazione (il "compaction block")
3. Sostituisce tutti i messaggi precedenti al compaction block con il summary
4. La conversazione continua dal summary in poi
5. In ogni request successiva, i messaggi precedenti al compaction block vengono droppati automaticamente

### Cosa viene preservato vs cosa viene droppato

**PRESERVATO (sopravvive SEMPRE):**
- CLAUDE.md files -- vengono ricaricati fresh da disco, non fanno parte della conversazione
- Ultime azioni intraprese (file modificati, comandi eseguiti)
- Stato del task corrente e obiettivi immediati
- Struttura del progetto (se e stata discussa di recente)
- Pattern e convenzioni di codice stabiliti
- Config e setup importanti

**DROPPATO (compresso in summary lossy):**
- Path esatti dei file (diventano descrizioni generiche)
- Numeri di riga (persi completamente)
- Messaggi di errore e stack trace (summarizzati o droppati)
- Ipotesi di debugging che non hanno portato a soluzioni
- Decisioni architetturali con il loro ragionamento
- Risultati specifici dei test
- Spiegazioni dettagliate che non sono piu immediatamente rilevanti
- Sessioni di debugging risolte

**Cosa dice il system prompt di compact:**
> "Provide a detailed but concise summary of our conversation above. Focus on information that would be helpful for continuing the conversation, including what we did, what we're doing, which files we're working on, and what we're going to do next."

Questo e il prompt che Claude usa per generare il summary. Notare: focalizzato su azioni, file correnti, e next steps. NON su ragionamenti o decisioni passate.

### Il "Re-Reading Loop" (problema noto)

Dopo un compact:
1. Il contesto si libera
2. Claude deve rileggere i file perche le info specifiche (path, line numbers) sono perse
3. La rilettura consuma i token liberati
4. Si ri-avvicina alla soglia
5. Nuovo compact

Ricerche indicano che "coding agents spendono il 60% del tempo a cercare codice" -- il post-compact recovery amplifica questo problema.

---

## 2. `/compact` MANUALE vs AUTO-COMPACT

### Sono la stessa cosa?

NO, ci sono differenze:

| Aspetto | Auto-compact | `/compact` manuale |
|---------|-------------|-------------------|
| Trigger | Automatico a ~83.5% | Tu lo decidi quando |
| Hook | `PreCompact` con `trigger: "auto"` | `PreCompact` con `trigger: "manual"` |
| Timing | Spesso mid-task | Tu scegli il momento ottimale |
| Custom instructions | No (usa system prompt base) | SI -- puoi passare istruzioni |
| Interruzione | Puo interrompere un task | Controllo totale |

### `/compact` con istruzioni custom

Puoi passare istruzioni specifiche al compact:

```
/compact preserve all file paths I modified, current test failures, and the rate limiting plan
/compact focus on the API changes we made
/compact only keep the names of the websites we reviewed
/compact preserve the coding patterns we established
```

Il campo `custom_instructions` nel PreCompact hook input riceve queste istruzioni:
```json
{
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": "preserve all file paths I modified...",
  "session_id": "...",
  "cwd": "..."
}
```

### Quando usare `/compact` manualmente?

Best practice: usare a **natural breakpoints** come:
- Dopo aver completato un blocco logico di lavoro
- Prima di iniziare una nuova feature/task separata
- Quando CTX supera 70-75% ma non hai ancora bisogno di tutti i dettagli passati
- Prima di sessioni di debugging intensive (parti pulito)

NON aspettare che si attivi da solo: l'auto-compact puo interrompere mid-task.

---

## 3. HOOK EVENTS: PreCompact e PostCompact

### PreCompact -- Schema COMPLETO

```json
{
  "session_id": "string",
  "hook_event_name": "PreCompact",
  "trigger": "manual|auto",
  "custom_instructions": "string",  // solo per /compact manuale con istruzioni
  "cwd": "string",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions"
}
```

**Supported hook types:** `command` e `http` SOLO (non prompt, non agent)
**Matcher values:** `"manual"` o `"auto"`
**Puo bloccare il compact?** NO -- e solo per preparazione/backup

Output atteso:
```json
{
  "continue": true,
  "suppressOutput": true
}
```

### PostCompact -- Schema COMPLETO

```json
{
  "session_id": "string",
  "hook_event_name": "PostCompact",
  "trigger": "manual|auto",
  "compact_summary": "string",  // CHIAVE: il summary generato da Claude!
  "cwd": "string",
  "permission_mode": "string"
}
```

**NOTA CRITICA:** Il PostCompact riceve `compact_summary` -- il testo esatto del summary generato. Possiamo leggere COSA e sopravvissuto al compact!

**Supported hook types:** `command` e `http` SOLO
**Non puo bloccare:** il compact e gia avvenuto

### SessionStart con matcher "compact"

C'e anche un SessionStart event che si attiva dopo il compact:
```json
{
  "source": "compact",
  "hook_event_name": "SessionStart"
}
```
Utile per reinizializzare stato dopo il compact.

---

## 4. VARIABLE DI AMBIENTE RILEVANTE

### CLAUDE_AUTOCOMPACT_PCT_OVERRIDE

```bash
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=75  # trigger al 75% invece di 83.5%
```

**LIMITAZIONE CRITICA (bug confermato, GitHub issues #18843, #31806):**
- Puo SOLO abbassare la soglia, MAI alzarla sopra il default
- Il codice usa `Math.min(userOverride, defaultThreshold)`
- Chiuso come duplicate, fix non pianificato
- Impostare a 90 non ha NESSUN effetto

---

## 5. ANALISI DEL NOSTRO SETUP CERVELLASWARM

### Stato attuale: OTTIMO (7/10)

Abbiamo gia:
- PreCompact hook con matcher `manual` e `auto` (corretto)
- `pre_compact_save.py` -- salva snapshot JSON con git status
- `update_prompt_ripresa.py` -- checkpoint automatico nel PROMPT_RIPRESA
- context-monitor.py -- statusline CTX% in tempo reale con notifiche macOS
- Soglie 85%/92% per 1M window (corrette post-S454)

### Gap identificati

**GAP 1: PostCompact hook non configurato**
Non abbiamo un hook PostCompact. Perdiamo il `compact_summary` che Claude genera -- potremmo salvarlo per capire cosa e sopravvissuto e cosa no.

**GAP 2: context-monitor.py non e nel path corretto**
Il settings.json usa `python3 /Users/rafapra/.claude/scripts/context-monitor.py` ma il file e in `/Users/rafapra/.claude/scripts/context-monitor.py` -- OK, questo e corretto.

**GAP 3: COST_CLIFF_THRESHOLD impostato a 20%**
Il context-monitor.py mostra "2x" sopra il 20% di context. Ma con 1M window, il pricing raddoppia sopra **200K token** (20% di 1M). Questo e CORRETTO!

**GAP 4: La soglia del compact non puo essere alzata**
Con 1M context, il compact si attiva a ~830K token (83% di 1M). Questa soglia non e modificabile verso l'alto (bug CLAUDE_AUTOCOMPACT_PCT_OVERRIDE). Per noi con 1M window non e un problema pratico -- raramente arriveremo a 830K.

**GAP 5: pre_compact_save.py non legge il transcript**
Per security, il pre_compact_save non legge il contenuto della conversazione. Giusto per sicurezza, ma potremmo aggiungere un hook PostCompact che salva il `compact_summary` (solo il summary, non il transcript completo).

**GAP 6: update_prompt_ripresa.py nel PreCompact**
Il timeout e 10 secondi -- tight. Se il PROMPT_RIPRESA e lungo o il git status e lento, potrebbe scadere. Verificare se questo crea problemi.

---

## 6. BEST PRACTICES PER SOPRAVVIVERE AL COMPACT

### Regola #1: CLAUDE.md e la tua migliore amica

CLAUDE.md viene ricaricato fresh da disco ad ogni compact. E l'unica cosa che sopravvive GARANTITA. Metti tutto cio che e critico li, non nella conversazione.

Il nostro CLAUDE.md e ottimo. La nostra `~/.claude/COSTITUZIONE.md` e ottima. Usarle bene.

### Regola #2: /compact prima dei task intensivi

Prima di iniziare un debugging lungo o una feature grossa, fai `/compact` con istruzioni specifiche:
```
/compact preserve: current task goal, files already modified [lista], decisions made about architecture X
```

### Regola #3: SNCP/PROMPT_RIPRESA come memoria persistente

Gia facciamo questo bene. Il PROMPT_RIPRESA viene aggiornato automaticamente al PreCompact. Dopo un compact, leggerlo di nuovo e il modo piu veloce per recuperare stato.

### Regola #4: Struttura le info critiche PRIMA che vengano compattate

Non mettere info critiche solo nella conversazione. Scrivi su file (PROMPT_RIPRESA, NORD.md) man mano che lavori. Gia lo facciamo con checkpoint.

### Regola #5: Compact a logical boundaries, non aspettare auto

Con 1M context, l'auto-compact e raro. Ma se lavori per ore, puo comunque attivarsi. Fare `/compact` manuale alla fine di ogni "blocco logico" di lavoro e una best practice.

### Regola #6: Non combattere il compact, adattati

Auto-compact NON puo essere disabilitato. E una safety measure. La strategia migliore e avere una buona "exit strategy" per le info critiche, non cercare di evitarlo.

---

## 7. RACCOMANDAZIONI SPECIFICHE PER CERVELLASWARM

### Azione 1: Aggiungere PostCompact hook (ALTA PRIORITA)

Aggiungere a settings.json:
```json
"PostCompact": [
  {
    "matcher": "auto",
    "hooks": [
      {
        "type": "command",
        "command": "python3 /Users/rafapra/.claude/hooks/post_compact_save.py",
        "timeout": 15
      }
    ]
  }
]
```

Il `post_compact_save.py` dovrebbe salvare il `compact_summary` in un file di log. Questo ci permette di:
- Capire COSA e sopravvissuto al compact
- Avere una traccia storica dei compact
- Diagnosticare perdite di contesto

### Azione 2: Aggiungere "Compact Instructions" a CLAUDE.md (MEDIA PRIORITA)

Aggiungere una sezione in CLAUDE.md:
```markdown
## COMPACT INSTRUCTIONS
When compacting, PRESERVE:
1. Current task state and decisions made (WHAT we were doing, WHY)
2. File paths and versions being worked on (exact paths)
3. SNCP paths and PROMPT_RIPRESA location
4. Active constraints from Rafa
5. git status (uncommitted files, current branch)

SAFE TO DROP: historical data, completed audit scores, example code blocks, error messages from resolved issues
```

Nota: queste istruzioni vengono usate SOLO se usi `/compact` senza argomenti. Per /compact manuale con istruzioni specifiche, quelle sovrascrivono.

### Azione 3: Pattern "/compact intelligente" pre-task (MEDIA PRIORITA)

Prima di iniziare task intensivi (Incident Replay, Protocol Zoo):
```
/compact preserve: task = Incident Replay build, files modified = [lista],
decisions = [lista], current CTX for context re-load = read PROMPT_RIPRESA at path X
```

### Azione 4: context-monitor.py -- aggiungere indicatore pre-compact (BASSA PRIORITA)

Attualmente a 85% manda notifica. Potrebbe anche suggerire:
- A 75%: "Considera /compact prima del prossimo task"
- A 85%: notifica warning attuale
- A 92%: notifica critica attuale

### NON fare:

- NON impostare CLAUDE_AUTOCOMPACT_PCT_OVERRIDE sopra l'83% (non funziona, bug)
- NON tentare di disabilitare auto-compact (impossibile)
- NON mettere info critiche SOLO nella conversazione senza salvarle su file

---

## 8. IL COMPACT CON 1M CONTEXT: REALTA PRATICA

Con Opus 4.6 + 1M context:
- **Compact a 830K token** (83% di 1M)
- Una sessione di lavoro tipica usa 50-200K token
- Il compact e raro in sessioni normali
- Puo attivarsi in sessioni multi-ore con molto tool use

Il nostro context-monitor.py e calibrato correttamente per 1M (soglie 85/92).

Il 20% COST_CLIFF (200K token) e corretto: sopra questo il pricing API raddoppia per i token di input.

---

## APPENDICE: Hook PreCompact nel settings.json attuale

Il nostro setup attuale:
```json
"PreCompact": [
  {
    "matcher": "manual",
    "hooks": [
      { "type": "command", "command": "python3 /.../pre_compact_save.py", "timeout": 30 },
      { "type": "command", "command": "python3 /.../update_prompt_ripresa.py", "timeout": 10 }
    ]
  },
  {
    "matcher": "auto",
    "hooks": [
      { "type": "command", "command": "python3 /.../pre_compact_save.py", "timeout": 30 },
      { "type": "command", "command": "python3 /.../update_prompt_ripresa.py", "timeout": 10 }
    ]
  }
]
```

**Valutazione:** Setup corretto e completo per PreCompact. Il PostCompact manca.

---

*Report generato da Cervella Researcher - CervellaSwarm*
*Fonti: Anthropic Compaction Docs, Claude Code Hooks Reference, GitHub issues #18843/#31806/#25867, claudefa.st, morphllm.com, claudelog.com, Piebald-AI system prompts*
