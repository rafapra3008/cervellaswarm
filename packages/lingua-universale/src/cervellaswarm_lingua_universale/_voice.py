# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Voice input processor: microphone capture + STT for ``lu chat --voice`` (E.4).

Implements a ``Callable[[str], str]`` that replaces ``input()`` in
``ChatSession``.  Push-to-talk: user presses ENTER to start recording,
ENTER again to stop.  Audio is transcribed locally via *faster-whisper*
(offline, privacy-first).

The ``faster-whisper`` and ``sounddevice`` packages are **optional**
dependencies::

    pip install cervellaswarm-lingua-universale[voice]

Design decisions (E.4 research, 24 sources):
    D1: Local-first (faster-whisper) -- privacy, zero cost, offline.
    D2: sounddevice over PyAudio -- cross-platform wheels, modern API.
    D3: Push-to-talk (ENTER) -- simple, no false positives.
    D4: Model "small" as default -- best latency/accuracy trade-off.
    D5: Integration via input_fn injection -- ZERO changes to _intent_bridge.
    D6: Lazy model loading -- avoid startup delay, download only once.
"""

from __future__ import annotations

import sys
import threading
from typing import Any

from ._colors import colors as _c


# ============================================================
# i18n strings for voice prompts
# ============================================================

_VOICE_STRINGS: dict[str, dict[str, str]] = {
    "press_enter_start": {
        "en": "Press ENTER to start recording...",
        "it": "Premi INVIO per iniziare a registrare...",
        "pt": "Pressione ENTER para iniciar a grava\u00e7\u00e3o...",
    },
    "recording": {
        "en": "Recording... Press ENTER to stop.",
        "it": "Registrazione... Premi INVIO per fermare.",
        "pt": "Gravando... Pressione ENTER para parar.",
    },
    "transcribing": {
        "en": "Transcribing...",
        "it": "Trascrizione in corso...",
        "pt": "Transcrevendo...",
    },
    "heard": {
        "en": "Heard",
        "it": "Sentito",
        "pt": "Ouvido",
    },
    "empty_recording": {
        "en": "No speech detected. Please try again.",
        "it": "Nessun parlato rilevato. Riprova.",
        "pt": "Nenhuma fala detectada. Tente novamente.",
    },
    "loading_model": {
        "en": "Loading voice model '{model}' (first time may download ~{size})...",
        "it": "Caricamento modello voce '{model}' (il primo avvio scarica ~{size})...",
        "pt": "Carregando modelo de voz '{model}' (primeiro uso pode baixar ~{size})...",
    },
    "model_ready": {
        "en": "Voice model ready.",
        "it": "Modello voce pronto.",
        "pt": "Modelo de voz pronto.",
    },
    "mic_error": {
        "en": "Microphone error: {error}",
        "it": "Errore microfono: {error}",
        "pt": "Erro no microfone: {error}",
    },
}

# Model size -> approximate download size for user feedback
_MODEL_SIZES: dict[str, str] = {
    "tiny": "75 MB",
    "base": "145 MB",
    "small": "466 MB",
    "medium": "1.5 GB",
    "large-v3": "2.9 GB",
    "turbo": "1.6 GB",
}

# ============================================================
# Whisper language codes
# ============================================================

_LANG_TO_WHISPER: dict[str, str] = {
    "en": "en",
    "it": "it",
    "pt": "pt",
}


# ============================================================
# Exception
# ============================================================


class VoiceProcessorError(Exception):
    """Raised when voice capture or transcription fails."""


# ============================================================
# Dependency check
# ============================================================


def _require_voice_deps() -> None:
    """Raise ``ImportError`` with a helpful message if deps are missing."""
    missing: list[str] = []
    try:
        import sounddevice as _sd  # noqa: F401
    except ImportError:
        missing.append("sounddevice")
    try:
        from faster_whisper import WhisperModel as _W  # noqa: F401
    except ImportError:
        missing.append("faster-whisper")
    if missing:
        deps = ", ".join(missing)
        raise ImportError(
            f"Voice mode requires: {deps}. "
            f"Install with: pip install cervellaswarm-lingua-universale[voice]"
        )


# ============================================================
# Private helpers
# ============================================================


def _record_audio(
    *,
    samplerate: int,
    output_fn: Any,
    lang: str,
    input_fn: Any,
) -> Any:
    """Record audio using push-to-talk (ENTER to start, ENTER to stop).

    Returns a 1-D float32 numpy array at *samplerate* Hz.
    """
    import numpy as np
    import sounddevice as sd

    prompt_start = _VOICE_STRINGS["press_enter_start"].get(lang, "Press ENTER...")
    prompt_recording = _VOICE_STRINGS["recording"].get(lang, "Recording...")

    output_fn(f"  {_c.YELLOW}{prompt_start}{_c.RESET}")
    input_fn("")  # wait for ENTER

    chunks: list[Any] = []
    stop_event = threading.Event()

    def _audio_callback(
        indata: Any, frames: int, time_info: Any, status: Any
    ) -> None:
        # status flags (e.g. overflow) are not fatal for STT but logged
        # via output_fn for diagnostics if they occur.
        if status:
            output_fn(f"  {_c.YELLOW}[audio: {status}]{_c.RESET}")
        chunks.append(indata.copy())

    stream = sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype="float32",
        callback=_audio_callback,
    )

    output_fn(f"  {_c.RED}{prompt_recording}{_c.RESET}")
    stream.start()

    def _wait_for_stop() -> None:
        try:
            input_fn("")
        except (EOFError, KeyboardInterrupt):
            pass
        stop_event.set()

    stopper = threading.Thread(target=_wait_for_stop, daemon=True)
    try:
        stopper.start()
        stop_event.wait()
    finally:
        stream.stop()
        stream.close()

    if not chunks:
        return np.array([], dtype="float32")

    return np.concatenate(chunks).flatten()


def _transcribe(
    model: Any,
    audio: Any,
    lang: str,
) -> str:
    """Transcribe audio array using a faster-whisper model.

    Returns the joined text of all segments, stripped.
    """
    import numpy as np

    if len(audio) == 0:
        return ""

    whisper_lang = _LANG_TO_WHISPER.get(lang, "en")
    segments, _info = model.transcribe(
        audio,
        language=whisper_lang,
        beam_size=5,
        vad_filter=True,
    )
    parts = [segment.text for segment in segments]
    return " ".join(parts).strip()


# ============================================================
# VoiceProcessor
# ============================================================


class VoiceProcessor:
    """Capture microphone audio and transcribe to text.

    Drop-in replacement for ``input()`` -- pass as ``input_fn`` to
    ``ChatSession``.

    Parameters:
        lang:        Interface language (``"en"``, ``"it"``, ``"pt"``).
        model_size:  Whisper model (``"tiny"``, ``"base"``, ``"small"``,
                     ``"medium"``, ``"turbo"``, ``"large-v3"``).
        compute_type: Quantization (``"int8"``, ``"float16"``, ``"float32"``).
        samplerate:  Recording sample rate in Hz (default 16000).
        output_fn:   Callable for printing messages (default ``print``).
        raw_input_fn: Underlying ``input()`` for ENTER detection (default
                      ``builtins.input``).
    """

    DEFAULT_MODEL = "small"
    DEFAULT_SAMPLERATE = 16000
    DEFAULT_COMPUTE_TYPE = "int8"

    def __init__(
        self,
        *,
        lang: str = "en",
        model_size: str | None = None,
        compute_type: str | None = None,
        samplerate: int | None = None,
        output_fn: Any = None,
        raw_input_fn: Any = None,
    ) -> None:
        _require_voice_deps()

        if lang not in ("en", "it", "pt"):
            lang = "en"
        self._lang = lang
        self._model_size = model_size if model_size is not None else self.DEFAULT_MODEL
        self._compute_type = compute_type if compute_type is not None else self.DEFAULT_COMPUTE_TYPE
        self._samplerate = samplerate if samplerate is not None else self.DEFAULT_SAMPLERATE
        self._output_fn = output_fn or print
        self._raw_input_fn = raw_input_fn or input
        self._model: Any = None  # lazy loaded

    # ----------------------------------------------------------
    # Lazy model loading
    # ----------------------------------------------------------

    def _ensure_model(self) -> Any:
        """Load the Whisper model on first use (downloads if needed)."""
        if self._model is not None:
            return self._model

        from faster_whisper import WhisperModel

        size_str = _MODEL_SIZES.get(self._model_size, "unknown")
        loading_msg = _VOICE_STRINGS["loading_model"].get(self._lang, "Loading...")
        self._output_fn(
            f"  {_c.CYAN}{loading_msg.format(model=self._model_size, size=size_str)}"
            f"{_c.RESET}"
        )

        self._model = WhisperModel(
            self._model_size,
            device="cpu",
            compute_type=self._compute_type,
        )

        ready_msg = _VOICE_STRINGS["model_ready"].get(self._lang, "Ready.")
        self._output_fn(f"  {_c.GREEN}{ready_msg}{_c.RESET}")
        return self._model

    # ----------------------------------------------------------
    # Public API: __call__ (compatible with input_fn)
    # ----------------------------------------------------------

    def __call__(self, prompt: str = "") -> str:
        """Record audio and transcribe -- drop-in for ``input()``.

        Parameters:
            prompt: The prompt string from ``ChatSession`` (displayed to user).

        Returns:
            Transcribed text string.

        Raises:
            VoiceProcessorError: On microphone or transcription failure.
        """
        # Show the chat prompt (same as input() would)
        if prompt:
            sys.stdout.write(prompt)
            sys.stdout.flush()

        model = self._ensure_model()

        try:
            audio = _record_audio(
                samplerate=self._samplerate,
                output_fn=self._output_fn,
                lang=self._lang,
                input_fn=self._raw_input_fn,
            )
        except Exception as exc:
            mic_msg = _VOICE_STRINGS["mic_error"].get(self._lang, "Mic error")
            raise VoiceProcessorError(
                mic_msg.format(error=exc)
            ) from exc

        # Transcribe
        transcribing_msg = _VOICE_STRINGS["transcribing"].get(
            self._lang, "Transcribing..."
        )
        self._output_fn(f"  {_c.CYAN}{transcribing_msg}{_c.RESET}")

        text = _transcribe(model, audio, self._lang)

        if not text:
            empty_msg = _VOICE_STRINGS["empty_recording"].get(
                self._lang, "No speech detected."
            )
            self._output_fn(f"  {_c.YELLOW}{empty_msg}{_c.RESET}")
            return ""

        # Echo transcription so user sees what was heard
        heard_label = _VOICE_STRINGS["heard"].get(self._lang, "Heard")
        self._output_fn(
            f"  {_c.GREEN}{heard_label}: {_c.RESET}{_c.BOLD}{text}{_c.RESET}"
        )
        return text
