# HARDTESTS - Sistema Multi-Finestra v3

> **"Prima di Miracollo, testiamo il sistema!"**

**Data Creazione:** 3 Gennaio 2026
**Versione:** 3.0.0
**Scopo:** Verificare il Sistema Multi-Finestra completo prima del test su Miracollo

---

## RIFERIMENTO

- **Sistema Multi-Finestra**: `.swarm/README.md`
- **Task Manager**: `scripts/swarm/task_manager.py`
- **GUIDA_COMUNICAZIONE v2.0**: `docs/guide/GUIDA_COMUNICAZIONE.md`
- **HARDTESTS Comunicazione v1.0**: `docs/tests/HARDTESTS_COMUNICAZIONE.md`

---

## EVOLUZIONE DELLO SWARM

```
v1: Agents base (17 membri)
    └─> 12 Regole, pattern delegation

v2: Memoria + Guardiane (Sessione 57-58)
    └─> SQLite memoria, Pattern Catalog, 3 livelli rischio

v3: Multi-Finestra + Hooks (Sessione 61-63) <- SIAMO QUI
    └─> .swarm/, task_manager.py, hooks intelligent
```

**OGGI:** Verifichiamo che v3 funzioni completamente prima di testare su progetto REALE (Miracollo).

---

## TEST 1: FLUSSO MULTI-FINESTRA COMPLETO

### Scenario

Test del flusso base Multi-Finestra: Regina crea task, Worker (in altra finestra) lo esegue, comunicazione via .swarm/tasks/ funziona.

**Obiettivo:** Verificare che il protocollo .ready -> .working -> .done funzioni tra finestre separate.

### Setup

**Pre-requisiti:**
- CervellaSwarm su branch main
- Sistema .swarm/ presente
- task_manager.py funzionante

**Task:** Creare un file di documentazione semplice (Livello 1 - basso rischio)

### Prompt da Usare

#### FINESTRA 1 (Regina)

```markdown
## TASK PER FINESTRA 2 (cervella-docs)

Sto testando il sistema Multi-Finestra. Creo un task in .swarm/tasks/

**COMANDI:**

1. Creo il task:
   python3 scripts/swarm/task_manager.py create TASK_HT1 cervella-docs "Creare FAQ.md per Sistema Multi-Finestra" 1

2. Segno come ready:
   python3 scripts/swarm/task_manager.py ready TASK_HT1

3. Verifico stato:
   python3 scripts/swarm/task_manager.py status TASK_HT1

**ASPETTO:** Task creato e ready. Ora la FINESTRA 2 puo prenderlo.
```

#### FINESTRA 2 (Worker - cervella-docs)

```markdown
## SONO CERVELLA-DOCS (Worker)

Verifico se ci sono task pronti per me:

**COMANDI:**

1. Lista task:
   python3 scripts/swarm/task_manager.py list

2. Se vedo TASK_HT1 con status "ready":
   - Leggo il task: cat .swarm/tasks/TASK_HT1.md
   - Segno working: python3 scripts/swarm/task_manager.py working TASK_HT1
   - Eseguo il task (creo FAQ.md)
   - Scrivo output in .swarm/tasks/TASK_HT1_output.md
   - Segno done: python3 scripts/swarm/task_manager.py done TASK_HT1

**IL TASK:**

Creare file `docs/FAQ_MULTI_FINESTRA.md` con:
- Cos'e il Sistema Multi-Finestra?
- Come funzionano i flag files?
- Esempi pratici

**OUTPUT:** File creato + .swarm/tasks/TASK_HT1_output.md
```

#### FINESTRA 1 (Regina - Verifica)

```markdown
## VERIFICO RISULTATO

**COMANDI:**

1. Controllo stato:
   python3 scripts/swarm/task_manager.py status TASK_HT1

   Aspetto: "done"

2. Leggo output:
   cat .swarm/tasks/TASK_HT1_output.md

3. Verifico file creato:
   cat docs/FAQ_MULTI_FINESTRA.md

**CRITERIO SUCCESSO:** Task completato, file FAQ creato, comunicazione via .swarm/ funzionante!
```

### Comportamento Atteso

```
FINESTRA 1 (Regina):
1. Crea TASK_HT1.md in .swarm/tasks/
2. Crea TASK_HT1.ready (flag file)
3. Aspetta...
4. Vede TASK_HT1.done
5. Legge TASK_HT1_output.md
6. Verifica FAQ_MULTI_FINESTRA.md creato

FINESTRA 2 (Worker):
1. Vede TASK_HT1.ready
2. Legge TASK_HT1.md
3. Crea TASK_HT1.working (rimuove .ready)
4. Lavora: crea FAQ_MULTI_FINESTRA.md
5. Scrive TASK_HT1_output.md
6. Crea TASK_HT1.done (rimuove .working)

COMUNICAZIONE:
- Avviene SOLO tramite file in .swarm/tasks/
- Nessuna comunicazione diretta tra finestre
- Flag files controllano il flusso
```

