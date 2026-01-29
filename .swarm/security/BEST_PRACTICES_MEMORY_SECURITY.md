# Best Practices: Memory Security for Workers

**Autrice:** Cervella Security
**Data:** 29 Gennaio 2026
**Scopo:** Educazione Workers su gestione sicura della memoria

---

## REGOLA SACRA

```
+================================================================+
|                                                                |
|   MAI SCRIVERE SECRETS IN MEMORY FILES                         |
|                                                                |
|   Secrets = API keys, passwords, tokens, connection strings    |
|                                                                |
|   Memoria = PROMPT_RIPRESA, stato.md, ricerche/, reports/      |
|                                                                |
|   Sempre: .env per secrets, reference nei docs                 |
|                                                                |
+================================================================+
```

---

## Cosa Sono i "Secrets"?

### Secrets (MAI in memory)

❌ **API Keys**
   - OpenAI: `sk-...`
   - Google: `AIza...`
   - Stripe: `sk_live_...`, `pk_live_...`

❌ **Passwords**
   - Database passwords
   - Admin passwords
   - Service account passwords

❌ **Tokens**
   - JWT tokens
   - OAuth access/refresh tokens
   - GitHub personal access tokens
   - Bearer tokens

❌ **Connection Strings**
   - `mysql://user:password@host/db`
   - `postgresql://user:password@host/db`
   - Con credenziali incluse

❌ **Private Keys**
   - RSA/EC/DSA private keys
   - SSH private keys
   - Signing keys

❌ **Credentials Sets**
   - Username + password combinations
   - Client ID + client secret
   - Public key + private key pairs

### Non-Secrets (OK in memory)

✅ **System Architecture**
   - "Usiamo PostgreSQL per il database"
   - "Autenticazione via JWT"
   - "API protette con rate limiting"

✅ **References to Secrets**
   - "Password stored in .env as DB_PASSWORD"
   - "API key configured in environment variable"
   - "Credentials managed via .env file"

✅ **Public Information**
   - API endpoint URLs (senza credenziali)
   - Port numbers
   - Service names
   - Technology stack

✅ **Examples/Placeholders**
   - "password: YOUR_PASSWORD_HERE"
   - "api_key: [your_key]"
   - Chiaramente non credenziali reali

---

## Pattern: Come Documentare Correttamente

### Scenario 1: Database Access

**❌ SBAGLIATO:**
```markdown
## Database PRA

Server: 192.168.200.5
Instance: NLTERMINAL01\SQLERICSOFT22
Username: sa
Password: YOUR_PASSWORD_HERE
Database: PRA
```

**✅ CORRETTO:**
```markdown
## Database PRA

**Connection:** Configured in `.env` file

Required environment variables:
- `ERICSOFT_DB_HOST` - Server IP
- `ERICSOFT_DB_INSTANCE` - SQL Server instance name
- `ERICSOFT_DB_USER` - Database username
- `ERICSOFT_DB_PASSWORD` - Database password
- `ERICSOFT_DB_NAME` - Database name

See `.env.example` for structure.
```

### Scenario 2: API Integration

**❌ SBAGLIATO:**
```markdown
## Bedzzle API

URL: https://connect.bedzzle.com/oapi/v1/marketplace
PublicKey: YOUR_PUBLIC_KEY_HERE
PrivateKey: YOUR_PRIVATE_KEY_HERE
ProductKey: YOUR_PRODUCT_UUID_HERE
```

**✅ CORRETTO:**
```markdown
## Bedzzle API

**Endpoint:** https://connect.bedzzle.com/oapi/v1/marketplace

**Authentication:** Requires 3 keys stored in environment variables:
- `BEDZZLE_PUBLIC_KEY` - Marketplace public key
- `BEDZZLE_PRIVATE_KEY` - Marketplace private key
- `BEDZZLE_PRODUCT_KEY` - Product UUID

Credentials provided by Bedzzle marketplace dashboard.
```

### Scenario 3: Service Account

**❌ SBAGLIATO:**
```markdown
## Gmail Service Account

Email: miracollook@gmail.com
Password: MySecretPass123!
App Password: abcd efgh ijkl mnop
```

