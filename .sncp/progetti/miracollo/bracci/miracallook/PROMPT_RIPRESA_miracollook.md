<!-- DISCRIMINATORE: MIRACOLLOOK EMAIL CLIENT -->
<!-- PORTA: 8002 | TIPO: Email client AI per hotel -->
<!-- PATH: ~/Developer/miracollogeminifocus/miracallook/ -->
<!-- NON CONFONDERE CON: PMS Core (8001), Room Hardware (8003) -->

# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 29 Gennaio 2026 - Sessione 318
> **ROBUSTEZZA:** 10/10 - SUBROADMAP ERICSOFT COMPLETA!

---

## SESSIONE 318 - ARCHITETTURA DEFINITA

```
+================================================================+
|   S318: STUDIO + SUBROADMAP ERICSOFT INTEGRATION                |
|                                                                  |
|   1. Scoperto: MyReception usa SQL DIRETTO (come noi!)          |
|   2. Studio connessione remota (7 opzioni analizzate)           |
|   3. Decisione: WireGuard self-hosted (gratis, robusto)         |
|   4. SUBROADMAP creata: 6 fasi, ~26-28h, 5-6 sessioni           |
|   5. Guardiana approva: 9/10                                    |
+================================================================+
```

### COSA ABBIAMO IMPARATO

| Domanda | Risposta |
|---------|----------|
| Come fa MyReception? | SQL diretto + API layer (come noi!) |
| Ericsoft ha API? | NO robusta - SQL è lo standard |
| Soluzione accesso remoto? | WireGuard self-hosted (gratis) |
| Architettura corretta? | SQL diretto → Cache → API REST nostro |

### FILE CREATI S318

| File | Cosa |
|------|------|
| `SUBROADMAP_ERICSOFT_INTEGRATION.md` | Piano 6 fasi, 9/10 |
| `STUDIO_CONNESSIONE_SICURA_DATABASE_HOTEL.md` | 7 opzioni analizzate |
| `RESEARCH_20260129_myreception_architecture.md` | Come funziona Bedzzle |

---

## STATO REALE (29 Gennaio 2026)

```
FASE 0 (Fondamenta)     [####################] 100%
FASE P (Performance)    [####################] 100%
FASE 1 (Email Solido)   [##################..] 92%
FASE 2 (PMS Integration)[#######.............] 35%
FASE 4 (OCR/Check-in)   [##################..] 90%
```

---

## PROSSIMO STEP: SUBROADMAP FASE A

**FASE A: Setup WireGuard (4-6h)**

```
PREREQUISITI:
1. Identificare server gateway (rete 200, sempre acceso)
2. Accesso admin al server
3. Router hotel accessibile per port forwarding

STEP:
A.1 → Installare WireGuard server
A.2 → Configurare chiavi e peer
A.3 → Port forwarding router (UDP 51820)
A.4 → Installare client su Mac
A.5 → Test: ping 192.168.200.5 da remoto
```

**DOMANDA PER RAFA:** Quale server usiamo come gateway nella rete 200?

---

## CONNETTORE ERICSOFT (S317)

**Path:** `miracallook/backend/ericsoft/`
**Status:** ✅ Completo, non testato (problema rete)

| File | LOC | Cosa |
|------|-----|------|
| `connector.py` | 441 | SQL client + sicurezza |
| `api.py` | 114 | 4 endpoints REST |
| `models.py` | 55 | Pydantic models |

**Endpoints pronti:**
```
GET /ericsoft/status          # Health check
GET /ericsoft/bookings        # Lista prenotazioni
GET /ericsoft/bookings/active # Ospiti in casa
GET /ericsoft/bookings/search # Cerca per email
```

---

## FILE CHIAVE

| File | Cosa |
|------|------|
| **SUBROADMAP_ERICSOFT_INTEGRATION.md** | Piano 6 fasi! |
| MAPPA_STRATEGICA_MIRACOLLOOK.md | Visione completa |
| NORD_MIRACOLLOOK.md | Direzione |
| `backend/ericsoft/` | Connettore SQL |

---

## ARCHITETTURA TARGET

```
[Ericsoft DB] ←SQL→ [Server Gateway] ←WireGuard→ [Miracollook Backend]
                    (rete 200)                    (ovunque)
                         ↓
                    [Cache Redis]
                         ↓
                    [API REST]
                         ↓
                    [Frontend + AI]
```

---

## SESSIONI PRECEDENTI

| Sessione | Cosa |
|----------|------|
| S318 | Studio architettura + Subroadmap Ericsoft |
| S317 | Connettore Ericsoft + Mappa Strategica |
| S316 | Schema DB + User READ-ONLY |
| S315 | Credenziali + Backup DB |

---

*"Come fanno i professionisti - ma con il nostro tocco AI!"*
*Cervella & Rafa - Sessione 318*
