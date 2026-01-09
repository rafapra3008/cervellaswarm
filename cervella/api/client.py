"""
Claude API Client - Wrapper per Anthropic API

BYOK - Bring Your Own Key: l'utente usa la propria API key.
"""

import os
from dataclasses import dataclass
from typing import Optional, Generator
import anthropic


@dataclass
class Message:
    """Messaggio nella conversazione."""
    role: str  # "user" o "assistant"
    content: str


@dataclass
class Response:
    """Risposta dal modello."""
    content: str
    model: str
    usage: dict
    stop_reason: str


class ClaudeClient:
    """Client per Claude API.

    Usa ANTHROPIC_API_KEY dall'environment.
    Supporta streaming per risposte lunghe.
    """

    DEFAULT_MODEL = "claude-sonnet-4-20250514"
    OPUS_MODEL = "claude-opus-4-0-20250514"

    def __init__(self, api_key: Optional[str] = None):
        """Inizializza il client.

        Args:
            api_key: API key Anthropic. Se None, usa ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key non trovata. "
                "Imposta ANTHROPIC_API_KEY o passa api_key al costruttore."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def send(
        self,
        messages: list[Message],
        system: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Response:
        """Invia messaggi e ottiene risposta.

        Args:
            messages: Lista di messaggi della conversazione.
            system: System prompt opzionale.
            model: Modello da usare (default: claude-sonnet).
            max_tokens: Massimo token in risposta.
            temperature: Creatività (0-1).

        Returns:
            Response con contenuto e metadata.
        """
        model = model or self.DEFAULT_MODEL

        # Converti messaggi in formato API
        api_messages = [{"role": m.role, "content": m.content} for m in messages]

        # Chiamata API
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "",
            messages=api_messages,
        )

        return Response(
            content=response.content[0].text,
            model=response.model,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            stop_reason=response.stop_reason,
        )

    def stream(
        self,
        messages: list[Message],
        system: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Generator[str, None, None]:
        """Invia messaggi e ottiene risposta in streaming.

        Args:
            messages: Lista di messaggi della conversazione.
            system: System prompt opzionale.
            model: Modello da usare.
            max_tokens: Massimo token in risposta.
            temperature: Creatività (0-1).

        Yields:
            Chunk di testo man mano che arrivano.
        """
        model = model or self.DEFAULT_MODEL

        # Converti messaggi
        api_messages = [{"role": m.role, "content": m.content} for m in messages]

        # Streaming
        with self.client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "",
            messages=api_messages,
        ) as stream:
            for text in stream.text_stream:
                yield text

    def quick(self, prompt: str, system: Optional[str] = None) -> str:
        """Chiamata rapida single-shot.

        Args:
            prompt: Il prompt da inviare.
            system: System prompt opzionale.

        Returns:
            Contenuto della risposta come stringa.
        """
        messages = [Message(role="user", content=prompt)]
        response = self.send(messages, system=system)
        return response.content