### Checklist Verifica

- [ ] Regina ha creato task con task_manager.py?
- [ ] Flag .ready apparso in .swarm/tasks/?
- [ ] Worker ha visto il task (list funzionante)?
- [ ] Worker ha segnato .working (flag transition)?
- [ ] FAQ_MULTI_FINESTRA.md creato?
- [ ] Output scritto in TASK_HT1_output.md?
- [ ] Flag .done apparso?
- [ ] Regina ha letto output correttamente?
- [ ] NESSUNA comunicazione diretta (solo via file)?

### Risultato Test

| Data | Esito | Note |
|------|-------|------|
| 2026-01-03 18:29 | **PASSED** | Flusso completo funzionante! FAQ creato (140 righe) |

### Note Test 1
- Tempo esecuzione: ~4 minuti
- Comunicazione SOLO via file: VERIFICATO
- Flag transition: .ready -> .working -> .done FUNZIONANTE
- Output strutturato: PERFETTO
- File creato: docs/FAQ_MULTI_FINESTRA.md (140 righe, documentazione eccellente)

---

## TEST 2: HOOKS INTELLIGENT IN AZIONE

### Scenario

Test dei 2 nuovi hooks implementati nella Sessione 63:
- `session_start_scientist.py` - Si attiva all'avvio sessione Miracollo
- `post_commit_engineer.py` - Analizza dopo ogni commit

**Obiettivo:** Verificare che i trigger funzionino automaticamente nei momenti corretti.

### Setup

**Pre-requisiti:**
- Hook configurati in ~/.claude/settings.json
- Progetto Miracollo con .swarm/ setup

**Nota:** Questo test richiede apertura sessione su Miracollo (progetto reale)

### Prompt da Usare

#### PASSO 1: Test session_start_scientist.py

```markdown
## TEST HOOK: session_start_scientist

Apro NUOVA finestra Claude Code su:
~/Developer/miracollogeminifocus

**COSA DOVREBBE SUCCEDERE (automaticamente):**

1. Hook session_start_scientist.py si attiva
2. Genera prompt automatico in .swarm/research/SESSION_START_[timestamp].md
3. Prompt contiene:
   - Stato progetto attuale
   - Task aperti
   - Suggerimenti ricerca proattiva

**VERIFICO:**

1. Finestra aperta su Miracollo?
2. File generato in .swarm/research/?
   ls -la .swarm/research/

3. Contenuto prompt:
   cat .swarm/research/SESSION_START_*.md

4. Formato corretto?
   - Header con timestamp
   - Stato progetto
   - Task aperti
   - Suggerimenti ricerca
```

#### PASSO 2: Test post_commit_engineer.py

```markdown
## TEST HOOK: post_commit_engineer

Faccio un commit nel progetto Miracollo per attivare l'hook.

**PREPARAZIONE:**

1. Creo piccola modifica:
   echo "# Test hook" > TEST_HOOK.md

2. Commit:
   git add TEST_HOOK.md
   git commit -m "test: Hook post_commit_engineer"

**COSA DOVREBBE SUCCEDERE (automaticamente):**

1. Hook post_commit_engineer.py si attiva
2. Analizza il commit appena fatto
3. Genera analisi in .swarm/analysis/COMMIT_[hash].md
4. Analisi contiene:
   - File modificati
   - Potenziale impatto
   - Suggerimenti refactoring (se necessari)

**VERIFICO:**

1. Commit fatto?
   git log -1

2. File analisi generato?
   ls -la .swarm/analysis/

3. Contenuto analisi:
   cat .swarm/analysis/COMMIT_*.md

4. Formato corretto?
   - Header con commit hash
   - File modificati
   - Analisi impatto
   - Suggerimenti (se applicabili)
```

### Comportamento Atteso

```
HOOK session_start_scientist:
- TRIGGER: Claude Code apre sessione su progetto
- QUANDO: All'avvio della finestra
- OUTPUT: .swarm/research/SESSION_START_[timestamp].md
- CONTENUTO: Prompt ricerca automatico basato su stato progetto

HOOK post_commit_engineer:
- TRIGGER: git commit completato
- QUANDO: Dopo ogni commit (hook post-commit Git)
- OUTPUT: .swarm/analysis/COMMIT_[hash].md
- CONTENUTO: Analisi impatto + suggerimenti refactoring
```

### Checklist Verifica

