# Code Review Settimanale CervellaSwarm

**Data:** 5 Gennaio 2026
**Reviewer:** cervella-reviewer
**Versione:** 1.0.0

---

## File Analizzati

| File | Path | Righe | Versione |
|------|------|-------|----------|
| spawn-workers.sh | scripts/swarm/ | 657 | v2.2.0 |
| swarm-status.sh | .swarm/scripts/ | 374 | v1.1.0 |
| swarm-review.sh | .swarm/scripts/ | 479 | v1.1.0 |
| context_scorer.py | scripts/memory/ | 388 | v1.0.0 |

**Note:** `quick-task`, `swarm-heartbeat` e `context_check.py` non trovati nel repository.

---

## 1. spawn-workers.sh

### Punteggio: 8.5/10

### Punti di Forza

1. **Configurazione centralizzata** (v2.0.0): Usa `~/.swarm/config` per settings globali
2. **Project-aware** (v1.9.0): Trova automaticamente la root del progetto cercando `.swarm/`
3. **Health tracking** (v1.6.0): Salva PID e timestamp per monitoring worker
4. **Auto-close elegante** (v1.5.0-1.8.0): Chiude finestra Terminal automaticamente senza dialogo conferma
5. **Cleanup function**: Rimuove file PID/start quando worker termina (trap EXIT)
6. **Heartbeat support** (v2.2.0): Prompt worker include istruzioni heartbeat ogni 60s
7. **Supporto Guardiane** (Opus): 3 guardiane con prompt specializzati

### Problemi Identificati

#### SICUREZZA - MEDIA

**Riga 41-44**: Source di file config senza validazione
```bash
if [[ -f "$SWARM_CONFIG" ]]; then
    source "$SWARM_CONFIG"
fi
```
**Rischio:** Se `$SWARM_CONFIG` viene manipolato, potrebbe eseguire codice arbitrario.
**Raccomandazione:** Validare che il file sia di proprieta dell'utente e non sia world-writable.

#### SICUREZZA - BASSA

**Riga 473-477**: AppleScript con interpolazione
```bash
osascript << APPLESCRIPTEOF
tell application "Terminal"
    do script "$runner_script"
end tell
APPLESCRIPTEOF
```
**Rischio:** Se `$runner_script` contiene caratteri speciali AppleScript, potrebbe causare problemi.
**Mitigazione attuale:** Il path e controllato dallo script stesso (non input utente).

#### BEST PRACTICE

**Riga 623**: Uso di `wc -w | xargs` per contare parole
```bash
worker_count=$(echo "$workers_to_spawn" | wc -w | xargs)
```
**Raccomandazione:** Usare array bash per gestione piu pulita:
```bash
read -ra workers_array <<< "$workers_to_spawn"
worker_count=${#workers_array[@]}
```

### Codice Duplicato

- **Funzione `get_worker_prompt`** (righe 182-320): Pattern ripetitivo per ogni worker. Potrebbe essere semplificato con un template e variabili.

---

## 2. swarm-status.sh

### Punteggio: 8.0/10

### Punti di Forza

1. **Visualizzazione chiara**: Riepilogo con emoji e colori
2. **Detection task STALE**: Identifica task working > 30 min senza done
3. **Cleanup automatico**: `--cleanup` rimuove file .working stale
4. **Multi-progetto**: `--all` mostra stato di tutti i progetti

### Problemi Identificati

#### COMPATIBILITA - MEDIA

**Righe 175-177, 183-184**: Uso di `stat` con syntax macOS-specific
```bash
done_time=$(stat -f %m "$done_file" 2>/dev/null || stat -c %Y "$done_file" 2>/dev/null)
```
**Status:** Gia gestito con fallback per Linux (`-c`). OK.

#### BEST PRACTICE

**Riga 103**: Pipe complessa difficile da leggere
```bash
grep -i "assegnato a:" "$task_file" 2>/dev/null | head -1 | sed 's/.*[Aa]ssegnato a:[[:space:]]*//' | sed 's/\*//g' | tr -d '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
```
**Raccomandazione:** Usare singola regex con sed o awk per leggibilita.

#### VARIABILE NON USATA

**Riga 49**: `PROJECTS` definita ma usata solo in `--all` mode
```bash
PROJECTS=("${SWARM_PROJECTS[@]}")
```
**Status:** OK, design corretto per supporto multi-progetto.

---

## 3. swarm-review.sh

### Punteggio: 7.5/10

### Punti di Forza

1. **Workflow review chiaro**: Stati .review_ready, .approved, .rejected
2. **Mapping automatico guardiane**: Assegna guardiana corretta per tipo agente
3. **Support per task specifico**: `--task NOME` per review singolo

### Problemi Identificati

#### SICUREZZA - MEDIA

