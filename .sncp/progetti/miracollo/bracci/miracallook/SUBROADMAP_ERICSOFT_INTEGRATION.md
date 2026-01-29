# SUBROADMAP: Integrazione Ericsoft Completa

> **Creata:** 29 Gennaio 2026 - Sessione 318
> **Obiettivo:** Miracollook legge dati Ericsoft da OVUNQUE, robusto e professionale
> **Approccio:** Come fanno i professionisti (Bedzzle/MyReception)

---

## VISIONE

```
+================================================================+
|                                                                  |
|   Quando arriva una email, Miracollook SA CHI È L'OSPITE!       |
|                                                                  |
|   - Nome, camera, check-in/out                                  |
|   - Storico prenotazioni                                        |
|   - Contesto per risposta AI intelligente                       |
|                                                                  |
|   Funziona da OVUNQUE: hotel, casa, cloud                       |
|                                                                  |
+================================================================+
```

---

## ARCHITETTURA TARGET

```
┌─────────────────────────────────────────────────────────────────┐
│                      RETE HOTEL (192.168.200.x)                  │
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │   ERICSOFT   │         │   SERVER     │                      │
│  │   SQL Server │◄────────│   GATEWAY    │                      │
│  │  (200.5)     │  SQL    │  (WireGuard) │                      │
│  └──────────────┘         └──────┬───────┘                      │
│                                   │                              │
└───────────────────────────────────┼──────────────────────────────┘
                                    │
                                    │ WireGuard VPN (criptato)
                                    │
┌───────────────────────────────────┼──────────────────────────────┐
│                      OVUNQUE (Internet)                          │
│                                   │                              │
│                           ┌───────▼───────┐                      │
│                           │  MIRACOLLOOK  │                      │
│                           │    BACKEND    │                      │
│                           │               │                      │
│                           │ - Connector   │                      │
│                           │ - Cache Redis │                      │
│                           │ - API REST    │                      │
│                           └───────┬───────┘                      │
│                                   │                              │
│                           ┌───────▼───────┐                      │
│                           │   FRONTEND    │                      │
│                           │ + WhatsApp    │                      │
│                           │ + Future      │                      │
│                           └───────────────┘                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## FASI

### FASE A: Accesso Remoto (WireGuard)
**Obiettivo:** Miracollook raggiunge Ericsoft da OVUNQUE
**Effort:** 4-6 ore
**Costo:** €0 (open source)

| Step | Task | Dettagli |
|------|------|----------|
| A.1 | Identificare server gateway | Server sempre acceso nella rete 200 |
| A.2 | Installare WireGuard server | `apt install wireguard` o equivalente |
| A.3 | Configurare WireGuard | Generare chiavi, configurare peer |
| A.4 | Port forwarding router | Aprire porta UDP (default 51820) |
| A.5 | Installare WireGuard client | Sul Mac/server Miracollook |
| A.6 | Test connessione | `ping 192.168.200.5` da remoto |

**Deliverable:** Miracollook può raggiungere rete 200 da ovunque

**Documentazione da creare:**
- `docs/WIREGUARD_SETUP.md` - Guida installazione
- `docs/WIREGUARD_TROUBLESHOOTING.md` - Problemi comuni

---

### FASE B: Test Connessione Reale
**Obiettivo:** Validare che il connettore S317 funziona
**Effort:** 2 ore
**Dipende da:** FASE A

| Step | Task | Dettagli |
|------|------|----------|
| B.1 | Configurare .env | Credenziali Ericsoft (già documentate) |
| B.2 | Avviare backend | `uvicorn main:app --port 8002` |
| B.3 | Test /ericsoft/status | Verifica connessione |
| B.4 | Test /ericsoft/bookings | Verifica dati reali |
| B.5 | Test /ericsoft/bookings/active | Ospiti in casa ORA |
| B.6 | Test /ericsoft/bookings/search | Cerca per email |

**Success Criteria:**
- [ ] Status 200 su tutti gli endpoint
- [ ] Dati prenotazioni REALI visibili
- [ ] Response time < 500ms
- [ ] Circuit breaker funziona (test con DB offline)

**Deliverable:** Screenshot/log dei test passati

---

### FASE C: Cache Layer (Redis)
**Obiettivo:** Performance + resilienza
**Effort:** 4 ore
**Dipende da:** FASE B

| Step | Task | Dettagli |
|------|------|----------|
| C.1 | Setup Redis | Docker o installazione locale |
| C.2 | Creare CacheService | `backend/services/cache.py` |
| C.3 | Cache guest by email | TTL 1 ora |
| C.4 | Cache active bookings | TTL 15 minuti |
| C.5 | Cache invalidation | Logica pulizia |
| C.6 | Fallback se Redis down | Graceful degradation |

**Schema Cache:**
```
ericsoft:guest:{email}     → GuestBooking JSON (TTL 1h)
ericsoft:active:{date}     → List[GuestBooking] JSON (TTL 15min)
ericsoft:health            → Status JSON (TTL 1min)
```

**Deliverable:** Cache funzionante con test

---

### FASE D: Guest Management Service (NUOVO S320)
**Obiettivo:** Gestione professionale TUTTI gli ospiti (non solo con email)
**Effort:** 6 giorni
**Dipende da:** FASE C

**NOTA S320:** Questa fase è stata COMPLETAMENTE ridisegnata dopo studio best practices PMS professionali.

| Step | Task | Dettagli |
|------|------|----------|
| D.1 | Modello GuestProfile completo | `models/guest_profile.py` - Separazione Guest/Booking |
| D.2 | Query Master (tutti ospiti) | Query Ericsoft che traccia TUTTI (con/senza email) |
| D.3 | Deduplicazione intelligente | Merge soggiorni per IdAnagrafica |
| D.4 | Multi-channel contacts | Email, SMS, WhatsApp, Manual fallback |
| D.5 | Stati lifecycle mapping | Pre-Arrival → Post-Stay completi |
| D.6 | Post-stay automation | Thank you, review, future booking offers |
| D.7 | Endpoint /guests/* | API REST completa gestione ospiti |
| D.8 | Test con dati reali | Validare coverage 100% ospiti |

**RICERCHE S320:**
- `studi/STUDIO_GUEST_MANAGEMENT_BEST_PRACTICES.md` (1265 righe)
- `studi/PROPOSTA_GUEST_MANAGEMENT_PROFESSIONALE.md` (723 righe)

**API Design (AGGIORNATO S320):**
```
GET /api/guests/all
Response:
{
  "guests": [
    {
      "id_anagrafica": 123,
      "nome_completo": "Mario Rossi",
      "contacts": [
        {"channel": "email", "value": "mario@example.com", "primary": true},
        {"channel": "whatsapp", "value": "+393331234567", "primary": false}
      ],
      "current_stay": {
        "room": "101",
        "check_in": "2026-01-30",
        "check_out": "2026-02-02",
        "status": "in_house"
      },
      "total_stays": 3,
      "is_repeat_guest": true
    }
  ],
  "total": 40,
  "coverage": "100%"
}

