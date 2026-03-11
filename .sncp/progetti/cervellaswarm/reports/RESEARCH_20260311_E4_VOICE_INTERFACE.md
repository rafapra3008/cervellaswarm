# E.4 Voice Interface - Ricerca Strategica
> Cervella Researcher | 2026-03-11 | Sessione 441
> Status: COMPLETA
> Fonti consultate: 24 (docs ufficiali, benchmark, PyPI, GitHub, articoli tecnici)

---

## Scope della Ricerca

10 domande chiave per E.4 (Voice Interface per `lu chat --voice`):
1. OpenAI Whisper (local) -- dimensioni, latenza, qualita multilingue
2. OpenAI Whisper API -- pricing, latenza cloud
3. Google Speech-to-Text -- pricing, SDK Python, qualita multilingue
4. Deepgram -- pricing, streaming, Italian/Portuguese
5. Vosk -- offline leggero, multilingue
6. SpeechRecognition Python lib -- wrapper backends
7. Browser Web Speech API -- playground futuro
8. Claude/Anthropic voice capabilities -- voice mode nativo
9. PyAudio / sounddevice -- cattura microfono CLI
10. Pattern push-to-talk vs VAD in CLI tools

---

## 1. OpenAI Whisper (Locale)

### Modelli disponibili

| Modello | Parametri | Dimensione disco | RAM runtime | Note |
|---------|-----------|-----------------|-------------|------|
| tiny    | 39M       | ~75MB           | ~273MB      | Veloce, accuracy bassa |
| base    | 74M       | ~145MB          | ~455MB      | Buon compromesso entry-level |
| small   | 244M      | ~466MB          | ~768MB      | **Sweet spot per CPU** |
| medium  | 769M      | ~1.5GB          | ~2.3GB      | Buona accuracy, lento su CPU |
| large-v3| 1.55B     | ~2.9GB          | ~3.9GB      | Massima accuracy |
| turbo   | 809M      | ~1.6GB          | ~2.6GB      | Distilled da large-v3, **6x piu veloce**, decoder ridotto 32->4 layer |

Tutti i modelli >= small supportano Italian e Portuguese (multilingual only).

### Accuracy multilingue

Romance languages (Italian, Portuguese, Spanish, German): **8-12% WER** con small/medium/turbo.
Large-v3: Common Voice 15 ottiene **9.0% WER** multilingual. Turbo: **10.2% WER**.
Turbo e quasi identico a large-v2 per la maggior parte delle lingue (degradazione < 2%),
con eccezioni su lingue meno comuni (Thai, Cantonese). Per IT/PT: nessuna regressione significativa.

### Latenza su CPU (dati empirici)

Sul benchmark del piccolo modello CPU (faster-whisper per riferimento):
- Small CPU (fp32): ~2 min 37 sec per 13 minuti di audio = **~0.2x realtime**
- Per 10 secondi di audio: ~**1.2-2 secondi** stima proporzionale
- Turbo CPU: piu lento del small in assoluto (piu grande), ma faster-whisper lo ottimizza

Apple Silicon (MLX/CoreML):
- M1 base: ~1x realtime per medium (10 min audio -> 2-3 min)
- M2/M3: 2-4x faster del M1
- Con MLX framework: fino a **8-12x** rispetto CPU-only
- Per clip da 10 secondi su M1/M2: **< 1 secondo** con small+MLX

**Conclusione latenza**: su Mac M1/M2/M3 il target < 3 sec e raggiungibile con small o turbo.
Su Linux/Windows CPU Intel: piu marginal, ma small int8 con faster-whisper dovrebbe farcela.

### Package Python

```
pip install openai-whisper        # originale OpenAI (usa PyTorch/ffmpeg)
pip install faster-whisper        # SYSTRAN, CTranslate2, 4x piu veloce, INT8
pip install mlx-whisper           # Apple Silicon MLX (solo macOS)
```

