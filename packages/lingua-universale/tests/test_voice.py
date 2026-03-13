# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _voice.py (E.4) -- VoiceProcessor: mic capture + STT.

Strategy:
  - faster-whisper and sounddevice are OPTIONAL deps -- not installed.
  - CRITICAL: We do NOT inject mocks into sys.modules globally because
    a mock numpy would break pytest.approx() used by other test files.
  - _voice.py imports nothing optional at module level, so direct imports work.
  - Tests that exercise runtime paths use ``patch`` locally.

Covers:
    1. Import and Structure (module-level constants)
    2. _require_voice_deps (ImportError paths + success)
    3. VoiceProcessor.__init__ (params, defaults, validation)
    4. VoiceProcessor._ensure_model (lazy load, caching, messages)
    5. VoiceProcessor.__call__ (prompt write, record, transcribe, echo)
    6. _record_audio (streams, chunks, push-to-talk flow)
    7. _transcribe (empty audio, segments joining, language mapping)
    8. CLI integration (--voice flags, parser, error paths)
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

# _voice.py has NO optional imports at module level, so this is safe.
from cervellaswarm_lingua_universale._voice import (
    VoiceProcessor,
    VoiceProcessorError,
    _LANG_TO_WHISPER,
    _MODEL_SIZES,
    _VOICE_STRINGS,
    _record_audio,
    _require_voice_deps,
    _transcribe,
)


# ============================================================
# 1. Import and Structure
# ============================================================


class TestImportAndStructure:
    """Module-level constants and types."""

    def test_voice_processor_error_is_exception(self) -> None:
        assert issubclass(VoiceProcessorError, Exception)

    def test_voice_strings_has_all_keys(self) -> None:
        expected_keys = {
            "press_enter_start",
            "recording",
            "transcribing",
            "heard",
            "empty_recording",
            "loading_model",
            "model_ready",
            "mic_error",
        }
        assert set(_VOICE_STRINGS.keys()) == expected_keys

    def test_voice_strings_all_locales(self) -> None:
        for key, locales in _VOICE_STRINGS.items():
            assert "en" in locales, f"Missing 'en' for {key}"
            assert "it" in locales, f"Missing 'it' for {key}"
            assert "pt" in locales, f"Missing 'pt' for {key}"

    def test_model_sizes_has_small(self) -> None:
        assert "small" in _MODEL_SIZES

    def test_model_sizes_has_turbo(self) -> None:
        assert "turbo" in _MODEL_SIZES

    def test_model_sizes_has_all_expected(self) -> None:
        expected = {"tiny", "base", "small", "medium", "large-v3", "turbo"}
        assert set(_MODEL_SIZES.keys()) == expected

    def test_lang_to_whisper_mapping(self) -> None:
        assert _LANG_TO_WHISPER == {"en": "en", "it": "it", "pt": "pt"}

    def test_voice_processor_has_defaults(self) -> None:
        assert VoiceProcessor.DEFAULT_MODEL == "small"
        assert VoiceProcessor.DEFAULT_SAMPLERATE == 16000
        assert VoiceProcessor.DEFAULT_COMPUTE_TYPE == "int8"


# ============================================================
# 2. _require_voice_deps
# ============================================================


class TestRequireVoiceDeps:
    """Dependency-check function."""

    def test_raises_when_sounddevice_missing(self) -> None:
        with patch.dict(sys.modules, {"sounddevice": None, "faster_whisper": MagicMock()}):
            with pytest.raises(ImportError, match="sounddevice"):
                _require_voice_deps()

    def test_raises_when_faster_whisper_missing(self) -> None:
        with patch.dict(sys.modules, {"sounddevice": MagicMock(), "faster_whisper": None}):
            with pytest.raises(ImportError, match="faster-whisper"):
                _require_voice_deps()

    def test_raises_when_both_missing(self) -> None:
        with patch.dict(sys.modules, {"sounddevice": None, "faster_whisper": None}):
            with pytest.raises(ImportError, match="sounddevice.*faster-whisper"):
                _require_voice_deps()

    def test_error_includes_install_hint(self) -> None:
        with patch.dict(sys.modules, {"sounddevice": None}):
            with pytest.raises(ImportError, match=r"pip install.*\[voice\]"):
                _require_voice_deps()

    def test_no_error_when_both_present(self) -> None:
        mock_sd = MagicMock()
        mock_fw = MagicMock()
        mock_fw.WhisperModel = MagicMock()
        with patch.dict(sys.modules, {"sounddevice": mock_sd, "faster_whisper": mock_fw}):
            _require_voice_deps()  # Should not raise


