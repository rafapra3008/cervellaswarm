# Report Esplorazione Backend Miracollo

**Data**: 11 Gennaio 2026
**Autore**: Cervella Backend
**Obiettivo**: Mappare struttura backend per integrazione client Ollama

---

## 1. STRUTTURA CARTELLE BACKEND

```
backend/
├── core/                    # Configurazione e utilità base
│   ├── config.py           # Settings via Pydantic (env-based)
│   ├── database.py         # SQLite connection
│   ├── security.py         # Auth utilities
│   └── immutable_guard.py  # Data integrity
│
├── models/                  # SQLAlchemy models
│   ├── booking.py
│   ├── guest.py
│   ├── hotel.py
│   └── ... (14+ models)
│
├── routers/                 # FastAPI endpoints (38 routers!)
│   ├── hotels.py           # /api/hotels
│   ├── bookings.py         # /api/bookings
│   ├── documents.py        # /api/documents (AI Scanner)
│   ├── whatsapp.py         # /api/whatsapp (Claude AI)
│   └── ... (34+ routers)
│
├── services/                # Business logic layer
│   ├── stripe_service.py   # Payment integration
│   ├── document_scanner.py # OCR + AI Vision
│   ├── rateboard_ai.py     # Revenue suggestions
│   ├── pagonline/          # Payment gateway client
│   │   ├── client.py
│   │   ├── models.py
│   │   └── signature.py
│   └── ... (30+ services)
│
├── middleware/              # FastAPI middleware
│   └── security.py         # Headers, CORS
│
├── compliance/              # Domain logic (GDPR, ISTAT)
│   ├── alloggiati.py
│   └── codes.py
│
├── ml/                      # Machine Learning
│   ├── model_trainer.py
│   └── confidence_scorer.py
│
└── tests/                   # Unit tests
```

---

## 2. PATTERN ARCHITETTURALI

### 2.1 Configurazione Centralizzata

**File**: `backend/core/config.py`

```python
class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./backend/data/miracollo.db"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # External APIs
    GEMINI_API_KEY: str = ""           # Google AI
    STRIPE_SECRET_KEY: str = ""        # Payments

    # Environment
    ENVIRONMENT: str = "development"

    @property
    def gemini_enabled(self) -> bool:
        return bool(self.GEMINI_API_KEY and len(self.GEMINI_API_KEY) > 20)

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global instance
settings = Settings()
```

**Pattern**:
- Pydantic Settings con validazione automatica
- Environment variables da `.env`
- Property helper per check configurazione
- Singleton globale importabile

---

### 2.2 Pattern Router (FastAPI)

**Esempio**: `backend/routers/documents.py`

```python
from fastapi import APIRouter, File, UploadFile, Depends
from ..core import get_db, logger
from ..services.document_scanner import scan_document

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/scan")
async def scan_identity_document(
    file: UploadFile = File(...),
    db=Depends(get_db)
):
    """Scan passaporto/CI con AI"""
    result = await scan_document(file, db)
    return {"success": True, "data": result}
```

**Pattern**:
- Router con prefix (`/api/documents`)
- Tag per OpenAPI docs
- Dependency injection (`Depends(get_db)`)
- Service layer separation

---

### 2.3 Pattern Service (External Clients)

**Esempi analizzati**:

#### A. Stripe Service (Payment Gateway)
```python
# File: backend/services/stripe_service.py

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_AVAILABLE = True

def create_checkout_session(
    booking_number: str,
    amount_cents: int,
    currency: str = "eur"
) -> Dict[str, Any]:
    """Crea Stripe Checkout Session"""
    if not STRIPE_AVAILABLE:
        raise RuntimeError("Stripe library not available")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[...],
        success_url=success_url
    )

    return {
        "provider": "stripe",
        "session_id": session.id,
        "checkout_url": session.url
    }
```

#### B. PagonLine Service (Custom HTTP Client)
```python
# File: backend/services/pagonline/client.py

import requests
from .models import AuthRequest, AuthResponse
from .signature import calculate_signature

class PagonLineClient:
    def __init__(self, sandbox: bool = True):
        self.base_url = SANDBOX_URL if sandbox else PROD_URL
        self.tid = os.getenv("PAGONLINE_TID")
        self.ksig = os.getenv("PAGONLINE_KSIG")

    def authorize(self, request: AuthRequest) -> AuthResponse:
        """Autorizza pagamento"""
        # Build XML body
        xml_body = self._build_auth_request(params)

        # POST request
        response = requests.post(
            url,
            data=xml_body.encode("utf-8"),
            headers={"Content-Type": "text/xml"}
        )

        # Parse response
        return self._parse_response(response.text)
```

