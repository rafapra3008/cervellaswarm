# PROPOSTA: Architettura Guest Management Professionale

> **Autore:** Cervella Backend
> **Data:** 29 Gennaio 2026
> **Target Quality Score:** 9.5/10
> **Status:** PROPOSTA - In attesa approvazione Rafa

---

## EXECUTIVE SUMMARY

**PROBLEMA ATTUALE:**
```python
WHERE a.TrListaEmail IS NOT NULL AND a.TrListaEmail != ''
# ❌ SBAGLIATO: Esclude 24 ospiti su 40! (60% copertura)
```

**PROBLEMA STRATEGICO:**
- ❌ Miracollook vede solo ospiti CON email
- ❌ Ospiti PARTITI non tracciati (no post-stay marketing)
- ❌ Comunicazione multi-canale impossibile (SMS, WhatsApp)
- ❌ Nessuna storicizzazione soggiorni

**SOLUZIONE PROPOSTA:**
Sistema Guest Management COMPLETO con:
- ✅ TUTTI gli ospiti (con/senza email)
- ✅ Stati lifecycle completi (Pre-Arrival → Post-Stay)
- ✅ Multi-channel contact (Email, SMS, WhatsApp, Manual)
- ✅ Guest History tracking
- ✅ Deduplicazione intelligente

**QUALITÀ TARGET:** 9.5/10 - Standard professionale PMS

---

## 1. MODELLO DATI GUEST PROFILE COMPLETO

### 1.1 Schema Pydantic Proposto

```python
"""
Guest Profile Model v2.0 - Gestione Professionale Ospiti
Target: Quality Score 9.5/10
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class GuestStatus(str, Enum):
    """Stati lifecycle ospite (mappati da IdStatoScheda Ericsoft)."""
    PRE_ARRIVAL = "pre_arrival"       # IdStatoScheda = 1 (Prenotazione confermata)
    ARRIVAL_DAY = "arrival_day"       # IdStatoScheda = 2 (Arrivo previsto oggi)
    IN_HOUSE = "in_house"             # IdStatoScheda = 3 (Ospite in casa)
    DEPARTURE_DAY = "departure_day"   # IdStatoScheda = 5 (Partenza prevista oggi)
    POST_STAY = "post_stay"           # Partito (check-out completato)
    CANCELLED = "cancelled"           # DataCancellazione IS NOT NULL


class ContactChannel(str, Enum):
    """Canali di comunicazione disponibili."""
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    MANUAL = "manual"        # Comunicazione tramite reception
    NONE = "none"            # Non contattabile


class ContactPreference(BaseModel):
    """Preferenze comunicazione ospite."""
    channel: ContactChannel
    value: Optional[str] = Field(None, description="Email/Telefono/WhatsApp ID")
    verified: bool = Field(False, description="Contatto verificato")
    primary: bool = Field(False, description="Canale primario")


class Stay(BaseModel):
    """Soggiorno singolo (SchedaConto)."""
    id_scheda_conto: int = Field(..., description="ID univoco soggiorno")
    check_in: date
    check_out: date
    camera: Optional[str] = Field(None, description="Codice camera")
    status: GuestStatus
    is_cancelled: bool = Field(False)
    cancellation_date: Optional[datetime] = None

    @field_validator('check_in', 'check_out', mode='before')
    @classmethod
    def convert_datetime_to_date(cls, v):
        """Converte datetime in date se necessario."""
        if isinstance(v, datetime):
            return v.date()
        return v

    @property
    def nights(self) -> int:
        """Numero notti soggiorno."""
        return (self.check_out - self.check_in).days

    @property
    def is_active(self) -> bool:
        """Soggiorno attivo (in corso)."""
        return self.status in [GuestStatus.ARRIVAL_DAY, GuestStatus.IN_HOUSE]

    @property
    def is_past(self) -> bool:
        """Soggiorno passato."""
        return self.status == GuestStatus.POST_STAY


class GuestProfile(BaseModel):
    """
    Profilo completo ospite - Aggregazione di tutti i soggiorni.

    Design principles:
    - Un GuestProfile = Una persona (deduplicato per Cognome+Nome)
    - Contiene tutti i soggiorni (storico completo)
    - Track del canale di contatto preferito
    - Gestisce ospiti senza email (SMS/WhatsApp/Manual)
    """
    # Identificazione
    id_anagrafica: int = Field(..., description="ID Ericsoft Anagrafica")
    cognome: str
    nome: Optional[str] = None

    # Contatti (multi-channel)
    contacts: List[ContactPreference] = Field(
        default_factory=list,
        description="Canali di comunicazione disponibili"
    )

    # Soggiorni
    stays: List[Stay] = Field(
        default_factory=list,
        description="Storico soggiorni (ordinato per check-in DESC)"
    )

    # Metadata
    first_stay: Optional[date] = Field(None, description="Primo soggiorno")
    last_stay: Optional[date] = Field(None, description="Ultimo soggiorno")
    total_stays: int = Field(0, description="Numero soggiorni totali")
    total_nights: int = Field(0, description="Numero notti totali")

    # Flags
    is_repeat_guest: bool = Field(False, description="Ospite ricorrente")
    is_contactable: bool = Field(False, description="Almeno un contatto valido")

    @property
    def nome_completo(self) -> str:
        """Nome completo dell'ospite."""
        if self.nome:
            return f"{self.nome} {self.cognome}"
        return self.cognome

    @property
    def current_stay(self) -> Optional[Stay]:
        """Soggiorno corrente (se in casa)."""
        for stay in self.stays:
            if stay.is_active:
                return stay
        return None

    @property
    def current_status(self) -> GuestStatus:
        """Stato corrente ospite (dello stay più recente)."""
        if self.stays:
            return self.stays[0].status
        return GuestStatus.POST_STAY

    @property
    def primary_contact(self) -> Optional[ContactPreference]:
        """Canale di contatto primario."""
        for contact in self.contacts:
            if contact.primary:
                return contact
        return self.contacts[0] if self.contacts else None

    def get_contact_by_channel(self, channel: ContactChannel) -> Optional[ContactPreference]:
        """Ottiene contatto per canale specifico."""
        for contact in self.contacts:
            if contact.channel == channel:
                return contact
        return None

    @field_validator('stays')
    @classmethod
    def sort_stays(cls, v: List[Stay]) -> List[Stay]:
        """Ordina soggiorni per check-in DESC (più recente primo)."""
        return sorted(v, key=lambda s: s.check_in, reverse=True)
```