GET /api/guests/search?email=mario@example.com
GET /api/guests/search?phone=3331234567
GET /api/guests/{id_anagrafica}
GET /api/guests/post-stay?days=7  # Ospiti partiti ultimi 7gg
```

**Deliverable:** API completa con GuestProfile model + test coverage 100% ospiti

---

### FASE E: Frontend GuestContextCard
**Obiettivo:** UI che mostra contesto ospite quando leggi email
**Effort:** 6 ore
**Dipende da:** FASE D

| Step | Task | Dettagli |
|------|------|----------|
| E.1 | Creare GuestContextCard | `components/GuestContextCard.tsx` |
| E.2 | Integrare in EmailView | Mostra card quando email selezionata |
| E.3 | Loading state | Skeleton mentre carica |
| E.4 | Empty state | Messaggio se ospite non trovato |
| E.5 | Error state | Gestione errori graceful |
| E.6 | Styling | Design coerente con Miracollook |

**UI Mockup:**
```
┌─────────────────────────────────────┐
│  🏨 Ospite: Mario Rossi             │
├─────────────────────────────────────┤
│  📅 Check-in:   30 Gen 2026         │
│  📅 Check-out:  02 Feb 2026         │
│  🚪 Camera:     101                 │
│  📊 Status:     ✅ Confermato       │
│                                     │
│  [Vedi Prenotazione] [Storico]      │
└─────────────────────────────────────┘
```

**Deliverable:** Componente funzionante in UI

---

### FASE F: Test End-to-End + Documentazione
**Obiettivo:** Tutto funziona insieme, documentato
**Effort:** 4 ore
**Dipende da:** FASE E

| Step | Task | Dettagli |
|------|------|----------|
| F.1 | Test E2E completo | Flow: email → enrichment → UI |
| F.2 | Test da remoto | Verifica funziona fuori hotel |
| F.3 | Test resilienza | Redis down, DB down, VPN down |
| F.4 | Documentazione utente | Come usare la feature |
| F.5 | Documentazione tecnica | Architettura, troubleshooting |
| F.6 | Update NORD + PROMPT_RIPRESA | Stato aggiornato |

**Deliverable:** Feature completa e documentata

---

## FUTURO (Post-MVP)

### FASE G: Multi-PMS Adapter Pattern
**Quando:** Dopo validazione con Ericsoft
**Obiettivo:** Supportare altri PMS (Opera, Mews, Protel)

```python
# Architettura Adapter
class PMSAdapter(ABC):
    @abstractmethod
    async def get_guest_by_email(self, email: str) -> Guest

    @abstractmethod
    async def get_active_bookings(self) -> List[Booking]

