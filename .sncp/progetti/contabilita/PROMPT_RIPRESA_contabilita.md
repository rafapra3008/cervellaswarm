# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 26 Febbraio 2026 - Sessione 188
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S188 (tipo_gir Pareggi + checkout Puzzle + Deploy)

| Cosa | Stato |
|------|-------|
| **Produzione V2** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | main.py v1.15.0 + pdf_parser v1.14.1 + **8 file frontend S188** |
| **Agent NL/SHE/HP** | v2.1.0 LIVE + reconcile v1.1.0 DEPLOYATO S184 |
| **HC.io** | **11 check** - TUTTI VERDI S184 |
| **Test portale** | **1559 PASS** (lab-v3) |
| **Test agent** | 362 PASS |
| **Lab-v2** | INTATTO, frozen da S87 |
| **Migrations DB VM** | **v15** su TUTTI e 3 i DB V3 |
| **GCP Snapshot** | `pre-deploy-s188-20260226-195604` |

---

## S188 - Cosa abbiamo fatto

### Feature 1: tipo_gir nei Pareggi (pareggi-display.js)

Aggiunto numero fattura (tipo_gir) con icona 🏷️ in 4 punti del foglio Pareggi:
- GIR singolo (riga 613)
- GIR in gruppo espanso con checkbox (riga 478)
- GIR in gruppo senza checkbox (riga 556)
- GIR non pareggiati/unmatched (riga 774)

Pattern: `${g.tipo_gir ? '| 🏷️ ${escapeHtml(g.tipo_gir)}' : ''}` - conditional, XSS-safe.
Audit Guardiana: **9.6/10** (4 P3 cosmetici, F2 unmatched fixato).

### Feature 2: checkout_date nel Puzzle (pareggi-puzzle.js)

Aggiunta data di checkout sulle caparre nel Rompicapo con emoji aereo 🛫.
- Variabile: `const checkoutDate = type === 'caparra' ? escapeHtml(item.checkout_date || '') : '';`
- Rendering: `${checkoutDate ? '<div class="puzzle-item-detail">🛫 ${checkoutDate}</div>' : ''}`
- Posizione: dopo stagione, prima di tipo_gir

Audit Guardiana: **9.6/10** (4 P3 pre-esistenti).

### Feature 3: Loading stat-card Pareggi (parziale)

Fix per skeleton loader sulle 4 stat-card quando si cambia al tab Pareggi:
- tabs.js: re-aggiunge `is-loading` alle stat-card al tab switch
- pareggi-core.js: `finally` block in `refreshPareggiStatus()` rimuove skeleton per tutti i path
- style.css: aggiunto `.stat-total` ai selettori `is-loading` e `transition`

Audit Guardiana: **9.3/10** (F1 P2 fixato - skeleton eterno).
**NOTA: Flash 0 persiste ~1-2s su VM** - vedi sezione "DA RISOLVERE" sotto.

### Deploy VM

8 file totali deployati in 2 round:
- Round 1 (5 file): style.css, app-init.js, data.js, pareggi-display.js, pareggi-puzzle.js
- Round 2 (3 file): tabs.js, pareggi-core.js, style.css (aggiornato)
- MD5 tutti verificati post-deploy
- Rafa ha testato: tipo_gir OK, checkout OK, loading ancora flash 0

---

## DA RISOLVERE - Loading stat-card Pareggi (P2)

### Il Problema
Quando si cambia al tab Pareggi su VM, le 4 stat-card (Caparre Pareggiate, GIR Pareggiati, Importo Pareggiato, Importo Non Pareggiato) mostrano "0" per 1-2 secondi prima dei numeri reali. In locale troppo veloce per vedere, su VM con latenza si vede.

### Root Cause Analisi
La chain asincrona e' il problema:
1. `showTab('pareggi')` -> aggiunge `is-loading` (skeleton visibile) -> chiama `refreshPareggiStatus()`
2. `refreshPareggiStatus()` -> fetch `/pareggi/status` (1a API call, ~200ms su VM)
3. Se status='completato' -> `loadPareggi()` -> fetch `/pareggi/status` ANCORA (2a call, ~200ms) + fetch `/pareggi/list` (3a call, ~500ms)
4. `displayPareggi()` -> `calculateQuadraturaStats()` -> aggiorna numeri -> rimuove `is-loading`