**Righe 379-389**: Escape AppleScript manuale potenzialmente incompleto
```bash
local escaped_prompt="${prompt//\\/\\\\}"
escaped_prompt="${escaped_prompt//\"/\\\"}"
escaped_prompt="${escaped_prompt//$'\n'/\\n}"
```
**Rischio:** Caratteri speciali AppleScript non gestiti (es. `$`, backticks).
**Raccomandazione:** Salvare prompt su file e passare path a claude invece di inline.

#### BEST PRACTICE

**Riga 387**: Uso di `--agent` flag che potrebbe non esistere in claude CLI
```bash
do script "cd '${project_path}' && claude --agent ${guardian} -p \"${escaped_prompt}\""
```
**Nota:** Verificare compatibilita con versione corrente Claude CLI.

#### CODICE DUPLICATO

- **Funzione `find_project_root`**: Identica in tutti e 3 gli script bash.
  **Raccomandazione:** Estrarre in `swarm-lib.sh` comune e source.

- **Funzione `get_assigned_to`**: Identica in `swarm-status.sh` e `swarm-review.sh`.
  **Raccomandazione:** Centralizzare in libreria comune.

---

## 4. context_scorer.py

### Punteggio: 9.0/10

### Punti di Forza

1. **Codice pulito e ben documentato**: Docstrings complete, type hints
2. **Design pattern solido**: Dataclass per config, classe scorer separata
3. **Test integrati**: CLI con `--test` per verifica rapida
4. **Estensibile**: Weights configurabili, facile aggiungere criteri

### Problemi Identificati

#### BEST PRACTICE - BASSA

**Riga 50**: `Optional[ScoringWeights]` con default `None` invece di factory
```python
def __init__(self, weights: ScoringWeights = None):
    self.weights = weights or ScoringWeights()
```
**Nota:** Pattern accettabile, ma `weights: ScoringWeights = None` dovrebbe usare `Optional[]` per chiarezza (gia presente nell'import).

#### OTTIMIZZAZIONE

**Righe 182-191, 193-216**: Funzioni `_parse_agents` e `_parse_tags` quasi identiche
```python
def _parse_agents(self, agents_field) -> List[str]:
def _parse_tags(self, tags_field) -> List[str]:
```
**Raccomandazione:** Unificare in singola funzione generica `_parse_list_field`.

---

## File Mancanti

I seguenti file richiesti nel task non sono stati trovati:

| File | Status |
|------|--------|
| quick-task | NON TROVATO (probabilmente alias/symlink esterno) |
| swarm-heartbeat | NON TROVATO (potrebbe essere integrato in spawn-workers v2.2.0) |
| context_check.py | NON TROVATO (potrebbe essere context_scorer.py?) |

---

## Riepilogo Problemi

| Severita | Problema | File | Azione |
|----------|----------|------|--------|
| MEDIA | Source config non validato | spawn-workers.sh:41 | Verificare ownership file |
| MEDIA | Escape AppleScript incompleto | swarm-review.sh:379 | Usare file per prompt |
| BASSA | Codice duplicato (find_project_root) | tutti .sh | Creare swarm-lib.sh |
| BASSA | Codice duplicato (get_assigned_to) | status/review.sh | Centralizzare |
| BASSA | Funzioni simili non unificate | context_scorer.py | Refactor _parse |

---

## Raccomandazioni Finali

### Priorita ALTA

1. **Creare `swarm-lib.sh`** con funzioni comuni:
   - `find_project_root()`
   - `get_assigned_to()`
   - `print_*()` functions
   - Colori e config loading

### Priorita MEDIA

2. **Validare config file** prima di source:
   ```bash
   validate_config() {
       local file="$1"
       [[ -O "$file" && ! -w "$file" ]] || [[ $(stat -f %Lp "$file") == "600" ]]
   }
   ```

3. **Usare file per prompt lunghi** in swarm-review.sh invece di escape inline

### Priorita BASSA

4. **Refactor `get_worker_prompt`** usando template + variabili
5. **Unificare `_parse_agents/_parse_tags`** in context_scorer.py

---

## Metriche Complessive

| Metrica | Valore |
|---------|--------|
| File analizzati | 4 |
| Righe totali | 1898 |
| Problemi sicurezza | 2 (media) |
| Problemi best practice | 4 (bassa) |
| Codice duplicato | 3 casi |
| Punteggio medio | 8.25/10 |

---

## Conclusione

Il codice dello sciame CervellaSwarm e **ben strutturato e funzionale**. I problemi identificati sono principalmente di manutenibilita (codice duplicato) e hardening sicurezza (validazione config). Nessun problema critico o bloccante.

**Verdetto:** APPROVED con raccomandazioni

---

*Report generato da cervella-reviewer*
*CervellaSwarm Code Review - 5 Gennaio 2026*
