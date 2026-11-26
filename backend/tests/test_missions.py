MISSION_ID = "example-mission-1"


def test_get_mission_returns_challenges(seeded_client):
    response = seeded_client.get(f"/api/missions/{MISSION_ID}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == MISSION_ID
    assert [c["id"] for c in body["challenges"]] == ["example-challenge-1", "example-challenge-2"]
    challenge = body["challenges"][0]
    assert set(challenge) == {"id", "conceptId", "title", "prompt", "options"}
    assert challenge["options"][1] == {
        "id": "B",
        "text": "Er kann das Konzept auf eine neue Aufgabe anwenden.",
    }


def test_get_mission_does_not_leak_solution(seeded_client):
    raw = seeded_client.get(f"/api/missions/{MISSION_ID}").text
    for secret in (
        "rubric",
        "correctOptionId",
        "correct_option_id",
        "valid_option_ids",
        "feedbackMessages",
        "REVIEW_CONCEPT",
        "Richtig!",  # feedback message text
    ):
        assert secret not in raw


def test_unknown_mission_returns_404(seeded_client):
    response = seeded_client.get("/api/missions/does-not-exist")
    assert response.status_code == 404


def test_unknown_mission_attempts_returns_404(seeded_client):
    assert seeded_client.get("/api/missions/does-not-exist/attempts").status_code == 404
