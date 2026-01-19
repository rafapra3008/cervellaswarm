# Ricerca: Encryption Token SQLite - Miracollo PMS

**Data:** 19 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Contesto:** Token Twilio salvati in chiaro nel DB (migration 020_whatsapp_messages.sql:103)

---

## TL;DR - Raccomandazione

✅ **USARE: Python `cryptography.fernet` con chiave in `.env`**

**Perché:**
- Soluzione SEMPLICE (no over-engineering)
- Standard industry (usato da Airflow, SQLAlchemy, etc)
- Chiave in environment variable (sicurezza + flessibilità)
- Zero dipendenze esterne complicate
- Funziona perfettamente con SQLite esistente

**NON serve:**
- ❌ SQLCipher (troppo complesso per il nostro caso)
- ❌ KMS/Vault cloud (overkill per progetto iniziale)
- ❌ Full database encryption (serve solo field-level)

---

## Approcci Disponibili

### 1. Field-Level Encryption (Fernet) ✅ RACCOMANDATO

**Pro:**
- Semplice implementazione
- Cripta solo campi sensibili (performance migliori)
- Compatibile con SQLite standard
- Chiave in `.env` (gestibile facilmente)
- Supporto universale (libreria cryptography)

**Contro:**
- Chiave in plaintext in `.env` (accettabile per deployment singolo)

**Caso d'uso:** PMS singolo, token API/credentials specifici

### 2. Full Database Encryption (SQLCipher)

**Pro:**
- Tutto il database criptato
- Protezione massima

**Contro:**
- Richiede SQLCipher installato
- Dipendenza esterna complessa
- Overhead performance
- Overkill per criptare 1-2 token

**Caso d'uso:** Database con MOLTI dati sensibili

### 3. Cloud KMS (AWS/Azure/GCP)

**Pro:**
- Gestione chiavi centralizzata
- Rotation automatica

**Contro:**
- Dipendenza cloud (noi vogliamo self-hosted)
- Complessità aggiuntiva
- Costi

**Caso d'uso:** Deployment enterprise multi-tenant

---

## Soluzione Implementata: Fernet + .env

### Schema Generale

```
1. Genera chiave encryption (una volta)
2. Salva chiave in .env
3. Crea utility encrypt/decrypt
4. Service usa utility prima di DB operations
```

### Sicurezza

**Cosa protegge:**
- Token in chiaro nel database ✅
- Backup database criptati ✅
- Accesso diretto al .db file ✅

**Cosa NON protegge:**
- Accesso al server (se attacker ha accesso al server, può leggere .env)
- Memory dump (token decriptato in RAM a runtime)

**Per il nostro caso:** SUFFICIENTE! Non gestiamo dati bancari/healthcare.

### Implementazione Python

#### 1. Genera Chiave (script one-time)

```python
# scripts/generate_encryption_key.py
from cryptography.fernet import Fernet

def generate_key():
    """Genera chiave encryption per token"""
    key = Fernet.generate_key()
    print(f"ENCRYPTION_KEY={key.decode()}")
    print("\nAggiungi questa riga a .env")
    print("IMPORTANTE: Backup sicuro della chiave!")

if __name__ == "__main__":
    generate_key()
```

**Uso:**
```bash
python scripts/generate_encryption_key.py >> .env
```

#### 2. Utility Encryption

```python
# backend/core/encryption.py
from cryptography.fernet import Fernet
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class TokenEncryptor:
    """Utility per encrypt/decrypt token sensibili"""

    def __init__(self):
        if not settings.ENCRYPTION_KEY:
            raise ValueError("ENCRYPTION_KEY not found in environment")

        self._cipher = Fernet(settings.ENCRYPTION_KEY.encode())

    def encrypt(self, value: str) -> str:
        """
        Encrypts a string value

        Args:
            value: Plaintext string to encrypt

        Returns:
            Encrypted string (base64 encoded)
        """
        if not value:
            return None

        try:
            encrypted_bytes = self._cipher.encrypt(value.encode())
            return encrypted_bytes.decode()  # Store as string in DB
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, encrypted_value: str) -> str:
        """
        Decrypts an encrypted string

        Args:
            encrypted_value: Encrypted string from DB

        Returns:
            Original plaintext string
        """
        if not encrypted_value:
            return None

        try:
            decrypted_bytes = self._cipher.decrypt(encrypted_value.encode())
            return decrypted_bytes.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise

# Singleton instance
encryptor = TokenEncryptor()
```

#### 3. Config (settings.py)

