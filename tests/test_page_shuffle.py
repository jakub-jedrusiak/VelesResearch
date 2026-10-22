"Tests for page shuffling blocks"

import json
import shutil
from importlib.resources import files
from pathlib import Path

import pytest
import velesresearch as vls
from velesresearch.helperModels import PageShuffleMarker


def _pages(n):
    return [vls.page(f"p{i}", vls.text(f"q{i}", f"Q{i}?")) for i in range(1, n + 1)]


def test_markers_are_plain_objects():
    "wrappers return start/end markers"
    assert vls.pageShuffleStart() == PageShuffleMarker(kind="start")
    assert vls.pageShuffleEnd() == PageShuffleMarker(kind="end")


def test_blocks_are_extracted_and_markers_removed():
    "markers vanish from pages and page names land in pageShuffleBlocks"
    p = _pages(6)
    s = vls.survey(
        p[0],
        vls.pageShuffleStart(),
        p[1],
        p[2],
        vls.pageShuffleEnd(),
        p[3],
        vls.pageShuffleStart(),
        p[4],
        p[5],
        vls.pageShuffleEnd(),
        build=False,
    )
    assert [page.name for page in s.pages] == ["p1", "p2", "p3", "p4", "p5", "p6"]
    assert s.pageShuffleBlocks == [["p2", "p3"], ["p5", "p6"]]


def test_markers_inside_unpacked_list():
    "markers may arrive via a flattened list"
    p = _pages(3)
    s = vls.survey(*[vls.pageShuffleStart(), *p, vls.pageShuffleEnd()], build=False)
    assert s.pageShuffleBlocks == [["p1", "p2", "p3"]]
    assert len(s.pages) == 3


def test_blocks_not_in_json():
    "pageShuffleBlocks must not leak into the SurveyJS JSON"
    p = _pages(2)
    s = vls.survey(vls.pageShuffleStart(), *p, vls.pageShuffleEnd(), build=False)
    assert "pageShuffleBlocks" not in s.json()
    assert "pageShuffleBlocks" not in s.dict()


def test_no_blocks_by_default():
    s = vls.survey(*_pages(2), build=False)
    assert s.pageShuffleBlocks is None
    assert s.pageShuffleCode() == ""


@pytest.mark.parametrize(
    "layout, message",
    [
        (["start", "p", "end", "end"], "without a preceding"),
        (["start", "p", "start", "p", "end"], "cannot be nested"),
        (["start", "p"], "missing a matching"),
        (["start", "end"], "contains no pages"),
    ],
)
def test_invalid_marker_usage_raises(layout, message):
    "every misuse of the markers is a ValueError"
    items = []
    for i, token in enumerate(layout):
        if token == "start":
            items.append(vls.pageShuffleStart())
        elif token == "end":
            items.append(vls.pageShuffleEnd())
        else:
            items.append(vls.page(f"p{i}", vls.text(f"q{i}", "Q?")))
    with pytest.raises(ValueError, match=message):
        vls.survey(*items, build=False)


def test_generated_code_mentions_blocks_and_variables():
    p = _pages(3)
    s = vls.survey(
        p[0], vls.pageShuffleStart(), p[1], p[2], vls.pageShuffleEnd(), build=False
    )
    code = s.pageShuffleCode()
    assert '[["p2", "p3"]]' in code
    assert "pageShuffle_" in code
    assert "survey.getPageByName" in code
    assert "survey.setVariable" in code
    assert "\\" not in code


def _build_to_tmp(tmp_path, survey_object):
    target = tmp_path / "generated"
    shutil.copytree(
        Path(str(files("velesresearch.website_template"))),
        target,
        ignore=shutil.ignore_patterns("__pycache__", "__init__.py", "node_modules"),
    )
    (target / "node_modules").mkdir()
    survey_object.build(path=tmp_path, folderName="generated", pauseBuild=True)
    survey_js = (target / "src" / "survey.js").read_text()
    component = (target / "src" / "SurveyComponent.jsx").read_text()
    return survey_js, component


def test_build_injects_shuffle_code_before_custom_code(tmp_path):
    "shuffle JS goes into SurveyComponent.jsx ahead of user customCode, not into survey.js"
    p = _pages(3)
    s = vls.survey(
        p[0],
        vls.pageShuffleStart(),
        p[1],
        p[2],
        vls.pageShuffleEnd(),
        build=False,
        customCode="USER_CUSTOM_CODE",
    )
    survey_js, component = _build_to_tmp(tmp_path, s)
    survey_data = json.loads(survey_js[len("export const json = ") : -1])
    assert "pageShuffleBlocks" not in survey_data
    assert "pageShuffle" not in survey_js
    assert "pageShuffle_" in component
    assert '[["p2", "p3"]]' in component
    assert component.index("pageShuffle_") < component.index("USER_CUSTOM_CODE")
    assert (
        "// placeholder"
        not in component.split("{% customCode %}")[1].split("{% end customCode %}")[0]
    )


def test_build_without_blocks_keeps_placeholder(tmp_path):
    s = vls.survey(*_pages(2), build=False)
    _, component = _build_to_tmp(tmp_path, s)
    block = component.split("{% customCode %}")[1].split("{% end customCode %}")[0]
    assert "// placeholder" in block
    assert "pageShuffle" not in component
