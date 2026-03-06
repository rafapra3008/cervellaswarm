# Script "La Nonna con le Ricette" - Demo Definitiva

> **Autrice:** Cervella Regina - Sessione 438
> **Data:** 6 Marzo 2026
> **Scopo:** Dialogo ESATTO parola per parola della demo che guida TUTTE le decisioni architetturali di FASE E.
> **Durata target:** 3 minuti dal primo messaggio al codice funzionante.

---

## IL SETUP

**Chi:** Maria, 68 anni, nonna italiana. Non ha mai programmato.
**Dove:** Terminal con `lu chat --lang it` attivo.
**Cosa sa:** Ha sentito dal nipote che "puoi dire al computer cosa fare e lui lo fa, con la PROVA che funziona."

---

## ATTO 1: L'INTENZIONE (30 secondi)

### Scena 1.1 - Il sistema si presenta

```
$ lu chat --lang it

  Lingua Universale - Chat Interattiva
  "Dimmi cosa vuoi creare e io lo costruisco, con la prova che funziona."

  Lingue: italiano | portugues | english
  Digita 'aiuto' per la guida. 'esci' per uscire.

>
```

### Scena 1.2 - Maria descrive

```
> Voglio un sistema per le ricette della nonna. Il cuoco chiede alla
  dispensa cosa c'e, la dispensa risponde, e il cuoco decide cosa cucinare.
```

### Scena 1.3 - IntentBridge capisce e chiarisce

```
  Ho capito! Stai descrivendo un sistema con 2 ruoli:

    Cuoco     - chiede ingredienti, decide la ricetta
    Dispensa  - risponde con cosa c'e disponibile

  Alcune domande per essere precisa:
  1. Il cuoco puo anche aggiungere ricette nuove?
  2. Qualcuno puo cancellare ricette?
  3. Quanto sei sicura di questa struttura?

> Si, il cuoco aggiunge ricette. Ma nessuno puo cancellare per sbaglio!
  Sono sicurissima.
```

**Sotto il cofano (non visibile a Maria):**
```
[IntentBridge] NL -> IntentDraft:
  protocol "Gestione Ricette"
    roles: Cuoco, Dispensa
    Cuoco asks Dispensa for "ingredienti disponibili"
    Dispensa returns list of "ingrediente"
    when Cuoco decides:
      "cucinare" -> Cuoco sends "ricetta scelta" to Dispensa
      "aggiungere" -> Cuoco sends "nuova ricetta" to Dispensa
    requires no_deletion
    requires always_terminates
    confidence >= high
```

---

## ATTO 2: LA SPECIFICA (45 secondi)

### Scena 2.1 - IntentBridge mostra il protocollo

```
  Perfetto! Ecco il protocollo che ho costruito:

  +------------------------------------------------------------+
  |  protocol GestioneRicette                                  |
  |    roles: Cuoco, Dispensa                                  |
  |                                                            |
  |    Cuoco asks Dispensa for "ingredienti disponibili"       |
  |    Dispensa returns list of "ingrediente"                  |
  |    when Cuoco decides:                                     |
  |      "cucinare":                                           |
  |        Cuoco sends "ricetta scelta" to Dispensa            |
  |      "aggiungere":                                         |
  |        Cuoco sends "nuova ricetta" to Dispensa             |
  |                                                            |
  |    requires always_terminates                              |
  |    requires no_deadlock                                    |
  |    requires no_deletion                                    |
  |    confidence >= high                                      |
  +------------------------------------------------------------+

  Proprieta di sicurezza:
    - Il sistema finisce SEMPRE (non si blocca mai)
    - Nessun ruolo resta in attesa per sempre
    - Nessuna ricetta viene cancellata

  Questo ti sembra giusto?

> Si!
```

### Scena 2.2 - Maria modifica (opzionale)

```
> Aspetta, voglio anche che solo il cuoco puo aggiungere ricette,
  non la dispensa.

  Capito! Aggiungo una restrizione sui permessi:
    requires role_exclusive("aggiungere", Cuoco)

  Ora solo il Cuoco puo aggiungere ricette. La Dispensa non puo.
  Confermato?

> Si, perfetto!
```

**Sotto il cofano:**
```
[IntentBridge] IntentDraft validato -> parse_intent() B.4
[B.4] IntentParseResult: 2 roles, 4 messages, 1 choice, 4 properties
[B.4] Deterministic parse: ZERO ambiguita, 100% syntactic correctness
```

---

## ATTO 3: LA PROVA (45 secondi)

### Scena 3.1 - Verifica formale

```
  Sto verificando il protocollo con prove matematiche...

  Verifica in corso...
    [1/5] always_terminates    ... PROVATO
    [2/5] no_deadlock          ... PROVATO
    [3/5] no_deletion          ... PROVATO
    [4/5] role_exclusive       ... PROVATO
    [5/5] confidence >= high   ... VERIFICATO

  +------------------------------------------------------------+
  |  TUTTE LE PROPRIETA VERIFICATE                             |
  |  5/5 provate matematicamente                               |
  |  Il tuo sistema e GARANTITO sicuro.                        |
  +------------------------------------------------------------+

  Vuoi vedere il codice Python?

> Si!
```