**Il `finally` block rimuove `is-loading` alla fine del passo 2**, ma i numeri vengono aggiornati solo al passo 4. Quindi tra passo 2 e passo 4 c'e' il gap dove i numeri mostrano 0 (valore HTML iniziale) senza skeleton.

### Possibili Soluzioni (da studiare S189)

**Soluzione A - Rimuovere `is-loading` SOLO in `calculateQuadraturaStats()`:**
- Togliere il `finally` block da `refreshPareggiStatus()`
- Aggiungere rimozione `is-loading` nei rami non-completato di `refreshPareggiStatus()` (in_corso, errore, default)
- PRO: skeleton resta finche i numeri sono pronti
- CON: se `loadPareggi()` fallisce silenziosamente, skeleton eterno

**Soluzione B - Nascondere stat-card finche non pronte:**
- Usare `visibility: hidden` sulle stat-card finche `calculateQuadraturaStats()` le rivela
- PRO: zero flash
- CON: layout shift (spazio vuoto)

**Soluzione C - Ridurre le API call:**
- `loadPareggi()` fa una fetch duplicata di `/pareggi/status` (gia' fatta da `refreshPareggiStatus()`). Passare il risultato come parametro elimina ~200ms
- PRO: piu veloce, meno fetch
- CON: refactoring piu ampio

**Soluzione D - Soluzione A + C combinata (RACCOMANDATA):**
- Rimuovere `finally`, gestire `is-loading` nei branch non-completato
- Passare statusData a `loadPareggi()` per evitare double fetch
- Skeleton resta visibile finche `calculateQuadraturaStats()` lo rimuove con i dati reali

### File coinvolti
- `frontend/js/pareggi-core.js` - `refreshPareggiStatus()` (riga 72) + `loadPareggi()` (riga 221) + `calculateQuadraturaStats()` (riga 352)
- `frontend/js/tabs.js` - `showTab()` (riga 109)
- `frontend/css/style.css` - selettori `is-loading`

---

## Prossima Sessione (S189)

| # | Prio | Cosa | Note |
|---|------|------|------|
| 1 | **P2** | **Fix loading stat-card Pareggi** | Soluzione D raccomandata (vedi sopra) |
| 2 | P2 | Verificare HC.io prossimo run | NL 14:00, SHE 14:10, HP 14:20 |
| 3 | P3 | Dipendenze vecchie (fastapi 0.104.1) | requirements_PROPOSTO.txt esiste |
| 4 | P3 | Pulire doppio .env NL+SHE | Prossima volta agent |

---

## Dove leggere

| Cosa | Path |
|------|------|
| **tipo_gir Pareggi (S188)** | `frontend/js/pareggi-display.js` (righe 478, 556, 613, 774) |
| **checkout Puzzle (S188)** | `frontend/js/pareggi-puzzle.js` (righe 173, 203) |
| **Loading stat-card (S188)** | `frontend/js/tabs.js` (110-116), `frontend/js/pareggi-core.js` (141-151) |
| **Loading UX S187** | `frontend/css/style.css`, `frontend/js/data.js`, `frontend/js/app-init.js` |

---

## Lezioni Apprese (Sessione 188)

### Cosa ha funzionato bene
- **Audit Guardiana dopo ogni step**: P2 reale trovato (skeleton eterno) su loading fix - fixato prima del deploy
- **Triple check MD5 pre/post deploy**: 8 file, tutti match, zero divergenze
- **Snapshot GCP pre-deploy**: safety net standard

### Cosa non ha funzionato
- **Chain asincrona non analizzata a fondo**: il `finally` block rimuove skeleton prima che i dati arrivino. Serviva analisi piu profonda della timeline

### Pattern candidato
- **Analizzare la TIMELINE asincrona prima di fixare loading**: non basta aggiungere/rimuovere classi CSS - serve capire QUANDO ogni step della chain finisce. Evidenza: S188 flash 0 persiste. MONITORARE.

---

*S188: tipo_gir Pareggi + checkout Puzzle + deploy 8 file VM. "Ultrapassar os proprios limites!"*

---