**Pattern comune**:
1. Client class con init da environment
2. Metodi pubblici per operazioni
3. Metodi privati per build/parse
4. Modelli Pydantic per request/response
5. Exception custom per errori

---

### 2.4 Pattern AI Integration (Document Scanner)

**File**: `backend/services/document_scanner.py`

```python
# Import condizionale
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("OCR not available")

def scan_document(image_bytes: bytes) -> Dict[str, Any]:
    """Scansiona documento con OCR locale"""
    if not OCR_AVAILABLE:
        return {"error": "OCR not configured"}

    # Preprocessing
    image = preprocess_image(image_bytes)

    # OCR
    text = pytesseract.image_to_string(image)

    # Parse
    return parse_document_type(text)
```

**Pattern**:
- Graceful degradation (import opzionale)
- Check availability prima di usare
- Log warning se non disponibile
- Fallback o errore chiaro

---

## 3. INTEGRAZIONI AI/LLM ESISTENTI

### 3.1 Document Scanner (OCR Locale)
- **Libreria**: Tesseract + Pillow + OpenCV
- **Uso**: Parsing passaporti/CI/patenti
- **Pattern**: Import condizionale, preprocessing immagini
- **File**: `services/document_scanner.py`

### 3.2 WhatsApp AI (Claude API)
- **Libreria**: `anthropic==0.39.0`
- **Uso**: Auto-reply WhatsApp Business
- **Pattern**: Client API esterno
- **File**: `services/whatsapp_service.py` (non analizzato nel dettaglio)

### 3.3 ML Enhancement (Locale)
- **Libreria**: `scikit-learn`, `pandas`
- **Uso**: Revenue predictions, confidence scoring
- **Pattern**: Training locale, model persistence con joblib
- **File**: `ml/model_trainer.py`, `ml/confidence_scorer.py`

---

## 4. DOVE INTEGRARE OLLAMA CLIENT

### 4.1 Posto Ideale: `services/ollama/`

Creare una struttura modulare come PagonLine:

```
backend/services/ollama/
├── __init__.py           # Exports pubblici
├── client.py             # OllamaClient class
├── models.py             # Request/Response Pydantic models
├── exceptions.py         # OllamaError, OllamaConnectionError
└── prompts.py            # Template prompts (opzionale)
```

### 4.2 File da Creare/Modificare

#### A. `backend/services/ollama/client.py`
```python
"""
Ollama Local LLM Client - Miracollo PMS
========================================
Client per integrazione con Ollama API locale.

@version 1.0.0
@date 2026-01-11
"""

import requests
from typing import Dict, Any, Optional, List
from .models import ChatRequest, ChatResponse
from .exceptions import OllamaError, OllamaConnectionError

class OllamaClient:
    """Client Python per Ollama API locale."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.timeout = 30
        self._validate_connection()

    def _validate_connection(self):
        """Verifica connessione a Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise OllamaConnectionError(f"Ollama not reachable: {response.status_code}")
        except requests.exceptions.ConnectionError:
            raise OllamaConnectionError("Cannot connect to Ollama. Is it running?")

    def chat(self, request: ChatRequest) -> ChatResponse:
        """Invia chat message a modello Ollama."""
        endpoint = f"{self.base_url}/api/chat"

        payload = {
            "model": request.model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "stream": False
        }

        try:
            response = requests.post(
                endpoint,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code != 200:
                raise OllamaError(f"HTTP {response.status_code}: {response.text}")

            data = response.json()
            return ChatResponse(
                model=data["model"],
                content=data["message"]["content"],
                done=data.get("done", True)
            )

        except requests.exceptions.Timeout:
            raise OllamaConnectionError("Request timeout")
        except requests.exceptions.RequestException as e:
            raise OllamaError(f"Request failed: {str(e)}")

    def list_models(self) -> List[str]:
        """Lista modelli disponibili."""
        response = requests.get(f"{self.base_url}/api/tags")
        return [m["name"] for m in response.json().get("models", [])]

    def health_check(self) -> Dict[str, Any]:
        """Verifica stato Ollama."""
        try:
            models = self.list_models()
            return {
                "available": True,
                "base_url": self.base_url,
                "models_count": len(models),
                "models": models
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e)
            }
```

