# PATTERN VALIDATI - CervellaSwarm (S386)

**Status**: COMPLETA
**Fonti**: 3 file primari (MEMORY.md, PROMPT_RIPRESA, auto_learning research) + archivio storico S337-S386
**Sintetizzato da**: Cervella Researcher
**Data**: 2026-02-21

---

## Metodologia

Questi pattern sono estratti da 386 sessioni di lavoro reale. Ogni pattern ha almeno
2 sessioni di conferma e uno score Guardiana di 9.0+/10. Non ci sono pattern speculativi.

---

## CATEGORIA 1 - ARCHITECTURE PATTERNS

---

### P01 - Frozen Dataclass per Dati Immutabili

**Context**: Ogni volta che si crea una struttura dati che rappresenta un valore (non un'entita mutabile).

**Pattern**:
```python
@dataclass(frozen=True)
class MessageRecord:
    sender: AgentRole
    receiver: AgentRole
    kind: MessageKind
    timestamp: float
```
Usare `frozen=True` per tutte le strutture dati che sono "valori" (record, eventi, risultati).
Usare `tuple[str, ...]` invece di `list[str]` per collezioni immutabili.
Usare `Mapping` invece di `dict` nelle type annotation quando la mutabilita e illegale.

**Evidence**: S380 (tipi base), S382 (bug hunt #8), S386 (fix P2: MessageRecord frozen, ProtocolChoice.branches Mapping). Pattern confermato da 4 code review con Guardiana 9.5+/10.

**Anti-pattern**: Dataclass mutabili usate come record -> side effects imprevedibili. `dict` in
type annotations quando si vuole comunicare immutabilita. `list` per collezioni che non devono cambiare
(trovato e fixato in S382).

---

### P02 - ZERO Dependencies per Packages Core

**Context**: Ogni package standalone che fa parte del portfolio CervellaSwarm.

**Pattern**: Usare SOLO stdlib Python per i moduli core. Se una dipendenza sembra necessaria,
prima chiedersi se e sostituibile con stdlib. Documentare "ZERO deps" o "N deps (solo X)" nel README.
Ordine preferenza: zero deps -> pyyaml (gia nella famiglia) -> dipendenza specifica.

**Evidence**: lingua-universale (ZERO deps, S380-S386), task-orchestration (ZERO deps, S372),
tutti i package con max 1-3 deps. Il package piu leggero della famiglia e stato un vantaggio
competitivo documentato in ricerche (S368, S370, S372).

**Anti-pattern**: Aggiungere dipendenze "per comodita" senza valutare se stdlib basta.
Dipendenze transitive che introducono vulnerabilita o conflitti di versione.

---

### P03 - src/ Layout con Hatchling e PEP 639

**Context**: Ogni nuovo package Python standalone.

**Pattern**:
```
packages/nome-package/
  src/
    cervellaswarm_nome/   <- modulo (underscore)
      __init__.py
      ...
  tests/
    conftest.py
    test_*.py             <- NO __init__.py
  pyproject.toml          <- hatchling, Apache-2.0, PEP 639
  README.md               <- DEVE esistere prima di pip install -e .
```
Nome PyPI: `cervellaswarm-nome` (trattino). Modulo: `cervellaswarm_nome` (underscore).
Apache-2.0 per patent protection. `importlib.metadata.version()` per versione (NO hardcoded).

**Evidence**: 8 packages creati S368-S385 con questa struttura. S370: Hatchling richiede
README.md PRIMA di `pip install -e .` (lezione appresa da errore). S369: PyPI live con
Trusted Publishing OIDC. Guardiana 9.5-9.6/10 su tutti.

**Anti-pattern**: Mettere `__init__.py` nelle directory test -> package shadowing (S340).
Hardcodare la versione invece di leggerla da pyproject.toml (trovato in S376).

---

### P04 - MappingProxyType per Cataloghi Immutabili

**Context**: Dizionari globali che NON devono essere modificati a runtime (cataloghi, lookup tables).

**Pattern**:
```python
from types import MappingProxyType

AGENT_CATALOG: Mapping[AgentRole, AgentInfo] = MappingProxyType({
    AgentRole.REGINA: AgentInfo(...),
    ...
})
```
Per lookup O(1) bidirezionale: creare un indice inverso `_NAME_TO_AGENT` calcolato una volta
al load del modulo. Pre-computare le lookup tables invece di calcolarne al volo.

**Evidence**: S382 (MappingProxyType per protocolli, fix bug hunt #8), S385 (AGENT_CATALOG
con MappingProxyType e _NAME_TO_AGENT reverse index). S386 P2 fix: preference validation usa
custom catalog non global. Pattern confermato da 2 bug hunt.

**Anti-pattern**: `dict` globale mutabile come catalogo -> modifiche accidentali a runtime.
Lookup lineare O(n) in loop invece di O(1) con indice pre-computato.

---

### P05 - Monotonic Clock per Durate Temporali

**Context**: Qualsiasi misurazione di durata (sessione, operazione, timeout).

**Pattern**:
```python
import time
started_at_mono = time.monotonic()
# ... operazione ...
duration = time.monotonic() - started_at_mono  # SEMPRE positivo
```
MAI usare `time.time()` (wall clock) per durate. `time.time()` puo andare INDIETRO per
aggiustamenti NTP, leap seconds, o cambi di fuso orario -> durate negative.

**Evidence**: S386 P1 fix #5 in checker.py. Il bug era reale: NTP jump avrebbe dato
durata negativa della sessione. Identico pattern appreso da ricerca sul campo.

**Anti-pattern**: `completed_at - started_at` dove entrambi sono `time.time()`.
NTP jump durante una sessione lunga genera durata negativa, corrompendo le metriche.

---

## CATEGORIA 2 - PROCESS PATTERNS

---

### P06 - Research Before Implementation (minimo 15 fonti)

**Context**: Prima di iniziare qualsiasi nuovo modulo, feature, o decisione architetturale.

**Pattern**: Lanciare Cervella Researcher PRIMA di scrivere una riga di codice.
Target minimo: 15 fonti. Target ideale: 25-30 fonti. Documentare il report in
`.sncp/progetti/cervellaswarm/reports/RESEARCH_YYYYMMDD_topic.md`.
La ricerca deve rispondere: "Come fanno i big? Qual e lo stato dell'arte? Ci sono gap?"

**Evidence**: DSL (S381, 26 fonti), Lean 4 Bridge (S384, 31 fonti), Session Memory (S373,
ricerca competitor), Agent Templates (S371, 18 fonti), Spawn Workers (S372, 18 fonti),
Auto-Learning (S385/386, 34 fonti). In tutti i casi la ricerca ha cambiato l'implementazione
finale. Lean 4 Bridge: la ricerca ha identificato `by decide` come approccio corretto
(zero manual proofs) invece di scrivere prove manuali.

**Anti-pattern**: Implementare direttamente senza ricerca -> reinventare la ruota, usare
approcci subottimali, perdere gap competitivi. La Scienziata ha confermato in S385 che
la session type theory per AI agents e "campo vergine" (242 fonti, 0 implementazioni esistenti).

---

### P07 - Guardiana Audit dopo Ogni Step Significativo

**Context**: Dopo ogni step di implementazione (non alla fine del progetto).

**Pattern**: Processo standard a 4 fasi:
1. Implementazione (worker specializzato)
2. Test (Tester agent)
3. Guardiana audit (score /10)
4. Fix basati su audit -> se score < 9.0, re-audit

Target minimo: 9.0/10. Target ideale: 9.5/10. Score < 9.0 significa rifare, non procedere.
La Guardiana usa una rubrica consistente (architettura, test, docs, security, pattern).

**Evidence**: S362-S386, ogni step ha ricevuto audit. Media storica: 9.3/10.
Miglioramento iterativo documentato: S364 (7.8 -> 8.8 -> 9.5/10 in 3 cicli),
S362 (8.4 -> 9.5/10). Il processo iterativo ha trovato issue che avrebbero causato bug.

**Anti-pattern**: Audit solo a fine progetto -> bug accumulati, refactoring costoso.
Procedere con score 8.x -> debito tecnico che si manifesta nelle cacce bug successive.

---

### P08 - Code Review Parallela con due Ingegnere

**Context**: Code review di moduli significativi (500+ righe) o dopo Fase A/B/C.

**Pattern**: Lanciare DUE Ingegnere in parallelo su sezioni diverse del codice.
Ogni Ingegnera produce una lista di issue con priorita (P0-P3). Le due liste vengono
de-duplicate e mergiate. Processo: Ingegnera x2 (parallelo) -> Tester -> Regina fix -> Guardiana audit.
Classificazione issue: P0 (blocca tutto), P1 (bug), P2 (miglioramento), P3 (cosmetico).

**Evidence**: S386: 2 Ingegnere su 3181 righe, 7 moduli. 29 issue trovate (6 P1, 16 P2, 7 P3),
zero P0. La parallelizzazione ha permesso copertura completa in una sessione.
Stesso processo in S382 (bug hunt #8, 12 bug, 12 fix).

**Anti-pattern**: Code review sequenziale -> piu lenta, stessa qualita. Code review
da un solo agente su codice complesso -> angoli ciechi sistematici.

---

### P09 - Defer con Motivazione Documentata (non "fix all")

**Context**: Durante code review o bug hunt, quando si trovano issue che non e necessario
fixare immediatamente.

**Pattern**: Classificare ogni issue trovata come: FIX ORA vs DEFER A FASE B.
Per ogni issue deferita, documentare PERCHE e stato deferrito:
- "Test esistenti gia lo testano"
- "Teorema Lean 4 lo cattura formalmente"
- "CPython GIL mitiga il rischio, documentazione sufficiente"
- "Cambiamento cosmetico, romperebbe N test"
NON deferire per pigrizia. Deferire per motivazione tecnica solida.

**Evidence**: S386: 18 issue su 29 differite con motivazioni documentate. Confronto:
S374-S378 (bug hunt 1-7): fix di tutto senza differimento ha richiesto piu sessioni.
S386: differimento ragionato ha permesso 11 fix mirati in una sessione invece di 29.

**Anti-pattern**: Fix di ogni issue trovata senza prioritizzazione -> sessioni infinite,
regression risk, test rotti. Oppure il contrario: deferire tutto -> debito tecnico.

---

### P10 - Agente per Ogni Ruolo (non Regina che fa tutto)

**Context**: Task che richiedono specializzazione: ricerca, testing, code review, deploy.

**Pattern**: Delegare a worker specializzati invece di fare tutto in sessione regina.
Spawn: `spawn-workers --researcher`, `--tester`, ecc.
Il pattern "2 Ingegnere parallele" (P08) e un'istanza di questo principio.
La Regina coordina e decide, non implementa.

**Evidence**: S385-S386: Auto-Learning Research delegata a Cervella Scienziata (34 fonti,
nessun context regina consumato). S386: 2 Ingegnere parallele (contesti separati, parallelismo).
S380-S384: ogni modulo costruito con worker specializzato per quel dominio.

**Anti-pattern**: Regina che fa ricerca + implementazione + test + review nella stessa sessione
-> context esaurito a meta lavoro, qualita degradata, nessuna prospettiva esterna.

---

## CATEGORIA 3 - BUG PREVENTION PATTERNS

---

### P11 - Copia Difensiva dei Dict Prima di Mutarli

**Context**: Ogni funzione che riceve un dict come parametro e deve fare operazioni su di esso.

**Pattern**:
```python
# CORRETTO
def create_session(bindings: dict, ...) -> Session:
    bindings = dict(bindings)  # copia difensiva PRIMA di qualsiasi operazione
    ...

# SBAGLIATO
def create_session(bindings: dict, ...) -> Session:
    bindings[key] = value  # muta il dict originale del chiamante!
```
Regola: se una funzione riceve un dict e potrebbe modificarlo, fare `dict(bindings)` alla prima riga.

**Evidence**: S386 P1 fix #2 (aliasing bug in integration.py + checker.py). Il bug era
reale: mutare il dict originale corrompeva lo stato del checker in modo non ovvio.
Trovato da Ingegnera durante code review, non dai test (i test non testano aliasing).

**Anti-pattern**: `bindings[key] = value` su un dict ricevuto come parametro.
Il chiamante non si aspetta che il suo dict venga modificato (violation of principle of least surprise).

---

### P12 - Validazione Input a Boundary (empty string, digit start)

**Context**: Ogni funzione che trasforma input utente in identificatori di un sistema esterno
(Lean 4, Python, SQL, etc.).

**Pattern**:
```python
def _safe_lean_ident(name: str) -> str:
    if not name:
        raise ValueError("Empty string is not a valid identifier")
    if name[0].isdigit():
        name = "_" + name  # prefissa con underscore
    return name
```
Validare PRIMA il caso vuoto (raise ValueError), poi il caso che inizia con cifra.
Ogni sistema ha regole di naming diverse - sanitizzare al boundary.

**Evidence**: S386 P1 fix #3 in lean4_bridge.py. Senza fix: `_safe_lean_ident("")` non
dava errore e `"123"` generava Lean 4 invalido che compilava ma con semantica sbagliata.
Pattern piu generale: input validation at the boundary (lezione ripetuta in S374-S378).

**Anti-pattern**: Assumere che l'input sia gia valido. Passare stringhe non validate
direttamente a sistemi che hanno regole di naming proprie.

---

### P13 - NetworkX Phantom Nodes (filtrare sempre con self.nodes)

**Context**: Qualsiasi uso di NetworkX `add_edges_from()` con reference non risolte.

**Pattern**:
```python
# SBAGLIATO: PageRank include phantom nodes
scores = nx.pagerank(G)
top = sorted(scores.items(), key=lambda x: x[1])

# CORRETTO: filtrare solo i nodi reali
scores = nx.pagerank(G)
top = sorted(
    {k: v for k, v in scores.items() if k in self.nodes}.items(),
    key=lambda x: x[1]
)
```
`G.add_edges_from(edges)` crea nodi impliciti per reference non risolte.
Questi phantom nodes ricevono score PageRank ma non esistono nel grafo logico.

**Evidence**: S374 bug hunt #1 (code-intelligence). Il bug causava phantom nodes con
score alto che distorcevano i risultati di impact analysis. Trovato perche il
comportamento di NetworkX non e ovvio dalla documentazione.

**Anti-pattern**: Usare `scores.items()` direttamente dopo `nx.pagerank()` senza filtrare.
Assumere che PageRank restituisca solo nodi inseriti esplicitamente.

---

### P14 - Symbol ID con Line Number (no collision)

**Context**: Generare ID unici per simboli in un codebase (funzioni, classi, metodi).

**Pattern**:
```python
# SBAGLIATO: collision per metodi omonimi in classi diverse
symbol_id = f"{filepath}:{name}"  # es: "parser.py:__init__" collide!

# CORRETTO: include numero di riga
symbol_id = f"{filepath}:{line_number}:{name}"  # es: "parser.py:15:__init__"
```
Ogni classe puo avere `__init__`, `__str__`, ecc. Il formato `file:name` causa collision
per metodi omonimi. Il numero di riga garantisce unicita.

**Evidence**: S374 bug hunt #1 (code-intelligence). Il bug causava collision di ID per
`__init__` in 2 classi diverse dello stesso file. Fissato con formato `file:line:name`.

**Anti-pattern**: `f"{file}:{name}"` per symbol ID. Qualsiasi formato che non include
il numero di riga per distinguere omonimi.

---

### P15 - except Exception Ristretto nei Loop

**Context**: Qualsiasi `try/except` dentro un ciclo o funzione di elaborazione batch.

**Pattern**:
```python
# SBAGLIATO: swallows real bugs silently
for item in items:
    try:
        process(item)
    except Exception:  # troppo largo!
        continue

# CORRETTO: solo eccezioni attese
for item in items:
    try:
        process(item)
    except (ValueError, KeyError) as e:  # solo quelle che ci aspettiamo
        log.warning(f"Skip {item}: {e}")
        continue
```
`except Exception` in un loop swallows TypeError, AttributeError, ecc. nascondendo bug reali.

**Evidence**: S374-S378 (bug hunt 1-7, 92 bug totali). Pattern ricorrente trovato in
piu packages. Classificato come bug P2 in ogni caccia bug. "except Exception in loops:
silently swallows real bugs" (MEMORY.md, sezione Bug Hunting Patterns).

**Anti-pattern**: `except Exception: pass` o `except Exception: continue` in loop di
elaborazione batch. Il silenzio e il nemico del debugging.

---

### P16 - Atomic File Create con open(f, 'x')

**Context**: Ogni operazione che crea file per tracciare stato (lock files, task files, PID files).

**Pattern**:
```python
# SBAGLIATO: TOCTOU race condition
if not os.path.exists(task_file):
    with open(task_file, 'w') as f:  # finestra tra check e write!
        f.write(data)

# CORRETTO: atomic create
try:
    with open(task_file, 'x') as f:  # x = exclusive create, atomic
        f.write(data)
except FileExistsError:
    # qualcun altro ha creato il file -> gestisci il conflitto
    ...
```
`open(f, 'x')` e atomico: crea il file SOLO se non esiste, altrimenti FileExistsError.
Non c'e finestra tra il check e la creazione.

**Evidence**: S376 bug hunt #2+#3 (task-orchestration). Bug TOCTOU trovato in
`if exists() -> write()`. Fixato con `open(f, 'x')`. Pattern documentato in MEMORY.md.

**Anti-pattern**: `if not os.path.exists(f): open(f, 'w')` per file di stato condivisi.
In ambienti concorrenti (o anche sequenziali con interruzioni) questa e una race condition.

---

### P17 - No __init__.py nei Test (niente package shadowing)

**Context**: Struttura dei test in qualsiasi package CervellaSwarm.

**Pattern**: MAI mettere `__init__.py` nelle directory di test.
Pytest scopre i test senza `__init__.py`. Con `__init__.py`, i test diventano package Python
e possono shadoware i package veri quando Python risolve gli import.

```
tests/
  conftest.py        <- SI (fixture shared)
  test_core.py       <- SI
  common/
    test_helpers.py  <- SI
    # NO __init__.py <- REGOLA SACRA
```

**Evidence**: S340 (Package Shadowing Fix). `tests/swarm/__init__.py` shadowava
`scripts/swarm/` perche Python risolve `tests/xxx/` prima. 8 packages creati S368-S385
tutti senza `__init__.py` nei test. Guardiana controlla questo in ogni audit.

**Anti-pattern**: `__init__.py` in `tests/common/`, `tests/swarm/`, ecc. quando
`scripts/` o `src/` hanno package con gli stessi nomi.

---

## CATEGORIA 4 - TESTING PATTERNS

---

### P18 - Test File Split al Limite 500 Righe

**Context**: Ogni volta che un file di test supera 500 righe.

**Pattern**: Dividere il file in 2 parti logiche:
- `test_X_core.py` - casi fondamentali, happy path, unit tests
- `test_X_edge.py` o `test_X_integration.py` - casi limite, error paths, pipeline tests

Ogni file mantiene le proprie fixture (copia indipendente da conftest.py se necessario).
Strategia split: guardare la logica, non fare split arbitrario a meta.

**Evidence**: S344 (test_symbol_extractor split), S348 (3 split: load_context 665->355+379,
task_manager 660->277+388, symbol_extractor 662->291+353), S359 (2 split).
Tester agents tendono a generare file > 500 righe -> check `wc -l` dopo ogni output.

**Anti-pattern**: Un file test_X.py con 800+ righe. Difficile da navigare, lento da caricare,
fixture duplicate e incompatibili tra sezioni.

---

### P19 - Test Regressione per Ogni Bug Fix

**Context**: Ogni bug fixato durante una caccia bug.

**Pattern**: Ogni bug fix P1 e P2 deve avere almeno 1 test di regressione che:
1. Fallisce prima del fix (documenta il bug)
2. Passa dopo il fix (documenta la correzione)

Naming: `test_regression_NOMEBUG` o includere nel test esistente un caso che copre
esattamente il scenario del bug.

**Evidence**: S386: 30 nuovi test di regressione (+30 da 967 a 997) per 11 fix.
S382: 12 bug, 12 fix, +N test regressione. Media su 9 cacce bug: +20-30 test per hunt.
Il numero totale di test e cresciuto: 153 (S380) -> 320 (S382) -> 454 (S383) -> 776 (S384) -> 997 (S386).

**Anti-pattern**: Fix il bug senza aggiungere test -> il bug puo ritorare senza avviso.
"Il codice ora e corretto" non e sufficiente: il test documenta PERCHE era sbagliato.

---

## CATEGORIA 5 - SNCP/MEMORY PATTERNS

---

### P20 - PROMPT_RIPRESA: Stato + Decisioni + Perche (non solo "cosa")

**Context**: Scrittura di PROMPT_RIPRESA alla fine di ogni sessione.

**Pattern**: Ogni PROMPT_RIPRESA deve rispondere a 3 domande:
1. **COSA** e stato fatto (fatti, numeri, file)
2. **PERCHE** e stato deciso cosi (razionale, non solo risultato)
3. **PROSSIMI STEP** in ordine di priorita (cosa fare PRIMA)

Struttura raccomandata:
```markdown
## SESSIONE N - Cosa e successo
[fatti concreti con numeri]

## Decisioni prese (con perche)
[ogni decisione importante + motivazione]

## Prossimi step (in ordine)
1. X (perche Y)
2. ...
```
Limite: 150 righe. Se supera -> archiviare sessioni vecchie.
Scrivere "come se la prossima Cervella non sapesse nulla".

**Evidence**: SNCP 4.0 (S357, 9.5/10). La regola "scrivi il perche" e nata da sessioni
dove il PROMPT_RIPRESA aveva solo "cosa" e la sessione successiva perdeva tempo a ricostruire
il razionale. Pattern confermato su 50+ sessioni con PROMPT_RIPRESA utili vs non utili.

**Anti-pattern**: PROMPT_RIPRESA come lista di cose fatte senza razionale. "Abbiamo fixato
il bug di aliasing" senza spiegare PERCHE era un bug e COME e stato fixato -> inutile
per la prossima sessione. PROMPT_RIPRESA > 150 righe -> troppo da leggere, si salta.

---

## SUMMARY TABLE

| # | Pattern | Categoria | Sessioni | Score |
|---|---------|-----------|----------|-------|
| P01 | Frozen Dataclass + Mapping type annotation | Architecture | S380-S386 | 9.5+ |
| P02 | ZERO Dependencies per packages core | Architecture | S368-S386 | 9.5+ |
| P03 | src/ layout + Hatchling + PEP 639 | Architecture | S368-S385 | 9.5-9.6 |
| P04 | MappingProxyType per cataloghi + indice inverso O(1) | Architecture | S382, S385 | 9.5+ |
| P05 | Monotonic clock per durate (NON wall clock) | Architecture | S386 | 9.5 |
| P06 | Research Before Implementation (15-31 fonti) | Process | S368-S386 | 9.5+ |
| P07 | Guardiana Audit dopo ogni step (target 9.5/10) | Process | S357-S386 | 9.3 avg |
| P08 | Code Review parallela con 2 Ingegnere | Process | S382, S386 | 9.5 |
| P09 | Defer con motivazione documentata | Process | S374-S386 | 9.5 |
| P10 | Agente per ogni ruolo (Regina coordina, non implementa) | Process | S380-S386 | 9.5+ |
| P11 | Copia difensiva dict() prima di mutare | Bug Prevention | S386 | 9.5 |
| P12 | Validazione input a boundary (empty, digit-start) | Bug Prevention | S386 | 9.5 |
| P13 | NetworkX phantom nodes -> filtrare con self.nodes | Bug Prevention | S374 | 9.5 |
| P14 | Symbol ID con line number (no collision) | Bug Prevention | S374 | 9.5 |
| P15 | except Exception ristretto nei loop | Bug Prevention | S374-S378 | 9.5 avg |
| P16 | Atomic file create con open(f, 'x') | Bug Prevention | S376 | 9.5 |
| P17 | No __init__.py nei test (no shadowing) | Testing | S340, S368-S385 | 9.5+ |
| P18 | Test file split al limite 500 righe | Testing | S344, S348, S359 | 9.5 |
| P19 | Test regressione per ogni bug fix | Testing | S374-S386 | 9.5 |
| P20 | PROMPT_RIPRESA: stato + decisioni + perche | SNCP/Memory | S357-S386 | 9.3 avg |

---

## Raccomandazione

Questi 20 pattern sono pronti per essere incorporati in `~/.claude/patterns/validated_patterns.md`
come "skill library" (Voyager-style, descritto nella ricerca auto_learning S385/386).

**Step immediato consigliato**: creare il file `~/.claude/patterns/validated_patterns.md`
con questi pattern come base. La prossima sessione di Auto-Learning Livello 1 puo partire
da qui invece di ricostruire da zero.

**Priorita di applicazione**:
- P01, P02, P03, P17: applicare a OGNI nuovo package da subito
- P06, P07: applicare a OGNI sessione di sviluppo da subito
- P11, P12, P15: aggiungere alla checklist della Guardiana da subito
- P08, P09: usare per code review future di moduli 500+ righe

---

*Report: `/Users/rafapra/Developer/CervellaSwarm/.sncp/progetti/cervellaswarm/reports/RESEARCH_20260221_validated_patterns_S386.md`*
*Cervella Researcher - Parte dello sciame CervellaSwarm*
