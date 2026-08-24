import velesresearch as vls
from velesresearch.models import PageModel


def test_psyframe_returns_page():
    "psyframe() must return a single-question, nav-button-free page"
    result = vls.psyframe("mars_cat", "https://example.com/test/")
    assert isinstance(result, PageModel)
    data = result.dict()
    assert data["name"] == "mars_cat"
    assert data["showNavigationButtons"] is False
    assert len(data["elements"]) == 1


def test_psyframe_kwargs_become_query_params():
    "kwargs not recognised by psyframe() must be appended to the iframe url"
    data = vls.psyframe(
        "t",
        "https://example.com/?a=1",
        goalReliability=0.8,
        skipTraining=True,
    ).dict()
    html = data["elements"][0]["html"]
    assert "a=1" in html
    assert "goalReliability=0.8" in html
    assert "skipTraining=true" in html


def test_psyframe_iframe_not_mangled_by_markdown():
    "the raw iframe tag must survive the QuestionHtmlModel markdown pass untouched"
    data = vls.psyframe("t", "https://example.com/").dict()
    html = data["elements"][0]["html"]
    assert html.startswith('<iframe id="psyframe-t"')
    assert "<p>" not in html


def test_psyframe_custom_code_references_expected_names():
    "the injected listener must be scoped to this page's origin, variable and iframe"
    data = vls.psyframe("mars_cat", "https://example.com/test/").dict()
    code = data["customCode"]
    assert "https://example.com" in code
    assert "mars_cat" in code
    assert "psyframe_result" in code
    assert "psyframe_resize" in code
    assert "survey.setVariable" in code
    assert "survey.nextPage" in code


def test_psyframe_result_hides_frame_before_advancing():
    "a result on a non-final psyframe page hides the frame before advancing"
    code = vls.psyframe("middle", "https://example.com/").dict()["customCode"]
    advance = code.index("survey.nextPage();")
    hide_frame = code.index("frameQuestion.visible = false;")

    assert "survey.setVariable(resultName, message.data);" in code
    assert hide_frame < advance


def test_psyframe_result_completes_final_page_before_hiding_frame():
    "a result on the final psyframe page completes without hiding the frame"
    code = vls.psyframe("final", "https://example.com/").dict()["customCode"]
    complete = code.index("survey.doComplete();")
    hide_frame = code.index("frameQuestion.visible = false;")

    assert "survey.tryComplete" not in code
    assert complete < hide_frame
    assert complete < code.index("return;", complete) < hide_frame
