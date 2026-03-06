# AUDIT SNCP COMPLETO - 12 Febbraio 2026
## Guardiana Ricerca - Verifica Tutti i 6 Progetti

---

## TABELLA RIASSUNTIVA

| Progetto | PROMPT_RIPRESA | Righe PR | Max 150 | Aggiornato | Decisioni | Prossima Sess | stato.md | Righe SM | Max 500 | FATOS_CONF |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **cervellaswarm** | OK | 95 | OK | 2026-02-10 S352 | OK | OK (S354) | OK | 148 | OK | NO |
| **miracollo** | OK | 75 | OK | 2026-01-20 S300 | NO | NO | OK | 115 | OK | NO |
| **contabilita** | OK | 106 | OK | 2026-02-12 S3 | OK | OK | OK | 30 | OK | NO |
| **cervellabrasil** | OK | 82 | OK | 2026-02-12 S359 | OK | OK (Fase 3) | **MANCA** | - | - | **SI** |
| **chavefy** | OK | 98 | OK | 2026-02-12 S354+ | OK | OK | OK | 117 | OK | NO |
| **cervellacostruzione** | OK | 89 | OK | 2026-02-04 S337 | OK | OK | OK | 112 | OK | NO |

---

## DETTAGLI PER PROGETTO

### 1. cervellaswarm
- **PROMPT_RIPRESA:** 95 righe, OK. Ultimo aggiornamento S352 (10/02/26)
- **stato.md:** 148 righe, OK. MA OBSOLETO: aggiornato a S321 (30/01/26) - NON riflette S337-S354!
- **Decisioni:** SI (sezione dedicata con PERCHE)
- **Prossima sessione:** SI (S354 - CervellaBrasil)
- **FATOS_CONFIRMADOS:** NO - Non necessario per progetto tecnico interno
- **ISSUE:** stato.md fermo a S321 (23 sessioni indietro!)

### 2. miracollo
- **PROMPT_RIPRESA:** 75 righe, OK. Ultimo aggiornamento S300 (20/01/26)
- **stato.md:** 115 righe, OK. Aggiornato a S272 (19/01/26)
- **Decisioni:** NO sezione esplicita
- **Prossima sessione:** NO sezione esplicita (solo "prossimo" generico nei bracci)
- **FATOS_CONFIRMADOS:** NO
- **ISSUE:** PROMPT_RIPRESA non ha sezione DECISIONI ne PROSSIMA SESSIONE esplicite. stato.md fermo a S272 (molto indietro). Il progetto pero e parcheggiato, quindi la stasi potrebbe essere intenzionale.

### 3. contabilita
- **PROMPT_RIPRESA:** 106 righe, OK. Ultimo aggiornamento 12/02/26 (oggi!)
- **stato.md:** 30 righe, OK. MA OBSOLETO: aggiornato a S171 (12/01/26) - dice "focus Miracollo" che non e piu vero
- **Decisioni:** Implicite nella MAPPA v2.0
- **Prossima sessione:** SI (lista chiara con priorita)
- **FATOS_CONFIRMADOS:** NO
- **ISSUE:** stato.md gravemente obsoleto. Dice "focus Miracollo" ma ora il focus e Chavefy/CervellaBrasil. PR dice v2.10.0 + lab-v2 con 8 commit. stato.md non sa nulla di tutto questo.

### 4. cervellabrasil
- **PROMPT_RIPRESA:** 82 righe, OK. Aggiornato oggi (S359)
- **stato.md:** MANCA COMPLETAMENTE
- **Decisioni:** SI (checklist dettagliata)
- **Prossima sessione:** SI (Fase 3 - Execucao, 6 step)
- **FATOS_CONFIRMADOS:** SI - Unico progetto che ce l'ha! In `~/Developer/CervellaBrasil/docs/FATOS_CONFIRMADOS.md`
- **ISSUE:** Manca stato.md. Con 60+ docs e 11 pesquisas, un stato.md sarebbe molto utile.