---

## 2. QUERY MASTER ERICSOFT CORRETTA

### 2.1 Problemi Query Attuale

```sql
-- ❌ ATTUALE: Solo ospiti con email
WHERE a.TrListaEmail IS NOT NULL AND a.TrListaEmail != ''

-- PROBLEMI:
-- 1. Esclude 24 ospiti su 40 (60% copertura!)
-- 2. Non traccia ospiti partiti (no post-stay)
-- 3. Non supporta SMS/WhatsApp
-- 4. No deduplicazione (stesso ospite, più soggiorni)
```

### 2.2 Query Proposta A: TUTTI gli Ospiti (Completa)

```sql
-- ✅ PROPOSTA A: Tutti gli ospiti con profilo completo
-- Include: con/senza email, stati completi, contatti multipli

SELECT
    -- Identificazione
    a.IdAnagrafica,
    a.Cognome,
    a.Nome,

    -- Soggiorno
    sc.IdSchedaConto,
    sc.TrDataInizio AS check_in,
    sc.TrDataFine AS check_out,
    sc.IdStatoScheda,

    -- Contatti (multi-channel)
    a.TrListaEmail AS email,
    a.TrListaTelefono AS telefono,  -- Per SMS/WhatsApp

    -- Camera
    r.Codice AS camera,

    -- Cancellazione
    sc.DataCancellazione,
    sc.IdTipoCancellazione

FROM SchedaConto sc

-- Join Anagrafica (ospite)
INNER JOIN SchedaContoAnagrafica sca
    ON sc.IdSchedaConto = sca.IdSchedaConto
INNER JOIN Anagrafica a
    ON sca.IdAnagrafica = a.IdAnagrafica

-- Join Camera (LEFT per gestire soggiorni senza camera assegnata)
LEFT JOIN SchedaContoRisorsa scr
    ON sc.IdSchedaConto = scr.IdSchedaConto
LEFT JOIN Risorsa r
    ON scr.IdRisorsa = r.IdRisorsa

WHERE
    -- Escludi solo cancellazioni
    sc.DataCancellazione IS NULL

    -- TUTTI gli stati (1=PreArrival, 2=Arrival, 3=InHouse, 5=Departure)
    AND sc.IdStatoScheda IN (1, 2, 3, 5)

ORDER BY
    a.Cognome, a.Nome, sc.TrDataInizio DESC
```

**COVERAGE:** 100% ospiti attivi (con/senza email)

### 2.3 Query Proposta B: Ospiti Attuali (Performance)

