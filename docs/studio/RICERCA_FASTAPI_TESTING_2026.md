# RICERCA: FastAPI Testing Best Practices 2026

> **Data:** 19 Gennaio 2026
> **Researcher:** Cervella Researcher
> **Contesto:** Miracollook Email Client (FastAPI Python 3.13)
> **Obiettivo:** Setup testing per FASE 4 Subroadmap Robustezza

---

## TL;DR - RACCOMANDAZIONI IMMEDIATE

```
FRAMEWORK:          pytest (NON unittest)
ASYNC TESTING:      pytest-asyncio + httpx.AsyncClient
OAUTH TESTING:      Mock per unit, integration per critical flows
RATE LIMITING:      Testabile con pytest + ab (Apache Bench)
ENCRYPTION:         Mock Fernet, test con chiavi temporanee
STRUTTURA:          tests/ mirror di src/
COVERAGE TARGET:    80%+ (realistico per FastAPI)
```

---

## 1. PYTEST vs UNITTEST

### Verdict: **PYTEST VINCE 2026**

**Perché pytest:**
- FastAPI documentazione ufficiale usa pytest
- TestClient basato su HTTPX è ottimizzato per pytest
- Fixtures più pulite e potenti
- Ecosystem più ricco (pytest-asyncio, pytest-cov, pytest-mock)
- Standard de-facto in comunità FastAPI 2026

**Quando unittest è utile:**
- Solo per `unittest.mock.patch` (mocking)
- Ma pytest include pytest-mock che wrappa unittest.mock