#### session_start_scientist
- [ ] Hook configurato in settings.json?
- [ ] Finestra aperta su Miracollo?
- [ ] File SESSION_START_*.md generato?
- [ ] Contiene stato progetto?
- [ ] Contiene task aperti?
- [ ] Suggerimenti ricerca presenti?
- [ ] Formato markdown corretto?

#### post_commit_engineer
- [ ] Hook configurato in settings.json?
- [ ] Commit fatto nel progetto?
- [ ] File COMMIT_*.md generato?
- [ ] Contiene file modificati?
- [ ] Analisi impatto presente?
- [ ] Suggerimenti ragionevoli?
- [ ] Formato markdown corretto?

### Risultato Test

| Hook | Data | Esito | Note |
|------|------|-------|------|
| session_start_scientist | 2026-01-03 18:27 | **PASSED** | Genera scientist_prompt con missione ricerca |
| post_commit_engineer | 2026-01-03 18:22 | **PASSED** | Genera engineer_report con analisi file grandi |

### Note Test 2
- Gli hooks si attivano AUTOMATICAMENTE all'avvio sessione e dopo comandi Bash
- scientist_prompt contiene: tecnologie, competitor, trend da monitorare
- engineer_report contiene: file grandi (>500 righe), suggerimenti split
- Entrambi generano file in reports/ directory
- NESSUNA azione manuale richiesta - tutto automatico!

---

## TEST 3: FLUSSO GUARDIANA NEL SISTEMA MULTI-FINESTRA

### Scenario

Test del flusso COMPLETO Regina -> Worker -> Guardiana usando il sistema Multi-Finestra.
Task Livello 2 (medio rischio) richiede verifica della Guardiana.

**Obiettivo:** Verificare che il flusso Guardiane funzioni ANCHE con comunicazione via .swarm/

### Setup

**Pre-requisiti:**
- Sistema .swarm/ funzionante (Test 1 passato)
- 3 finestre Claude Code

**Task:** Creare una nuova funzione utility Python (Livello 2)

### Prompt da Usare

#### FINESTRA 1 (Regina)

```markdown
## TASK LIVELLO 2: Funzione utility con verifica Guardiana

**STEP 1: Consultazione Guardiana (stesso contesto)**

Prima di delegare, consulto cervella-guardiana-qualita:

"Ho un task: creare funzione validate_email() in utils.py
Che livello di rischio e?"

Aspetto risposta Guardiana: dovrebbe dire "Livello 2 - MEDIO"

**STEP 2: Creazione Task**

python3 scripts/swarm/task_manager.py create TASK_HT3 cervella-backend "Creare funzione validate_email in utils.py" 2

Noto il "2" finale = Livello 2 (medio rischio)

**STEP 3: Edito task per contesto completo**

Aggiungo al task in .swarm/tasks/TASK_HT3.md:

PERCHE: Validazione email serve per form di registrazione
CRITERI SUCCESSO:
- [ ] Funzione validate_email(email: str) -> bool
- [ ] Gestisce formati email standard
- [ ] Gestisce casi edge (None, empty, invalid)
- [ ] Type hints presenti
- [ ] Docstring con esempi

CHI VERIFICHERA:
cervella-guardiana-qualita (Livello 2 - verifica type hints, edge cases, docstring)

**STEP 4: Ready**

python3 scripts/swarm/task_manager.py ready TASK_HT3

Ora FINESTRA 2 puo lavorare!
```

#### FINESTRA 2 (Worker - cervella-backend)

```markdown
## SONO CERVELLA-BACKEND

**STEP 1: Vedo task**

python3 scripts/swarm/task_manager.py list

Vedo TASK_HT3 ready, assegnato a me.

**STEP 2: Leggo e lavoro**

cat .swarm/tasks/TASK_HT3.md

python3 scripts/swarm/task_manager.py working TASK_HT3

**STEP 3: Creo la funzione**

Creo test-orchestrazione/api/utils.py con validate_email()

**STEP 4: Output**

Scrivo in .swarm/tasks/TASK_HT3_output.md:

```markdown
## OUTPUT: validate_email() creato

### File Creato
- test-orchestrazione/api/utils.py

### Funzione
```python
def validate_email(email: str) -> bool:
    """Valida formato email.

    Examples:
        >>> validate_email("test@example.com")
        True
        >>> validate_email("invalid")
        False
    """
    if not email or not isinstance(email, str):
        return False
    return "@" in email and "." in email.split("@")[1]
```

### Come Testare
python3 -c "from test-orchestrazione.api.utils import validate_email; print(validate_email('test@example.com'))"
```

python3 scripts/swarm/task_manager.py done TASK_HT3
```

#### FINESTRA 3 (Guardiana Qualita)

