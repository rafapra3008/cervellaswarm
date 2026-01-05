# Task: RICERCA AUTO-SVEGLIA REGINA

**Assegnato a:** cervella-researcher
**Stato:** ready
**Priorita:** ALTISSIMA - Questa e' la MAGIA SOPRA MAGIA!

---

## Il Problema

Quando la Regina (Claude Code) spawna un worker e resta in attesa:
- Il worker lavora nella sua finestra
- Il worker finisce e manda notifica macOS
- MA la Regina NON riceve nulla!
- La Regina resta FERMA finche' l'umano non scrive qualcosa

**VOGLIAMO:** La Regina viene "svegliata" automaticamente quando un worker finisce!

## Obiettivo della Ricerca

Studiare TUTTE le possibili soluzioni tecniche per far si' che:
1. Worker finisce il suo lavoro
2. Qualcosa "sveglia" la Regina automaticamente
3. La Regina legge l'output e continua
4. SENZA intervento umano!

## Aree da Investigare

### 1. Hook di Claude Code
- Esistono hook che possono INIETTARE messaggi nella conversazione?
- `UserPromptSubmit` puo' essere triggerato programmaticamente?
- Ci sono hook non documentati?

### 2. MCP Servers
- Un MCP server puo' PUSHARE messaggi a Claude?
- O Claude deve sempre CHIEDERE al MCP?
- Esistono pattern di "callback" in MCP?

### 3. File Watcher + Automazione
- Se il worker scrive un file "done", possiamo triggerare qualcosa?
- AppleScript puo' simulare input nella finestra Claude?
- Automator/Shortcuts possono aiutare?

### 4. stdin/stdout Injection
- Claude Code legge da stdin?
- Possiamo iniettare testo nel processo Claude?
- Named pipes o altri meccanismi IPC?

### 5. WebSocket/HTTP
- Claude Code ha un server interno?
- Esiste un'API locale per comunicare?

### 6. Workaround Creativi
- Due istanze Claude che si parlano?
- Un "watcher" esterno che simula l'utente?
- Qualsiasi altra idea!

## Output Atteso

Crea il file `TASK_RICERCA_AUTO_SVEGLIA_REGINA_output.md` con:

1. **Analisi Tecnica** - Come funziona Claude Code internamente
2. **Soluzioni Possibili** - Lista con pro/contro di ciascuna
3. **Soluzione Raccomandata** - La piu' fattibile
4. **Piano di Implementazione** - Come realizzarla
5. **Limitazioni** - Cosa NON si puo' fare

## Risorse da Consultare

- `~/.claude/settings.json` - Configurazione Claude
- `~/.claude/hooks/` - Hook esistenti
- Documentazione Claude Code online
- GitHub issues/discussions di Claude Code
- Pattern usati da altri tool simili

## Criteri di Successo

- [ ] Almeno 3 possibili soluzioni identificate
- [ ] Pro/contro di ciascuna
- [ ] Una raccomandazione chiara
- [ ] Fattibilita' valutata (facile/medio/difficile)

---

*RICERCA CRITICA - CervellaSwarm Sessione 95*
*Questa e' la MAGIA SOPRA MAGIA!*
