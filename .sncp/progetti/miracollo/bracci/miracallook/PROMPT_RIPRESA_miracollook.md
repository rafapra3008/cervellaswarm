<!-- DISCRIMINATORE: MIRACOLLOOK EMAIL CLIENT -->
<!-- PORTA: 8002 | TIPO: Email client AI per hotel -->
<!-- PATH: ~/Developer/miracollogeminifocus/miracallook/ -->
<!-- NON CONFONDERE CON: PMS Core (8001), Room Hardware (8003) -->

# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 29 Gennaio 2026 - Sessione 320
> **ROBUSTEZZA:** 9.5/10 - STUDIO GUEST MANAGEMENT COMPLETATO!

---

## SESSIONE 320 - STUDIO GUEST MANAGEMENT PROFESSIONALE COMPLETATO!

```
+================================================================+
|   S320: STUDIATO GUEST MANAGEMENT PROFESSIONALE!                |
|                                                                  |
|   ✅ RICERCA COMPLETATA: Best practices PMS professionali       |
|   ✅ PROBLEMA IDENTIFICATO: Query S319 escludeva 24 ospiti!    |
|   ✅ SOLUZIONE: GuestProfile separato da Booking (1:N)         |
|   ✅ PROPOSTA: Architettura completa 9.5/10 quality            |
|                                                                  |
|   PROSSIMO STEP: Implementare Phase 1 (modello dati)           |
|                                                                  |
|   File creati S320:                                             |
|   - STUDIO_GUEST_MANAGEMENT_BEST_PRACTICES.md (1265 righe!)    |
|   - PROPOSTA_GUEST_MANAGEMENT_PROFESSIONALE.md (723 righe!)    |
+================================================================+
```

### COSA ABBIAMO SCOPERTO S320

| Problema | Soluzione | Impatto |
|----------|-----------|---------|
| Query esclude 24 ospiti | Rimuovere filtro email, tracciare TUTTI | Coverage 60% → 100% |
| Booking = Guest (sbagliato) | Separare GuestProfile da Booking (1:N) | Storico completo |
| Solo email | Multi-canale (Email, SMS, WhatsApp, Manual) | Tutti contattabili |
| Nessun post-stay | Workflow automatico (thank you, review) | +31-40% repeat bookings |

**RIFERIMENTI CHIAVE:**
- Best practices: Mews, Opera, Cloudbeds, RoomRaccoon, Protel
- Modello dati: GuestProfile (permanente) + Stay (transazionale)
- Stati lifecycle: Pre-Arrival → Arrival → In-House → Departure → Post-Stay
- Quality target: 9.5/10 (standard PMS professionali)

**File creati S320:**
- `studi/STUDIO_GUEST_MANAGEMENT_BEST_PRACTICES.md` (1265 righe)
- `studi/PROPOSTA_GUEST_MANAGEMENT_PROFESSIONALE.md` (723 righe)

---

## STATO REALE (29 Gennaio 2026)

```
FASE 0 (Fondamenta)       [####################] 100%
FASE P (Performance)      [####################] 100%
FASE 1 (Email Solido)     [##################..] 92%
FASE 2.0 (Guest Mgmt)     [....................] 0%   ← S320: STUDIATO! Pronto implementare
FASE 2.1 (PMS UI)         [##########..........] 50%  ← S319: CONNESSIONE OK!
FASE 4 (OCR/Check-in)     [##################..] 90%
```

---

## PROSSIMO STEP: IMPLEMENTARE GUEST MANAGEMENT (FASE 2.0)

**✅ STUDIO COMPLETATO S320 - Ora si implementa!**

**PIANO S320:**
1. ✅ Studiato best practices PMS professionali (Mews, Opera, Cloudbeds)
2. ✅ Identificato problema: query esclude 24 ospiti su 40 (60% coverage)
3. ✅ Proposta architettura: GuestProfile + multi-canale + post-stay
4. ⏳ PROSSIMO: Implementare Phase 1 (modello GuestProfile completo)

**FASE 2.0 - GUEST MANAGEMENT (6 giorni):**
1. Modello GuestProfile + Stay (separazione 1:N)
2. Query Master (TUTTI gli ospiti, non solo email)
3. Stati lifecycle completi (Pre-Arrival → Post-Stay)
4. Multi-canale (Email, SMS, WhatsApp, Manual)
5. Post-stay automation (thank you, review, offers)
6. Testing coverage 100% ospiti

**DOPO FASE 2.0:** WireGuard per accesso remoto (SUBROADMAP Fase A)

---

## CONNETTORE ERICSOFT

**Path:** `miracallook/backend/ericsoft/`
**Status:** ✅ FUNZIONANTE (testato S319, solo rete locale)

**Endpoints attuali:**
- `/ericsoft/status` - Health check ✅
- `/ericsoft/bookings/active` - Ospiti in casa ✅ (16 trovati - LIMITATO!)
- `/ericsoft/bookings/search` - Cerca per email
- `/ericsoft/bookings` - Lista prenotazioni

**⚠️ LIMITAZIONE S319:** Query esclude 24 ospiti (filtro email!)

**PROSSIMI ENDPOINT S320 (Guest Management):**
- `/api/guests/all` - TUTTI gli ospiti (100% coverage)
- `/api/guests/search?email=X` - Cerca per email
- `/api/guests/search?phone=X` - Cerca per telefono
- `/api/guests/{id}` - Dettagli singolo ospite
- `/api/guests/post-stay?days=7` - Ospiti partiti (post-stay marketing)

**Funziona:** Porta 54081, filtro cancellazioni, performance OK
**Serve:** Guest Management completo (S320), WireGuard (remoto), Cache Redis

---

## FILE CHIAVE

| File | Cosa |
|------|------|
| **MAPPA_STRATEGICA_MIRACOLLOOK.md** | Visione completa (AGGIORNATA S320!) |
| **SUBROADMAP_ERICSOFT_INTEGRATION.md** | Piano 6 fasi (AGGIORNATA S320!) |
| **STUDIO_GUEST_MANAGEMENT_BEST_PRACTICES.md** | **NUOVO S320!** Best practices PMS (1265 righe) |
| **PROPOSTA_GUEST_MANAGEMENT_PROFESSIONALE.md** | **NUOVO S320!** Architettura 9.5/10 (723 righe) |
| NORD_MIRACOLLOOK.md | Direzione (DA CREARE!) |
| `backend/ericsoft/` | Connettore SQL |

---

## ARCHITETTURA

```
Ericsoft DB (200.5:54081) → Server Gateway → WireGuard → Miracollook
                                                              ↓
                                                         Cache Redis
                                                              ↓
                                                           API REST
```

---

## SESSIONI PRECEDENTI

| Sessione | Cosa |
|----------|------|
| **S320** | 📚 **STUDIO GUEST MANAGEMENT COMPLETATO! 1988 righe ricerca!** |
| S319 | Connessione funzionante (porta 54081, 16 ospiti) |
| S318 | Studio architettura + Subroadmap Ericsoft |
| S317 | Connettore Ericsoft + Mappa Strategica |
| S316 | Schema DB + User READ-ONLY |
| S315 | Credenziali + Backup DB |

---

*"Studio professionale completato - ora implementiamo!"*
*Cervella Docs & Rafa - Sessione 320*