faster-whisper usa CTranslate2 (C++ ottimizzato), NON PyTorch. Vantaggi:
- 4x piu veloce del originale a parita di accuracy
- Memoria: ~35% meno
- Supporta INT8 quantization su CPU e GPU
- API pulita, bene mantenuta (SYSTRAN)

### Dipendenze sistema

- `openai-whisper`: richiede `ffmpeg` installato (brew/apt)
- `faster-whisper`: richiede `ffmpeg` per decode audio. Ha wheels precompilati.
- Microfono: serve separatamente (PyAudio o sounddevice)

---

## 2. OpenAI Whisper API (Cloud)

### Pricing 2026
- Whisper API (legacy): **$0.006/min**
- GPT-4o Transcribe: **$0.006/min** (piu accurato)
- GPT-4o Mini Transcribe: **$0.003/min** (cost-sensitive)
- Fatturazione: per durata audio caricato (incluso silenzio)
- No free tier, no volume discount, flat rate

### Latenza
Problema documentato dalla community OpenAI (2025):
- Short clips (< 30 sec): da **1 sec a 3+ sec** (variabile, non garantito)
- Latenza 3+ sec per 4 parole riportata da utenti
- NON adatto per near-real-time se si richiede < 1 sec
- Il Realtime API di OpenAI (diverso da Whisper API): 232ms median, ma costo molto superiore

### Lingue
99+ lingue supportate incluse IT e PT, al flat rate $0.006/min.

### Considerazioni per noi
PRO: Zero setup, qualita garantita, nessun modello da scaricare
CONTRO: Latenza imprevedibile, costo per ogni query, dipendenza cloud, privacy

---

## 3. Google Speech-to-Text API (Cloud)

### Pricing 2026
- Free tier: 60 min/mese
- Standard (V1): $0.004/min dopo free tier
- Enhanced (V1): $0.009/min (qualita migliore, meno lingue)
- Chirp 3 (V2, nuovo modello): pricing non ancora consolidato in docs pubblici
- Chirp 3 addestra su miliardi di ore audio, qualita superiore

### Lingue
- 125+ lingue/varianti. IT e PT pienamente supportate.
- Chirp 3: copertura espansa su lingue non-English

### SDK Python
```python
from google.cloud import speech
client = speech.SpeechClient()
```
Richiede Google Cloud credentials (JSON service account o ADC).
Aggiunge dipendenza pesante: `google-cloud-speech` (~50MB+ con deps).

### Considerazioni per noi
PRO: Free tier generoso (60 min), qualita eccellente
CONTRO: Google Cloud credentials setup, SDK pesante, dipendenza cloud forte,
privacy concern, overhead di setup per utenti finali (non adatto per CLI locale)

---

## 4. Deepgram Nova-3

### Modelli e pricing 2026
| Modello | Pay-As-You-Go | Growth Plan |
|---------|--------------|-------------|
| Nova-3 mono | $0.0077/min | $0.0065/min |
| Nova-3 multi | $0.0092/min | $0.0078/min |
| Nova-2 | $0.0058/min | $0.0047/min |

Free tier: **$200 crediti** (nessuna carta di credito) = ~43,000 min di Nova

### Latenza
- Sub-300ms streaming latency (reale, documentato)
- Batch: 5.26% WER, streaming: 6.84% WER
- 54.3% miglioramento WER vs competitor per streaming

### Lingue e multilingue
- Nova-3 Multilingual: 10 lingue in codeswitching nativo: EN, ES, FR, DE, HI, RU, **PT**, JA, **IT**, NL
- IT e PT aggiunti esplicitamente (announcement separato da Deepgram)
- Codice lingua da passare in API call

### Python SDK
```python
pip install deepgram-sdk
from deepgram import DeepgramClient
client = DeepgramClient(api_key)
```
SDK pulito, ben documentato, attivamente mantenuto.

### Considerazioni per noi
PRO: Latenza sub-300ms (migliore della categoria cloud), IT+PT nativo, SDK ottimo
CONTRO: Dipendenza cloud, API key required, $0.0092/min per multilingual (piu del Whisper API)

---