# ============================================================
# 3. VoiceProcessor.__init__
# ============================================================


class TestVoiceProcessorInit:
    """Constructor parameter handling."""

    def _make(self, **kwargs: object) -> VoiceProcessor:
        """Create VoiceProcessor with deps mocked."""
        mock_sd = MagicMock()
        mock_fw = MagicMock()
        mock_fw.WhisperModel = MagicMock()
        with patch.dict(sys.modules, {"sounddevice": mock_sd, "faster_whisper": mock_fw}):
            return VoiceProcessor(**kwargs)  # type: ignore[arg-type]

    def test_default_lang(self) -> None:
        vp = self._make()
        assert vp._lang == "en"

    def test_custom_lang_it(self) -> None:
        vp = self._make(lang="it")
        assert vp._lang == "it"

    def test_custom_lang_pt(self) -> None:
        vp = self._make(lang="pt")
        assert vp._lang == "pt"

    def test_invalid_lang_falls_back(self) -> None:
        vp = self._make(lang="xx")
        assert vp._lang == "en"

    def test_default_model_size(self) -> None:
        vp = self._make()
        assert vp._model_size == "small"

    def test_custom_model_size(self) -> None:
        vp = self._make(model_size="turbo")
        assert vp._model_size == "turbo"

    def test_default_compute_type(self) -> None:
        vp = self._make()
        assert vp._compute_type == "int8"

    def test_custom_compute_type(self) -> None:
        vp = self._make(compute_type="float16")
        assert vp._compute_type == "float16"

    def test_default_samplerate(self) -> None:
        vp = self._make()
        assert vp._samplerate == 16000

    def test_custom_samplerate(self) -> None:
        vp = self._make(samplerate=44100)
        assert vp._samplerate == 44100

    def test_model_is_none_after_init(self) -> None:
        vp = self._make()
        assert vp._model is None

    def test_output_fn_default(self) -> None:
        vp = self._make()
        assert vp._output_fn is print

    def test_custom_output_fn(self) -> None:
        fn = MagicMock()
        vp = self._make(output_fn=fn)
        assert vp._output_fn is fn

    def test_raises_if_deps_missing(self) -> None:
        with patch.dict(sys.modules, {"sounddevice": None, "faster_whisper": None}):
            with pytest.raises(ImportError):
                VoiceProcessor()


# ============================================================
# 4. VoiceProcessor._ensure_model
# ============================================================


class TestEnsureModel:
    """Lazy model loading."""

    def _make(self, **kwargs: object) -> tuple[VoiceProcessor, MagicMock]:
        """Create VoiceProcessor with mocked deps, return (vp, mock_fw)."""
        mock_sd = MagicMock()
        mock_fw = MagicMock()
        mock_model_instance = MagicMock(name="whisper_model")
        mock_fw.WhisperModel.return_value = mock_model_instance
        with patch.dict(sys.modules, {"sounddevice": mock_sd, "faster_whisper": mock_fw}):
            vp = VoiceProcessor(**kwargs)  # type: ignore[arg-type]
        return vp, mock_fw

    def test_lazy_loads_on_first_call(self) -> None:
        vp, mock_fw = self._make()
        assert vp._model is None
        with patch.dict(sys.modules, {"faster_whisper": mock_fw}):
            vp._ensure_model()
        assert vp._model is not None

    def test_returns_cached_model(self) -> None:
        vp, mock_fw = self._make()
        with patch.dict(sys.modules, {"faster_whisper": mock_fw}):
            m1 = vp._ensure_model()
            m2 = vp._ensure_model()
        assert m1 is m2
        assert mock_fw.WhisperModel.call_count == 1

    def test_shows_loading_message(self) -> None:
        output = []
        vp, mock_fw = self._make(output_fn=output.append)
        with patch.dict(sys.modules, {"faster_whisper": mock_fw}):
            vp._ensure_model()
        loading_msgs = [m for m in output if "small" in str(m) or "466" in str(m)]
        assert len(loading_msgs) >= 1

    def test_shows_ready_message(self) -> None:
        output = []
        vp, mock_fw = self._make(output_fn=output.append)
        with patch.dict(sys.modules, {"faster_whisper": mock_fw}):
            vp._ensure_model()
        # Check last message contains ready indicator
        ready_words = {"ready", "pronto"}
        assert any(
            any(w in msg.lower() for w in ready_words)
            for msg in output
        )

    def test_passes_device_cpu(self) -> None:
        vp, mock_fw = self._make()
        with patch.dict(sys.modules, {"faster_whisper": mock_fw}):
            vp._ensure_model()
        mock_fw.WhisperModel.assert_called_once()
        _, kwargs = mock_fw.WhisperModel.call_args
        assert kwargs.get("device") == "cpu"

    def test_passes_compute_type(self) -> None:
        vp, mock_fw = self._make(compute_type="float16")
        with patch.dict(sys.modules, {"faster_whisper": mock_fw}):
            vp._ensure_model()
        _, kwargs = mock_fw.WhisperModel.call_args
        assert kwargs.get("compute_type") == "float16"