### 5. chavefy
- **PROMPT_RIPRESA:** 98 righe, OK. Aggiornato oggi (S354+)
- **stato.md:** 117 righe, OK. Aggiornato oggi (S354+)
- **Decisioni:** SI (tabella con "por que")
- **Prossima sessione:** SI (7 step Fase 0)
- **FATOS_CONFIRMADOS:** NO
- **ISSUE:** Nessun problema critico. Progetto ben documentato.

### 6. cervellacostruzione
- **PROMPT_RIPRESA:** 89 righe, OK. Aggiornato S337 (04/02/26)
- **stato.md:** 112 righe, OK. Aggiornato S333 (03/02/26)
- **Decisioni:** SI (tabella con perche)
- **Prossima sessione:** SI (4 step + viaggio Aprile)
- **FATOS_CONFIRMADOS:** NO
- **ISSUE:** Nessun problema critico. Progetto in attesa viaggio.

---

## PROMPT_RIPRESA_MASTER

- **Righe:** 54
- **Aggiornato:** 10/02/26 S338
- **PROBLEMI GRAVI:**
  1. **MANCANO 2 PROGETTI:** cervellabrasil e chavefy NON sono nella tabella!
  2. **Date obsolete:** Miracollo dice "2026-01-30" ma PR dice S300 (20/01). Contabilita dice "2026-01-20 In pausa" ma PR dice S3 (12/02/26) con lavoro attivo.
  3. **TL;DR obsoleti:** CervellaSwarm dice "FASE 2 Roadmap Interna" ma siamo a FASE completata. Contabilita dice "In pausa" ma c'e lavoro attivo recente.

---

## FATOS_CONFIRMADOS - STATO COMPLETO

| Progetto | Ha FATOS_CONFIRMADOS? | Path |
|----------|:-:|------|
| CervellaSwarm | NO | - |
| Miracollo | NO | - |
| Contabilita | NO | - |
| **CervellaBrasil** | **SI** | `~/Developer/CervellaBrasil/docs/FATOS_CONFIRMADOS.md` |
| Chavefy | NO | - |
| CervellaCostruzione | NO | - |

**Nota:** Per CervellaBrasil i FATOS sono nel workspace del progetto, NON nello SNCP. Questo e corretto perche il hook subagent li cerca li.

---

## VERDETTO COMPLESSIVO

### Problemi CRITICI (da risolvere)
1. **PROMPT_RIPRESA_MASTER manca 2 progetti** (cervellabrasil + chavefy) - GRAVE
2. **cervellabrasil manca stato.md** - MEDIO
3. **stato.md cervellaswarm obsoleto** di 23 sessioni (S321 vs S354) - MEDIO
4. **stato.md contabilita obsoleto** dice "focus Miracollo" - MEDIO

### Problemi MINORI
5. PROMPT_RIPRESA_MASTER ha date e TL;DR obsoleti per 3 progetti
6. miracollo PROMPT_RIPRESA non ha sezioni Decisioni/Prossima esplicite
7. stato.md miracollo fermo a S272 (ma progetto parcheggiato, accettabile)

### Cosa VA BENE
- Tutti i PROMPT_RIPRESA rispettano il limite 150 righe
- Tutti i stato.md rispettano il limite 500 righe
- Chavefy e il progetto meglio documentato (PR + stato + mapppe)
- CervellaBrasil ha ottimo PR e unico progetto con FATOS_CONFIRMADOS
- CervellaCostruzione ben documentato per un progetto in attesa

### SCORE COMPLESSIVO: 6.5/10
- Struttura OK, ma manutenzione carente su MASTER e stato.md
- 2 progetti nuovi non integrati nel MASTER
- stato.md di 3 progetti obsoleti

---

*Guardiana Ricerca - Audit SNCP - 12 Febbraio 2026*
*"Ogni fonte conta. Ogni dettaglio importa."*