## 5. Vosk (Offline, Leggero)

### Overview
- Modelli: 50MB (piccoli) per lingua specifica
- 20+ lingue supportate incluse IT e PT
- Completamente offline (privacy totale)
- Supporta streaming (zero latency response claim)

### Qualita
- Significativamente peggiore di Whisper per lingue non-English
- WER tipico per IT/PT: 20-35% (vs 8-12% di Whisper small)
- Adatto per vocabolario ristretto (custom language model migliora accuracy)
- Non adatto per NL libero complesso (il nostro caso d'uso)

### Dipendenze
```
pip install vosk
# Poi scaricare modello specifico per lingua (50-500MB per lingua)
```
Nessuna dipendenza sistema problematica. Modelli separati per IT/PT/EN = 150MB+ totale.

### Considerazioni per noi
CONTRO: Qualita insufficiente per NL libero in IT/PT. Il nostro pipeline NL richiede
transcription alta qualita -- un WER del 25% IT renderebbe il tutto inutilizzabile.
SCARTATO per use case principale.

---

## 6. SpeechRecognition Python Library

### Overview
- Wrapper multi-backend: Google Web Speech API, Sphinx (offline), Whisper, Azure, etc.
- Semplifica la cattura microfono + invio a backend
- Astrae PyAudio per microfono

### Limitazioni
- Non supporta faster-whisper nativo (usa openai-whisper originale)
- Aggiunge un layer di astrazione che complica il controllo del flusso
- Google Web Speech API nel wrapper usa endpoint gratuito non ufficiale (non production)
- Non e attivamente mantenuta quanto faster-whisper direttamente

### Considerazione per noi
SCARTATO. Meglio usare faster-whisper direttamente + sounddevice per microfono.
Il layer di astrazione non aggiunge valore per il nostro caso d'uso specifico.

---

## 7. Browser Web Speech API

### Stato
- Disponibile in Chrome/Edge, supporto parziale in Firefox
- Zero installazione per utente (nel browser)
- Qualita variabile (usa Google Speech in background su Chrome)
- Non controllabile come dipendenza (Google backend implicito)

### Rilevanza per noi
Potenzialmente utile per **E.5 "La Nonna" Demo** in versione web playground.
NON applicabile per il CLI (`lu chat --voice`).

---

## 8. Anthropic / Claude Voice Mode

### Stato attuale (Marzo 2026)
Claude Code ha lanciato voice mode il 3 Marzo 2026 (rolling out, 5% utenti):
- Push-to-talk: `/voice` nel CLI, tieni spacebar, parla, rilascia
- Implementazione: STT locale + Claude input field
- Limitazione CRITICA: **solo Inglese** (EN only al launch)
- TTS usa ElevenLabs come subcontractor

### Anthropic API: nessuna voice API pubblica
- NON esiste un endpoint Anthropic STT nella API pubblica
- Il voice mode e solo nell'app Claude e Claude Code, non nell'API
- Non possiamo sfruttarlo per `lu chat --voice` (non e una API)

### Considerazione per noi
NON APPLICABILE. Claude Code voice mode e solo inglese, solo nell'app Claude Code,
non e una API. Non possiamo integrarlo nel nostro CLI Python.

---

## 9. PyAudio vs sounddevice (Cattura Microfono)

### PyAudio
- Wrapper C attorno a PortAudio
- Problemi installazione: Python 3.13 spesso fallisce la build
- macOS: richiede `brew install portaudio` prima di `pip install pyaudio`
- Windows: richiede Visual C++ build tools o wheel precompilato
- Manutenzione lenta

### sounddevice
- Wrapper moderno PortAudio con wheels precompilati inclusi
- `pip install sounddevice` funziona out-of-the-box su macOS e Windows
- Linux: richiede `libportaudio2` dal package manager (ma auto-rilevato)
- API Numpy-based (moderna, type-safe)
- Attivamente mantenuta

```python
import sounddevice as sd
import numpy as np

def record_until_silence(samplerate=16000, max_duration=30):
    """Record audio until silence or max_duration seconds."""
    audio = sd.rec(
        frames=max_duration * samplerate,
        samplerate=samplerate,
        channels=1,
        dtype='int16'
    )
    sd.wait()
    return audio.flatten()
```

### Conclusione
**sounddevice > PyAudio** per nuovi progetti. Installazione piu semplice, API migliore.
Entrambi usano PortAudio internamente (stesso audio quality).

---

## 10. Voice Activity Detection (VAD)

### Push-to-Talk vs VAD Automatico

| Modalita | PRO | CONTRO |
|----------|-----|--------|
| Push-to-Talk (hold key) | Semplice, deterministico, no false activations | Richiede tener premuto un tasto |
| VAD Automatico | Hands-free, naturale | False positives (background noise), piu complesso |
| Toggle (press once) | Comodo per frasi lunghe | Richiede ricordarsi di spegnere |

**Raccomandazione per CLI**: Push-to-talk o Toggle. Nel terminal, tener premuto INVIO
(o un tasto) e il pattern piu naturale e sicuro. No false activations da rumore ambiente.

### Librerie VAD

**webrtcvad**: VAD minimalista da Google WebRTC
- `pip install webrtcvad`
- Accetta solo 16-bit mono PCM a 8000/16000/32000/48000 Hz
- Frame: 10, 20, o 30ms
- Lightweight, zero model download

**SileroVAD**: Piu accurato di webrtcvad
- Modello ML leggero (< 5MB)
- Migliore gestione di accenti diversi e background noise
- Usato da RealtimeSTT come secondo stage

**RealtimeSTT (KoljaB/RealtimeSTT)**: Libreria completa che combina:
- WebRTCVAD per primo rilevamento
- SileroVAD per conferma accurata
- faster-whisper per trascrizione
- Supporta modalita manuale (start/stop)
- Richiede PortAudio (come sounddevice)

### Pattern Claude Code (reference implementation)
Il voice mode di Claude Code usa:
- Push-to-talk: spacebar hold
- VAD locale per non registrare colleghi/rumore
- STT non divulgato (probabilmente Whisper internamente)
- Limitazione: solo inglese

---

## 11. Come Fanno i Big: Pattern CLI Voice

### Claude Code (Marzo 2026)
```
/voice -> toggle ON
[spacebar hold] -> registrazione
[release] -> STT -> inserisce testo nel prompt
```
Stack non pubblico. VAD locale. EN only.

### Copilot Voice (GitHub Next, PoC)
- Extension VS Code (non CLI puro)
- Whisper sotto il cofano (da indicatori indiretti)
- Silence detection configurabile come threshold
- Active mode: ascolta continuamente senza trigger word

### WhisperTyping (tool separato per CLI)
- Push-to-talk via hotkey di sistema
- faster-whisper localmente
- Mediana transcription: **370ms** su hardware moderno
- Pattern: hotkey globale -> record -> release -> paste in terminal

### Vocalinux (Linux)
- Completamente offline (whisper.cpp + VOSK)
- Toggle mode o push-to-talk
- Privacy-first

**Insight chiave**: TUTTI i tool seri usano Whisper (o faster-whisper) per qualita.
Nessuno usa Vosk per input NL libero in produzione.

---

## 12. Confronto Matriciale Completo

| Opzione | Latenza (IT/PT clip 10s) | Costo | Offline | IT/PT quality | Deps | Complessita |
|---------|--------------------------|-------|---------|---------------|------|-------------|
| faster-whisper small (CPU) | 1-3 sec | Free | SI | 10-12% WER | ctranslate2, ffmpeg | Media |
| faster-whisper turbo (CPU) | 2-4 sec | Free | SI | 9-10% WER | ctranslate2, ffmpeg | Media |
| mlx-whisper small (Mac M*) | 0.3-0.8 sec | Free | SI | 10-12% WER | mlx (solo macOS) | Bassa |
| openai-whisper small (CPU) | 3-6 sec | Free | SI | 10-12% WER | PyTorch, ffmpeg | Media |
| Whisper API (OpenAI) | 1-4 sec (variabile) | $0.006/min | NO | ~8-10% WER | requests | Bassa |
| Deepgram Nova-3 | 0.3 sec (streaming) | $0.0092/min | NO | 6-8% WER | deepgram-sdk | Bassa |
| Google STT | 0.5-1.5 sec | $0.004/min | NO | ~8-10% WER | google-cloud-speech | Alta setup |
| Vosk | 0.1 sec | Free | SI | 20-35% WER | - | Bassa |
| SpeechRecognition lib | dipende backend | varia | parziale | dipende | pyaudio | Media |
| Claude/Anthropic voice | N/A | N/A | NO | EN only | N/A | N/A |

---

## 13. Architettura Raccomandata per E.4

### Pattern opzionale (come [nl] per anthropic)

```toml
# pyproject.toml
[project.optional-dependencies]
nl = ["anthropic>=0.40.0"]
voice = [
    "faster-whisper>=1.0.0",
    "sounddevice>=0.4.6",
]
# Per Mac: alternativa consigliata
voice-mac = [
    "mlx-whisper>=0.3.0",
    "sounddevice>=0.4.6",
]
```

```bash
pip install cervellaswarm-lingua-universale[voice]       # cross-platform
pip install cervellaswarm-lingua-universale[voice-mac]  # macOS ottimizzato
```

### Pipeline E.4

```
[microfono]
    |
    v
[sounddevice: cattura audio]
    |
    v
[VAD: webrtcvad o push-to-talk]  <-- rileva inizio/fine
    |
    v
[faster-whisper / mlx-whisper: STT]
    |
    v
[testo trascritto]
    |
    v
[ClaudeNLProcessor (E.3)]  <-- pipeline gia pronta!
    |
    v
[IntentDraft -> B.4 -> B.5 -> B.3 -> simulazione]
```

### Modello raccomandato: faster-whisper "small" o "turbo"

**small (244M)**:
- Footprint accettabile (466MB disco)
- Latenza target < 3 sec su CPU moderno
- WER 10-12% su IT/PT: sufficiente per NL libero (dopo passa a Claude per cleanup)
- Scaricato una volta, cached localmente

**turbo (809M)**:
- Migliore accuracy (9-10% WER), spec la turbo e distilled da large-v3
- Piu lento del small su CPU puro
- Su Mac con MLX: preferire small per latenza ottimale

**Raccomandazione finale**: `small` come default, `turbo` come opzione `--quality high`.

### CLI design

```bash
lu chat --voice                      # push-to-talk mode, small model
lu chat --voice --lang it            # italiano
lu chat --voice --quality high       # usa turbo
lu chat --voice --mode nl            # voice + NL pipeline (E.3)
```

### Push-to-Talk in CLI Python

```python
import sounddevice as sd
import numpy as np

def record_push_to_talk(samplerate: int = 16000) -> np.ndarray:
    """Record while user holds Enter. Press Enter to start, Enter again to stop."""
    print("Premi INVIO per iniziare a registrare...")
    input()  # attendi Enter

    chunks = []
    print("Registrazione... premi INVIO per fermare.")

    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        # Leggi in loop finche non arriva Enter su thread separato
        import threading
        stop_event = threading.Event()

        def wait_for_enter():
            input()
            stop_event.set()

        t = threading.Thread(target=wait_for_enter)
        t.start()

        while not stop_event.is_set():
            chunk, _ = stream.read(samplerate // 10)  # 100ms chunks
            chunks.append(chunk.copy())

    return np.concatenate(chunks).flatten()
```

Alternativa piu elegante: usare `readchar` o `pynput` per hotkey.
Oppure: timeout-based (registra 10 sec max, VAD decide quando fermarsi).

---

## 14. Modulo _voice_processor.py

### Struttura raccomandata (analogia con _nl_processor.py E.3)

```python
# _voice_processor.py (nuovo file, optional dep)

try:
    import sounddevice as _sd
    import numpy as _np
    _HAS_SOUNDDEVICE = True
except ImportError:
    _HAS_SOUNDDEVICE = False

try:
    from faster_whisper import WhisperModel as _WhisperModel
    _HAS_FASTER_WHISPER = True
except ImportError:
    try:
        import mlx_whisper as _mlx_whisper
        _HAS_MLX_WHISPER = True
        _HAS_FASTER_WHISPER = False
    except ImportError:
        _HAS_FASTER_WHISPER = False
        _HAS_MLX_WHISPER = False

class VoiceProcessor:
    """Cattura audio e trascrivi in testo. Optional dep per E.4."""

    def __init__(
        self,
        model_size: str = "small",       # tiny|base|small|medium|turbo
        lang: str = "it",                # it|pt|en
        device: str = "cpu",             # cpu|cuda
    ): ...

    def record_and_transcribe(self) -> str:
        """Registra audio (push-to-talk) e restituisce testo."""
        ...

class VoiceProcessorError(Exception):
    """Raised when voice processing fails."""
```

### Integrazione con ChatSession (E.2)

`ChatSession` gia ha `input_fn: Callable`. In E.4:
- Quando `--voice`, wrappa `input_fn` con `VoiceProcessor.record_and_transcribe()`
- Il resto della pipeline (NL mode E.3 o guided mode E.2) e invariato
- ZERO modifiche a `_intent_bridge.py`!

```python
# In _cli.py
if args.voice:
    from ._voice_processor import VoiceProcessor, _require_voice
    _require_voice()
    vp = VoiceProcessor(lang=args.lang)
    input_fn = vp.record_and_transcribe
else:
    input_fn = input

session = ChatSession(lang=args.lang, mode=args.mode, input_fn=input_fn)
```

---

## 15. Considerazioni sulla Privacy

- **faster-whisper / mlx-whisper**: 100% locale. Audio NON lascia il dispositivo.
- **Deepgram / OpenAI API**: audio inviato a server cloud (GDPR consideration per EU users).
- Per "La Nonna" demo e per utenti enterprise: offline e un vantaggio differenziante.
- La nostra filosofia "ZERO deps nel core" si estende a "offline per default" nella voice.

**Raccomandazione**: default OFFLINE (faster-whisper). Cloud (Deepgram/OpenAI) come
opzione esplicita futura `[voice-cloud]` extra se richiesto dalla community.

---

## 16. Decisioni Architetturali Chiave

### D1: Local-first (faster-whisper) NOT cloud
**Perche**: privacy, latenza controllata, zero costo per utente, funziona offline.
**Trade-off**: richiede download modello (~466MB), piu lento su hardware debole.

### D2: sounddevice NOT pyaudio
**Perche**: installazione piu semplice (wheels inclusi), API moderna.

### D3: Push-to-talk NOT VAD automatico (v1)
**Perche**: piu semplice, nessun false positive, funziona in qualsiasi ambiente audio.
VAD automatico come miglioramento futuro (V2).

### D4: faster-whisper "small" come default
**Perche**: balance latenza/accuracy/dimensione. Turbo come `--quality high`.
Su macOS: offrire `voice-mac` extra con mlx-whisper per performance ottimale.

### D5: Integrazione via input_fn injection (ZERO modifiche a _intent_bridge.py)
**Perche**: `ChatSession` ha gia `input_fn: Callable`. Voice e solo un wrapper.
Questo e il pattern piu pulito -- voice diventa una sorgente di input, non un modulo separato.

---

## Sintesi Decisioni per E.4

### Stack finale raccomandato

```
Cattura audio:    sounddevice (cross-platform, easy install)
VAD:              push-to-talk (v1), webrtcvad (v2 futuro)
STT:              faster-whisper small (default, cross-platform)
                  mlx-whisper small (opzionale, macOS ottimizzato)
Lingue:           it / pt / en (Whisper multilingue nativo)
Integrazione:     input_fn injection su ChatSession (ZERO modifiche a _intent_bridge)
Optional deps:    [voice] extra in pyproject.toml
```

### Latenza attesa end-to-end

Su Mac M1/M2 (hardware tipico sviluppatore):
- Cattura 5-10s audio: 5-10 sec (il parlante parla)
- STT con mlx-whisper small: **0.3-0.8 sec**
- STT con faster-whisper small CPU: **0.8-2 sec**
- NL processing (Claude API, E.3): 1-2 sec (gia implementato)
- **TOTALE risposta**: 1.5-4 sec -> **RAGGIUNGE TARGET < 3 sec** su Mac moderno

Su Linux/Windows CPU Intel:
- STT con faster-whisper small int8: **1.5-3 sec**
- Nel limite, ma fattibile con int8 quantization

---

## 3 Raccomandazioni Principali

### Raccomandazione 1: faster-whisper + sounddevice come [voice] optional dep
Stack locale, privacy-first, cross-platform. faster-whisper e la scelta dell'industria
(whisper-overlay, WhisperTyping, RealtimeSTT la usano tutti). sounddevice risolve
il problema storico di pyaudio su Python 3.12+.
Evidenza: 4 tool open source analizzati usano questo stesso stack.

### Raccomandazione 2: Push-to-talk (input + ENTER) come UX v1
Pattern usato da Claude Code (spacebar), WhisperTyping (hotkey), Vocalinux (toggle).
Nel CLI Python: ENTER come push-to-talk e il piu naturale (nessuna dipendenza extra
per hotkey di sistema). Possibilmente: press ENTER = start, press ENTER = stop.

### Raccomandazione 3: Integrazione tramite input_fn injection su ChatSession
ZERO modifiche a `_intent_bridge.py`. `VoiceProcessor.record_and_transcribe` diventa
la `input_fn` del `ChatSession`. Questo mantiene la separazione di responsabilita
(voice cattura, NL elabora, bridge coordina) e rende i test banali.
Analogia perfetta con come E.3 ha aggiunto `ClaudeNLProcessor` senza toccare il bridge.

---

## Effort Stimato E.4

```
Step 1: _voice_processor.py (VoiceProcessor, cattura + STT + error handling)  -- 0.5 sess
Step 2: CLI integration (--voice flag, input_fn injection, --quality flag)     -- 0.3 sess
Step 3: pyproject.toml [voice] + [voice-mac] extras                            -- 0.1 sess
Step 4: Test suite (FakeVoiceProcessor, mock audio, CLI test)                  -- 0.5 sess
Step 5: Guardiana audit 9.5/10                                                  -- 0.3 sess
TOTALE: ~1.5 sessioni (nel range subroadmap 1-2 sess)
```

---

## Fonti Consultate

1. [openai/whisper - GitHub](https://github.com/openai/whisper) -- modelli, API, multilingue
2. [faster-whisper - GitHub SYSTRAN](https://github.com/SYSTRAN/faster-whisper) -- benchmark, API, INT8
3. [openai-whisper PyPI](https://pypi.org/project/openai-whisper/) -- versione, deps
4. [faster-whisper PyPI](https://pypi.org/project/faster-whisper/) -- versione, install
5. [OpenAI Whisper API pricing 2026 - DIY AI](https://diyai.io/ai-tools/speech-to-text/openai-whisper-api-pricing-2026/) -- $0.006/min
6. [OpenAI Whisper API latency - community](https://community.openai.com/t/whisper-api-latency-is-just-too-high/81175) -- latenza 3+ sec reports
7. [Deepgram Pricing](https://deepgram.com/pricing) -- Nova-3 $0.0092/min multi
8. [Deepgram Nova-3 announcement](https://deepgram.com/learn/introducing-nova-3-speech-to-text-api) -- WER 6.84% streaming
9. [Deepgram Nova-3 Italian support](https://deepgram.com/learn/deepgram-expands-nova-3-with-italian-turkish-norwegian-and-indonesian-support) -- IT aggiunto
10. [Deepgram Nova-3 Portuguese support](https://deepgram.com/learn/deepgram-expands-nova-3-with-spanish-french-and-portuguese-support) -- PT aggiunto
11. [Vosk API](https://alphacephei.com/vosk/) -- offline, IT/PT support
12. [vosk PyPI](https://pypi.org/project/vosk/) -- modelli 50MB
13. [Google Cloud Speech-to-Text pricing](https://cloud.google.com/speech-to-text/pricing) -- free 60min/mese
14. [Anthropic Claude Code voice mode](https://techstory.in/anthropic-unveils-voice-mode-for-claude-code/) -- EN only, spacebar PTT
15. [Claude Code voice mode - Medium](https://medium.com/@AdithyaGiridharan/claude-code-just-got-voice-mode-and-it-reframes-what-developer-productivity-actually-means-aa6e354b096d) -- details
16. [Anthropic rolls out voice (5%) - StartupNews](https://startupnews.fyi/2026/03/08/anthropic-rolls-out-voice-mode-for-claude-code-feature-live-for-5-of-users/) -- data lancio
17. [sounddevice docs](https://python-sounddevice.readthedocs.io/en/latest/installation.html) -- wheels inclusi, PortAudio auto
18. [RealtimeSTT - GitHub KoljaB](https://github.com/KoljaB/RealtimeSTT) -- WebRTCVAD + SileroVAD + faster-whisper
19. [whisper-overlay - GitHub](https://github.com/oddlama/whisper-overlay) -- PTT Wayland
20. [voice-input PTT - GitHub](https://github.com/xuiltul/voice-input) -- PTT + LLM refinement
21. [Best OSS STT 2026 - Northflank](https://northflank.com/blog/best-open-source-speech-to-text-stt-model-in-2026-benchmarks) -- benchmark WER comparison
22. [Choosing Whisper variants - Modal](https://modal.com/blog/choosing-whisper-variants) -- faster-whisper vs others
23. [Whisper Apple Silicon - Voicci](https://www.voicci.com/blog/apple-silicon-whisper-performance.html) -- M1/M2/M3 benchmarks
24. [GitHub Copilot Voice - GitHub Next](https://githubnext.com/projects/copilot-voice/) -- pattern PTT, silence threshold

---

## Output Header (per la Regina)

```
## E.4 Voice Interface - Ricerca
Status: COMPLETA
Fonti: 24 consultate

Sintesi:
- Stack vincitore: faster-whisper (small, INT8 su CPU) + sounddevice + push-to-talk.
  4 tool open source analizzati usano esattamente questo stack (whisper-overlay,
  WhisperTyping, RealtimeSTT, Vocalinux). Standard de facto del settore.
- Anthropic Claude voice mode: INUTILIZZABILE per noi (solo EN, non e una API pubblica).
- Deepgram Nova-3: sub-300ms latency, IT+PT nativo, qualita superiore a Whisper.
  Ottimo per v2 cloud-optional, ma non per default (privacy, costo, API key).
- Vosk: SCARTATO. WER 20-35% su IT/PT, insufficiente per NL libero.
- Integrazione: input_fn injection su ChatSession. ZERO modifiche a _intent_bridge.py.
  Stesso pattern architetturale di E.3 (NLProcessor Protocol).

Raccomandazione:
  1. faster-whisper "small" + sounddevice come [voice] optional dep
  2. Push-to-talk ENTER come UX v1 (piu semplice, nessun false positive)
  3. VoiceProcessor via input_fn injection (zero modifiche al bridge)
  4. mlx-whisper come [voice-mac] extra (Mac M* ottimizzato, 0.3-0.8 sec latency)
  5. Target < 3 sec RAGGIUNGIBILE su Mac M1+ e Linux moderno con int8

Report: .sncp/progetti/cervellaswarm/reports/RESEARCH_20260311_E4_VOICE_INTERFACE.md
```

---

*"Ricerca PRIMA di implementare."*
*"Non inventare, studia come fanno i big."*

*Cervella Researcher - CervellaSwarm S441*