```python
# backend/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ... existing settings ...

    # Encryption
    ENCRYPTION_KEY: str = None  # Required for token encryption

    class Config:
        env_file = ".env"

settings = Settings()
```

#### 4. Service Layer

```python
# backend/services/whatsapp_config_service.py
from core.encryption import encryptor
from database.repositories.whatsapp_config_repo import WhatsAppConfigRepository

class WhatsAppConfigService:
    def __init__(self, db: Session):
        self.repo = WhatsAppConfigRepository(db)

    def save_config(self, property_id: int, config_data: dict) -> WhatsAppConfig:
        """Save WhatsApp config with encrypted token"""

        # Encrypt token BEFORE saving
        if config_data.get("twilio_auth_token"):
            config_data["twilio_auth_token"] = encryptor.encrypt(
                config_data["twilio_auth_token"]
            )

        return self.repo.create_or_update(property_id, config_data)

    def get_config(self, property_id: int) -> dict:
        """Get config with decrypted token"""

        config = self.repo.get_by_property(property_id)
        if not config:
            return None

        # Decrypt token AFTER reading
        return {
            "property_id": config.property_id,
            "twilio_account_sid": config.twilio_account_sid,
            "twilio_auth_token": encryptor.decrypt(config.twilio_auth_token),
            "whatsapp_number": config.whatsapp_number,
            # ... altri campi
        }
```

#### 5. Migration per Dati Esistenti

```python
# backend/database/migrations/021_encrypt_existing_tokens.py
"""
Encrypt existing plaintext tokens
ONE-TIME migration dopo implementazione encryption
"""
from cryptography.fernet import Fernet
import sqlite3
import os

def migrate():
    # Load encryption key
    encryption_key = os.getenv("ENCRYPTION_KEY")
    if not encryption_key:
        raise ValueError("ENCRYPTION_KEY not found")

    cipher = Fernet(encryption_key.encode())

    # Connect DB
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Fetch all configs with plaintext tokens
    cursor.execute("""
        SELECT id, twilio_auth_token
        FROM whatsapp_config
        WHERE twilio_auth_token IS NOT NULL
    """)

    rows = cursor.fetchall()

    # Encrypt each token
    for config_id, plaintext_token in rows:
        encrypted_token = cipher.encrypt(plaintext_token.encode()).decode()

        cursor.execute("""
            UPDATE whatsapp_config
            SET twilio_auth_token = ?
            WHERE id = ?
        """, (encrypted_token, config_id))

    conn.commit()
    conn.close()

    print(f"✅ Encrypted {len(rows)} tokens")

if __name__ == "__main__":
    migrate()
```

---

## Esempio Uso Completo

### Setup Iniziale (una volta)

```bash
# 1. Genera chiave
python scripts/generate_encryption_key.py >> .env

# 2. Verifica .env
cat .env
# Output:
# ENCRYPTION_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 3. Se hai già token in DB plaintext, cripta
python backend/database/migrations/021_encrypt_existing_tokens.py
```

### Uso in API Endpoint

```python
# backend/api/endpoints/whatsapp.py
from fastapi import APIRouter, Depends
from services.whatsapp_config_service import WhatsAppConfigService

router = APIRouter()

@router.post("/properties/{property_id}/whatsapp/config")
async def save_whatsapp_config(
    property_id: int,
    config: WhatsAppConfigCreate,
    service: WhatsAppConfigService = Depends()
):
    """Save WhatsApp config - token encrypted automatically"""

    # Service layer handles encryption
    saved_config = service.save_config(property_id, config.dict())

    return {"status": "ok", "config_id": saved_config.id}

@router.get("/properties/{property_id}/whatsapp/config")
async def get_whatsapp_config(
    property_id: int,
    service: WhatsAppConfigService = Depends()
):
    """Get config - token decrypted automatically"""

    # Service returns decrypted token
    config = service.get_config(property_id)

    return config
```

### Uso in Twilio Client

```python
# backend/integrations/twilio_client.py
from twilio.rest import Client
from services.whatsapp_config_service import WhatsAppConfigService

def send_whatsapp_message(property_id: int, to: str, message: str):
    """Send WhatsApp via Twilio"""

    # Get config (with decrypted token)
    service = WhatsAppConfigService(db)
    config = service.get_config(property_id)

    # Use decrypted credentials
    client = Client(
        config["twilio_account_sid"],
        config["twilio_auth_token"]  # Decrypted!
    )

    # Send message
    message = client.messages.create(
        from_=f"whatsapp:{config['whatsapp_number']}",
        to=f"whatsapp:{to}",
        body=message
    )

    return message.sid
```