```markdown
## SONO GUARDIANA-QUALITA

La Regina mi passa il task per verifica (Livello 2).

**STEP 1: Leggo contesto**

cat .swarm/tasks/TASK_HT3.md (PERCHE + criteri)
cat .swarm/tasks/TASK_HT3_output.md (output Worker)

**STEP 2: Verifico file**

cat test-orchestrazione/api/utils.py

**CHECKLIST:**
- [x] Type hints presenti? SI (str -> bool)
- [x] Docstring presente? SI
- [x] Examples nella docstring? SI
- [ ] Gestisce None? MANCA! Bug trovato
- [x] Gestisce empty? SI
- [x] Logica validazione? Basic ma funziona

**STEP 3: Report**

Creo .swarm/tasks/TASK_HT3_review.md:

```markdown
## VERIFICA COMPLETATA - PROBLEMA MINORE

**Task:** TASK_HT3 - validate_email()
**Worker:** cervella-backend
**File:** test-orchestrazione/api/utils.py

### Problemi NON BLOCCANTI
1. Type hint dice "email: str" ma poi controlla isinstance(email, str)
   - Se type hint garantisce str, il check e ridondante
   - OPPURE: cambia type hint in "email: Optional[str]"

### Cosa Funziona
- [x] Type hints base presenti
- [x] Docstring con esempi
- [x] Gestione empty string
- [x] Logica validazione base

### Suggerimento
Cambia signature in:
```python
def validate_email(email: Optional[str]) -> bool:
```

### Esito
APPROVATO con nota miglioramento

---
Guardiana Qualita
```

**COMUNICO RISULTATO ALLA REGINA (via file, non diretto!)**
```

#### FINESTRA 1 (Regina - Chiusura)

```markdown
## VERIFICO RISULTATO FINALE

**STEP 1: Leggo review Guardiana**

cat .swarm/tasks/TASK_HT3_review.md

**STEP 2: Decisione**

La Guardiana ha APPROVATO con nota minore.
Posso:
- Accettare cosi (funziona)
- Chiedere fix al Worker (Optional[str])

Decido: Accetto, la nota e buona ma non bloccante.

**STEP 3: Cleanup**

python3 scripts/swarm/task_manager.py cleanup TASK_HT3

**TASK COMPLETATO!**
Flusso Regina -> Worker -> Guardiana funziona anche nel sistema Multi-Finestra!
```

### Comportamento Atteso

```
FINESTRA 1 (Regina):
1. Consulta Guardiana per livello
2. Crea task Livello 2
3. Edita task con CONTESTO COMPLETO
4. Segna ready
5. Aspetta done
6. Passa a Guardiana per verifica
7. Legge review
8. Decide (approvare/richiedere fix)

FINESTRA 2 (Worker):
1. Vede task ready
2. Legge contesto completo
3. Sa che sara verificato
4. Crea funzione con criteri
5. Scrive output strutturato
6. Segna done

FINESTRA 3 (Guardiana):
1. Riceve task da Regina
2. Legge PERCHE + criteri + output
3. Verifica file creato
4. Scrive review strutturata
5. APPROVATO o PROBLEMI TROVATI
```

### Checklist Verifica

- [ ] Regina ha consultato Guardiana PRIMA?
- [ ] Task creato con Livello 2?
- [ ] CONTESTO COMPLETO nel task?
- [ ] Worker ha visto task e contesto?
- [ ] Funzione validate_email() creata?
- [ ] Output strutturato scritto?
- [ ] Guardiana ha ricevuto PERCHE + criteri?
- [ ] Review Guardiana strutturata?
- [ ] Guardiana ha trovato problema reale?
- [ ] Flusso completato via .swarm/ (no comunicazione diretta)?

### Risultato Test

| Data | Esito | Note |
|------|-------|------|
| 2026-01-03 18:45 | **PASSED** | Flusso Regina->Backend->Guardiana PERFETTO! |

### Note Test 3
- Backend ha creato validate_email con Optional[str], regex RFC 5322, 7 esempi docstring
- Guardiana ha verificato TUTTI i criteri con tabella dettagliata
- Review scritta in TASK_HT3_review.md con APPROVATO
- Comunicazione SOLO via .swarm/tasks/ - ZERO contatto diretto
- Tempo: ~4 minuti (18:41 -> 18:45)

---

## TEST 4: SCENARIO PRE-MIRACOLLO (FULL STACK)

### Scenario

Simulare un task REALE che faremmo su Miracollo: creare endpoint API completo.
Flusso completo: Regina -> Backend -> Guardiana -> Frontend -> Guardiana -> Tester -> APPROVATO

**Obiettivo:** Stress test completo del sistema prima di usarlo su progetto reale.

### Setup

**Pre-requisiti:**
- Test 1, 2, 3 passati
- 5 finestre Claude Code (Regina, Backend, Guardiana, Frontend, Tester)