**✅ CORRETTO:**
```markdown
## Gmail Service Account

**Account:** miracollook@gmail.com

**Authentication:** OAuth 2.0 with service account
- Service account JSON: `credentials/gmail-service-account.json` (gitignored)
- Scopes: gmail.readonly, gmail.send

**Setup:**
1. Create service account in Google Cloud Console
2. Download JSON credentials
3. Place in `credentials/` directory (excluded from git)
4. Reference in code via `GOOGLE_APPLICATION_CREDENTIALS` env var
```

### Scenario 4: Research/Discovery

**❌ SBAGLIATO:**
```markdown
# Ricerca: Accesso Database

Ho trovato le credenziali nel file config:
- User: admin
- Pass: admin123
```

**✅ CORRETTO:**
```markdown
# Ricerca: Accesso Database

**Finding:** Configurazione database trovata in `config/database.ini`

**Credenziali:**
- Username: [redacted - vedi .env]
- Password: [redacted - vedi .env]

**Action:** Credenziali spostate in `.env`, file config aggiornato per leggere da environment.
```

---

## Pattern: Codice Sicuro

### Python (FastAPI/Backend)

**❌ SBAGLIATO:**
```python
# database.py
connection = pymssql.connect(
    server="192.168.200.5",
    user="sa",
    password="YOUR_PASSWORD_HERE",
    database="PRA"
)
```

**✅ CORRETTO:**
```python
# database.py
import os
from dotenv import load_dotenv

load_dotenv()

connection = pymssql.connect(
    server=os.getenv("ERICSOFT_DB_HOST"),
    user=os.getenv("ERICSOFT_DB_USER"),
    password=os.getenv("ERICSOFT_DB_PASSWORD"),
    database=os.getenv("ERICSOFT_DB_NAME")
)
```

### React (Frontend)

**❌ SBAGLIATO:**
```javascript
// config.js
export const API_KEY = "sk-1234567890abcdef";
```

**✅ CORRETTO:**
```javascript
// config.js
// Public keys only! Private keys must stay on backend
export const STRIPE_PUBLIC_KEY = import.meta.env.VITE_STRIPE_PUBLIC_KEY;

// ❌ Never expose private/secret keys in frontend!
// Private keys belong in backend .env
```

---

## File Structure per Secrets

### Repository Layout

```
project/
├── .env                    # LOCAL secrets (gitignored)
├── .env.example            # Template (committed, no real secrets)
├── .gitignore              # MUST include .env*
├── credentials/            # Service account JSONs (gitignored)
│   └── .gitkeep
├── backend/
│   └── config.py           # Loads from .env
└── .sncp/
    └── progetti/
        └── progetto/
            ├── PROMPT_RIPRESA_progetto.md   # NO SECRETS
            └── stato.md                      # NO SECRETS
```

### .gitignore (Obbligatorio)

```gitignore
# Environment variables
.env
.env.*
!.env.example

# Credentials
credentials/*.json
credentials/*.pem
credentials/*.key
!credentials/.gitkeep

# Secrets
secrets/
*.secret
```

### .env.example (Template)

```bash
# Database
ERICSOFT_DB_HOST=192.168.200.5
ERICSOFT_DB_INSTANCE=INSTANCE_NAME
ERICSOFT_DB_USER=your_username_here
ERICSOFT_DB_PASSWORD=your_password_here
ERICSOFT_DB_NAME=database_name

# Bedzzle API
BEDZZLE_PUBLIC_KEY=your_public_key
BEDZZLE_PRIVATE_KEY=your_private_key
BEDZZLE_PRODUCT_KEY=your_product_uuid

# OpenAI
OPENAI_API_KEY=sk-your-key-here
```

**Nota:** `.env.example` non contiene secrets reali, solo placeholders.

---

## Checklist per Workers

### Prima di Scrivere in Memory Files

```
[ ] Sto per scrivere una password? → NO! Metti in .env
[ ] Sto per scrivere un API key? → NO! Metti in .env
[ ] Sto per scrivere un token? → NO! Metti in .env
[ ] Sto per scrivere una connection string con credenziali? → NO! Usa riferimento
[ ] Sto documentando COSA serve (ok) o IL VALORE (no)? → COSA serve
[ ] Il valore che scrivo è pubblico/esempio? → OK se chiaramente placeholder
```

### Prima di Commit

```
[ ] Ho fatto scan con audit-secrets.sh?
[ ] Nessun CRITICAL/HIGH trovato?
[ ] File .env escluso da git?
[ ] Solo references ai secrets, non valori reali?
```

