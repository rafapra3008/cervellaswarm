# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 21 Febbraio 2026 - Sessione 125
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S125: Studio Qualita Dati + PAYMENT_MAP Multi-Hotel

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | LIVE - v3.contabilitafamigliapra.it, porta 8003, Fortezza attiva |
| **V3 Transformer** | **v1.2.0 DEPLOYATO** - PAYMENT_MAP multi-hotel (NL + SHE) |
| **Agent NL** | ATTIVO v1.2.0 - watermark 4007, HC.io VERDE + Telegram, 1h auto |
| **Agent SHE** | ATTIVO v1.2.0 - watermark 21623, HC.io VERDE + Telegram, 1h auto |
| **Agent HP** | PENDING (FASE I.2 - serve info da Rafa) |
| **Lab v2** | INTOCCATO, frozen S87 |
| **Test** | **1370 portale** + 276 agent = **1646 PASS** (0 warnings) |

---

## S125 - Cosa e' stato fatto

| Step | Cosa | Risultato |
|------|------|-----------|
| **1. Telegram HC.io** | Rafa ha configurato | SHE + NL, notifica test OK |
| **2. Studio PAYMENT_MAP** | Script `research_payment_types.py` su SHE + NL | Scoperto 5 codici SHE mancanti |
| **3. Fix PAYMENT_MAP** | Aggiunto CAR, BN, BNU, BONUS, BAN | EricsoftTransformer v1.1.0 -> v1.2.0, +5 test |
| **4. Guardiana R1** | Audit PAYMENT_MAP | **9.5/10** APPROVED |
| **5. Studio nomi** | Script `research_name_resolution.py` su SHE + NL | Nomi OK 99.9%, 3 path COALESCE funziona |
| **6. Deploy VM** | Transformer v1.2.0 + fix record Gandin Leone | backup + deploy + restart + health OK |
| **7. Guardiana R2** | Audit deploy | **9.5/10** APPROVED |

---

## Scoperte S125 - Dati REALI

### Codici pagamento per hotel (PAYMENT_MAP)

```
COMUNI:      BK, CAP, CON, U100M, U100V, VOU
SOLO NL:     POS, BONC, BONU, PAGON, CONDINL, ACC
SOLO SHE:    CAR (4264!), BN (1375), BNU (13), BONUS (91), BAN (7)
SHE ESCLUSI: DEP (6, solo INC), TESS (0), SOP (0), TAS (0)
```

### Name resolution (3 path)

```
Path 1 (SchedaContoAnagrafica): SHE 99.0%, NL 86.0% - NULL per Gruppo (Tipo=G)
Path 2 (Scheda.IdAnagraficaPrenotato): SHE 99.7%, NL 99.8% - IL PIU AFFIDABILE
Path 3 (MovimentoCassa.IdAnagrafica): SHE 0.1%, NL 0.1% - QUASI INUTILE
COALESCE finale: SHE 99.9%, NL 99.8% - FUNZIONA
```

### DB V3 SHE VM (post-deploy S125)

```
4 caparre ericsoft: Gemelli(BK), Scaggiante(BK), Rossi(U100M), Gandin Leone(BN->BONIFICO)
4 giroconti ericsoft: Lawrence, Serejko, Favaro, Vandamme
1 marker: WATERMARK_INIT (importo 0, skipped - by design)
Watermark attuale: 21623
```

---

## Prossimi step (S126)

```
1. [ ] FASE I.2 HP: serve da Rafa -> IP server, porta SQL, nome DB, VPN
2. [ ] HP: stessa procedura SHE (discovery, reader, Python, agent, sync, HC.io, scheduler)
3. [ ] Dopo HP: monitor 48h tutti e 3 hotel, poi FASE I chiusa
4. [ ] Studio codici pagamento HP (research_payment_types.py --pyodbc)
5. [ ] Aggiungere codici HP al PAYMENT_MAP + deploy
```

---

## Mappa Sistema (aggiornata S125)

```
                    PRODUZIONE (INTATTA)
                    contabilitafamigliapra.it:443
                    v2.11.0, porta 8000
                    |
    VM Google Cloud (cervello-contabilita)
    35.193.39.185, e2-medium, $28/mese
                    |
        +-----------+-----------+
        |                       |
    LAB V2                  V3 (lab-v3)
    INTOCCATO               v3.contabilita...
    frozen S87              porta 8003
                            FORTEZZA ATTIVA
                            Transformer v1.2.0
                            |
                +-----------+-----------+
                |           |           |
            Hotel NL    Hotel SHE   Hotel HP
            ATTIVO      ATTIVO      PENDING
            pymssql     pyodbc      ???
            WM 4007     WM 21623    Step I.2
            HC.io+TG    HC.io+TG    serve info
            1h auto     1h auto     da Rafa
```

---

## Mappa Connessione Per-Hotel

```
NL:  192.168.200.5:54081 -> DB PRA    -> pymssql -> Agent v1.2.0 -> WM 4007  -> HC.io+TG -> 1h auto
SHE: 127.0.0.1:1433      -> DB SUITE  -> pyodbc  -> Agent v1.2.0 -> WM 21623 -> HC.io+TG -> 1h auto
HP:  ???                  -> DB ???    -> ???     -> Agent v1.3.0 -> PENDING
```

---

## Lezioni S125

- **PAYMENT_MAP era solo NL**: Costruito in FASE B su dati NL. Ogni hotel ha codici diversi - SEMPRE fare research_payment_types.py prima di attivare un hotel
- **research_payment_types.py**: Script riutilizzabile per HP (supporta --pyodbc)
- **research_name_resolution.py**: Diagnostica 3 path nomi - Path 2 e il piu affidabile
- **Record "skipped" con importo 0**: Era il WATERMARK_INIT marker di S124, non un bug
- **data_conferma_bonifici**: Quando si cambia circuito a BONIFICO, ricordarsi di popolare anche data_conferma
- **P1 vs P2 nomi diversi**: Normale - P1=ospite camera, P2=prenotante. COALESCE prende P1 (corretto)

---

## Dove leggere

| Cosa | File |
|------|------|
| EricsoftTransformer v1.2.0 | `backend/processors/ericsoft_transformer.py` |
| research_payment_types.py | `agent/scripts/research_payment_types.py` |
| research_name_resolution.py | `agent/scripts/research_name_resolution.py` |
| sync_she.bat v1.2.0 | `agent/scripts/sync_she.bat` |
| Piano FASE I SHE | `docs/FASE_I_PIANO_SHE.md` |
| Checklist HP | Sezione "Prossimi step" sopra |

---

*S125: Studio qualita dati + PAYMENT_MAP multi-hotel + deploy VM. Prossimo: FASE I.2 HP.*

