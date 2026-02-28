# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 28 Febbraio 2026 - Sessione 219
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

**Questo file e' un PUNTATORE. La source of truth e' la versione canonica.**

Per il contesto completo:
```
CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md
```

## Quick Status S219

| Cosa | Stato |
|------|-------|
| Produzione V2 | v2.11.0 LIVE (INTATTA) |
| V3 VM | v1.16.0 + 33 file (S199) |
| Agent 3 hotel | v2.1.0 + reconcile v1.1.0, HC.io VERDI |
| **SPRING DB** | **3 tipi FUNZIONANTI ma CONTATORI SCOPERTI!** |
| **Script INSERT** | **v4.2.0 S216 - DA AGGIORNARE (contatori!)** |
| **SCOPERTA S219** | **SPRING usa tabelle contatore separate!** |
| **Prossimo** | **Fix script (contatori) -> ripetere C.7 Step 1** |

## S219 - SCOPERTA CRITICA: Tabelle Contatore SPRING

### Cosa e' successo

1. **Step 1 C.7 COMMIT eseguito**: GIR 3 ospiti fittizi SHE INVERNO
   - COMMIT OK, RegisNumero=854, IDDocumento=78712, bilancio 600.00 OK
   - SPRING UI: GIR #854 visibile, 3 ospiti corretti, firma RAFAEL, conti OK
   - **TUTTO PERFETTO nell'INSERT!**

2. **ERRORE durante cancellazione da SPRING UI**:
   - SPRING prova a inserire evento in EQTabCronEvDoc con IdCronEventi=110494
   - Ma la nostra riga ha GIA' IdCronEventi=110494 -> PK duplicata!
   - Le 3 tabelle principali cancellate OK (EQDocCataloghi/Righe/MovContabili)
   - 2 righe orfane rimaste in EQTabCronEvDoc (IdCron=110494 + 110495, IDDoc=78712)

3. **SCOPERTA: SPRING usa tabelle contatore SEPARATE!**

   | Contatore | Tabella SPRING | Il nostro metodo (SBAGLIATO) |
   |-----------|---------------|------------------------------|
   | IdCronEventi | **`EQTabCronEventi`** | MAX+1 da EQTabCronEvDoc |
   | RegisNumero | **`EQProgNumerazioniDoc`** (CodClasseNumerazione=90) | MAX+1 da EQDocCataloghi |

   Il nostro script calcolava MAX+1 dalla tabella dati. SPRING legge da tabelle contatore.
   Quando i numeri coincidono va bene, ma quando SPRING prova a usare il "suo" prossimo numero
   e lo trova gia' occupato dalla nostra riga -> collisione!

4. **Discovery script eseguiti su HPTERMINAL01**:
   - `spring_find_numeratori.py` v1.0.0: scan 5414 tabelle, trovato EQTabCronEventi
   - `spring_study_contatori.py` v1.0.0: approfondimento (DA ESEGUIRE/IN CORSO)
   - Report: `SPRING_NUMERATORI_20260228_1535.txt` su Desktop HPTERMINAL01

### Dati chiave dal discovery

- `EQTabCronEventi.IdCronEventi = 110493` (1 riga) -> il contatore di SPRING!
- `EQProgNumerazioniDoc` ha 116 righe, CodClasseNumerazione=90 = il nostro tipo
- MAX(IdCronEventi) in EQTabCronEvDoc ora e' 110495 (le 2 orfane)
- IDDocumento=78712: 0 righe in Cataloghi/Righe/MovContabili, 2 righe orfane in CronEvDoc

## Documenti SPRING

| Documento | Path | Versione |
|-----------|------|----------|
| Bibbia INSERT | `docs/SPRING_INSERT_STUDIO.md` | **S219 (SCOPERTA contatori!)** |
| Bibbia logica | `docs/SPRING_LOGICA_CONTABILE.md` | v1.5.0 S217 |
| Subroadmap C.7 | `docs/SUBROADMAP_C7_COMMIT_TEST.md` | **S219 (Step 1 risultato + blocco)** |
| Script INSERT | `scripts/spring_insert_hotel.py` | v4.2.0 S216 (**DA AGGIORNARE!**) |
| Script planner | `scripts/spring_day_planner.py` | v1.1.0 S217 |
| **Script discovery** | `scripts/spring_find_numeratori.py` | **v1.0.0 S219 (NUOVO)** |
| **Script contatori** | `scripts/spring_study_contatori.py` | **v1.0.0 S219 (NUOVO)** |

## Prossimi step (S219 continuazione o S220)

1. **Analizzare output `spring_study_contatori.py`** (da eseguire su HPTERMINAL01)
   - Capire struttura completa EQTabCronEventi
   - Verificare se EQProgNumerazioniDoc ha riga per 2026/CodClasse=90
   - Confrontare contatori vs MAX reali
2. **Pulire orfani**: 2 righe in EQTabCronEvDoc per IDDoc=78712 (serve GRANT DELETE)
3. **Fix script INSERT v4.3.0**: leggere/aggiornare tabelle contatore dopo INSERT
   - Leggere IdCronEventi da EQTabCronEventi (non MAX da EQTabCronEvDoc)
   - Aggiornare EQTabCronEventi dopo INSERT
   - Verificare se RegisNumero va aggiornato in EQProgNumerazioniDoc
   - Servono GRANT UPDATE su EQTabCronEventi + EQProgNumerazioniDoc
4. **Audit Guardiana** su script v4.3.0
5. **Ripetere C.7 Step 1** con script corretto
6. Continuare Step 2-4 della subroadmap

## Lezioni Apprese (Sessione 219)

### Cosa ha funzionato bene
- **Approccio progressivo confermato**: Step 1 con dati fittizi ha trovato il bug PRIMA di dati reali
- **Script discovery efficace**: scan 5414 tabelle ha trovato la tabella contatore
- **INSERT perfetto**: la GIR era corretta al 100% in SPRING UI - il problema e' solo nei contatori

### Cosa non ha funzionato
- **MAX+1 sbagliato per IdCronEventi**: assumevamo che SPRING usasse MAX dalla tabella dati, ma usa tabella contatore separata
- **Assunzione "ZERO DEFAULT" su EQTabCronEvDoc**: SPRING inserisce solo 12/20 colonne (8 hanno default)

### Pattern CONFERMATO (da S218 -> S219)
- **Test progressivo salva**: OGNI volta che testiamo con dati fittizi prima, troviamo bug prima di toccare dati reali. Evidenza: S209 (SegnoContabile), S215 (colonne fantasma), S219 (contatori). Azione: **PROMUOVERE a pattern validato!**