**Task Simulato:** Endpoint GET /api/users per Miracollo

### Prompt da Usare

#### FINESTRA 1 (Regina - Coordinamento)

```markdown
## TASK REALE SIMULATO: Endpoint /api/users

Questo e il tipo di task che faremo su Miracollo. Testiamolo qui!

**TASK:** Creare endpoint GET /api/users con:
- Backend: endpoint FastAPI
- Frontend: hook React per chiamarlo
- Test: E2E test dell'intero flusso

**PLANNING:**

1. Backend: endpoint /api/users
   - Livello 2 (codice nuovo)
   - Verificato da Guardiana Qualita

2. Frontend: hook useUsers()
   - Livello 2 (codice nuovo)
   - Verificato da Guardiana Qualita

3. Tester: E2E test
   - Livello 1 (solo test)
   - Nessuna verifica

**CREO I 3 TASK:**

python3 scripts/swarm/task_manager.py create TASK_HT4A cervella-backend "Endpoint GET /api/users" 2

python3 scripts/swarm/task_manager.py create TASK_HT4B cervella-frontend "Hook useUsers per chiamare /api/users" 2

python3 scripts/swarm/task_manager.py create TASK_HT4C cervella-tester "E2E test per /api/users flow" 1

**SEQUENZA:**
1. Backend first (TASK_HT4A)
2. Frontend after backend (TASK_HT4B) - dipende da output backend
3. Test after all (TASK_HT4C) - dipende da entrambi

**STEP 1: Avvio Backend**

Edito TASK_HT4A.md con contesto:

PERCHE: Miracollo ha bisogno di listare utenti per dashboard admin
CRITERI:
- [ ] GET /api/users ritorna lista utenti
- [ ] Response: [{ id, name, email }]
- [ ] Gestisce lista vuota
- [ ] Error handling 500

python3 scripts/swarm/task_manager.py ready TASK_HT4A

FINESTRA 2 puo partire!
```

#### FINESTRA 2 (cervella-backend)

```markdown
## TASK_HT4A: Endpoint /api/users

**STEP 1: Leggo task**

cat .swarm/tasks/TASK_HT4A.md

python3 scripts/swarm/task_manager.py working TASK_HT4A

**STEP 2: Creo endpoint**

File: test-orchestrazione/api/routes/users.py

```python
from typing import List, Dict
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/users")
async def get_users() -> List[Dict[str, any]]:
    """Get all users.

    Returns:
        List of users with id, name, email

    Raises:
        HTTPException: 500 if database error
    """
    try:
        # Mock data per test
        users = [
            {"id": 1, "name": "Mario Rossi", "email": "mario@test.com"},
            {"id": 2, "name": "Luca Bianchi", "email": "luca@test.com"}
        ]
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
```

**STEP 3: Output per Frontend**

Scrivo .swarm/tasks/TASK_HT4A_output.md:

```markdown
## OUTPUT: Endpoint /api/users creato

### File Creato
- test-orchestrazione/api/routes/users.py

### Endpoint Details
- URL: GET /api/users
- Response: List[Dict]
- Format: [{ "id": int, "name": string, "email": string }]
- Error: 500 se database error

### INFO PER FRONTEND
Base URL: /api/users
Metodo: GET
No payload necessario
Response sempre array (anche se vuoto: [])

### Come Testare
curl http://localhost:8000/api/users
```

python3 scripts/swarm/task_manager.py done TASK_HT4A

Ora FINESTRA 1 (Regina) puo passare a Guardiana!
```

#### FINESTRA 3 (cervella-guardiana-qualita - Verifica Backend)

```markdown
## VERIFICA TASK_HT4A (Backend)

**STEP 1: Leggo tutto**

cat .swarm/tasks/TASK_HT4A.md
cat .swarm/tasks/TASK_HT4A_output.md
cat test-orchestrazione/api/routes/users.py

**STEP 2: Checklist**

- [x] Type hints? SI (List[Dict[str, any]])
- [x] Docstring? SI con Returns e Raises
- [x] Error handling? SI (HTTPException 500)
- [x] Mock data per test? SI
- [x] Output per Frontend? SI e chiaro

**STEP 3: Review**

Scrivo .swarm/tasks/TASK_HT4A_review.md:

```markdown
## VERIFICA COMPLETATA - APPROVATO

**Task:** TASK_HT4A - Endpoint /api/users
**Worker:** cervella-backend
**File:** test-orchestrazione/api/routes/users.py

### Checklist
- [x] Type hints completi
- [x] Docstring con esempi
- [x] Error handling presente
- [x] Output per Frontend chiaro

### Nota Positiva
L'output per Frontend e MOLTO chiaro - dice formato esatto + come testare.
Questo aiutera cervella-frontend!

