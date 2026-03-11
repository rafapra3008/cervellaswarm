# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-11 - Sessione 441
> **STATUS:** FASE E in progress. E.1-E.4 DONE! Pronta per E.5 La Nonna Demo.

---

## SESSIONE 441 - E.4 Voice Interface COMPLETO

### E.4 Voice Interface (NUOVO!)
**VoiceProcessor** implementato: STT locale via faster-whisper, push-to-talk con ENTER.
- `_voice.py` (~290 LOC): VoiceProcessor (Callable[[str], str]), push-to-talk, lazy model loading
- **Stack scelto** (ricerca 24 fonti): faster-whisper + sounddevice (standard de facto)
- **Scartati**: Claude voice (EN only, non API), Vosk (WER 20-35% IT/PT), cloud APIs (privacy)
- **Integrazione**: `input_fn` injection su ChatSession -- ZERO modifiche a `_intent_bridge.py`
- CLI: `lu chat --voice [--voice-model tiny|base|small|medium|turbo|large-v3]`
- Optional dep: `pip install cervellaswarm-lingua-universale[voice]`
- 1 audit Guardiana: 9.5/10, 6 P3 tutti fixati
- **70 test** in 8 classi (structure, deps, init, model, call, record, transcribe, CLI)

### File chiave (E.4)
- `_voice.py` (NUOVO): VoiceProcessor, VoiceProcessorError, _record_audio, _transcribe
- `_cli.py` (modificato): +--voice, +--voice-model
- `pyproject.toml`: +[voice] optional dep (faster-whisper, sounddevice)
- `__init__.py`: +VoiceProcessor, VoiceProcessorError in __all__
- `test_voice.py` (NUOVO): 70 test
- Report ricerca: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260311_E4_VOICE_INTERFACE.md`

### Decisioni architetturali E.4 (con PERCHE)
1. faster-whisper (non Whisper API) -- privacy, offline, zero costo, 4x piu veloce
2. sounddevice (non PyAudio) -- cross-platform wheels, Python 3.13 compatible
3. Push-to-talk ENTER (non VAD) -- zero false positives, semplice, come Claude Code
4. Model "small" default -- 466MB, WER 10-12% IT/PT, latenza 0.8-2s su Mac M1+
5. input_fn injection -- VoiceProcessor.__call__ e un drop-in per input()
6. Lazy model loading -- scarica ~466MB solo al primo uso

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A-D: COMPLETE (A+B+C+D, 25 moduli base, media 9.5/10)
  FASE E: PER TUTTI -- IN PROGRESS
    E.1 Script "La Nonna"           DONE (S438)
    E.2 IntentBridge Core           DONE (S438-S440, 9.5/10)
    E.3 NL Processing               DONE (S440, 9.5/10)
    E.4 Voice Interface              DONE (S441, 9.5/10)
    E.5 La Nonna Demo               TODO <-- PROSSIMO
    E.6 CervellaLang 1.0            TODO
  PyPI: v0.3.0 (waiting Rafa environment approval)
```

---

## PROSSIMA SESSIONE

### E.5 La Nonna Demo Finale
1. Demo end-to-end come da script (3 minuti)
2. Video registrato (screen recording + narrazione)
3. Blog post "From Vibe Coding to Vericoding: La Nonna Edition"
4. Test persona non-tecnica reale (feedback)
5. Script: `.sncp/progetti/cervellaswarm/reports/SCRIPT_LA_NONNA_DEMO.md`

### TODO Rafa
- Approvare PyPI publish environment su GitHub

### BACKLOG
- 3 Dependabot PR rimaste (SKIP tier): #19 stripe, #14 express, #11 zod
- VS Code Marketplace (publisher account)
- Refactoring P2 residuo: _lsp.create_server() 136 righe (rimandato)

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test LU | **3249** |
| Test totali (13 pkg) | **~5561** |
| Moduli LU | **28** (+_voice.py) |
| Audit Guardiana S441 | **9.5/10** (6 P3 tutti fixati) |
| PyPI | **v0.3.0** (waiting approval) |
| IntentBridge test | **340** (55 core + 47 session + 100 e2e + 68 NL + 70 voice) |

---

## Lezioni Apprese (S441)

### Cosa ha funzionato bene
- **Formula Magica: Ricerca PRIMA** -- 24 fonti STT, raccomandazione chiara, zero incertezza durante implementazione
- **input_fn injection** -- pattern elegantissimo, ZERO modifiche al bridge. Voice = solo un wrapper di input()
- **Mock strategy: MAI mock numpy globale** -- il mock numpy contamina pytest.approx(). Mocking locale con patch.dict
- **Guardiana dopo ogni step** CONFERMATO -- trovati 6 P3, tutti fixati, da 9.3 a 9.5

### Cosa non ha funzionato
- **Tester mock globale** -- la prima versione dei test iniettava mock numpy in sys.modules globale, rompendo 79 test di confidence/trust. Fix: mocking solo locale

### Pattern confermato
- **"Script PRIMA, codice DOPO"** (S438) -> ora anche "Ricerca PRIMA, codice DOPO" (S441)
- **P3 = diamante** -- fixare tutti i P3 porta consistentemente a 9.5/10
- **Agenti fuori context** -- Tester e Guardiana lavorano fuori, Regina controlla e integra

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S441*