class EricsoftAdapter(PMSAdapter):
    # Implementazione SQL diretta (esistente)

class OperaAdapter(PMSAdapter):
    # Implementazione via API REST

class MewsAdapter(PMSAdapter):
    # Implementazione via API REST
```

### FASE H: Webhook Real-time
**Quando:** Se Ericsoft aggiunge supporto o per PMS cloud
**Obiettivo:** Notifiche push invece di polling

### FASE I: Analytics Dashboard
**Quando:** Dopo accumulo dati
**Obiettivo:** Insights su ospiti, comunicazioni, trend

---

## TIMELINE STIMATA

```
FASE A (WireGuard)         ████████░░░░  4-6h      Sessione 319 (NEXT)
FASE B (Test)              ████░░░░░░░░  2h        Sessione 319
FASE C (Cache)             ████████░░░░  4h        Sessione 320-321
FASE D (Guest Mgmt)        ████████████  6 giorni  Sessione 321-325 (NUOVO!)
FASE E (Frontend)          ████████████  6h        Sessione 326-327
FASE F (E2E + Docs)        ████████░░░░  4h        Sessione 327

TOTALE MVP:                              ~7-8 giorni (~8-10 sessioni)
                                         (aumentato per Guest Management completo)
```

---

## DIPENDENZE

```
FASE A ──► FASE B ──► FASE C ──► FASE D ──► FASE E ──► FASE F
  │                                                       │
  └───────────────── BLOCCO CRITICO ─────────────────────┘

Se FASE A non funziona, tutto si ferma!
Priorità MASSIMA: risolvere accesso rete.
```

---

## RISCHI E MITIGAZIONI

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Router hotel non permette port forwarding | Media | Alto | Usare Tailscale come fallback |
| Server gateway non disponibile | Bassa | Alto | Identificare alternative |
| Schema Ericsoft cambia | Bassa | Medio | Test automatici, monitoring |
| Performance query lente | Media | Medio | Cache Redis, query optimization |
| Redis down | Bassa | Basso | Fallback a query dirette |

---

## CHECKLIST PRE-INIZIO

- [ ] Identificato server gateway nella rete 200
- [ ] Accesso admin al server gateway
- [ ] Credenziali Ericsoft verificate (S315)
- [ ] Router hotel accessibile per port forwarding
- [ ] Backup piano (Tailscale) se WireGuard non funziona

---

## METRICHE SUCCESSO

| Metrica | Target | Come Misurare |
|---------|--------|---------------|
| Tempo risposta enrichment | < 200ms | Log + monitoring |
| Accuracy match email→guest | > 95% | Test su dati reali |
| Uptime connessione | > 99% | Health checks |
| Cache hit rate | > 80% | Redis stats |

---

## NOTE

**Approccio validato:** MyReception/Bedzzle usa lo stesso pattern (SQL diretto + API layer).

**Differenziatore:** Miracollook aggiunge AI (email intelligenti, preventivi automatici, OCR).

**Filosofia:** Un passo alla volta, fatto BENE. Ogni fase completa prima di procedere.

---

*"Come fanno i professionisti - ma con il nostro tocco AI!"*
*Cervella & Rafa - Sessione 318*
