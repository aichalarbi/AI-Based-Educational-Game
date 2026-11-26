# Knowledge Islands – REST API (Backend ↔ Frontend)

Stand: M1 · Owner: P2 · Basis-URL lokal: `http://localhost:8000/api`

- JSON, Feldnamen in **camelCase**.
- Fehler haben immer die Form `{"detail": ...}` (FastAPI-Standard).
- Interaktive, automatisch generierte Doku: `http://localhost:8000/docs`.
- Studenten sehen **nie** Lösungsschlüssel/Rubric. Bewertet wird ausschließlich serverseitig
  über `learning_engine.evaluate_answer()` (P3).

## `GET /api/health`

`200` → `{"status": "ok"}`

## `GET /api/missions/{missionId}`

Mission mit ihren Challenges in Reihenfolge – ohne Lösung.

```json
{
  "id": "example-mission-1",
  "title": "[BEISPIEL] Lernen vs. Engagement",
  "description": "…",
  "challenges": [
    {
      "id": "example-challenge-1",
      "conceptId": "example-concept-learning-evidence",
      "title": "[BEISPIEL] Lernnachweis",
      "prompt": "Welche Beobachtung zeigt …?",
      "options": [
        {"id": "A", "text": "…"},
        {"id": "B", "text": "…"}
      ]
    }
  ]
}
```

| Status | Bedeutung |
|--------|-----------|
| 200 | OK |
| 404 | Mission unbekannt |

## `POST /api/attempts`

Antwort einreichen. Wird bewertet und gespeichert.

Request:

```json
{"challengeId": "example-challenge-1", "selectedOptionId": "A", "playerId": "player-1"}
```

| Feld | Typ | Pflicht |
|------|-----|---------|
| `challengeId` | string, nicht leer | ja |
| `selectedOptionId` | string, nicht leer | ja |
| `playerId` | string (1–100 Zeichen) | nein – bis es Login gibt, vom Frontend frei gewählt (z. B. in `localStorage`) |

Weitere Felder sind nicht erlaubt (→ 422).

Response `201`:

```json
{
  "id": 1,
  "challengeId": "example-challenge-1",
  "playerId": "player-1",
  "selectedOptionId": "A",
  "isCorrect": false,
  "feedbackCode": "REVIEW_CONCEPT",
  "feedbackMessage": "Noch nicht. Abzeichen und Spielhäufigkeit messen Engagement, nicht Lernen.",
  "nextAction": "review",
  "createdAt": "2026-11-26T10:15:00.123456Z"
}
```

- `nextAction`: `"continue"` (richtig) oder `"review"` (falsch).
- `feedbackMessage` kommt aus den Inhalten (P4); `""`, falls für den Code kein Text hinterlegt ist.
- Die richtige Option wird bei falscher Antwort **nicht** verraten.
- `createdAt`: ISO 8601, UTC.

| Status | Bedeutung |
|--------|-----------|
| 201 | Versuch bewertet und gespeichert |
| 404 | Challenge unbekannt |
| 422 | Body ungültig (fehlende/falsche Felder) **oder** Option gehört nicht zur Challenge |
| 500 | Inhalt der Challenge fehlerhaft (Rubric kaputt) |

## `GET /api/missions/{missionId}/attempts?playerId=…`

Alle gespeicherten Versuche zu den Challenges dieser Mission, älteste zuerst (für den Zustand
nach Neuladen). `playerId` ist optional und filtert. Elemente haben dasselbe Format wie die
Response von `POST /api/attempts`. `404`, wenn die Mission unbekannt ist.

---

## Inhaltsformat für den Import (P4 → Backend)

Wird **nicht** über die API ausgeliefert, sondern per Kommando in die DB importiert:

```sh
python -m backend.app.import_content pfad/zur/datei.json
```

Import ist idempotent (Upsert über `id`). Beispiel: `backend/sample_content/EXAMPLE_missions.json`.

```json
{
  "missions": [
    {
      "id": "mission-id",
      "title": "…",
      "description": "…",
      "challenges": [
        {
          "id": "challenge-id",
          "conceptId": "concept-id",
          "title": "…",
          "prompt": "…",
          "options": [{"id": "A", "text": "…"}, {"id": "B", "text": "…"}],
          "rubric": {
            "correctOptionId": "B",
            "correctFeedbackCode": "CORRECT",
            "incorrectFeedbackCode": "REVIEW_CONCEPT"
          },
          "feedbackMessages": {"CORRECT": "…", "REVIEW_CONCEPT": "…"}
        }
      ]
    }
  ]
}
```

- Mindestens 2 Optionen, Options-IDs eindeutig, `correctOptionId` muss eine der Optionen sein.
- Die Reihenfolge in `challenges` bestimmt die Reihenfolge in der Mission.
- Das Backend speichert daraus die Rubric im Format von P3:
  `{valid_option_ids, correct_option_id, correct_feedback_code, incorrect_feedback_code}`.
