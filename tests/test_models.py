import warnings
import velesresearch as vls


def test_survey_list_dict_fields_validate():
    "SurveyModel's own dict() method must not shadow the builtin dict type for List[dict]-like fields"
    s = vls.survey(
        vls.page("p1", vls.text("q1", "Q?")),
        build=False,
        triggers=[{"type": "complete", "expression": "{q1} notempty"}],
        completedHtmlOnCondition=[{"expression": "{q1} notempty", "html": "done"}],
        navigateToUrlOnCondition=[
            {"expression": "{q1} notempty", "url": "https://example.com"}
        ],
        calculatedValues=[{"name": "foo", "expression": "{q1}"}],
    )
    data = s.dict()
    assert data["triggers"][0]["type"] == "complete"
    assert data["completedHtmlOnCondition"][0]["html"] == "done"
    assert data["navigateToUrlOnCondition"][0]["url"] == "https://example.com"
    assert data["calculatedValues"][0]["name"] == "foo"


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


def test_isRequired_env_var_does_not_apply_to_info_page_or_panel(monkeypatch):
    "The `veles.isRequired` env variable must only affect real questions, not info boxes, pages or panels"
    monkeypatch.setenv("veles.isRequired", "true")
    assert vls.info("i1", "hello").isRequired is False
    assert vls.page("p1", vls.info("i2", "hello")).isRequired is False
    assert vls.panel("pan1", vls.info("i3", "hello")).isRequired is False


def test_surveyjs_v3_question_page_panel_properties_are_serialized():
    "New SurveyJS 3 properties are emitted under their current JSON names"
    question = vls.dropdown(
        "q1",
        "Question?",
        ["A", "B"],
        clearIfInvisible="onHidden",
        colSpan=2,
        indent=1,
        valueName="answer",
        allowCustomChoices=True,
        choicesLazyLoadEnabled=True,
    )
    page = vls.page(
        "p1",
        question,
        questionStartIndex="A.",
    )
    page_data = page.dict()
    question_data = page_data["elements"][0]

    assert question_data["clearIfInvisible"] == "onHidden"
    assert question_data["colSpan"] == 2
    assert question_data["indent"] == 1
    assert question_data["valueName"] == "answer"
    assert question_data["allowCustomChoices"] is True
    assert question_data["choicesLazyLoadEnabled"] is True
    assert page_data["questionStartIndex"] == "A."

    panel_data = vls.panel(
        "panel1",
        vls.text("q2", "Question?"),
        gridLayoutColumns=[{"width": "1fr"}],
    ).dict()
    assert panel_data["gridLayoutColumns"] == [{"width": "1fr"}]


def test_surveyjs_v3_survey_progress_bar_properties_are_serialized():
    data = vls.survey(
        vls.page("p1", vls.text("q1", "Question?")),
        build=False,
        progressBarShowNavigationText=True,
        progressBarNavigationTextLocation="bottom",
    ).dict()

    assert data["progressBarShowNavigationText"] is True
    assert data["progressBarNavigationTextLocation"] == "bottom"
    assert "progressBarShowPageTitles" not in data
