# DECISIONI SESSIONE 213 - Room Manager

> **Data:** 15 Gennaio 2026
> **Con:** Rafa

---

## DECISIONE 1: Mobile Housekeeping = WebApp (PWA)

```
+================================================================+
|   WEBAPP invece di App Store                                    |
+================================================================+

PERCHE':
- Uso INTERNO (staff hotel)
- Niente review App Store
- Niente aggiornamenti manuali
- Ogni uno usa il suo cellulare
- Funziona su QUALSIASI device

COME:
- Progressive Web App (PWA)
- Offline-first (Service Worker)
- Installabile su home screen
- Push notifications

VANTAGGI:
- Deploy immediato
- Aggiornamenti automatici
- Zero costi store
- Funziona anche senza internet

+================================================================+
```

---

## DECISIONE 2: Touchscreen In-Camera (Futuro)

```
+================================================================+
|   IDEA: Touchscreen in ogni camera                              |
+================================================================+

SITUAZIONE ATTUALE:
- Pannello controllo VDA esistente
- Funzionale ma non bello

IDEA RAFA:
- Acquistare 1 touchscreen per test
- Sviluppare UI bellissima
- Se funziona -> tutte le camere

FASE:
- FUTURO (dopo MVP Room Manager)
- Prima studiare, poi implementare

NOTE:
- Questo e' parte di IN-ROOM EXPERIENCE
- Modulo SEPARATO da Room Manager

+================================================================+
```

---

## DECISIONE 3: Studio Nonius TV System

```
+================================================================+
|   NONIUS - Sistema TV Interattiva Esistente                     |
+================================================================+

COSA C'E' OGGI:
- TV connesse a internet in ogni camera
- "Chromecast" Nonius
- Canali TV via internet
- Template iniziale all'accensione:
  * Info zona
  * Temperatura
- QR code per:
  * Netflix
  * YouTube
  * Casting da cellulare ospite

LINKS:
- https://noniussolutions.com/it/tv-interattiva-per-hotel/
- https://noniussolutions.com/it/

PROBLEMA RAFA:
- Sistema "bloccato"
- Poco personalizzabile
- Vogliamo qualcosa di NOSTRO

IDEA FUTURA:
- Studiare Nonius API (se esistono)
- Capire cosa possiamo personalizzare
- Eventualmente SOSTITUIRE con sistema nostro

+================================================================+
```

---

## ORGANIZZAZIONE MODULI

```
+================================================================+
|   Room Manager vs In-Room Experience                            |
+================================================================+

ROOM MANAGER (MVP ora):
├── Target: STAFF hotel
├── Funzioni:
│   ├── Housekeeping status
│   ├── Activity log
│   ├── Room blocks
│   └── PWA Housekeeping
└── Focus: Gestione operativa

IN-ROOM EXPERIENCE (Futuro):
├── Target: OSPITI
├── Funzioni:
│   ├── Touchscreen camera
│   ├── TV interattiva
│   ├── Controllo temperatura
│   ├── Info hotel/zona
│   └── Servizi (room service, spa)
└── Focus: Guest experience

COLLEGAMENTO:
- Room Manager -> stato camera
- In-Room Experience -> legge stato, mostra a ospite
- Comunicano via API

+================================================================+
```

---

## ROADMAP AGGIORNATA

```
ORA (Sessione 213+):
└── MVP Room Manager (5 sessioni A-E)
    └── Include: PWA Housekeeping offline-first

PROSSIMO:
└── VDA Integration (temperature read)

FUTURO:
└── In-Room Experience
    ├── Studio Nonius (cosa si puo' fare?)
    ├── Prototipo touchscreen (1 camera test)
    └── Se OK -> roll-out tutte camere

+================================================================+
```

---

*"Una cosa alla volta, fino al 100000%!"*
*Documentato: 15 Gennaio 2026 - Sessione 213*
