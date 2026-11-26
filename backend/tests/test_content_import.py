import json

import pytest

from backend.app import import_content as cli
from backend.app.models import Challenge, Mission
from backend.app.schemas import ContentFile
from backend.app.services.content_import import ContentError, import_content
from backend.tests.conftest import EXAMPLE_CONTENT


def example_dict():
    return json.loads(EXAMPLE_CONTENT.read_text(encoding="utf-8"))


def test_import_is_idempotent_and_updates(session_factory):
    content = example_dict()
    with session_factory() as db:
        assert import_content(db, ContentFile.model_validate(content)) == (1, 2)
        content["missions"][0]["title"] = "Updated"
        import_content(db, ContentFile.model_validate(content))
        assert db.query(Mission).count() == 1
        assert db.query(Challenge).count() == 2
        assert db.get(Mission, "example-mission-1").title == "Updated"


def test_import_rejects_unknown_correct_option(session_factory):
    content = example_dict()
    content["missions"][0]["challenges"][0]["rubric"]["correctOptionId"] = "X"
    with session_factory() as db, pytest.raises(ContentError):
        import_content(db, ContentFile.model_validate(content))


def test_cli_reports_invalid_file(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text('{"missions": [{"id": "m"}]}', encoding="utf-8")
    assert cli.main([str(bad)]) == 1
    assert "ERROR" in capsys.readouterr().err