```sql
-- ✅ PROPOSTA B: Solo ospiti IN CASA + ARRIVI OGGI
-- Ottimizzata per dashboard real-time

SELECT
    a.IdAnagrafica,
    a.Cognome,
    a.Nome,
    sc.IdSchedaConto,
    sc.TrDataInizio AS check_in,
    sc.TrDataFine AS check_out,
    sc.IdStatoScheda,
    a.TrListaEmail AS email,
    a.TrListaTelefono AS telefono,
    r.Codice AS camera

FROM SchedaConto sc
INNER JOIN SchedaContoAnagrafica sca ON sc.IdSchedaConto = sca.IdSchedaConto
INNER JOIN Anagrafica a ON sca.IdAnagrafica = a.IdAnagrafica
LEFT JOIN SchedaContoRisorsa scr ON sc.IdSchedaConto = scr.IdSchedaConto
LEFT JOIN Risorsa r ON scr.IdRisorsa = r.IdRisorsa

WHERE
    sc.DataCancellazione IS NULL

    -- Solo stati attivi (Arrival + InHouse)
    AND sc.IdStatoScheda IN (2, 3)

    -- Filter temporale aggiuntivo (sicurezza)
    AND sc.TrDataInizio <= GETDATE()
    AND sc.TrDataFine >= GETDATE()

ORDER BY r.Codice, a.Cognome
```

**COVERAGE:** Ospiti attuali (arrivi + in casa) - ~27 ospiti

### 2.4 Query Proposta C: Post-Stay (Marketing)

```sql
-- ✅ PROPOSTA C: Ospiti PARTITI (ultimi 7 giorni)
-- Per post-stay marketing (recensioni, ringraziamenti)

SELECT
    a.IdAnagrafica,
    a.Cognome,
    a.Nome,
    sc.IdSchedaConto,
    sc.TrDataInizio AS check_in,
    sc.TrDataFine AS check_out,
    a.TrListaEmail AS email,
    a.TrListaTelefono AS telefono,
    r.Codice AS camera,
    DATEDIFF(day, sc.TrDataFine, GETDATE()) AS days_since_checkout

FROM SchedaConto sc
INNER JOIN SchedaContoAnagrafica sca ON sc.IdSchedaConto = sca.IdSchedaConto
INNER JOIN Anagrafica a ON sca.IdAnagrafica = a.IdAnagrafica
LEFT JOIN SchedaContoRisorsa scr ON sc.IdSchedaConto = scr.IdSchedaConto
LEFT JOIN Risorsa r ON scr.IdRisorsa = r.IdRisorsa

WHERE
    sc.DataCancellazione IS NULL

    -- Partiti negli ultimi 7 giorni
    AND sc.TrDataFine >= DATEADD(day, -7, GETDATE())
    AND sc.TrDataFine < GETDATE()

    -- Almeno un contatto disponibile
    AND (
        a.TrListaEmail IS NOT NULL
        OR a.TrListaTelefono IS NOT NULL
    )

ORDER BY sc.TrDataFine DESC
```

**USE CASE:** Email post-soggiorno, richiesta recensioni

---

## 3. MAPPING STATI LIFECYCLE

### 3.1 Stati Ericsoft → GuestStatus

```python
# Mapping completo IdStatoScheda → GuestStatus

ERICSOFT_STATUS_MAP = {
    1: GuestStatus.PRE_ARRIVAL,     # Prenotazione confermata (futuro)
    2: GuestStatus.ARRIVAL_DAY,     # Arrivo previsto oggi
    3: GuestStatus.IN_HOUSE,        # Ospite in casa
    5: GuestStatus.DEPARTURE_DAY,   # Partenza prevista oggi
}

def map_ericsoft_status(
    id_stato: int,
    check_out: date,
    is_cancelled: bool
) -> GuestStatus:
    """
    Mappa stato Ericsoft a GuestStatus.

    Logica:
    - Se cancellato → CANCELLED
    - Se check_out passato → POST_STAY
    - Altrimenti → mapping diretto
    """
    if is_cancelled:
        return GuestStatus.CANCELLED

    if check_out < date.today():
        return GuestStatus.POST_STAY

    return ERICSOFT_STATUS_MAP.get(id_stato, GuestStatus.PRE_ARRIVAL)
```

### 3.2 Validazione Stati con Date

```python
def validate_status_consistency(
    id_stato: int,
    check_in: date,
    check_out: date,
    today: date = None
) -> bool:
    """
    Valida coerenza stato vs date.

    Regole:
    - PRE_ARRIVAL: check_in > oggi
    - ARRIVAL_DAY: check_in == oggi
    - IN_HOUSE: check_in <= oggi < check_out
    - DEPARTURE_DAY: check_out == oggi
    - POST_STAY: check_out < oggi
    """
    if today is None:
        today = date.today()

    status = ERICSOFT_STATUS_MAP.get(id_stato)

    if status == GuestStatus.PRE_ARRIVAL:
        return check_in > today
    elif status == GuestStatus.ARRIVAL_DAY:
        return check_in == today
    elif status == GuestStatus.IN_HOUSE:
        return check_in <= today < check_out
    elif status == GuestStatus.DEPARTURE_DAY:
        return check_out == today

    return True  # Default: accetta
```