# ============================================================
# 5. VoiceProcessor.__call__
# ============================================================


class TestVoiceProcessorCall:
    """The main __call__ method."""

    def _make_vp(
        self, *, lang: str = "en", output_fn: object | None = None
    ) -> tuple[VoiceProcessor, MagicMock, MagicMock]:
        """Build a VoiceProcessor with mocked internals.

        Returns (vp, mock_fw, mock_sd).
        """
        mock_sd = MagicMock()
        mock_fw = MagicMock()
        mock_model = MagicMock(name="model")
        mock_fw.WhisperModel.return_value = mock_model
        with patch.dict(sys.modules, {"sounddevice": mock_sd, "faster_whisper": mock_fw}):
            vp = VoiceProcessor(
                lang=lang,
                output_fn=output_fn or MagicMock(),
                raw_input_fn=MagicMock(return_value=""),
            )
        return vp, mock_fw, mock_sd

    def test_writes_prompt_to_stdout(self) -> None:
        vp, mock_fw, _ = self._make_vp()
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="hello",
            ),
            patch("sys.stdout") as mock_stdout,
        ):
            vp("> ")
            mock_stdout.write.assert_called_with("> ")

    def test_returns_transcribed_text(self) -> None:
        vp, mock_fw, _ = self._make_vp()
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="hello world",
            ),
        ):
            result = vp("> ")
        assert result == "hello world"

    def test_echoes_heard_text(self) -> None:
        output: list[str] = []
        vp, mock_fw, _ = self._make_vp(output_fn=output.append)
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="ciao mondo",
            ),
        ):
            vp("> ")
        heard_msgs = [m for m in output if "ciao mondo" in str(m)]
        assert len(heard_msgs) >= 1

    def test_empty_transcription_returns_empty(self) -> None:
        vp, mock_fw, _ = self._make_vp()
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="",
            ),
        ):
            result = vp("> ")
        assert result == ""

    def test_empty_transcription_shows_message(self) -> None:
        output: list[str] = []
        vp, mock_fw, _ = self._make_vp(output_fn=output.append)
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="",
            ),
        ):
            vp("> ")
        no_speech = [m for m in output if "speech" in str(m).lower() or "detected" in str(m).lower()]
        assert len(no_speech) >= 1

    def test_mic_error_raises_voice_error(self) -> None:
        vp, mock_fw, _ = self._make_vp()
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                side_effect=OSError("No mic"),
            ),
        ):
            with pytest.raises(VoiceProcessorError, match="No mic"):
                vp("> ")

    def test_italian_locale_heard(self) -> None:
        output: list[str] = []
        vp, mock_fw, _ = self._make_vp(lang="it", output_fn=output.append)
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="ciao",
            ),
        ):
            vp("> ")
        heard_msgs = [m for m in output if "Sentito" in str(m)]
        assert len(heard_msgs) >= 1

    def test_portuguese_locale_heard(self) -> None:
        output: list[str] = []
        vp, mock_fw, _ = self._make_vp(lang="pt", output_fn=output.append)
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="ola",
            ),
        ):
            vp("> ")
        heard_msgs = [m for m in output if "Ouvido" in str(m)]
        assert len(heard_msgs) >= 1

    def test_english_locale_heard(self) -> None:
        output: list[str] = []
        vp, mock_fw, _ = self._make_vp(lang="en", output_fn=output.append)
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="hi",
            ),
        ):
            vp("> ")
        heard_msgs = [m for m in output if "Heard" in str(m)]
        assert len(heard_msgs) >= 1

    def test_calls_ensure_model(self) -> None:
        vp, mock_fw, _ = self._make_vp()
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="test",
            ),
            patch.object(vp, "_ensure_model", wraps=vp._ensure_model) as spy,
        ):
            vp("> ")
        spy.assert_called_once()

    def test_no_prompt_still_works(self) -> None:
        vp, mock_fw, _ = self._make_vp()
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="hello",
            ),
        ):
            result = vp("")
        assert result == "hello"

    def test_transcribing_message_shown(self) -> None:
        output: list[str] = []
        vp, mock_fw, _ = self._make_vp(output_fn=output.append)
        with (
            patch.dict(sys.modules, {"faster_whisper": mock_fw}),
            patch(
                "cervellaswarm_lingua_universale._voice._record_audio",
                return_value=MagicMock(__len__=lambda s: 100),
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._transcribe",
                return_value="test",
            ),
        ):
            vp("> ")
        transcribing = [m for m in output if "ranscri" in str(m).lower()]
        assert len(transcribing) >= 1