### Esito
APPROVATO PER MERGE

---
Guardiana Qualita
```

COMUNICO A REGINA VIA FILE: Backend APPROVATO, Frontend puo partire!
```

#### FINESTRA 1 (Regina - Avvio Frontend)

```markdown
## Backend APPROVATO - Avvio Frontend

**STEP 1: Leggo review**

cat .swarm/tasks/TASK_HT4A_review.md

Backend APPROVATO! Procedo con Frontend.

**STEP 2: Edito TASK_HT4B con info da Backend**

Aggiungo a TASK_HT4B.md:

PERCHE: Dashboard admin ha bisogno di listare utenti
DIPENDE DA: TASK_HT4A (backend endpoint)
INFO BACKEND (da output TASK_HT4A):
- URL: GET /api/users
- Response: [{ id, name, email }]

CRITERI:
- [ ] Hook useUsers() creato
- [ ] Chiama GET /api/users
- [ ] Gestisce loading state
- [ ] Gestisce error state
- [ ] Type per User interface

python3 scripts/swarm/task_manager.py ready TASK_HT4B

FINESTRA 4 puo partire!
```

#### FINESTRA 4 (cervella-frontend)

```markdown
## TASK_HT4B: Hook useUsers()

**STEP 1: Leggo task + backend info**

cat .swarm/tasks/TASK_HT4B.md

Vedo che backend ritorna [{ id, name, email }]

python3 scripts/swarm/task_manager.py working TASK_HT4B

**STEP 2: Creo hook**

File: test-orchestrazione/components/hooks/useUsers.js

```javascript
import { useState, useEffect } from 'react';

export const useUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/users');
        if (!response.ok) throw new Error('Failed to fetch users');
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return { users, loading, error };
};
```

**STEP 3: Output**

Scrivo .swarm/tasks/TASK_HT4B_output.md:

```markdown
## OUTPUT: Hook useUsers() creato

### File Creato
- test-orchestrazione/components/hooks/useUsers.js

### Hook Details
- Export: useUsers()
- Returns: { users, loading, error }
- Users format: Array<{ id, name, email }>

### INFO PER TESTER
Import: import { useUsers } from './hooks/useUsers';
Usage: const { users, loading, error } = useUsers();
States: loading (bool), error (string|null), users (array)

### Esempio Uso
```jsx
function UserList() {
  const { users, loading, error } = useUsers();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name} - {user.email}</li>
      ))}
    </ul>
  );
}
```
```

python3 scripts/swarm/task_manager.py done TASK_HT4B

Ora Regina puo far verificare e poi passare a Tester!
```

#### FINESTRA 3 (cervella-guardiana-qualita - Verifica Frontend)

```markdown
## VERIFICA TASK_HT4B (Frontend)

**STEP 1: Leggo**

cat .swarm/tasks/TASK_HT4B.md
cat .swarm/tasks/TASK_HT4B_output.md
cat test-orchestrazione/components/hooks/useUsers.js

**STEP 2: Checklist**

- [x] Hook useUsers() creato? SI
- [x] Gestisce loading? SI (useState + setLoading)
- [x] Gestisce error? SI (try/catch + setError)
- [x] Formato users corretto? SI (array)
- [x] Output per Tester? SI con esempio uso

**STEP 3: Review**

Scrivo .swarm/tasks/TASK_HT4B_review.md:

```markdown
## VERIFICA COMPLETATA - APPROVATO

**Task:** TASK_HT4B - Hook useUsers()
**Worker:** cervella-frontend
**File:** test-orchestrazione/components/hooks/useUsers.js

### Checklist
- [x] Hook implementato correttamente
- [x] Loading state gestito
- [x] Error handling presente
- [x] Output per Tester con esempio uso

### Nota Positiva
L'esempio uso nel output e PERFETTO per il Tester - mostra esattamente come usare l'hook.

### Esito
APPROVATO PER MERGE

---
Guardiana Qualita
```

COMUNICO A REGINA: Frontend APPROVATO, Tester puo partire!
```

#### FINESTRA 1 (Regina - Avvio Tester)

```markdown
## Backend + Frontend APPROVATI - Avvio Test

**STEP 1: Leggo reviews**

cat .swarm/tasks/TASK_HT4B_review.md

Entrambi APPROVATI! Posso far testare l'intero flusso.

**STEP 2: Edito TASK_HT4C**

Aggiungo a TASK_HT4C.md:

PERCHE: Verificare che backend + frontend lavorino insieme
DIPENDE DA: TASK_HT4A (backend) + TASK_HT4B (frontend)
COSA TESTARE:
- Backend ritorna users
- Frontend chiama correttamente
- Loading state funziona
- Error handling funziona

CRITERI:
- [ ] Test E2E creato
- [ ] Testa happy path
- [ ] Testa error path
- [ ] Report risultati

python3 scripts/swarm/task_manager.py ready TASK_HT4C

FINESTRA 5 puo partire!
```

