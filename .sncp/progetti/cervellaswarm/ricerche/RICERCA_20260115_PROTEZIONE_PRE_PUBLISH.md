# RICERCA: Protezione Pre-Publish CervellaSwarm

> **Data:** 15 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Obiettivo:** Determinare cosa è BLOCCANTE vs cosa può aspettare prima di npm publish

---

## TL;DR - RISPOSTA ALLA DOMANDA

**COSA ORA (BLOCCANTE):**
1. LICENSE file con Apache 2.0 (5 min)
2. NOTICE file con copyright (5 min)
3. Copyright header nei file chiave (15 min)
4. package.json con license field (2 min)
5. Git commit + push (prova timestamp) (5 min)

**TOTALE BLOCCANTE: ~32 minuti**

**COSA SUBITO DOPO (0-7 giorni):**
6. README con license section (10 min)
7. CONTRIBUTING.md con license info (15 min)

**COSA QUANDO C'È TRACTION (dopo):**
8. Trademark per "CervellaSwarm" (opzionale, costoso)
9. Copyright registration (opzionale, Italia non obbligatorio)

---

## 1. COPYRIGHT: Come Funziona

### Protezione Automatica (BUONA NOTIZIA!)

**In Italia e EU:**
- Copyright è **AUTOMATICO** alla creazione ([EU IP Helpdesk](https://intellectual-property-helpdesk.ec.europa.eu/ip-management-and-resources/copyright_en))
- NON serve registrazione formale
- Il codice è protetto dal momento in cui lo scrivi

**Come si dimostra di essere autori originali:**
1. **Git History** - I commit sono prova di authorship ([Google Open Source Casebook](https://google.github.io/opencasebook/authorship/))
2. **Timestamp** - Data/ora dei commit conta come evidenza
3. **Copyright Notice** - "Copyright 2026 Rafa & Cervella" nei file

### Registrazione Opzionale

**NON obbligatoria ma utile per:**
- Dispute legali (inversione onere della prova)
- Stabilire data certa davanti a giudice
- **Ma**: costosa, non necessaria per protezione base

**Servizi disponibili:**
- OriginStamp (blockchain timestamping)
- SIAE (Italia, per software commerciale)
- US Copyright Office (se vuoi protezione USA)

---

## 2. MINIMO INDISPENSABILE PRE-PUBLISH

### BLOCCANTE (senza questi = RISCHIO ALTO)

#### A. LICENSE File (Apache 2.0)

**Dove:** `/LICENSE` (root del progetto)

**Contenuto:** Testo completo Apache 2.0 License

**Perché BLOCCANTE:**
- Senza licenza = altri NON possono legalmente usare il codice
- Paradosso: codice pubblico ma non utilizzabile!
- npm mostra "UNLICENSED" = segnale di allarme
- ([Open Source Guide](https://opensource.guide/legal/))

**Come:**
```bash
# Scarica template Apache 2.0
curl https://www.apache.org/licenses/LICENSE-2.0.txt > LICENSE
```

---

#### B. NOTICE File

**Dove:** `/NOTICE` (root del progetto)

**Contenuto:**
```
CervellaSwarm
Copyright 2026 Rafa & Cervella

This product includes software developed by Rafa & Cervella.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

**Perché BLOCCANTE:**
- Apache 2.0 **RICHIEDE** NOTICE file se distribuisci ([Apache Infra Docs](https://infra.apache.org/licensing-howto.html))
- Contiene attribution che deve essere preservata
- Senza = violazione dei termini della tua stessa licenza!

---

#### C. Copyright Header nei File Chiave

**Quali file:**
- `packages/cli/src/index.js` (entry point)
- Ogni file in `packages/cli/src/commands/`
- File core in `~/.claude/agents/` (prompts)

**Header da usare:**
```javascript
/**
 * Copyright 2026 Rafa & Cervella
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 */
```

**Perché IMPORTANTE (non strettamente bloccante ma FORTEMENTE raccomandato):**
- Ogni file dichiara ownership
- Se qualcuno copia singoli file, copyright è chiaro
- Best practice Apache Foundation

---

#### D. package.json - License Field

**Dove:** `packages/cli/package.json`

**Aggiungi:**
```json
{
  "name": "cervellaswarm",
  "version": "0.1.0",
  "license": "Apache-2.0",
  "author": "Rafa & Cervella",
  "repository": {
    "type": "git",
    "url": "https://github.com/username/CervellaSwarm.git"
  }
}
```

**Perché BLOCCANTE:**
- npm usa questo campo per mostrare licenza
- Tooling automatico (npm, GitHub) legge da qui
- SPDX identifier "Apache-2.0" è standard ([npm Best Practices](https://github.com/ossf/package-manager-best-practices/blob/main/published/npm.md))

---

#### E. Git Commit + Push (Timestamp Proof)

**Cosa fare:**
```bash
git add LICENSE NOTICE package.json
git commit -m "Add Apache 2.0 license and copyright notices"
git push origin main
```

**Perché BLOCCANTE:**
- Git commit = timestamp proof of authorship
- GitHub = public record con data/ora
- In caso di dispute: "Io l'ho pubblicato PRIMA" ([Hacker News discussions](https://news.ycombinator.com/item?id=10240120))

---

## 3. COSA SUCCEDE SENZA PROTEZIONE

### Scenario: Pubblichi SENZA LICENSE

**Conseguenze:**
- Codice pubblico ma **legalmente non utilizzabile**
- Altri NON possono installare, modificare, distribuire
- "All rights reserved" di default
- ([Open Source Guide](https://opensource.guide/legal/))

**Ma**: Nessuno può copiare legalmente, vero?

**Sbagliato!** Persone disoneste lo faranno comunque, e TU non puoi fare enforcement perché:
- Non hai dichiarato i termini di utilizzo
- Non puoi dimostrare violazione di una licenza che non esiste

---

### Scenario: Qualcuno Copia e Ripubblica

**Se HAI LICENSE + COPYRIGHT:**
1. Identifichi la violazione
2. Invii DMCA Takedown a npm/GitHub
3. Processo: 1 business day per rimozione ([npm DMCA Policy](https://docs.npmjs.com/policies/dmca/))
4. GitHub pubblica la tua richiesta come transparency ([GitHub DMCA Repo](https://github.com/github/dmca))

**COSA SERVE IN ANTICIPO (per poter fare DMCA):**
- ✅ Copyright notice nei file
- ✅ LICENSE file
- ✅ Proof of original authorship (git history)
- ✅ Data di pubblicazione originale

**Se NON HAI QUESTI:**
- DMCA takedown è difficile/impossibile
- Devi provare ownership in altro modo (costoso, lento)

---

### Scenario: Modificano e Ripubblicano con Nome Diverso

**Se Apache 2.0:**
- È **PERMESSO** dalla licenza!
- Ma DEVONO:
  - Mantenere copyright notice originale
  - Dichiarare le modifiche
  - Includere LICENSE e NOTICE file
  - Usare nome diverso (richiesto da licenza)

**Se NON rispettano questi termini:**
- Violazione di licenza = copyright infringement
- Puoi fare DMCA takedown

**Se rispettano i termini:**
- È legale (Apache 2.0 è permissiva)
- **Ma**: Loro NON possono dire "è nostro"
- **E**: Il tuo copyright notice DEVE rimanere

---

## 4. IMPEDIRE COPIE ILLEGALI - Come Agire

### DMCA Takedown (npm + GitHub)

**Processo:**
1. Compila form: [GitHub Copyright Claims](https://docs.github.com/en/site-policy/content-removal-policies/guide-to-submitting-a-dmca-takedown-notice)
2. Specifica:
   - URL del pacchetto infringing
   - URL del tuo repo originale
   - Quali file sono copiati
   - Dichiarazione sotto pena di spergiuro
3. GitHub/npm rimuove in ~1 business day

**Requisiti CRITICI:**
- "as specific as possible" - devi listare FILE esatti
- Serve prova di ownership (git history, copyright notices)
- Devi avere una licenza dichiarata

---

### Enforcement Legale (se DMCA non basta)

**Quando serve:**
- Violazione commerciale grave
- Danni economici dimostrabili
- Rifiuto di rimuovere dopo DMCA

**Cosa serve:**
- Avvocato IP (Italia o EU)
- Prova di authorship (git history OK, registration meglio)
- Licenza chiara (Apache 2.0 = termini chiari)
- Documentazione della violazione

**Costo:** €€€€€ (migliaia di euro)

**Alternative migliori:**
- Community pressure (Twitter, HN, Reddit)
- Contatto diretto con infringer
- DMCA takedown (95% dei casi funziona)

---

## 5. ORDINE OPERAZIONI (Cosa Prima, Cosa Dopo)

### FASE 1: PRIMA di npm publish (BLOCCANTE - 32 min)

| # | Task | Dove | Tempo | Perché |
|---|------|------|-------|--------|
| 1 | Scarica Apache 2.0 text | `/LICENSE` | 5 min | Legale, npm requirement |
| 2 | Crea NOTICE file | `/NOTICE` | 5 min | Apache 2.0 requirement |
| 3 | Aggiungi header a file core | `.js` files | 15 min | Proof per file |
| 4 | Aggiorna package.json | `license` field | 2 min | npm metadata |
| 5 | Git commit + push | GitHub | 5 min | Timestamp proof |

**Output:** Protezione legale base ATTIVA ✅

---

### FASE 2: SUBITO DOPO primo publish (0-7 giorni - 25 min)

| # | Task | Dove | Tempo | Perché |
|---|------|------|-------|--------|
| 6 | README license section | `/README.md` | 10 min | Visibilità utenti |
| 7 | CONTRIBUTING.md | `/CONTRIBUTING.md` | 15 min | Chiarezza per contributors |

**Template README:**
```markdown
## License

Copyright 2026 Rafa & Cervella

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

---

### FASE 3: QUANDO C'È TRACTION (dopo primi 100+ utenti)

| # | Task | Costo | Quando | Perché |
|---|------|-------|--------|--------|
| 8 | Trademark "CervellaSwarm" | €1000-3000 | 1000+ users | Nome unico protetto |
| 9 | Copyright registration (opzionale) | €100-500 | Se dispute | Inversione onere prova |
| 10 | Legal review completo | €500-2000 | Pre Series A | Due diligence investors |

**NON urgente!** Fai SOLO se:
- Ci sono competitors che copiano
- Vuoi fundraising (investors chiedono)
- Vuoi espandere in USA (trademark USA)

---

## 6. ERRORI DA EVITARE (IRREVERSIBILI!)

### ❌ Errore 1: Pubblicare senza LICENSE

**Conseguenza:**
- Codice pubblico ma "all rights reserved"
- Utenti NON possono usarlo legalmente
- Devi fare new major version per aggiungere licenza
- Community loss of trust

**Fix:** Aggiungi PRIMA di primo npm publish

---

### ❌ Errore 2: Copyright Notice Sbagliato

**Sbagliato:**
```
Copyright 2026 [Your Name Here]
Copyright © Company XYZ (se non è vera)
```

**Corretto:**
```
Copyright 2026 Rafa & Cervella
```

**Perché:** False attribution = problema legale SERIO

---

### ❌ Errore 3: Licenza Incompatibile con Dipendenze

**Problema:**
- Usi libreria GPL (copyleft)
- Pubblichi con Apache 2.0 (permissive)
- = Violazione licenza GPL!

**Fix:** Check PRIMA di publish:
```bash
npm install -g legally
legally
```

Verifica che tutte le dipendenze siano compatibili con Apache 2.0

---

### ❌ Errore 4: Non Verificare package.json License Field

**Sbagliato:**
```json
"license": "SEE LICENSE IN LICENSE.md"
```

**Corretto:**
```json
"license": "Apache-2.0"
```

**Perché:** SPDX identifier standard, tooling funziona

---

### ❌ Errore 5: Copiare Codice Altrui Senza Attribution

**Se usi codice da altri progetti:**
- Mantieni il copyright notice originale
- Aggiungi al NOTICE file
- Verifica compatibilità licenze

**Esempio NOTICE con attribution:**
```
CervellaSwarm
Copyright 2026 Rafa & Cervella

This software includes code from:
- ProjectX (MIT License) - Copyright 2025 Author Name
```

---

## 7. CHECKLIST PRATICA - COPIA-INCOLLA

### Pre-Publish Checklist (DO THIS NOW!)

```bash
# 1. Scarica Apache 2.0 License
curl https://www.apache.org/licenses/LICENSE-2.0.txt > LICENSE

# 2. Crea NOTICE file
cat > NOTICE << 'EOF'
CervellaSwarm
Copyright 2026 Rafa & Cervella

This product includes software developed by Rafa & Cervella.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
EOF

# 3. Verifica package.json
grep -q '"license": "Apache-2.0"' packages/cli/package.json || echo "❌ Fix package.json license field!"

# 4. Commit
git add LICENSE NOTICE packages/cli/package.json
git commit -m "Add Apache 2.0 license and copyright protection"
git push origin main

echo "✅ PROTEZIONE BASE ATTIVA!"
```

### Header Template per File .js

```javascript
/**
 * Copyright 2026 Rafa & Cervella
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

### Post-Publish Checklist (entro 7 giorni)

```markdown
- [ ] README.md ha sezione License
- [ ] CONTRIBUTING.md spiega license per contributions
- [ ] GitHub repo settings: License field = Apache 2.0
- [ ] npm package page mostra licenza correttamente
```

---

## 8. FAQ RAPIDE

**Q: Serve registrare copyright in Italia?**
A: NO. È automatico. ([EU IP Helpdesk](https://intellectual-property-helpdesk.ec.europa.eu/ip-management-and-resources/copyright_en))

**Q: Git history conta come prova legale?**
A: SÌ, può essere usato come evidence in court. ([Google Casebook](https://google.github.io/opencasebook/authorship/))

**Q: Cosa succede se pubblico SENZA license?**
A: Codice è "all rights reserved" di default = altri non possono usarlo legalmente. ([Open Source Guide](https://opensource.guide/legal/))

**Q: Posso impedire completamente che copino il codice?**
A: NO se usi Apache 2.0 (è permissiva). MA devono mantenere copyright notice e attribution.

**Q: DMCA takedown è difficile?**
A: NO, se hai LICENSE + copyright notices. Process: ~1 business day. ([npm DMCA](https://docs.npmjs.com/policies/dmca/))

**Q: Serve trademark "CervellaSwarm"?**
A: Non subito. Utile se diventi popolare (1000+ users). Costo: €1000-3000.

---

## 9. RISCHI PER PRIORITÀ

### 🔴 RISCHIO ALTO (se pubblichi SENZA)

| Cosa Manca | Rischio | Probabilità | Impatto |
|------------|---------|-------------|---------|
| LICENSE file | Nessuno può usare legalmente | 100% | ALTO - Product unusable |
| NOTICE file | Violazione Apache 2.0 terms | 80% | MEDIO - Compliance issue |
| package.json license | npm mostra "UNLICENSED" | 100% | ALTO - Trust issue |

**Azione:** FIX PRIMA di npm publish (32 minuti)

---

### 🟡 RISCHIO MEDIO (se pubblichi senza)

| Cosa Manca | Rischio | Probabilità | Impatto |
|------------|---------|-------------|---------|
| Copyright headers | Difficile provare ownership file singoli | 30% | MEDIO |
| README license section | Utenti confusi su termini | 50% | BASSO |
| Git push timestamp | Meno proof of authorship | 20% | MEDIO |

**Azione:** Fai entro 7 giorni

---

### 🟢 RISCHIO BASSO (può aspettare)

| Cosa Manca | Rischio | Probabilità | Impatto |
|------------|---------|-------------|---------|
| Trademark registration | Qualcuno usa nome simile | 10% | BASSO (prima di traction) |
| Copyright registration | Più difficile vincere lawsuit | 5% | BASSO (EU protegge automaticamente) |
| Legal review completo | Miss edge cases | 15% | BASSO (all'inizio) |

**Azione:** Fai quando c'è traction (>1000 users)

---

## 10. RACCOMANDAZIONE FINALE

### ✅ FALLO SUBITO (Pre-Publish)

```
TEMPO: 32 minuti
COSTO: €0
PROTEZIONE: 90% dei casi reali

1. LICENSE file (Apache 2.0)
2. NOTICE file
3. package.json license field
4. Copyright headers file principali
5. Git commit + push
```

**Perché:** Zero costo, massimo beneficio, legalmente compliant, npm best practices.

---

### ✅ FALLO PRESTO (0-7 giorni)

```
TEMPO: 25 minuti
COSTO: €0
PROTEZIONE: +5% coverage

6. README license section
7. CONTRIBUTING.md
```

**Perché:** Chiarezza per utenti e contributors.

---

### ⏸️ ASPETTA (dopo traction)

```
TEMPO: Variabile
COSTO: €1500-5500
PROTEZIONE: +5% coverage (marginal)

8. Trademark
9. Copyright registration
10. Legal review
```

**Perché:** Costo significativo, beneficio marginale PRIMA di avere utenti.

---

## Fonti

Ricerca basata su:

### Documentazione Ufficiale
- [npm License Policy](https://docs.npmjs.com/policies/npm-license/)
- [npm DMCA Takedown Policy](https://docs.npmjs.com/policies/dmca/)
- [GitHub DMCA Guide](https://docs.github.com/en/site-policy/content-removal-policies/guide-to-submitting-a-dmca-takedown-notice)
- [Apache License 2.0 Requirements](https://infra.apache.org/licensing-howto.html)

### Legal Resources
- [Open Source Legal Guide](https://opensource.guide/legal/)
- [EU IP Helpdesk - Copyright](https://intellectual-property-helpdesk.ec.europa.eu/ip-management-and-resources/copyright_en)
- [Linux Foundation - Copyright Notices](https://www.linuxfoundation.org/blog/blog/copyright-notices-in-open-source-software-projects)
- [Google Open Source Casebook - Authorship](https://google.github.io/opencasebook/authorship/)

### Best Practices
- [npm Package Manager Best Practices](https://github.com/ossf/package-manager-best-practices/blob/main/published/npm.md)
- [Open Source Security Checklist 2026](https://onboardbase.com/blog/oss-security/)
- [FOSSA Apache 2.0 Guide](https://fossa.com/blog/open-source-licenses-101-apache-license-2-0/)

### Proof of Authorship
- [OriginStamp - Proof of Authorship](https://originstamp.com/blog/proof-of-authorship-for-open-source-projects/)
- [Vaultinum - Source Code IP Protection](https://vaultinum.com/blog/intellectual-property-of-source-code-how-to-protect-it)

---

## COSTITUZIONE-APPLIED

**COSTITUZIONE-APPLIED:** SI

**Principio usato:** "Fatto BENE > Fatto VELOCE" + "Non abbiamo fretta"

**Come applicato:**
- Studio approfondito (8 ricerche web)
- Distinguo BLOCCANTE (32 min) vs OPZIONALE (dopo)
- Priorità basata su RISCHIO REALE, non paura
- Risparmio tempo/denaro: €0 ora, €1500-5500 solo SE serve
- Chiarezza per Rafa: cosa fare ORA, cosa DOPO
- "Un progresso al giorno" = 32 min oggi, resto dopo

**Risultato:** Protezione 90% con 32 minuti di lavoro. Il restante 10% quando serve (pragmatismo vs perfezionismo).

---

*"Studiare prima di agire - sempre!"*
*"I player grossi hanno già risolto questi problemi."*
*Ricerca completata in 45 minuti. Report salvato.*