# ============================================================
# 6. _record_audio
# ============================================================


class TestRecordAudio:
    """Push-to-talk recording via sounddevice."""

    def test_shows_press_enter_prompt(self) -> None:
        output: list[str] = []
        calls: list[str] = []

        def fake_input(prompt: str) -> str:
            calls.append(prompt)
            return ""

        mock_sd = MagicMock()
        mock_np = MagicMock()
        mock_np.array.return_value = MagicMock(name="empty_arr")
        mock_np.concatenate.return_value = MagicMock(
            flatten=MagicMock(return_value=MagicMock(name="flat"))
        )

        # Mock InputStream as context manager
        mock_stream = MagicMock()
        mock_sd.InputStream.return_value = mock_stream

        with (
            patch.dict(sys.modules, {"sounddevice": mock_sd, "numpy": mock_np}),
            patch("cervellaswarm_lingua_universale._voice.threading") as mock_threading,
        ):
            # Make the stopper thread set stop_event immediately
            def fake_thread(**kwargs: object) -> MagicMock:
                target = kwargs.get("target")
                if callable(target):
                    target()  # immediately call the stop function
                t = MagicMock()
                return t

            mock_threading.Event.return_value = MagicMock(
                wait=MagicMock(),
                set=MagicMock(),
                is_set=MagicMock(return_value=True),
            )
            mock_threading.Thread.side_effect = fake_thread

            _record_audio(
                samplerate=16000,
                output_fn=output.append,
                lang="en",
                input_fn=fake_input,
            )

        press_enter = [m for m in output if "ENTER" in str(m) or "start" in str(m).lower()]
        assert len(press_enter) >= 1

    def test_shows_recording_message(self) -> None:
        output: list[str] = []

        mock_sd = MagicMock()
        mock_np = MagicMock()
        mock_np.concatenate.return_value = MagicMock(
            flatten=MagicMock(return_value=MagicMock())
        )

        mock_stream = MagicMock()
        mock_sd.InputStream.return_value = mock_stream

        with (
            patch.dict(sys.modules, {"sounddevice": mock_sd, "numpy": mock_np}),
            patch("cervellaswarm_lingua_universale._voice.threading") as mock_threading,
        ):
            mock_threading.Event.return_value = MagicMock(
                wait=MagicMock(),
                set=MagicMock(),
                is_set=MagicMock(return_value=True),
            )
            mock_threading.Thread.side_effect = lambda **kw: (
                kw.get("target", lambda: None)(),
                MagicMock(),
            )[1]

            _record_audio(
                samplerate=16000,
                output_fn=output.append,
                lang="en",
                input_fn=MagicMock(return_value=""),
            )

        recording_msgs = [m for m in output if "ecording" in str(m)]
        assert len(recording_msgs) >= 1

    def test_italian_recording_messages(self) -> None:
        output: list[str] = []

        mock_sd = MagicMock()
        mock_np = MagicMock()
        mock_np.concatenate.return_value = MagicMock(
            flatten=MagicMock(return_value=MagicMock())
        )
        mock_sd.InputStream.return_value = MagicMock()

        with (
            patch.dict(sys.modules, {"sounddevice": mock_sd, "numpy": mock_np}),
            patch("cervellaswarm_lingua_universale._voice.threading") as mock_threading,
        ):
            mock_threading.Event.return_value = MagicMock(
                wait=MagicMock(), set=MagicMock(),
                is_set=MagicMock(return_value=True),
            )
            mock_threading.Thread.side_effect = lambda **kw: (
                kw.get("target", lambda: None)(), MagicMock()
            )[1]

            _record_audio(
                samplerate=16000,
                output_fn=output.append,
                lang="it",
                input_fn=MagicMock(return_value=""),
            )

        invio_msgs = [m for m in output if "INVIO" in str(m)]
        assert len(invio_msgs) >= 1

    def test_creates_input_stream_with_correct_params(self) -> None:
        mock_sd = MagicMock()
        mock_np = MagicMock()
        mock_np.concatenate.return_value = MagicMock(
            flatten=MagicMock(return_value=MagicMock())
        )
        mock_sd.InputStream.return_value = MagicMock()

        with (
            patch.dict(sys.modules, {"sounddevice": mock_sd, "numpy": mock_np}),
            patch("cervellaswarm_lingua_universale._voice.threading") as mock_threading,
        ):
            mock_threading.Event.return_value = MagicMock(
                wait=MagicMock(), set=MagicMock(),
                is_set=MagicMock(return_value=True),
            )
            mock_threading.Thread.side_effect = lambda **kw: (
                kw.get("target", lambda: None)(), MagicMock()
            )[1]

            _record_audio(
                samplerate=44100,
                output_fn=MagicMock(),
                lang="en",
                input_fn=MagicMock(return_value=""),
            )

        mock_sd.InputStream.assert_called_once()
        _, kwargs = mock_sd.InputStream.call_args
        assert kwargs["samplerate"] == 44100
        assert kwargs["channels"] == 1
        assert kwargs["dtype"] == "float32"

    def test_empty_chunks_returns_empty_array(self) -> None:
        mock_sd = MagicMock()
        mock_np = MagicMock()
        empty_arr = MagicMock(name="empty_arr")
        mock_np.array.return_value = empty_arr
        mock_sd.InputStream.return_value = MagicMock()

        with (
            patch.dict(sys.modules, {"sounddevice": mock_sd, "numpy": mock_np}),
            patch("cervellaswarm_lingua_universale._voice.threading") as mock_threading,
        ):
            mock_threading.Event.return_value = MagicMock(
                wait=MagicMock(), set=MagicMock(),
                is_set=MagicMock(return_value=True),
            )
            mock_threading.Thread.side_effect = lambda **kw: (
                kw.get("target", lambda: None)(), MagicMock()
            )[1]

            result = _record_audio(
                samplerate=16000,
                output_fn=MagicMock(),
                lang="en",
                input_fn=MagicMock(return_value=""),
            )

        # Should call np.array([], dtype="float32") for empty chunks
        mock_np.array.assert_called()

    def test_keyboard_interrupt_handled(self) -> None:
        mock_sd = MagicMock()
        mock_np = MagicMock()
        mock_np.array.return_value = MagicMock()
        mock_sd.InputStream.return_value = MagicMock()

        # First input_fn call succeeds (start recording), second raises
        mock_input = MagicMock(side_effect=["", KeyboardInterrupt])

        with (
            patch.dict(sys.modules, {"sounddevice": mock_sd, "numpy": mock_np}),
            patch("cervellaswarm_lingua_universale._voice.threading") as mock_threading,
        ):
            # Simulate KeyboardInterrupt in the stop thread
            def call_target_immediately(**kw: object) -> MagicMock:
                target = kw.get("target")
                if callable(target):
                    target()  # calls input_fn which raises KeyboardInterrupt
                return MagicMock()

            mock_threading.Event.return_value = MagicMock(
                wait=MagicMock(), set=MagicMock(),
                is_set=MagicMock(return_value=True),
            )
            mock_threading.Thread.side_effect = call_target_immediately

            # Should not propagate KeyboardInterrupt
            _record_audio(
                samplerate=16000,
                output_fn=MagicMock(),
                lang="en",
                input_fn=mock_input,
            )