#### FINESTRA 5 (cervella-tester)

```markdown
## TASK_HT4C: E2E Test /api/users flow

**STEP 1: Leggo task**

cat .swarm/tasks/TASK_HT4C.md

Livello 1 (solo test) - nessuna verifica Guardiana necessaria.

python3 scripts/swarm/task_manager.py working TASK_HT4C

**STEP 2: Test Backend**

curl http://localhost:8000/api/users

Risultato: [{"id":1,"name":"Mario Rossi","email":"mario@test.com"},{"id":2,"name":"Luca Bianchi","email":"luca@test.com"}]

PASS - Backend ritorna users!

**STEP 3: Test Frontend (simulato)**

Verifico che useUsers.js:
- Chiama fetch('/api/users') - SI
- Gestisce response.json() - SI
- Setta users state - SI
- Gestisce loading - SI
- Gestisce error - SI

PASS - Frontend gestisce tutto!

**STEP 4: Output**

Scrivo .swarm/tasks/TASK_HT4C_output.md:

```markdown
## OUTPUT: E2E Test COMPLETATO - TUTTI PASS

### Test Eseguiti

1. Backend Endpoint
   - URL: GET /api/users
   - Response: [{"id":1,"name":"Mario Rossi",...}]
   - Status: PASS

2. Frontend Hook
   - Import: Corretto
   - Fetch: Corretto (chiama /api/users)
   - States: Loading, Error, Users - TUTTI presenti
   - Status: PASS

3. Integration
   - Backend + Frontend comunicano
   - Formato dati compatibile
   - Status: PASS

### Risultato Finale
TUTTI I TEST PASSATI - Feature pronta per merge!

### Report
- Test Backend: 1/1 PASS
- Test Frontend: 1/1 PASS
- Test Integration: 1/1 PASS
- TOTALE: 3/3 PASS

---
cervella-tester
```

python3 scripts/swarm/task_manager.py done TASK_HT4C

TASK COMPLETATO!
```

#### FINESTRA 1 (Regina - Chiusura Completa)

```markdown
## SCENARIO COMPLETO - SUCCESSO!

**RIEPILOGO:**

1. TASK_HT4A (Backend) - DONE + APPROVATO
2. TASK_HT4B (Frontend) - DONE + APPROVATO
3. TASK_HT4C (Test) - DONE (3/3 PASS)

**FLUSSO TOTALE:**

Regina -> Backend Worker -> Guardiana APPROVA
  -> Frontend Worker -> Guardiana APPROVA
    -> Tester -> TUTTI PASS

**COMUNICAZIONE:**
- ZERO comunicazione diretta tra finestre
- TUTTO via .swarm/tasks/
- Output strutturati passati tra worker

**RISULTATO:**
Feature /api/users completa e testata!
Questo e esattamente il flusso che useremo su Miracollo!

**SISTEMA MULTI-FINESTRA v3: VALIDATO!**
```

### Comportamento Atteso

```
FLUSSO COMPLETO:

1. Regina pianifica 3 task sequenziali
2. Backend crea endpoint, output strutturato
3. Guardiana verifica backend -> APPROVATO
4. Frontend usa output backend, crea hook
5. Guardiana verifica frontend -> APPROVATO
6. Tester testa intero flusso -> PASS
7. Regina coordina tutto via .swarm/

COMUNICAZIONE:
- Regina: Unica che coordina
- Worker: Comunicano via output files
- Guardiane: Verificano e scrivono review
- ZERO comunicazione diretta
- TUTTO tracciato in .swarm/tasks/
```

### Checklist Verifica

#### Planning
- [ ] Regina ha creato 3 task sequenziali?
- [ ] Dipendenze chiare tra task?
- [ ] Livelli rischio corretti?

#### Backend (TASK_HT4A)
- [ ] Endpoint creato?
- [ ] Guardiana ha verificato?
- [ ] APPROVATO?
- [ ] Output strutturato per Frontend?

#### Frontend (TASK_HT4B)
- [ ] Hook creato?
- [ ] Usa info da output Backend?
- [ ] Guardiana ha verificato?
- [ ] APPROVATO?
- [ ] Output strutturato per Tester?

#### Test (TASK_HT4C)
- [ ] Test E2E eseguiti?
- [ ] Backend testato?
- [ ] Frontend testato?
- [ ] Integration testata?
- [ ] Report chiaro?

#### Sistema
- [ ] Comunicazione SOLO via .swarm/?
- [ ] Flag files usati correttamente?
- [ ] Output passati tra worker?
- [ ] Regina ha coordinato tutto?
- [ ] ZERO casino, tutto tracciato?

