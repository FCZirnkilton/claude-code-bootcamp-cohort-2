"""Business rules for notes: validation and partial updates. No HTTP, no SQL."""

from __future__ import annotations

from typing import Any

from .repository import NoteRepository

MAX_TITLE = 120
MAX_BODY = 10_000


class ValidationError(ValueError):
    """Input violates a business rule (HTTP 400)."""


class NotFound(LookupError):
    """The note does not exist (HTTP 404)."""


def _title(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError("title is required")
    value = value.strip()
    if len(value) > MAX_TITLE:
        raise ValidationError(f"title must be at most {MAX_TITLE} characters")
    return value


def _body(value: Any) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValidationError("body must be a string")
    if len(value) > MAX_BODY:
        raise ValidationError(f"body must be at most {MAX_BODY} characters")
    return value


class NoteService:
    def __init__(self, repo: NoteRepository) -> None:
        self.repo = repo

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self.repo.create(_title(data.get("title")), _body(data.get("body")))

    def get(self, note_id: int) -> dict[str, Any]:
        note = self.repo.get(note_id)
        if note is None:
            raise NotFound(f"note {note_id} not found")
        return note

    def list(self) -> list[dict[str, Any]]:
        return self.repo.list()

    def update(self, note_id: int, data: dict[str, Any]) -> dict[str, Any]:
        current = self.get(note_id)
        if not {"title", "body"} & data.keys():
            raise ValidationError("provide title and/or body")
        title = _title(data["title"]) if "title" in data else current["title"]
        body = _body(data.get("body"))
        note = self.repo.update(note_id, title, body)
        if note is None:
            raise NotFound(f"note {note_id} not found")
        return note

    def delete(self, note_id: int) -> None:
        if not self.repo.delete(note_id):
            raise NotFound(f"note {note_id} not found")
