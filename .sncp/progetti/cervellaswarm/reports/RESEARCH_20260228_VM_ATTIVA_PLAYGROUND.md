# VM Attiva per Lingua Universale - Ricerca

**Data:** 2026-02-28
**Researcher:** Cervella Researcher
**Status:** COMPLETA
**Fonti:** 14 consultate

---

## Contesto

Lingua Universale e un linguaggio (.lu files) implementato in Python puro, ZERO deps.
Ha gia: CLI (`lu run`, `lu check`, `lu verify`), REPL interattivo, 2806 test, 0.91s suite.

Il progetto e a **Fase C completa**. L'idea di Rafa: una VM sempre attiva per:
1. Utenti che provano il linguaggio online
2. Team di 17 agenti che testano in CI/CD
3. Sviluppo continuo del linguaggio stesso

---

## 1. Come Fanno i Grossi

### Go Playground (play.golang.org)
- **Architettura:** Frontend React + backend Go. Codice mandato al server, compilato e eseguito.
- **Sandbox:** Docker + gVisor (application kernel in user-space). gVisor intercetta tutte le syscall.
- **Sicurezza:** No rete, no filesystem esterno, output solo su stdout/stderr. Tempo deterministico (2009-11-10).
- **Caching:** Risultati cachati perche output e deterministico.
- **Lezione:** gVisor e la scelta production-grade di Google per untrusted code.

### Rust Playground (play.rust-lang.org)
- **Architettura:** Frontend React + backend Iron (Rust). Docker containers per ogni compilation.
- **Sandbox:** Docker network isolation + resource limits (CPU, RAM, tempo).
- **Sicurezza:** No connessione di rete tra compiler container e mondo esterno.
- **Lezione:** Per linguaggi che compilano, Docker senza gVisor e sufficiente. Per interpreted code serve di piu.