---

## 4. COMUNICAZIONE MULTI-CANALE

### 4.1 Estrazione Contatti da Ericsoft

```python
def extract_contacts_from_ericsoft_row(row: dict) -> List[ContactPreference]:
    """
    Estrae tutti i contatti disponibili da riga Ericsoft.

    Priority:
    1. Email (se valida)
    2. Telefono (per SMS/WhatsApp)
    3. Manual (se nessun contatto digitale)
    """
    contacts = []

    # 1. Email
    email = row.get("email")
    if email and "@" in email:
        contacts.append(ContactPreference(
            channel=ContactChannel.EMAIL,
            value=email.strip(),
            verified=False,  # Da verificare con invio
            primary=True     # Email è canale primario se presente
        ))

    # 2. Telefono (SMS/WhatsApp)
    telefono = row.get("telefono")
    if telefono:
        # Sanitize (rimuovi spazi, +39 etc)
        tel_clean = sanitize_phone(telefono)

        if tel_clean:
            # Assume WhatsApp disponibile per mobili italiani
            if is_italian_mobile(tel_clean):
                contacts.append(ContactPreference(
                    channel=ContactChannel.WHATSAPP,
                    value=tel_clean,
                    verified=False,
                    primary=len(contacts) == 0  # Primary se no email
                ))

            # Aggiungi sempre come SMS fallback
            contacts.append(ContactPreference(
                channel=ContactChannel.SMS,
                value=tel_clean,
                verified=False,
                primary=False
            ))

    # 3. Fallback: Manual communication
    if not contacts:
        contacts.append(ContactPreference(
            channel=ContactChannel.MANUAL,
            value=None,
            verified=True,  # Reception può sempre comunicare
            primary=True
        ))

    return contacts


def sanitize_phone(phone: str) -> Optional[str]:
    """Pulisce numero telefono."""
    import re

    # Rimuovi spazi, trattini, parentesi
    clean = re.sub(r'[^\d+]', '', phone)

    # Rimuovi +39 iniziale (assume Italia)
    clean = re.sub(r'^\+39', '', clean)

    # Verifica lunghezza (mobile italiano = 10 cifre)
    if len(clean) == 10 and clean.startswith('3'):
        return clean

    return None


def is_italian_mobile(phone: str) -> bool:
    """Verifica se è mobile italiano."""
    return len(phone) == 10 and phone.startswith('3')
```

### 4.2 Logica Invio Messaggi

```python
async def send_message_to_guest(
    guest: GuestProfile,
    message: str,
    fallback: bool = True
) -> bool:
    """
    Invia messaggio all'ospite usando canale primario.

    Args:
        guest: Profilo ospite
        message: Messaggio da inviare
        fallback: Se True, prova canali alternativi in caso di errore

    Returns:
        True se inviato, False altrimenti
    """
    if not guest.is_contactable:
        logger.warning(f"guest_not_contactable", guest=guest.nome_completo)
        return False

    primary = guest.primary_contact

    # 1. Prova canale primario
    if primary.channel == ContactChannel.EMAIL:
        success = await send_email(primary.value, message)
        if success or not fallback:
            return success

    elif primary.channel == ContactChannel.WHATSAPP:
        success = await send_whatsapp(primary.value, message)
        if success or not fallback:
            return success

    elif primary.channel == ContactChannel.SMS:
        success = await send_sms(primary.value, message)
        if success or not fallback:
            return success

    # 2. Fallback su canali alternativi
    if fallback:
        for contact in guest.contacts:
            if contact == primary:
                continue  # Già provato

            if contact.channel == ContactChannel.EMAIL:
                success = await send_email(contact.value, message)
                if success:
                    return True

            elif contact.channel == ContactChannel.SMS:
                success = await send_sms(contact.value, message)
                if success:
                    return True

    # 3. Manual fallback: notifica reception
    await notify_reception_manual_message(guest, message)
    return False
```

---

## 5. PIANO IMPLEMENTAZIONE

### Phase 1: Modello Dati (1 giorno)
```
1.1 Crea models/guest_profile.py
1.2 Crea enums (GuestStatus, ContactChannel)
1.3 Test Pydantic validation
1.4 Migrazione database locale (se serve cache)
```

