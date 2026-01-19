INIZIA SESSIONE -> Miracollo PMS

Ciao! Oggi lavoriamo su MIRACOLLO PMS (porta 8001) - il sistema alberghiero.
NON Miracollook (quello è il client email, porta 8002).

STATO ATTUALE:
- PMS Core: 90% LIVE su miracollo.com
- Modulo Finanziario: 75% completato
  - Ricevute PDF: 100% REALE
  - Checkout UI: 100% REALE
  - Scontrini RT: 90% (adapter SOAP fixato, test su stampante Bar da fare)
  - Fatture XML: 40% (GUIDA COMPLETA, manca implementazione)

FOCUS OGGI: FASE 3 - FATTURE XML

Prossimi step concreti:
1. Generare 1 XML test (fattura 200/NL)
2. Validare con tool online (es. fattureincloud validator)
3. Test import in SPRING (con contabilista quando possibile)

DATI FISCALI (già estratti):
- P.IVA: 00658350251
- Denominazione: Famiglia Pra Srl
- Regime: RF01 (ordinario)
- SPRING: 3.5.02A (server locale)
- Numerazione test: 200/NL in poi

FILE CHIAVE:
- Guida: .sncp/progetti/miracollo/guide/GUIDA_FATTURE_XML_MIRACOLLO.md
- PROMPT_RIPRESA: .sncp/progetti/miracollo/bracci/pms-core/PROMPT_RIPRESA_pms-core.md
- Subroadmap: docs/roadmap/SUBROADMAP_FASE3_FATTURE_XML.md

Quando sei pronta, leggi la guida fatture e iniziamo!