---

## Checklist Implementazione

- [ ] Install `cryptography`: `pip install cryptography`
- [ ] Genera ENCRYPTION_KEY e aggiungi a `.env`
- [ ] Crea `backend/core/encryption.py` con TokenEncryptor
- [ ] Aggiungi `ENCRYPTION_KEY` a `settings.py`
- [ ] Modifica Service Layer per encrypt/decrypt
- [ ] Se hai già dati: esegui migration 021
- [ ] Test manuale: salva config, verifica DB (deve essere encrypted), leggi config (deve essere decrypted)
- [ ] Aggiungi `.env` a `.gitignore` (CRITICO!)
- [ ] Backup sicuro di ENCRYPTION_KEY (se perdi chiave, perdi dati!)

---

## Confronto Soluzioni

| Criterio | Fernet | SQLCipher | Cloud KMS |
|----------|--------|-----------|-----------|
| Complessità | ⭐ Bassa | ⭐⭐⭐ Alta | ⭐⭐ Media |
| Setup | 5 minuti | 30+ minuti | 15 minuti |
| Dipendenze | cryptography | SQLCipher build | Cloud SDK |
| Performance | Ottima | Buona | Network latency |
| Self-hosted | ✅ Si | ✅ Si | ❌ No |
| Cost | Free | Free | $ Cloud costs |
| Fit nostro caso | ✅ Perfetto | ❌ Overkill | ❌ Non necessario |

---

## FAQ

### Q: Cosa succede se perdo la ENCRYPTION_KEY?

**A:** Token criptati diventano irrecuperabili. Devi:
1. Generare nuova chiave
2. Chiedere ai clienti di re-inserire token
3. **Soluzione:** Backup sicuro della chiave (password manager, safe fisico)

### Q: Devo criptare anche twilio_account_sid?

**A:** NO. L'Account SID è pubblico (è un identificatore, non un segreto). Solo il `twilio_auth_token` è sensibile.

### Q: Posso usare la stessa chiave per più progetti?

**A:** Tecnicamente si, ma meglio chiave DIVERSA per progetto (se una leaked, altre protette).

### Q: Come faccio rotation della chiave?

**A:**
1. Genera nuova chiave
2. Decrypt tutti token con vecchia chiave
3. Re-encrypt con nuova chiave
4. Aggiorna .env

Script:
```python
# scripts/rotate_encryption_key.py
old_cipher = Fernet(old_key)
new_cipher = Fernet(new_key)

for token in tokens:
    decrypted = old_cipher.decrypt(token)
    new_encrypted = new_cipher.encrypt(decrypted)
    # Update DB
```

### Q: Performance impact?

**A:** Minimo. Fernet è veloce:
- Encrypt: ~0.1ms per token
- Decrypt: ~0.1ms per token
- Non noterai differenza nel PMS

---

## Fonti

### Documentazione Ufficiale
- [Fernet - Cryptography.io](https://cryptography.io/en/latest/fernet/)
- [Fernet Airflow](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/fernet.html)

### Best Practices
- [Basic Security Practices for SQLite](https://dev.to/stephenc222/basic-security-practices-for-sqlite-safeguarding-your-data-23lh)
- [Securing SQLite Database Best Practices](https://www.sqliteforum.com/p/securing-your-sqlite-database-best)
- [Encryption at Rest with SQLAlchemy](https://blog.miguelgrinberg.com/post/encryption-at-rest-with-sqlalchemy)

### Implementazioni Pratiche
- [Securely Encrypting Data with Fernet](https://parthibanmarimuthu.medium.com/securely-encrypting-sensitive-data-in-python-with-fernet-dd50638bde0f)
- [Fernet Python Guide - CodeRivers](https://coderivers.org/blog/fernet-python/)
- [How to Encrypt SQLite with Fernet](https://www.thiscodeworks.com/how-to-encrypt-and-decrypt-data-in-sqlite-with-python-s-fernet-python-coding-python/674ce8f4e3db6f00149d2798)

### Confronto Approcci
- [SQLCipher Encrypted Databases](https://charlesleifer.com/blog/encrypted-sqlite-databases-with-python-and-sqlcipher/)
- [Database Encryption Python Guide](https://bobbyconnolly.github.io/python-database-encryption-guide/)

---

**Status:** ✅ Ricerca completata
**Raccomandazione:** Implementare Fernet con chiave in .env
**Effort stimato:** 2-3 ore (inclusi test)
**Rischio:** Basso (soluzione standard industry-proven)

*Cervella Researcher - 19 Gennaio 2026*