# ============================================================
# 7. _transcribe
# ============================================================


class TestTranscribe:
    """Whisper transcription helper."""

    def test_empty_audio_returns_empty(self) -> None:
        mock_np = MagicMock()
        empty = MagicMock()
        empty.__len__ = MagicMock(return_value=0)
        with patch.dict(sys.modules, {"numpy": mock_np}):
            result = _transcribe(MagicMock(), empty, "en")
        assert result == ""

    def test_calls_transcribe_with_language(self) -> None:
        mock_np = MagicMock()
        model = MagicMock()
        seg = MagicMock()
        seg.text = "hello"
        model.transcribe.return_value = ([seg], MagicMock())
        audio = MagicMock()
        audio.__len__ = MagicMock(return_value=16000)

        with patch.dict(sys.modules, {"numpy": mock_np}):
            _transcribe(model, audio, "it")

        model.transcribe.assert_called_once()
        _, kwargs = model.transcribe.call_args
        assert kwargs["language"] == "it"

    def test_uses_vad_filter(self) -> None:
        mock_np = MagicMock()
        model = MagicMock()
        model.transcribe.return_value = ([], MagicMock())
        audio = MagicMock()
        audio.__len__ = MagicMock(return_value=100)

        with patch.dict(sys.modules, {"numpy": mock_np}):
            _transcribe(model, audio, "en")

        _, kwargs = model.transcribe.call_args
        assert kwargs["vad_filter"] is True

    def test_joins_segments_with_space(self) -> None:
        mock_np = MagicMock()
        model = MagicMock()
        seg1 = MagicMock()
        seg1.text = "hello"
        seg2 = MagicMock()
        seg2.text = "world"
        model.transcribe.return_value = ([seg1, seg2], MagicMock())
        audio = MagicMock()
        audio.__len__ = MagicMock(return_value=16000)

        with patch.dict(sys.modules, {"numpy": mock_np}):
            result = _transcribe(model, audio, "en")

        assert result == "hello world"

    def test_strips_result(self) -> None:
        mock_np = MagicMock()
        model = MagicMock()
        seg = MagicMock()
        seg.text = "  hello  "
        model.transcribe.return_value = ([seg], MagicMock())
        audio = MagicMock()
        audio.__len__ = MagicMock(return_value=100)

        with patch.dict(sys.modules, {"numpy": mock_np}):
            result = _transcribe(model, audio, "en")

        assert result == "hello"

    def test_portuguese_language_mapping(self) -> None:
        mock_np = MagicMock()
        model = MagicMock()
        model.transcribe.return_value = ([], MagicMock())
        audio = MagicMock()
        audio.__len__ = MagicMock(return_value=100)

        with patch.dict(sys.modules, {"numpy": mock_np}):
            _transcribe(model, audio, "pt")

        _, kwargs = model.transcribe.call_args
        assert kwargs["language"] == "pt"

    def test_unknown_lang_falls_back_to_en(self) -> None:
        mock_np = MagicMock()
        model = MagicMock()
        model.transcribe.return_value = ([], MagicMock())
        audio = MagicMock()
        audio.__len__ = MagicMock(return_value=100)

        with patch.dict(sys.modules, {"numpy": mock_np}):
            _transcribe(model, audio, "xx")

        _, kwargs = model.transcribe.call_args
        assert kwargs["language"] == "en"