**Sotto il cofano:**
```
[B.5] spec.check_properties(protocol):
  always_terminates:  PropertyVerdict.PROVED
  no_deadlock:       PropertyVerdict.PROVED
  no_deletion:       PropertyVerdict.PROVED
  role_exclusive:    PropertyVerdict.PROVED
  confidence_min:    PropertyVerdict.PROVED
[Lean4Bridge] lean4_bridge.generate_lean4(protocol) -> lean4_source
```

---

## ATTO 4: IL CODICE (30 secondi)

### Scena 4.1 - Codice generato

```
  Ecco il codice Python certificato:

  --- gestione_ricette.py ---

  class Cuoco:
      def chiedi_ingredienti(self, dispensa):
          """Chiede alla dispensa gli ingredienti disponibili."""
          return self.session.send("ingredienti_disponibili", to=dispensa)

      def decidi(self, ingredienti, scelta, dispensa):
          """Decide se cucinare o aggiungere una ricetta."""
          if scelta == "cucinare":
              return self.session.send("ricetta_scelta", to=dispensa)
          elif scelta == "aggiungere":
              return self.session.send("nuova_ricetta", to=dispensa)

  class Dispensa:
      def rispondi_ingredienti(self):
          """Restituisce la lista degli ingredienti disponibili."""
          return self.session.send("ingrediente_list", to="Cuoco")

  ---

  Il codice implementa ESATTAMENTE il protocollo verificato.
  Ogni metodo segue le regole: chi puo parlare, a chi, in che ordine.

  Vuoi eseguire una simulazione?

> Si!
```

**Sotto il cofano:**
```
[B.3] codegen.generate_python(protocol) -> GeneratedCode
[B.3] 2 classi, 3 metodi, session checker integrato
[B.3] Runtime enforcement: SessionChecker valida ogni messaggio
```

---

## ATTO 5: LA MAGIA (30 secondi)

### Scena 5.1 - Simulazione

```
  Simulazione "Gestione Ricette":

  [Cuoco]    -> Dispensa: "Cosa c'e in dispensa?"
  [Dispensa] -> Cuoco:    "pomodori, basilico, mozzarella, pasta"
  [Cuoco]    decide: "cucinare"
  [Cuoco]    -> Dispensa: "Insalata Caprese!"

  +------------------------------------------------------------+
  |  PROTOCOLLO COMPLETATO CON SUCCESSO                        |
  |                                                            |
  |  Messaggi scambiati: 4                                     |
  |  Violazioni:         0                                     |
  |  Proprieta:          5/5 rispettate                        |
  |  Tempo:              0.003s                                |
  +------------------------------------------------------------+

> Che bello! Posso aggiungere una ricetta?
```

### Scena 5.2 - Seconda simulazione

```
  Certo! Simulazione con "aggiungere":

  [Cuoco]    -> Dispensa: "Cosa c'e in dispensa?"
  [Dispensa] -> Cuoco:    "pomodori, basilico, mozzarella, pasta"
  [Cuoco]    decide: "aggiungere"
  [Cuoco]    -> Dispensa: "Pasta al Pomodoro della Nonna Maria"

  Ricetta aggiunta! Protocollo completato. 0 violazioni.

> E se la dispensa prova a cancellare una ricetta?
```

### Scena 5.3 - La prova di sicurezza

```
  Proviamo:

  [Dispensa] tenta: cancellare "Insalata Caprese"

  VIOLAZIONE RILEVATA!
    Proprieta: no_deletion
    Messaggio: "La cancellazione non e permessa in questo protocollo."
    Azione bloccata.

  Il sistema ha IMPEDITO la cancellazione, come promesso.
  Le prove matematiche non sono solo teoria: FUNZIONANO.

> Incredibile! Grazie!
```

---

## EPILOGO

```
  Riepilogo sessione:
    Tempo totale:    2 minuti 47 secondi
    Protocollo:      GestioneRicette (2 ruoli, 4 messaggi, 5 proprieta)
    Codice:          gestione_ricette.py (salvato)
    Verifiche:       5/5 provate
    Lingua:          italiano

  "Non e magia. E matematica."

  Vuoi creare un altro protocollo?
```

---

## REQUISITI TECNICI ESTRATTI

Ogni scena richiede capacita specifiche dal sistema:

### Da Atto 1 (L'Intenzione):
| Req | Descrizione | Modulo | Status |
|-----|-------------|--------|--------|
| R1 | CLI interattiva `lu chat` con prompt e colori | CLI (`__main__.py`) | DA FARE |
| R2 | Flag `--lang` per scegliere lingua (it/pt/en) | CLI | DA FARE |
| R3 | Traduzione NL italiano -> IntentDraft B.4 | `_intent_bridge.py` | DA FARE |
| R4 | Domande di chiarimento (disambiguazione) | `_intent_bridge.py` | DA FARE |
| R5 | Supporto multi-turno (memoria del dialogo) | `_intent_bridge.py` | DA FARE |