### Phase 2: Query Master (0.5 giorni)
```
2.1 Test Query Proposta A su DB Ericsoft reale
2.2 Validazione coverage (deve essere 100%)
2.3 Verifica performance (< 500ms)
2.4 Aggiungi query B e C per use case specifici
```

### Phase 3: Connector Refactor (1 giorno)
```
3.1 Refactor connector.py per Query A
3.2 Aggiungi metodi:
    - get_all_guests() → Query A
    - get_current_guests() → Query B
    - get_recent_checkouts(days=7) → Query C
3.3 Aggiungi deduplicazione (merge stays per IdAnagrafica)
3.4 Aggiungi extract_contacts()
```

### Phase 4: Multi-Channel (2 giorni)
```
4.1 Setup Twilio (SMS)
4.2 Setup WhatsApp Business API
4.3 Implementa send_message_to_guest()
4.4 Test invio multi-canale
```

### Phase 5: Post-Stay Marketing (1 giorno)
```
5.1 Cron job: check ospiti partiti oggi
5.2 Template email ringraziamento
5.3 Template richiesta recensione
5.4 Dashboard post-stay analytics
```

### Phase 6: Testing & Monitoring (0.5 giorni)
```
6.1 Test copertura 100% ospiti
6.2 Test deduplicazione
6.3 Test multi-channel fallback
6.4 Setup monitoring (Sentry, Grafana)
```

**TOTALE: 6 giorni lavorativi**

---

## 6. METRICHE QUALITÀ (Target 9.5/10)

### Coverage
- ✅ 100% ospiti attivi (con/senza email)
- ✅ 100% ospiti partiti (ultimi 30 giorni)
- ✅ Deduplicazione corretta (stesso ospite, più soggiorni)

### Performance
- ✅ Query < 500ms (anche con 1000+ ospiti)
- ✅ Cache Redis per profili frequenti
- ✅ Batch processing per storico completo

### Reliability
- ✅ Multi-channel fallback
- ✅ Circuit breaker su Ericsoft
- ✅ Retry logic su SMS/WhatsApp
- ✅ Manual fallback sempre disponibile

### Data Quality
- ✅ Validazione contatti (email, telefono)
- ✅ Coerenza stati vs date
- ✅ Nessun duplicato (deduplicazione IdAnagrafica)
- ✅ Audit log completo (chi, quando, cosa)

### User Experience
- ✅ Dashboard ospiti real-time
- ✅ Storico soggiorni completo
- ✅ Comunicazione seamless (scelta automatica canale)
- ✅ Post-stay automation

---

## 7. RISCHI & MITIGAZIONI

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Ericsoft DB lento | Media | Alto | Cache Redis, Query ottimizzate |
| Telefono non valido | Alta | Medio | Sanitize + Fallback email/manual |
| WhatsApp non disponibile | Media | Basso | Fallback SMS |
| Deduplicazione fallisce | Bassa | Alto | Test robusto + Review manuale |
| Stati Ericsoft cambiano | Bassa | Medio | Config mapping esterna |

---

## 8. NEXT STEPS

**IMMEDIATE (Sessione 320):**
1. ✅ Review proposta con Rafa
2. ⏳ Decisione: Query A (completa) o B (performance)?
3. ⏳ Test Query A su DB reale
4. ⏳ Validazione coverage (deve essere 100%)

**SHORT-TERM (Settimana 1):**
1. Implementa GuestProfile model
2. Refactor connector.py
3. Test deduplicazione
4. Setup cache Redis

**MEDIUM-TERM (Settimana 2-3):**
1. Multi-channel integration (Twilio, WhatsApp)
2. Post-stay automation
3. Dashboard analytics
4. Monitoring completo

---

## 9. CONCLUSIONI

**QUESTA PROPOSTA RISOLVE:**
- ✅ Coverage 100% ospiti (non più 60%)
- ✅ Post-stay marketing (recensioni, fidelizzazione)
- ✅ Comunicazione professionale (multi-canale)
- ✅ Guest history completo (CRM alberghiero)

**QUALITÀ ATTESA:** 9.5/10
- Architettura solida
- Deduplicazione robusta
- Multi-channel fallback
- Performance < 500ms
- Monitoring completo

**EFFORT:** 6 giorni lavorativi (1.5 settimane)

**ROI:**
- Marketing post-stay automatizzato
- Esperienza ospite migliorata
- Dati completi per analytics
- Riduzione comunicazione manuale

---

*Proposta preparata da Cervella Backend*
*29 Gennaio 2026 - Miracollook Project*
*"Ogni riga deve quadrare. I dettagli fanno sempre la differenza."*