# ============================================================
# 8. CLI Integration
# ============================================================


class TestCLIIntegration:
    """lu chat --voice flag parsing and wiring."""

    def test_voice_flag_exists(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat", "--voice"])
        assert args.voice is True

    def test_voice_flag_default_false(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat"])
        assert args.voice is False

    def test_voice_model_choices(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat", "--voice-model", "small"])
        assert args.voice_model == "small"

    def test_voice_model_default_none(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat"])
        assert args.voice_model is None

    def test_voice_model_accepts_turbo(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat", "--voice-model", "turbo"])
        assert args.voice_model == "turbo"

    def test_voice_model_accepts_large_v3(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat", "--voice-model", "large-v3"])
        assert args.voice_model == "large-v3"

    def test_voice_with_lang(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat", "--voice", "--lang", "it"])
        assert args.voice is True
        assert args.lang == "it"

    def test_voice_with_mode_nl(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat", "--voice", "--mode", "nl"])
        assert args.voice is True
        assert args.mode == "nl"

    def test_cmd_chat_voice_missing_deps_returns_1(self) -> None:
        from cervellaswarm_lingua_universale._cli import _cmd_chat
        import argparse

        args = argparse.Namespace(
            voice=True,
            voice_model=None,
            mode="guided",
            lang="en",
            output=None,
        )

        # Ensure voice deps are NOT available
        with patch.dict(sys.modules, {"sounddevice": None, "faster_whisper": None}):
            # Need to reload _voice so _require_voice_deps sees the patched modules
            with patch(
                "cervellaswarm_lingua_universale._voice._require_voice_deps",
                side_effect=ImportError("missing deps"),
            ):
                result = _cmd_chat(args)
        assert result == 1

    def test_cmd_chat_no_voice_does_not_import_voice(self) -> None:
        from cervellaswarm_lingua_universale._cli import _cmd_chat
        import argparse

        args = argparse.Namespace(
            voice=False,
            voice_model=None,
            mode="guided",
            lang="en",
            output=None,
        )

        with patch(
            "cervellaswarm_lingua_universale._intent_bridge.ChatSession"
        ) as MockSession:
            mock_session = MagicMock()
            mock_session.run.return_value = None
            MockSession.return_value = mock_session

            result = _cmd_chat(args)

        assert result == 0
        # ChatSession should NOT receive a custom input_fn
        _, kwargs = MockSession.call_args
        assert "input_fn" not in kwargs

    def test_cmd_chat_voice_creates_voice_processor(self) -> None:
        from cervellaswarm_lingua_universale._cli import _cmd_chat
        import argparse

        args = argparse.Namespace(
            voice=True,
            voice_model="tiny",
            mode="guided",
            lang="it",
            output=None,
        )

        mock_vp_instance = MagicMock(name="voice_processor_instance")
        mock_vp_cls = MagicMock(return_value=mock_vp_instance)

        with (
            patch(
                "cervellaswarm_lingua_universale._voice.VoiceProcessor",
                mock_vp_cls,
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._require_voice_deps",
            ),
            patch(
                "cervellaswarm_lingua_universale._intent_bridge.ChatSession",
            ) as MockSession,
        ):
            mock_session = MagicMock()
            mock_session.run.return_value = None
            MockSession.return_value = mock_session

            _cmd_chat(args)

        # VoiceProcessor was constructed with correct args
        mock_vp_cls.assert_called_once_with(lang="it", model_size="tiny")

    def test_cmd_chat_voice_passes_lang_and_model(self) -> None:
        from cervellaswarm_lingua_universale._cli import _cmd_chat
        import argparse

        args = argparse.Namespace(
            voice=True,
            voice_model="turbo",
            mode="guided",
            lang="pt",
            output=None,
        )

        mock_vp_instance = MagicMock(name="voice_processor_instance")
        mock_vp_cls = MagicMock(return_value=mock_vp_instance)

        with (
            patch(
                "cervellaswarm_lingua_universale._voice.VoiceProcessor",
                mock_vp_cls,
            ),
            patch(
                "cervellaswarm_lingua_universale._voice._require_voice_deps",
            ),
            patch(
                "cervellaswarm_lingua_universale._intent_bridge.ChatSession",
            ) as MockSession,
        ):
            mock_session = MagicMock()
            mock_session.run.return_value = None
            MockSession.return_value = mock_session

            _cmd_chat(args)

        mock_vp_cls.assert_called_once_with(lang="pt", model_size="turbo")
