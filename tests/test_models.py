import warnings
import velesresearch as vls


def test_page_addcode_is_injected():
    "PageModel.dict() must merge addCode, like QuestionModel.dict() already does"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        data = vls.page("p1", vls.info("i", "hello"), addCode={"foo": "bar"}).dict()
    assert data["foo"] == "bar"


def test_page_addcode_warns_deprecated():
    "Explicit addCode= must still work but emit a DeprecationWarning"
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        vls.page("p1", vls.info("i", "hello"), addCode={"foo": "bar"})
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)


def test_page_kwargs_are_injected_as_addcode():
    "Unrecognized keyword arguments must be injected as addCode with a runtime note, no addCode= needed"
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        data = vls.page("p1", vls.info("i", "hello"), foo="bar").dict()
    assert data["foo"] == "bar"
    assert not any(issubclass(w.category, DeprecationWarning) for w in caught)
    assert any("foo" in str(w.message) for w in caught)


def test_page_addcode_can_override_fields():
    "addCode on a page must be able to override computed fields, same as for questions"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        data = vls.page("p1", vls.info("i", "hello"), addCode={"elements": []}).dict()
    assert data["elements"] == []


def test_survey_addcode_is_injected():
    "SurveyModel.dict() must merge addCode, like QuestionModel.dict() already does"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        data = vls.survey(
            vls.page("p1", vls.info("i", "hello")), addCode={"foo": "bar"}, build=False
        ).dict()
    assert data["foo"] == "bar"


def test_panel_addcode_is_injected():
    "PanelModel now supports addCode, same as questions, pages and surveys"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        data = vls.panel("pan1", vls.info("i", "hello"), addCode={"foo": "bar"}).dict()
    assert data["foo"] == "bar"


def test_question_kwargs_are_injected_as_addcode():
    "Unrecognized keyword arguments on questions must be merged into addCode too"
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        data = vls.info("i", "hello", foo="bar").dict()
    assert data["foo"] == "bar"
    assert not any(issubclass(w.category, DeprecationWarning) for w in caught)


def test_isRequired_defaults_to_false_without_env_var(monkeypatch):
    "Without `veles.isRequired` set, isRequired must default to False"
    monkeypatch.delenv("veles.isRequired", raising=False)
    assert vls.text("q1", "Question?").isRequired is False


def test_isRequired_reads_env_var(monkeypatch):
    "With `veles.isRequired` set to a truthy value, isRequired must default to True"
    monkeypatch.setenv("veles.isRequired", "true")
    assert vls.text("q1", "Question?").isRequired is True


def test_isRequired_explicit_value_takes_precedence(monkeypatch):
    "An explicit isRequired must override the `veles.isRequired` env variable"
    monkeypatch.setenv("veles.isRequired", "true")
    assert vls.text("q1", "Question?", isRequired=False).isRequired is False
