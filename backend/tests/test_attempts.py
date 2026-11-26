import pytest

from backend.app.models import Attempt
from backend.app.routers import attempts


def post_attempt(client, option, challenge="example-challenge-1", **extra):
    return client.post(
        "/api/attempts",
        json={"challengeId": challenge, "selectedOptionId": option, **extra},
    )


def test_correct_answer(seeded_client):
    response = post_attempt(seeded_client, "B")
    assert response.status_code == 201
    body = response.json()
    assert body["isCorrect"] is True
    assert body["feedbackCode"] == "CORRECT"
    assert body["feedbackMessage"].startswith("Richtig")
    assert body["nextAction"] == "continue"
    assert body["selectedOptionId"] == "B"


def test_wrong_answer(seeded_client):
    response = post_attempt(seeded_client, "A")
    assert response.status_code == 201
    body = response.json()
    assert body["isCorrect"] is False
    assert body["feedbackCode"] == "REVIEW_CONCEPT"
    assert body["nextAction"] == "review"
    # The correct option must not be revealed.
    assert "correctOptionId" not in body


def test_attempt_is_persisted(seeded_client, seeded_session_factory):
    attempt_id = post_attempt(seeded_client, "A", playerId="player-1").json()["id"]

    with seeded_session_factory() as db:
        stored = db.get(Attempt, attempt_id)
        assert stored is not None
        assert (stored.challenge_id, stored.selected_option_id, stored.is_correct) == (
            "example-challenge-1",
            "A",
            False,
        )

    # Reading attempts back (what the frontend does after a page reload).
    listed = seeded_client.get("/api/missions/example-mission-1/attempts").json()
    assert [a["id"] for a in listed] == [attempt_id]
    assert listed[0]["playerId"] == "player-1"
    assert listed[0]["createdAt"].endswith("Z")


def test_attempts_filtered_by_player(seeded_client):
    post_attempt(seeded_client, "A", playerId="alice")
    post_attempt(seeded_client, "B", playerId="bob")
    listed = seeded_client.get(
        "/api/missions/example-mission-1/attempts", params={"playerId": "bob"}
    ).json()
    assert [a["playerId"] for a in listed] == ["bob"]


def test_unknown_challenge_returns_404(seeded_client):
    assert post_attempt(seeded_client, "A", challenge="nope").status_code == 404


def test_unknown_option_returns_422(seeded_client, seeded_session_factory):
    assert post_attempt(seeded_client, "Z").status_code == 422
    with seeded_session_factory() as db:
        assert db.query(Attempt).count() == 0


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"challengeId": "example-challenge-1"},
        {"challengeId": "example-challenge-1", "selectedOptionId": 5},
        {"challengeId": "", "selectedOptionId": "A"},
        {"challengeId": "example-challenge-1", "selectedOptionId": "A", "isCorrect": True},
    ],
)
def test_invalid_body_returns_422(seeded_client, body):
    assert seeded_client.post("/api/attempts", json=body).status_code == 422


def test_scoring_is_delegated_to_learning_engine(seeded_client, monkeypatch):
    calls = []

    def fake_engine(selected_option_id, rubric):
        calls.append((selected_option_id, rubric))
        return {"is_correct": True, "feedback_code": "CORRECT", "next_action": "continue"}
    monkeypatch.setattr(attempts, "evaluate_answer", fake_engine)
    post_attempt(seeded_client, "A")
    assert calls == [
        (
            "A",
            {
                "valid_option_ids": ["A", "B", "C"],
                "correct_option_id": "B",
                "correct_feedback_code": "CORRECT",
                "incorrect_feedback_code": "REVIEW_CONCEPT",
            },
        )
    ]