#### B. `backend/services/ollama/models.py`
```python
"""Pydantic models per Ollama API."""

from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="user | assistant | system")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    model: str = Field(default="llama3.2", description="Model name")
    messages: List[ChatMessage]
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=512, gt=0)

class ChatResponse(BaseModel):
    model: str
    content: str
    done: bool = True
```

#### C. `backend/services/ollama/__init__.py`
```python
"""Ollama Service - Public API."""

from .client import OllamaClient
from .models import ChatRequest, ChatResponse, ChatMessage
from .exceptions import OllamaError, OllamaConnectionError

__all__ = [
    "OllamaClient",
    "ChatRequest",
    "ChatResponse",
    "ChatMessage",
    "OllamaError",
    "OllamaConnectionError"
]
```

#### D. `backend/core/config.py` (MODIFICARE)
Aggiungere alla classe Settings:

```python
# Ollama LLM (Local AI)
OLLAMA_BASE_URL: str = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL: str = "llama3.2"

@property
def ollama_enabled(self) -> bool:
    """Check if Ollama is reachable"""
    try:
        import requests
        response = requests.get(f"{self.OLLAMA_BASE_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False
```

#### E. `backend/services/__init__.py` (MODIFICARE)
Aggiungere export:

```python
from .ollama import (
    OllamaClient,
    ChatRequest,
    ChatResponse,
    OllamaError
)

__all__ = [
    # ... esistenti ...
    # Ollama Local LLM
    'OllamaClient',
    'ChatRequest',
    'ChatResponse',
    'OllamaError'
]
```

---

### 4.3 Router API (Opzionale)

**File**: `backend/routers/ollama_api.py`

```python
"""Ollama API Router - Test e utilities."""

from fastapi import APIRouter, HTTPException
from ..services.ollama import OllamaClient, ChatRequest
from ..core import settings

router = APIRouter(prefix="/api/ollama", tags=["Ollama"])

@router.get("/health")
async def ollama_health():
    """Check Ollama availability"""
    client = OllamaClient(settings.OLLAMA_BASE_URL)
    return client.health_check()

@router.post("/chat")
async def ollama_chat(request: ChatRequest):
    """Send chat message to Ollama"""
    client = OllamaClient(settings.OLLAMA_BASE_URL)
    try:
        response = client.chat(request)
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_models():
    """List available Ollama models"""
    client = OllamaClient(settings.OLLAMA_BASE_URL)
    return {"models": client.list_models()}
```

Poi registrare in `main.py`:
```python
from .routers import ollama_api_router
app.include_router(ollama_api_router)
```

---

## 5. DEPENDENCIES DA AGGIUNGERE

**File**: `requirements.txt`

```txt
# HTTP Client (già presente)
requests>=2.31.0

# Nessun'altra dipendenza richiesta!
# Ollama usa API REST standard.
```

---

## 6. TESTING PATTERN

Guardando i test esistenti (`tests/`), il pattern è:

```python
"""Test Ollama Client"""

import pytest
from backend.services.ollama import OllamaClient, ChatRequest, ChatMessage

def test_ollama_connection():
    """Test connessione a Ollama"""
    client = OllamaClient()
    health = client.health_check()
    assert health["available"] is True

def test_ollama_chat():
    """Test chat message"""
    client = OllamaClient()

    request = ChatRequest(
        model="llama3.2",
        messages=[
            ChatMessage(role="user", content="Hello, respond with just 'OK'")
        ]
    )

    response = client.chat(request)
    assert response.done is True
    assert len(response.content) > 0

def test_ollama_list_models():
    """Test lista modelli"""
    client = OllamaClient()
    models = client.list_models()
    assert isinstance(models, list)
    assert len(models) > 0
```

---

## 7. CONFIGURAZIONE ENVIRONMENT

**File**: `.env`

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3.2
```

**File**: `.env.example` (template)

```bash
# Ollama Local LLM (optional)
# Assicurati che Ollama sia in esecuzione: ollama serve
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3.2  # o mistral, codellama, etc
```

---

## 8. WORKFLOW INTEGRAZIONE

### Step 1: Creare Service Layer
1. `mkdir -p backend/services/ollama`
2. Creare `client.py`, `models.py`, `exceptions.py`, `__init__.py`
3. Test isolato con `pytest backend/tests/test_ollama.py`

### Step 2: Aggiungere Config
1. Modificare `backend/core/config.py`
2. Aggiungere variabili in `.env`

### Step 3: Export nel Package
1. Modificare `backend/services/__init__.py`
2. Importabile come: `from backend.services import OllamaClient`

### Step 4: Router API (opzionale)
1. Creare `backend/routers/ollama_api.py`
2. Registrare in `main.py`
3. Test via curl: `curl http://localhost:8001/api/ollama/health`