**Fonti:**
- [FastAPI Official Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [FrugalTesting FastAPI Best Practices](https://www.frugaltesting.com/blog/what-is-fastapi-testing-tools-frameworks-and-best-practices)
- [Apidog Unit Testing Guide](https://apidog.com/blog/unit-testing-fastapi/)

---

## 2. PYTEST-ASYNCIO SETUP

### Setup Raccomandato 2026

**Packages necessari:**
```bash
pip install pytest pytest-asyncio httpx pytest-cov
```

**IMPORTANTE: FastAPI raccomanda AnyIO invece di pytest-asyncio!**

Dalla documentazione ufficiale 2026:
> "AnyIO provides a neat plugin for this, that allows us to specify that some test functions are to be called asynchronously."

**Setup con AnyIO (RACCOMANDATO):**

```python
# pytest.ini o pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"

# conftest.py
import pytest

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
```

**Pattern di Test Async:**

```python
from httpx import AsyncClient, ASGITransport

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.get("/")
        assert response.status_code == 200
```

**ATTENZIONE:**
- NON usare TestClient per route async (non triggera lifespan events)
- Usare `httpx.AsyncClient` per route async
- Per lifespan events, usare `florimondmanca/asgi-lifespan`

**Best Practices Async:**
1. Usare async SOLO dove misurabilmente utile
2. Usare `AsyncMock` per mock async (non `Mock` normale)
3. Preferire librerie async-compatible per I/O
4. Evitare blocking calls in async functions

**Fonti:**
- [FastAPI Async Tests Official](https://fastapi.tiangolo.com/advanced/async-tests/)
- [TestDriven.io FastAPI + Pytest](https://testdriven.io/blog/fastapi-crud/)
- [woteq Testing Async FastAPI](https://woteq.com/testing-async-fastapi-applications-with-pytest-a-comprehensive-guide/)

---

## 3. OAUTH FLOW TESTING

### Approccio Ibrido: Mock + Integration

**RACCOMANDAZIONE:**
- **Unit tests:** Mock OAuth (veloce, affidabile)
- **Critical flows:** Integration tests (1-2 test end-to-end)

**Perché NON solo mock:**

Dal sondaggio FusionAuth 2026:
> "Mocks always return what you expect, so if your real provider changes a token format or an auth flow breaks, your test suite won't catch it."
>
> "When you mock, you skip login flows, MFA enforcement, redirect handling, and token validation - your tests say 'working' while real logins may fail."

**Perché NON solo integration:**
- Setup complesso
- Test lenti
- Rate limiting provider OAuth
- Difficile testare edge cases (timeout, token invalido)

### Pattern Raccomandato per Miracollook

**1. Mock per Unit Tests (80% dei test):**

```python
# FastAPI dependency override pattern
from fastapi.testclient import TestClient

def override_get_current_user():
    return {"email": "test@example.com", "user_id": "123"}

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_protected_endpoint():
    response = client.get("/gmail/inbox")
    assert response.status_code == 200
```

**2. Integration per Critical Flows (20% dei test):**

```python
# Test OAuth callback completo
def test_oauth_full_flow():
    # 1. Richiedi authorization URL
    # 2. Simula callback con code
    # 3. Verifica token salvato
    # 4. Verifica refresh funziona
    pass
```

**Cosa mockare in Miracollook:**
- Gmail API responses (inbox, send, labels)
- OAuth token exchange
- Access token validation

**Cosa NON mockare (integration):**
- OAuth callback flow completo
- Refresh token flow completo
- Encryption/decryption token

**Fonti:**
- [FusionAuth Mock Auth Debate](https://fusionauth.io/blog/to-mock-or-not-mock-auth)
- [FastAPI Testing Dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Medium Unit Testing with Mocks](https://medium.com/@joel.rompis/unit-testing-in-fastapi-using-mocks-and-patches-a7ecb39b30b5)

---

## 4. RATE LIMITING (SLOWAPI) TESTING

### Pattern di Test

**Setup pytest per slowapi:**

```python
# conftest.py
import pytest
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

@pytest.fixture
def client():
    from main import app
    app.state.limiter._rate_limit_exceeded_handler = _rate_limit_exceeded_handler
    return TestClient(app)
```

**Test rate limit:**

```python
def test_rate_limit_exceeded(client):
    # Supera il limite (es: 10 req/min)
    for i in range(11):
        response = client.get("/gmail/inbox")

    # L'11esima request deve dare 429
    assert response.status_code == 429
    assert "rate limit exceeded" in response.text.lower()
```

**Test con Apache Bench (manuale):**

```bash
# Genera 200 richieste con concorrenza 10
ab -n 200 -c 10 http://localhost:8002/gmail/inbox

# Verifica risposta 429 nei log
```

**ATTENZIONE:**
- SlowAPI usa `limits` library per rate limiting
- In test, il limiter potrebbe non resettarsi tra test
- Usare fixture che ripulisce state tra test

**Pattern per reset state:**

```python
@pytest.fixture(autouse=True)
def reset_limiter():
    from main import app
    # Reset limiter state prima di ogni test
    app.state.limiter.reset()
    yield
```

**Fonti:**
- [SlowAPI GitHub](https://github.com/laurentS/slowapi)
- [SlowAPI Documentation](https://slowapi.readthedocs.io/)
- [LoadForge Rate Limiting Guide](https://loadforge.com/guides/implementing-rate-limits-in-fastapi-a-step-by-step-guide)

---

## 5. FERNET ENCRYPTION TESTING

### Best Practices 2026

**REGOLA D'ORO:**
> "SEMPRE testare encryption con chiavi temporanee, MAI con chiavi di produzione!"

**Pattern Raccomandato:**

```python
import pytest
from cryptography.fernet import Fernet

@pytest.fixture
def test_encryption_key():
    """Genera chiave temporanea per ogni test"""
    return Fernet.generate_key()

@pytest.fixture
def fernet_cipher(test_encryption_key):
    return Fernet(test_encryption_key)

def test_token_encryption(fernet_cipher):
    # Test encryption/decryption
    original = "sensitive_token_12345"
    encrypted = fernet_cipher.encrypt(original.encode())
    decrypted = fernet_cipher.decrypt(encrypted).decode()

    assert decrypted == original
    assert encrypted != original.encode()  # Verifica che sia criptato
```

**Test Token Expiration (Metodi per Testing):**

Fernet fornisce metodi specifici per testare:
- `encrypt_at_time(data, current_time)` - Cripta con timestamp custom
- `decrypt_at_time(token, ttl, current_time)` - Decripta con timestamp custom

```python
import time

def test_token_expiration():
    cipher = Fernet(Fernet.generate_key())

    # Cripta "nel passato"
    past_time = int(time.time()) - 3600  # 1 ora fa
    token = cipher.encrypt_at_time(b"data", past_time)

    # Deve fallire se ttl=60 (scaduto)
    with pytest.raises(Exception):
        cipher.decrypt_at_time(token, ttl=60, current_time=int(time.time()))
```

**IMPORTANTE - Key Management Testing:**

NON testare:
- ❌ Hardcoded keys in test
- ❌ Production keys
- ❌ Weak keys (< 32 bytes)

TESTARE:
- ✅ Key rotation (MultiFernet.rotate())
- ✅ Key loading da environment
- ✅ Fallback su key mancante
- ✅ Encryption/decryption roundtrip

**Security Best Practices (2026):**

Dal sondaggio crypto 2026:
> "Use at least 200,000 to 600,000 iterations for PBKDF2 depending on target hardware, with 600,000+ recommended for critical applications. Argon2id is preferred with 2-3 iterations and 64MB memory cost."

Per Miracollook:
- Fernet va bene (simmetrico, veloce)
- Key da environment (ENCRYPTION_KEY)
- NO key derivation da password (usa chiave generata)
- Considera MultiFernet per key rotation futura

**Fonti:**
- [Cryptography Fernet Docs](https://cryptography.io/en/latest/fernet/)
- [WideWiki Fernet Guide](https://widewiki.com/posts/python/geek-pie/fernet-securing-data-with-python-s-encryption-library/)
- [BomberBot Fernet Exploration](https://www.bomberbot.com/python/fernet-symmetric-encryption-in-python-an-in-depth-exploration/)

---

## 6. STRUTTURA CARTELLE TESTING

### Pattern Raccomandato 2026

**Opzione A: Test folder separata (RACCOMANDATO per Miracollook)**

```
miracallook/backend/
├── gmail/
│   ├── __init__.py
│   ├── api.py
│   ├── inbox.py
│   ├── actions.py
│   ├── labels.py
│   └── utils.py
├── db/
│   ├── models.py
│   └── database.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures globali
│   ├── test_gmail_inbox.py
│   ├── test_gmail_actions.py
│   ├── test_gmail_labels.py
│   ├── test_oauth_flow.py
│   └── test_encryption.py
├── pytest.ini
└── requirements-dev.txt
```

**Opzione B: Test inline (NON raccomandato per progetti grandi)**

```
app/
├── __init__.py
├── main.py
├── test_main.py  # Test accanto al codice
```

**pytest.ini (Configuration):**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --cov=gmail
    --cov=db
    --cov-report=html
    --cov-report=term-missing
    --verbose
```

**conftest.py (Fixtures Globali):**

```python
import pytest
from fastapi.testclient import TestClient
from cryptography.fernet import Fernet

@pytest.fixture(scope="session")
def test_app():
    from main import app
    return app

@pytest.fixture
def client(test_app):
    return TestClient(test_app)

@pytest.fixture
def test_encryption_key():
    return Fernet.generate_key()

@pytest.fixture
def mock_gmail_api():
    """Mock Gmail API responses"""
    # Return mock object
    pass
```

**Naming Conventions:**

| Cosa | Pattern | Esempio |
|------|---------|---------|
| Test file | `test_<module>.py` | `test_inbox.py` |
| Test function | `test_<feature>` | `test_get_inbox_success` |
| Test class | `Test<Feature>` | `TestInboxAPI` |
| Fixture | `<name>_fixture` | `mock_gmail_api` |

**Fonti:**
- [FastAPI Official Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Medium FastAPI Test Structure](https://medium.com/@philipokiokio/product-engineering-fastapi-test-series-unit-test-part-i-0a3348284400)
- [DEV.to FastAPI Project Structure](https://dev.to/timo_reusch/how-i-structure-big-fastapi-projects-260e)

---

## 7. COVERAGE TARGET

### Raccomandazione: **80%+ Coverage**

**Perché 80%?**
- Standard industria per backend API
- Realistico da mantenere
- Copre logica critica senza ossessione

**Coverage per Area (Miracollook):**

| Modulo | Target | Priorità | Nota |
|--------|--------|----------|------|
| `gmail/inbox.py` | 90%+ | ALTA | Logica core |
| `gmail/actions.py` | 90%+ | ALTA | Batch operations |
| `gmail/labels.py` | 85%+ | ALTA | CRUD labels |
| `gmail/compose.py` | 85%+ | ALTA | Send email |
| `gmail/utils.py` | 95%+ | CRITICA | OAuth + token mgmt |
| `db/models.py` | 70%+ | MEDIA | Definizioni ORM |
| `ai.py` | 60%+ | BASSA | Mock AI calls |

**Cosa NON deve raggiungere 100%:**
- Boilerplate code (init files)
- Main.py (bootstrap)
- Config files
- Type stubs

**Setup Coverage con pytest:**

```bash
# Install
pip install pytest-cov

# Run con coverage
pytest --cov=gmail --cov=db --cov-report=html --cov-report=term-missing

# Apri report HTML
open htmlcov/index.html
```

**Coverage Thresholds (pytest.ini):**

```ini
[pytest]
addopts =
    --cov=gmail
    --cov-fail-under=80  # Fail se coverage < 80%
```

**ATTENZIONE - Coverage Issues con FastAPI (2026):**

Dal GitHub Issue FastAPI:
> "FastAPI uses threads and SQLAlchemy uses greenlet for async behavior, which can cause coverage tracking issues; using 'concurrency=greenlet' config can help."

**Fix per Coverage con Async:**

```ini
# pytest.ini
[coverage:run]
concurrency = greenlet,thread
```

**Metriche di Successo:**

```
✅ 80%+ total coverage
✅ 90%+ coverage su moduli critici (utils, actions, inbox)
✅ Zero funzioni critiche non testate
✅ Test suite runs < 30 secondi (per fast feedback)
```

**Fonti:**
- [AugustInfotech FastAPI Coverage Guide](https://www.augustinfotech.com/blogs/how-to-use-coverage-unit-testing-in-fastapi-using-pytest/)
- [GitHub FastAPI Coverage Discussion](https://github.com/fastapi/fastapi/discussions/8750)
- [Harness FastAPI Test Tutorial](https://developer.harness.io/docs/continuous-integration/use-ci/run-tests/ci-fastapi-test/)

---

## 8. SETUP COMPLETO - FASE 4.1 (MIRACOLLOOK)

### Step-by-Step Implementation

**1. Installare Dipendenze:**

```bash
cd ~/Developer/miracollogeminifocus/miracallook/backend
source venv/bin/activate

pip install pytest pytest-asyncio pytest-cov httpx pytest-mock
pip freeze > requirements-dev.txt
```

**2. Creare Struttura:**

```bash
mkdir -p tests
touch tests/__init__.py
touch tests/conftest.py
touch pytest.ini
```

**3. pytest.ini:**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --cov=gmail
    --cov=db
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --verbose
asyncio_mode = auto

[coverage:run]
source = gmail,db
omit =
    */tests/*
    */venv/*
    */__pycache__/*
concurrency = greenlet,thread
```

**4. conftest.py (Fixtures Base):**

```python
import pytest
from fastapi.testclient import TestClient
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def test_app():
    """FastAPI app instance"""
    from main import app
    return app

@pytest.fixture
def client(test_app):
    """TestClient per chiamate sincrone"""
    return TestClient(test_app)

@pytest.fixture
def test_db():
    """Database temporaneo per test"""
    engine = create_engine("sqlite:///:memory:")
    # Setup schema
    yield engine
    # Teardown

@pytest.fixture
def test_encryption_key():
    """Chiave Fernet temporanea"""
    return Fernet.generate_key()

@pytest.fixture
def mock_gmail_api(mocker):
    """Mock Gmail API responses"""
    # Usa pytest-mock per mock
    pass
```

**5. Test di Verifica (test_setup.py):**

```python
def test_app_loads(test_app):
    """Verifica che l'app si carichi"""
    assert test_app is not None

def test_client_works(client):
    """Verifica che TestClient funzioni"""
    response = client.get("/health")
    assert response.status_code == 200
```

**6. Eseguire Test:**

```bash
pytest -v
pytest --cov=gmail --cov-report=html
```

**7. CI/CD Integration (GitHub Actions):**

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov=gmail --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## 9. ESEMPI CONCRETI PER MIRACOLLOOK

### Test Gmail Inbox

```python
# tests/test_gmail_inbox.py
import pytest
from unittest.mock import Mock, patch

def test_get_inbox_success(client, mock_gmail_api):
    """Test: GET /gmail/inbox restituisce lista email"""
    # Mock Gmail API response
    mock_gmail_api.list_messages.return_value = {
        "messages": [{"id": "123", "threadId": "456"}]
    }

    response = client.get("/gmail/inbox")

    assert response.status_code == 200
    assert "messages" in response.json()

def test_get_inbox_unauthorized(client):
    """Test: GET /gmail/inbox senza token -> 401"""
    # Override dependency per simulare no token
    response = client.get("/gmail/inbox")
    assert response.status_code == 401
```

### Test OAuth Flow

```python
# tests/test_oauth_flow.py
def test_oauth_callback_success(client, mocker):
    """Test: OAuth callback salva token correttamente"""
    # Mock Google token exchange
    mock_exchange = mocker.patch("gmail.utils.exchange_code_for_token")
    mock_exchange.return_value = {
        "access_token": "test_access",
        "refresh_token": "test_refresh"
    }

    response = client.get("/auth/callback?code=test_code")

    assert response.status_code == 200
    # Verifica token salvato in DB (encrypted)
```

### Test Encryption

```python
# tests/test_encryption.py
def test_token_encryption_roundtrip(test_encryption_key):
    """Test: Token encryption/decryption funziona"""
    from cryptography.fernet import Fernet

    cipher = Fernet(test_encryption_key)
    original = "sensitive_token_12345"

    encrypted = cipher.encrypt(original.encode())
    decrypted = cipher.decrypt(encrypted).decode()

    assert decrypted == original
    assert encrypted != original.encode()
```

### Test Rate Limiting

```python
# tests/test_rate_limiting.py
def test_rate_limit_exceeded(client):
    """Test: Rate limit blocca dopo N richieste"""
    # Supera limite (es: 10 req/min)
    for i in range(11):
        response = client.get("/gmail/inbox")

    assert response.status_code == 429
```

---

## 10. CHECKLIST IMPLEMENTAZIONE FASE 4

```
FASE 4.1 - SETUP PYTEST:
[ ] pytest, pytest-asyncio, pytest-cov installati
[ ] Struttura tests/ creata
[ ] pytest.ini configurato
[ ] conftest.py con fixtures base
[ ] Test di verifica passa (test_setup.py)
[ ] Coverage report funziona

FASE 4.2 - UNIT TESTS:
[ ] test_gmail_inbox.py (90%+ coverage)
[ ] test_gmail_actions.py (90%+ coverage)
[ ] test_gmail_labels.py (85%+ coverage)
[ ] test_gmail_compose.py (85%+ coverage)
[ ] test_gmail_utils.py (95%+ coverage - CRITICO)
[ ] test_encryption.py (token encrypt/decrypt)

FASE 4.3 - INTEGRATION TESTS:
[ ] test_oauth_flow.py (callback + refresh)
[ ] test_api_endpoints.py (end-to-end)
[ ] test_rate_limiting.py (slowapi)

ACCEPTANCE CRITERIA FINALE:
[ ] 80%+ total coverage
[ ] 95%+ coverage su gmail/utils.py
[ ] Zero test failures
[ ] Test suite runs < 30 secondi
[ ] Coverage report HTML generato
```

---

## FONTI COMPLETE

### Documentazione Ufficiale
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [FastAPI Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/)
- [FastAPI Testing Dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Cryptography Fernet Docs](https://cryptography.io/en/latest/fernet/)
- [SlowAPI Documentation](https://slowapi.readthedocs.io/)

### Best Practices & Tutorials
- [FrugalTesting FastAPI Best Practices](https://www.frugaltesting.com/blog/what-is-fastapi-testing-tools-frameworks-and-best-practices)
- [AugustInfotech PyTest Coverage Guide](https://www.augustinfotech.com/blogs/how-to-use-coverage-unit-testing-in-fastapi-using-pytest/)
- [TestDriven.io FastAPI + Pytest](https://testdriven.io/blog/fastapi-crud/)
- [woteq Testing Async FastAPI](https://woteq.com/testing-async-fastapi-applications-with-pytest-a-comprehensive-guide/)
- [Alex Jacobs Integration Testing](https://alex-jacobs.com/posts/fastapitests/)

### Security & Auth Testing
- [FusionAuth Mock Auth Debate](https://fusionauth.io/blog/to-mock-or-not-mock-auth)
- [Medium Unit Testing with Mocks](https://medium.com/@joel.rompis/unit-testing-in-fastapi-using-mocks-and-patches-a7ecb39b30b5)
- [WideWiki Fernet Guide](https://widewiki.com/posts/python/geek-pie/fernet-securing-data-with-python-s-encryption-library/)

### Structure & Coverage
- [Medium FastAPI Test Structure](https://medium.com/@philipokiokio/product-engineering-fastapi-test-series-unit-test-part-i-0a3348284400)
- [DEV.to FastAPI Project Structure](https://dev.to/timo_reusch/how-i-structure-big-fastapi-projects-260e)
- [GitHub FastAPI Coverage Discussion](https://github.com/fastapi/fastapi/discussions/8750)

### Rate Limiting
- [SlowAPI GitHub](https://github.com/laurentS/slowapi)
- [LoadForge Rate Limiting Guide](https://loadforge.com/guides/implementing-rate-limits-in-fastapi-a-step-by-step-guide)

---

*Ricerca completata: 19 Gennaio 2026*
*Cervella Researcher - CervellaSwarm*

*"Studiare prima di agire - sempre!"*
*"I player grossi hanno già risolto questi problemi."*