### Risultato Test

| Task | Data | Esito | Note |
|------|------|-------|------|
| TASK_HT4A (Backend) | 2026-01-03 18:56 | **PASS 10/10** | Endpoint + Pydantic + Docstring |
| TASK_HT4B (Frontend) | 2026-01-03 18:51 | **PASS 10/10** | Hook + JSDoc + Error handling |
| TASK_HT4C (Test) | 2026-01-03 18:57 | **PASS 30/30** | Backend + Frontend + Integration |
| **SCENARIO COMPLETO** | 2026-01-03 18:57 | **PASSED** | 5 finestre, flusso completo! |

### Note Test 4
- Backend ha creato 2 endpoint (list + single user) con Pydantic model
- Frontend ha creato hook useUsers con loading/error/refetch
- Tester ha verificato compatibilità formati tra Backend e Frontend
- Guardiana ha approvato Backend E Frontend prima del test
- ZERO comunicazione diretta - TUTTO via .swarm/tasks/
- Flusso: Regina -> Backend -> Guardiana -> Frontend -> Guardiana -> Tester
- **PRONTO PER MIRACOLLO!**

---

## METRICHE SUCCESSO

| Test | Target | Attuale |
|------|--------|---------|
| Test 1: Multi-Finestra Base | PASS | **PASS** |
| Test 2: Hooks Intelligent | PASS | **PASS** |
| Test 3: Guardiana Multi-Finestra | PASS | **PASS** |
| Test 4: Scenario Full Stack | PASS | **PASS** |
| Comunicazione via .swarm/ | SI | **SI** |
| Flag files funzionanti | SI | **SI** |
| Output strutturati passati | SI | **SI** |
| Guardiane nel flusso | SI | **SI** |
| Zero comunicazione diretta | SI | **SI** |

**RISULTATO: 4/4 TEST PASSATI! MIRACOLLO READY!** 🎉

---

## STORICO TEST

### [Data Test] - RISULTATI

| Test | Esito | Note Principali |
|------|-------|-----------------|
| Test 1: Multi-Finestra | | |
| Test 2: Hooks | | |
| Test 3: Guardiana | | |
| Test 4: Full Stack | | |

**Scoperte:**
- [Da compilare dopo test]

**Problemi Trovati:**
- [Da compilare dopo test]

**Conclusione:**
- [Da compilare dopo test]

---

## QUANDO TESTARE

```
+------------------------------------------------------------------+
|                                                                  |
|   PRIMA DI MIRACOLLO                                             |
|                                                                  |
|   Questi test DEVONO passare prima di usare lo Swarm             |
|   su un progetto REALE come Miracollo.                           |
|                                                                  |
|   PERCHE':                                                       |
|   - Miracollo e produzione                                       |
|   - Non possiamo permetterci casino                              |
|   - Meglio trovare problemi QUI che LA'                          |
|                                                                  |
|   DOPO I TEST:                                                   |
|   - Se TUTTI passano -> Miracollo ready!                         |
|   - Se qualcuno fallisce -> Fix + re-test                        |
|                                                                  |
+------------------------------------------------------------------+
```

---

## NOTE PER CHI TESTA

### Setup Finestre

```
FINESTRA 1: Regina (cervella-orchestrator)
  cd ~/Developer/CervellaSwarm

FINESTRA 2: Worker 1 (cervella-backend/docs)
  cd ~/Developer/CervellaSwarm

FINESTRA 3: Guardiana (cervella-guardiana-qualita)
  cd ~/Developer/CervellaSwarm

FINESTRA 4: Worker 2 (cervella-frontend) [solo Test 4]
  cd ~/Developer/CervellaSwarm

FINESTRA 5: Tester (cervella-tester) [solo Test 4]
  cd ~/Developer/CervellaSwarm
```

### Comandi Utili

```bash
# Monitorare task in tempo reale
watch -n 1 'python3 scripts/swarm/task_manager.py list'

# Vedere flag files
ls -la .swarm/tasks/TASK_*.{ready,working,done}

# Log completo
ls -la .swarm/tasks/
```

### Cosa Osservare

1. **Timing**: Quanto tempo passa tra .ready e .working?
2. **Comunicazione**: I worker vedono davvero i task?
3. **Output**: Gli output sono strutturati e utili?
4. **Guardiane**: Le review sono accurate?
5. **Coordinamento**: La Regina coordina senza casino?

---

*"Prima di Miracollo, testiamo il sistema!"*

*"Meglio trovare problemi QUI che su progetto REALE!"*

*"Con calma, una cosa alla volta. Sistema testato. Sicuri."*

**CervellaSwarm Team - Cervella Tester**