### Da Atto 2 (La Specifica):
| Req | Descrizione | Modulo | Status |
|-----|-------------|--------|--------|
| R6 | Rendering protocollo human-readable in italiano | `_intent_bridge.py` | DA FARE |
| R7 | Spiegazione proprieta in linguaggio naturale | `_intent_bridge.py` | DA FARE |
| R8 | Modifica interattiva del protocollo | `_intent_bridge.py` | DA FARE |
| R9 | `parse_intent()` gia funziona (B.4) | `intent.py` | ESISTE |
| R10 | Mapping nuove proprieta (role_exclusive) | `spec.py` | DA VALUTARE |

### Nuove Proprieta Richieste dalla Demo (P2 Guardiana):
| Req | Descrizione | Modulo | Status |
|-----|-------------|--------|--------|
| R22 | `no_deletion` come nuovo PropertyKind | `spec.py` | DA FARE |
| R23 | `role_exclusive` come nuovo PropertyKind | `spec.py` | DA FARE |

### Da Atto 3 (La Prova):
| Req | Descrizione | Modulo | Status |
|-----|-------------|--------|--------|
| R11 | `check_properties()` gia funziona (B.5) | `spec.py` | ESISTE |
| R12 | `generate_lean4()` gia funziona (Lean4) | `lean4_bridge.py` | ESISTE |
| R13 | Output progressivo delle verifiche (1/5, 2/5...) | `_intent_bridge.py` | DA FARE |
| R14 | Messaggio risultato in lingua target | `errors.py` (3 locales) | PARZIALE |

### Da Atto 4 (Il Codice):
| Req | Descrizione | Modulo | Status |
|-----|-------------|--------|--------|
| R15 | `generate_python()` gia funziona (B.3) | `codegen.py` | ESISTE |
| R16 | Nomi metodi in italiano (non solo inglese) | `codegen.py` | DA FARE |
| R17 | Salvataggio file .py generato | `_intent_bridge.py` | DA FARE |

### Da Atto 5 (La Magia):
| Req | Descrizione | Modulo | Status |
|-----|-------------|--------|--------|
| R18 | Simulazione protocollo con SessionChecker | `checker.py` | ESISTE |
| R19 | Output simulazione narrativo (non tecnico) | `_intent_bridge.py` | DA FARE |
| R20 | Demo violazione (tentativo bloccato) | `checker.py` | ESISTE |
| R21 | Riepilogo sessione con metriche | `_intent_bridge.py` | DA FARE |

### Riepilogo

| Categoria | Esiste | Da Fare | Da Valutare |
|-----------|--------|---------|-------------|
| Core pipeline (B.3/B.4/B.5/A.3/Lean4) | 5 | 0 | 0 |
| IntentBridge (`_intent_bridge.py`) | 0 | 9 | 0 |
| CLI (`__main__.py`) | 0 | 2 | 0 |
| Localizzazione/Multi-lingua | 1 | 2 | 1 |
| Nuove Proprieta (R22-R23) | 0 | 2 | 0 |
| **Totale** | **6** | **15** | **1** |

**Il 27% del lavoro e GIA FATTO.** Il core pipeline esiste e funziona. Serve il layer conversazionale sopra + 2 nuove proprieta in spec.py.

---

## NOTE ARCHITETTURALI (per E.2)

### Pattern Two-Stage (da Req2LTL)
```
Maria parla (NL italiano)
  |
  v
[IntentBridge] traduce in B.4 micro-linguaggio (strutturato)
  |
  v
[B.4 parse_intent()] parser deterministico -> ParseResult
  |
  v
[B.5 check_properties()] verifica formale -> PropertyReport
  |
  v
[Lean4Bridge] prove matematiche -> proof_text
  |
  v
[B.3 generate_python()] codice certificato -> GeneratedCode
  |
  v
[A.3 SessionChecker] esecuzione con enforcement -> simulazione
```

### Conversazione Multi-Turn
```
Turn 1: Maria descrive -> IntentBridge capisce -> chiede chiarimenti
Turn 2: Maria chiarisce -> IntentBridge completa IntentDraft
Turn 3: IntentBridge mostra specifica -> Maria conferma/modifica
Turn 4: Verifica + codice + simulazione (automatico)
```

### Stato Interno (da mantenere tra i turni)
```python
@dataclass
class ChatSession:
    lang: str                    # "it" | "pt" | "en"
    turns: list[Turn]            # storia conversazione
    draft: IntentDraft | None    # bozza protocollo in costruzione
    protocol: Protocol | None    # protocollo verificato
    code: GeneratedCode | None   # codice generato
    phase: ChatPhase             # INTENT | SPEC | VERIFY | CODE | SIM
```

---

> "La nonna non sa cosa sono i session types.
>  Ma sa che le sue ricette sono AL SICURO.
>  E questa e la differenza."

> "Non e sempre come immaginiamo... ma alla fine e il 100000%!"

*Cervella Regina - CervellaSwarm S438*