### TypeScript Playground
- **Architettura:** 100% client-side. tsc compilato in browser via WebWorker.
- **Sandbox:** Nessuna (il codice gira nel browser dell'utente).
- **Lezione:** Funziona perche TypeScript si compila in JS. Noi non abbiamo questa opzione (Python non si compila in WASM nativamente senza Pyodide).

### Pyodide (Python in WebAssembly)
- **Cos'e:** CPython compilato in WebAssembly/Emscripten. Gira nel browser.
- **Compatibilita:** Qualsiasi pure Python wheel su PyPI e supportato via micropip.
- **Installazione custom wheel:**
  ```python
  import micropip
  await micropip.install('https://example.com/cervellaswarm_lingua_universale-0.1.0-py3-none-any.whl')
  ```
- **Requisiti CORS:** Il server che serve la wheel deve avere CORS headers corretti.
- **Dimensione:** CPython WASM = ~26 MB da scaricare al primo uso (poi cached).
- **Lezione:** Per un package ZERO DEPS in pure Python, Pyodide funziona nativamente. La wheel su PyPI sarebbe gia supportata.

---

## 2. Tecnologie di Sandboxing -- Confronto

| Tecnologia | Sicurezza | Performance | Complessita | Uso tipico |
|------------|-----------|-------------|-------------|------------|
| **Docker standard** | Media | Alta | Bassa | Trusted internal code |
| **Docker + seccomp** | Alta | Alta (overhead minimo) | Media | Production workloads |
| **Docker + gVisor** | Molto Alta | Media (syscall overhead) | Alta | Untrusted user code (Google) |
| **Firecracker microVM** | Massima | Media (boot 80ms) | Alta | AI agents (E2B, AWS Lambda) |
| **WebAssembly/WASI** | Massima | Alta | Alta | Browser, stateless functions |

**Verdict per noi:** Per utenti che scrivono codice .lu nel browser, WebAssembly (Pyodide) elimina il problema alla radice. Per CI/CD interno, Docker standard e sufficiente (codice trusted).

---

## 3. Opzioni per Lingua Universale

### Opzione A: Pyodide (WASM nel Browser)

**Come funziona:**
```
Browser -> carica Pyodide (~26MB, cached) -> micropip install lingua-universale -> esegui .lu
```

**Architettura concreta:**
- Una singola pagina HTML statica (deploy su GitHub Pages, Cloudflare Pages, GRATIS)
- Monaco Editor (stessa base di VS Code) per editing .lu
- Pyodide in background thread (non blocca UI)
- Output in un pannello sotto

**Pro:**
- Zero costi server (CDN statico)
- Zero sicurezza da gestire (sandbox e il browser)
- Deploy in 1 giorno
- Non si scala (ogni utente usa la propria macchina)
- Funziona offline dopo il primo caricamento

**Contro:**
- 26 MB download iniziale (poi cached)
- Primo avvio lento (~3-5 secondi per inizializzare Pyodide)
- No stato persistente tra sessioni (senza backend)
- Limitato a pure Python (ma LU ha zero deps, perfetto)

**Effort:** 1-2 giorni. Un file HTML + JS + Monaco Editor.

**Costo:** 0 euro/mese.

---

### Opzione B: Server-Side su Fly.io (Gia Abbiamo)

**Come funziona:**
```
Browser -> API FastAPI su Fly.io -> Docker container -> lu run codice -> risposta JSON
```

**Architettura concreta:**
- FastAPI app con endpoint `/run`, `/check`, `/verify`
- Input: sorgente .lu come stringa
- Output: stdout, stderr, errori strutturati
- Docker con resource limits (timeout 10s, 128MB RAM per request)
- Rate limiting per IP

**Pro:**
- Risultati server-side (logging, analytics, caching)
- Gia abbiamo Fly.io
- Controllo totale
- Supporta sessioni future (salvare programmi utente)

**Contro:**
- Costo: ~$5-10/mese per istanza piccola sempre attiva
- Sicurezza: codice utente esegue Python arbitrario via `exec()` (eval.py lo fa gia)
- Sandboxing necessario: almeno seccomp + timeout
- Cold start se non always-on

**Effort:** 3-5 giorni (FastAPI + Docker + deploy + rate limiting + basic sandbox).

**Costo:** ~$5-15/mese (Fly.io shared-cpu-1x, 256MB RAM).

---

### Opzione C: E2B (Sandbox as a Service)

**Come funziona:**
```
Browser -> nostro backend leggero -> E2B API -> Firecracker microVM -> lu run -> risposta
```

**Architettura concreta:**
- E2B SDK Python/JS per creare sandbox on-demand
- Ogni run di codice utente = microVM Firecracker isolata (boot 80ms)
- Nessuna gestione sicurezza da parte nostra

**Pro:**
- Sicurezza massima (Firecracker, stessa tech di AWS Lambda)
- Zero ops su sandboxing
- Pay-per-use

**Contro:**
- Latenza: ~80-400ms per cold start microVM (ok per playground, non per CI)
- Costo: $0 fino a 100GB-hours (Hobby), poi $29/mese. Per uso leggero = gratis.
- Dipendenza da terzi per infrastruttura critica
- Overkill per un package che e pure Python e sicuro di default

**Effort:** 1-2 giorni (solo integrazione SDK).

**Costo:** Gratis per uso leggero, $29/mese se scala.

---

### Opzione D: VM Persistente per il Team (Development VM)

**Come funziona:**
```
GitHub Actions trigger -> Fly.io VM sempre attiva -> agenti CI/CD -> test + iterazione
```

**Architettura concreta:**
- Fly.io VM (1 core, 512MB) sempre accesa
- SSH o API per gli agenti per lanciare test
- `pytest` continuo su ogni push
- Potenziale: REPL sempre aperto per agenti

**Pro:**
- Ambiente identico per tutti (no "works on my machine")
- CI/CD piu veloce (no cold start di GitHub Actions runner)
- Gli agenti possono tenere stato tra chiamate

**Contro:**
- Costo: ~$7-14/mese (shared-cpu-1x, 512MB, always-on)
- Ma: GitHub Actions e gia gratis e funziona bene
- Aggiunge complessita di gestione senza chiaro vantaggio su setup attuale

**Effort:** 2-3 giorni.

**Costo:** ~$10/mese.

---

## 4. Analisi Sicurezza

### Il Problema Specifico per LU

Il codice .lu viene:
1. Parsato (gia safe - nessun eval)
2. Compilato in AST (safe)
3. Convertito in Python sorgente (`_compiler.py`)
4. Eseguito via `exec()` (`_interop.py`)

**Il passo 4 e dove sta il rischio.** Chi controlla il codice .lu controlla l'`exec()`.

### Mitigazioni Consigliate

**Per Pyodide (Opzione A):**
- Nessun rischio server. Il codice esegue nella sandbox del browser.
- Rischio: XSS se mostriamo output HTML senza escape. Soluzione: escape sempre.

**Per Server-Side (Opzione B):**
- Timeout obbligatorio: `subprocess.run(timeout=10)` o `threading.Timer`
- Limite memoria: Docker `--memory=128m`
- No network access nel container: `--network=none`
- Limite filesystem: container read-only + tmpfs per /tmp
- Limite processi: `--pids-limit=50`
- seccomp profile custom (blocca fork, exec di binari esterni, mount)

**Schema sicurezza minimo per server-side:**
```
Docker run \
  --network=none \
  --memory=128m \
  --pids-limit=50 \
  --read-only \
  --tmpfs /tmp \
  --timeout 10s \
  lu run <file.lu>
```

---

## 5. Confronto Finale

| Dimensione | Pyodide (A) | Fly.io DIY (B) | E2B (C) | Dev VM (D) |
|------------|-------------|----------------|---------|------------|
| **Costo/mese** | $0 | $5-15 | $0-29 | $10 |
| **Effort setup** | 1-2gg | 3-5gg | 1-2gg | 2-3gg |
| **Sicurezza** | Browser sandbox | Media (da hardare) | Massima | N/A (interno) |
| **Latenza** | 3-5s primo carico | <500ms | 80-400ms | N/A |
| **Scalabilita** | Infinita (client) | Limitata VM | Alta | N/A |
| **Use case fit** | Playground pubblico | API backend | Playground con stato | CI/CD team |
| **Dipendenze** | Pyodide + CDN | Fly.io | E2B | Fly.io |

---

## 6. Raccomandazione

### Per Fase D (ora, costo zero)

**Raccomandazione PRIMARIA: Opzione A (Pyodide)**

Motivazione:
- Lingua Universale e ZERO DEPS pure Python: e il caso d'uso perfetto per Pyodide
- Costo zero, sicurezza zero da gestire, deploy immediato
- GitHub Pages o Cloudflare Pages: statico, veloce, gratis
- La wheel su PyPI (quando pubblichiamo) sara gia installabile con micropip senza configurazione

**Architettura raccomandata:**

```
GitHub Pages (gratis)
  |
  +-- index.html
  |     Monaco Editor (editor .lu)
  |     [Run] [Check] [Verify] buttons
  |
  +-- playground.js
      Pyodide init in WebWorker
      micropip.install('cervellaswarm-lingua-universale')
      Intercetta stdout -> mostra nel pannello output
```

**Prerequisito:** Pubblicare su PyPI prima (Fase D: Packaging). La wheel su PyPI rende il playground triviale.

### Per la VM del Team

**Raccomandazione: NON farlo ora.**

GitHub Actions funziona. La test suite gira in 0.91s. Non c'e un problema reale da risolvere. Una VM sempre attiva aggiunge $10/mese e complessita senza beneficio concreto.

**Eccezione:** Se in futuro gli agenti AI devono fare sessioni REPL persistenti o testare il linguaggio in modo interattivo, allora una Fly.io VM dedicata ha senso.

### Per il Futuro (post-PyPI, post-comunita)

Se arrivano utenti reali che vogliono salvare programmi, condividere link, avere sessioni:
- Aggiungere Opzione B (Fly.io FastAPI) come backend leggero
- Tenere Pyodide come esecuzione client-side
- Backend solo per: salvataggio, condivisione, analytics

---

## 7. Quick Start Implementation

### Pyodide Playground - Snippet Core

```javascript
// playground.js
async function initPlayground() {
    const pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");

    // Quando sara su PyPI:
    // await micropip.install("cervellaswarm-lingua-universale");

    // Prima del PyPI, da URL diretta (GitHub Releases):
    await micropip.install(
        "https://github.com/rafapra3008/cervellaswarm/releases/download/v0.1.0/cervellaswarm_lingua_universale-0.1.0-py3-none-any.whl"
    );
}

async function runCode(source) {
    // Cattura stdout
    let output = [];
    pyodide.globals.set("_output", output);

    const code = `
import sys, io
from cervellaswarm_lingua_universale._eval import run_source
result = run_source(${JSON.stringify(source)}, label="playground")
print(result.python_source or "")
for err in result.errors:
    print(f"Errore: {err}", file=sys.stderr)
`;
    await pyodide.runPythonAsync(code);
    return output.join("\n");
}
```

---

## Riferimenti

- [Go Playground Sandbox (GitHub)](https://github.com/golang/playground/blob/master/sandbox/sandbox.go)
- [Rust Playground (GitHub)](https://github.com/rust-lang/rust-playground)
- [Pyodide - Python in WebAssembly](https://pyodide.org/)
- [micropip - Loading Packages](https://pyodide.org/en/stable/usage/loading-packages.html)
- [gVisor Security Model](https://gvisor.dev/docs/architecture_guide/security/)
- [Confronto Isolation Technologies per AI](https://www.softwareseni.com/firecracker-gvisor-containers-and-webassembly-comparing-isolation-technologies-for-ai-agents/)
- [E2B Code Sandbox per AI Agents](https://e2b.dev/)
- [E2B vs Modal vs Fly.io Confronto](https://getathenic.com/blog/e2b-vs-modal-vs-flyio-sandbox-comparison)
- [In-Browser Code Playgrounds (Anton Zhiyanov)](https://antonz.org/in-browser-code-playgrounds/)
- [Top AI Code Sandbox Products 2025](https://modal.com/blog/top-code-agent-sandbox-products)