### Step 5: Uso in Altri Service
Esempio in `rateboard_ai.py`:

```python
from ..services import OllamaClient, ChatRequest, ChatMessage

def generate_smart_suggestion(data: Dict) -> str:
    """Genera suggerimento con Ollama"""
    client = OllamaClient()

    prompt = f"Analizza questi dati: {data}. Suggerisci pricing strategy."

    request = ChatRequest(
        messages=[ChatMessage(role="user", content=prompt)]
    )

    response = client.chat(request)
    return response.content
```

---

## 9. BEST PRACTICES OSSERVATE

### ✅ Pattern da Seguire

1. **Separation of Concerns**
   - Router = HTTP layer
   - Service = Business logic
   - Models = Data validation
   - Core = Configuration

2. **Graceful Degradation**
   - Import condizionali
   - Check availability runtime
   - Fallback se servizio non disponibile

3. **Environment-Based Config**
   - Tutto in `.env`
   - Validazione con Pydantic
   - Property helper per check

4. **Type Hints Everywhere**
   - Tutti i metodi tipizzati
   - Pydantic per validation
   - MyPy compatible

5. **Logging Appropriato**
   - Logger per debug
   - Warning per config mancanti
   - Error per failures

6. **Docstring Completi**
   - Ogni file ha header con versione
   - Ogni funzione pubblica documentata
   - Args/Returns espliciti

### ❌ Anti-pattern da Evitare

1. ❌ Import assoluti fuori dal package
2. ❌ Hardcoded URLs (usa config)
3. ❌ Print invece di logger
4. ❌ Eccezioni generiche (`except Exception`)
5. ❌ Nessuna validazione input

---

## 10. PROSSIMI STEP CONSIGLIATI

### Priorità 1: MVP Client
- [ ] Creare `services/ollama/client.py`
- [ ] Creare `services/ollama/models.py`
- [ ] Creare `services/ollama/exceptions.py`
- [ ] Test connessione base

### Priorità 2: Integration
- [ ] Aggiungere config in `core/config.py`
- [ ] Export in `services/__init__.py`
- [ ] Scrivere test suite

### Priorità 3: API Endpoints
- [ ] Router `/api/ollama/health`
- [ ] Router `/api/ollama/chat`
- [ ] Router `/api/ollama/models`

### Priorità 4: Use Cases
- [ ] Integrare in `rateboard_ai.py` per suggerimenti
- [ ] Integrare in `whatsapp_service.py` (alternativa a Claude)
- [ ] Nuovo feature: "AI Assistant" per operatori

---

## 11. CONSIDERAZIONI ARCHITETTURALI

### Pro di Ollama vs API Cloud
✅ **Nessun costo per token**
✅ **Privacy completa** (dati non escono dal server)
✅ **Latency bassa** (LAN/localhost)
✅ **Nessun rate limit esterno**
✅ **Offline-capable**

### Contro
⚠️ **Richiede GPU** per performance decenti
⚠️ **Manutenzione modelli** (pull, update)
⚠️ **Limite memoria** (modelli grandi = RAM alta)

### Hybrid Approach (Consigliato)
```python
def get_llm_client():
    """Ritorna client LLM disponibile con fallback"""
    if settings.ollama_enabled:
        return OllamaClient()
    elif settings.ANTHROPIC_API_KEY:
        return AnthropicClient()
    else:
        raise RuntimeError("No LLM configured")
```

---

## CONCLUSIONE

Il backend Miracollo ha una **struttura molto pulita e modulare**.

### Dove mettere Ollama Client
```
✅ backend/services/ollama/    # Pattern service modulare
✅ backend/core/config.py      # Aggiungere OLLAMA_* settings
✅ backend/routers/ollama_api.py  # Opzionale, per test/debug
```

### Pattern da seguire
1. **PagonLine pattern**: Client class + models + exceptions
2. **Stripe pattern**: Funzioni helper + import condizionale
3. **Document Scanner pattern**: Graceful degradation

### File da creare (ordine)
1. `services/ollama/client.py` (core logic)
2. `services/ollama/models.py` (Pydantic)
3. `services/ollama/exceptions.py` (errors)
4. `services/ollama/__init__.py` (exports)
5. `core/config.py` (add settings)
6. `tests/test_ollama.py` (validation)

**Tempo stimato**: 2-3 ore per MVP completo + test.

---

**Report completato**. Pronta per implementazione! 🐍
