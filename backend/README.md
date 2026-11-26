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
    import_content.py  Challenge-JSON in die DB importieren
    routers/       Endpunkte (health, missions, attempts)
    services/      Inhaltsimport, Adapter zur learning_engine
  sample_content/  BEISPIEL-Inhalte (Platzhalter, echte Inhalte liefert P4)
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

API-Format: [contracts/api.md](../contracts/api.md).

### Inhalte importieren

```sh
python -m backend.app.import_content backend/sample_content/EXAMPLE_missions.json
```

Danach z. B. <http://localhost:8000/api/missions/example-mission-1>.
Die Datei enthält nur **Platzhalter**; echte, geprüfte Inhalte liefert P4 im selben Format.

### Bewertung (learning_engine)

Das Backend bewertet nicht selbst, sondern ruft `learning_engine.evaluate_answer()` (P3) auf –
siehe `app/services/evaluation.py`. Solange P3s Code noch nicht im Branch ist, wird ein klar
markierter **STUB** (`app/services/_learning_engine_stub.py`) verwendet und beim Start eine
Warnung geloggt. Nach dem Merge von P3 kann der Stub gelöscht werden.

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
