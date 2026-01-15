# IN-ROOM EXPERIENCE - Idea Iniziale

> **Data:** 15 Gennaio 2026 - Sessione 213
> **Status:** IDEA - Da studiare dopo MVP Room Manager
> **Origine:** Conversazione con Rafa

---

## LA VISIONE

```
+================================================================+
|                                                                |
|   "Ogni camera ha una TV, un Chromecast, internet...           |
|    Usiamo quello che c'e' per creare qualcosa di BELLO!"       |
|                                                                |
|   Oggi: Nonius (bloccato, limitato)                            |
|   Domani: MIRACOLLO In-Room Experience                         |
|                                                                |
+================================================================+
```

---

## HARDWARE ESISTENTE (per camera)

| Device | Status | Note |
|--------|--------|------|
| TV Smart | Presente | Connessa a internet |
| Nonius Box | Presente | "Chromecast" per TV |
| VDA Panel | Presente | Controllo temperatura/luci |
| Internet | Presente | WiFi hotel |

---

## NONIUS - Sistema Attuale

### Cosa Fa
- Template iniziale all'accensione TV
- Info zona/hotel
- Temperatura
- Canali TV via internet
- QR code per casting Netflix/YouTube

### Links da Studiare
- https://noniussolutions.com/it/tv-interattiva-per-hotel/
- https://noniussolutions.com/it/

### Limitazioni (secondo Rafa)
- Sistema "bloccato"
- Poco personalizzabile
- Non integrato con PMS

---

## IDEA TOUCHSCREEN

### Concept
Sostituire/affiancare il pannello VDA con touchscreen moderno.

### Approccio
1. Acquistare 1 touchscreen per test
2. Sviluppare UI bellissima
3. Testare in 1 camera
4. Se funziona -> roll-out

### Funzionalita Possibili
- Controllo temperatura (via VDA)
- Controllo luci
- Do Not Disturb
- Make Up Room request
- Info hotel
- Ordini room service
- Prenotazione spa
- Meteo locale
- Info attrazioni zona

---

## STUDIO DA FARE

### Fase 1: Ricerca Nonius
```
[ ] Esistono API Nonius?
[ ] Cosa possiamo personalizzare?
[ ] Costi licenza?
[ ] Alternative?
```

### Fase 2: Ricerca Touchscreen
```
[ ] Quali device sul mercato?
[ ] Costi hardware?
[ ] Come comunicano con VDA?
[ ] Esempi hotel simili?
```

### Fase 3: Prototipo
```
[ ] UI design concept
[ ] Tech stack (React? Flutter?)
[ ] Integrazione VDA
[ ] Test 1 camera
```

---

## PRIORITA'

```
ALTA:   MVP Room Manager (ora)
MEDIA:  VDA Integration
BASSA:  In-Room Experience (questo modulo)

Questo modulo e' FUTURO.
Prima completiamo Room Manager!
```

---

## COLLEGAMENTO CON ROOM MANAGER

```
Room Manager                    In-Room Experience
     │                                │
     │  room.status                   │
     │  room.housekeeping_status      │
     │  room.temperature              │
     ├────────────────────────────────┤
     │         SHARED API             │
     │         /api/rooms/{id}        │
     └────────────────────────────────┘
```

---

*"Prima studiare, poi costruire!"*
*Idea documentata: 15 Gennaio 2026 - Sessione 213*