---

## Automated Tools

### 1. Pre-commit Hook

**Location:** `.git/hooks/pre-commit`

```bash
#!/bin/bash
./scripts/sncp/audit-secrets.sh .sncp/progetti/

if [ $? -ne 0 ]; then
    echo "❌ COMMIT BLOCKED: Secrets detected!"
    exit 1
fi
```

**Installa:**
```bash
chmod +x .git/hooks/pre-commit
```

### 2. Audit Script

**Manual scan:**
```bash
./scripts/sncp/audit-secrets.sh .sncp/progetti/
```

**CI/CD scan:**
```yaml
# .github/workflows/security.yml
- name: Scan for secrets
  run: ./scripts/sncp/audit-secrets.sh
```

---

## Cosa Fare Se Trovi Secrets Esposti

### 1. NON FARTI PRENDERE DAL PANICO

✅ Identifica il problema
✅ Segui la procedura
✅ Documenta l'azione

### 2. ESCALATION IMMEDIATA

```bash
# Usa protocol swarm
scripts/swarm/ask-regina.sh BLOCKER "Found plaintext password in file X"
```

### 3. IMMEDIATE ACTIONS

1. **STOP** - Non fare altri commit
2. **ROTATE** - Cambia le credenziali esposte
3. **REMOVE** - Rimuovi dai file
4. **REFERENCE** - Sostituisci con reference a .env
5. **VERIFY** - Scan completo con audit-secrets.sh

### 4. DOCUMENTATION

Documenta l'incidente in `.swarm/security/incidents/`:
- Cosa è stato esposto
- Quando è stato scoperto
- Azioni prese
- Lezioni apprese

---

## Examples: Good vs Bad

### Example 1: Database Migration

**❌ BAD:**
```markdown
# Migration 020: Setup Database

Run on production:
```sql
CREATE USER 'app'@'localhost' IDENTIFIED BY 'MyP@ssw0rd123';
GRANT SELECT ON db.* TO 'app'@'localhost';
```
```

**✅ GOOD:**
```markdown
# Migration 020: Setup Database

**Prerequisites:**
- Database credentials configured in `.env`
- User with admin privileges

**Steps:**
1. Load credentials: `source .env`
2. Run script: `./scripts/db/create_user.sh`

The script creates application user with permissions defined in `db/grants.sql`.
```

### Example 2: API Documentation

**❌ BAD:**
```markdown
# API Testing

cURL example:
```bash
curl -H "Authorization: Bearer sk-1234567890abcdef" \
  https://api.example.com/endpoint
```
```

**✅ GOOD:**
```markdown
# API Testing

**Setup:**
```bash
export API_KEY=$(cat .env | grep API_KEY | cut -d= -f2)
```

**cURL example:**
```bash
curl -H "Authorization: Bearer $API_KEY" \
  https://api.example.com/endpoint
```
```

---

## FAQ

### Q: Posso scrivere credenziali temporanee per test?

**A:** NO. Anche credenziali di test vanno in `.env.test` (gitignored).

### Q: E se è un servizio di terze parti con chiave pubblica?

**A:** Chiavi PUBBLICHE (es: Stripe publishable key) possono stare in codice. Chiavi PRIVATE/SECRET sempre in .env.

### Q: Come so se una chiave è pubblica o privata?

**A:** Se inizia con `pk_`, `pub_`, è pubblica. Se inizia con `sk_`, `secret_`, è privata. In dubbio → .env.

### Q: Posso committare .env.example?

**A:** SÌ! `.env.example` è un template SENZA valori reali. Esempio:
```
API_KEY=your_key_here
```

### Q: E se trovo credenziali in un file vecchio?

**A:** Escalation a Cervella Security → Valutiamo se serve pulizia git history.

---

## Mantra

```
"Secrets in .env, references in docs."

"Document WHAT is needed, not WHAT it is."

"When in doubt, .env it out."

"Automation prevents, humans forget."
```

---

## Risorse

| Risorsa | Link |
|---------|------|
| Audit Script | `scripts/sncp/audit-secrets.sh` |
| Security Report | `.swarm/security/AUDIT_SNCP_SECRETS.md` |
| .env Example | `.env.example` (root progetto) |

---

**Cervella Security**
*"La miglior difesa è prevenire, non reagire."*

29 Gennaio 2026
