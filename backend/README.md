# Backend – Knowledge Islands

FastAPI + Pydantic + SQLAlchemy + SQLite. Owner: P2 (Backend & Datenbank).

## Struktur

```
backend/
  app/
    main.py        FastAPI-App, CORS, Router-Registrierung
    config.py      Einstellungen (Umgebungsvariablen mit Präfix KI_)
    db.py          Engine, Session, Base, init_db()
    models.py      SQLAlchemy-Tabellen
    schemas.py     Pydantic-Modelle (API-Vertrag, siehe contracts/)
    init_db.py     Schema anlegen
    routers/       Endpunkte
  tests/           pytest
```

## Installation

Voraussetzung: Python ≥ 3.9. Alle Befehle im **Repository-Root** ausführen.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## Starten

```sh
python -m backend.app.init_db            # optional – passiert auch beim Start automatisch
uvicorn backend.app.main:app --reload --port 8000
```

- Health-Check: <http://localhost:8000/api/health> → `{"status": "ok"}`
- Interaktive API-Doku: <http://localhost:8000/docs>

Die SQLite-Datei liegt standardmäßig unter `backend/knowledge_islands.db` (nicht im Git).

### Konfiguration

| Variable          | Standard                                         |
|-------------------|--------------------------------------------------|
| `KI_DATABASE_URL` | `sqlite:///<repo>/backend/knowledge_islands.db`  |
| `KI_CORS_ORIGINS` | `["http://localhost:5173","http://127.0.0.1:5173"]` (JSON-Liste) |

## Tests

```sh
pytest
```

Die Tests nutzen eine In-Memory-SQLite-Datenbank und verändern die lokale DB-Datei nicht.
