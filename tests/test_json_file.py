"Test json file"

import json
import os
import shutil
from importlib.resources import files
from pathlib import Path
from shutil import rmtree
from velesresearch import survey, page, radio

RSES_items = """I feel that I am a person of worth, at least on an equal plane with others.
I feel that I have a number of good qualities.
All in all, I am inclined to feel that I am a failure.
I am able to do things as well as most other people.
I feel I do not have much to be proud of.
I take a positive attitude toward myself.
On the whole, I am satisfied with myself.
I wish I could have more respect for myself.
I certainly feel useless at times.
At times I think I am no good at all."""

RSES_scale = "Strongly Agree; Agree; Disagree; Strongly Disagree"


def test_creation():
    "Test that survey files are created"

    os.mkdir("build_dir")
    wd = Path(os.getcwd()) / "build_dir"

    survey(
        page("RSES", radio("RSES", RSES_items.split("\n"), RSES_scale.split("; "))),
        path=wd,
        folderName="RSES",
    )

    # Check if the file was created

    for file in [
        "src",
        "public",
        "build",
        "package.json",
        "node_modules",
        "src/survey.js",
        "src/SurveyComponent.jsx",
        "public/index.html",
    ]:
        assert os.path.exists(wd / "RSES" / file)

    rmtree(wd)


def test_custom_javascript_is_written_to_component(tmp_path):
    "custom JavaScript belongs in SurveyComponent.jsx, not survey.js"
    target = tmp_path / "generated"
    shutil.copytree(
        Path(str(files("velesresearch.website_template"))),
        target,
        ignore=shutil.ignore_patterns("__pycache__", "__init__.py"),
    )
    (target / "node_modules").mkdir()

    survey_object = survey(
        page(
            "custom_page",
            radio(
                "custom_question",
                ["Yes", "No"],
                customCode="question code",
                customFunctions="function questionFunction() {}",
            ),
            customCode="page code",
            customFunctions="function pageFunction() {}",
        ),
        build=False,
    )
    survey_object.build(path=tmp_path, folderName="generated", pauseBuild=True)

    survey_js = (target / "src" / "survey.js").read_text(encoding="utf-8")
    survey_data = json.loads(survey_js[len("export const json = ") : -1])
    component = (target / "src" / "SurveyComponent.jsx").read_text(encoding="utf-8")

    assert "customCode" not in survey_js
    assert "customFunctions" not in survey_js
    assert "page code" in component
    assert "question code" in component
    assert "pageFunction" in component
    assert "questionFunction" in component
    assert survey_data["pages"][0]["name"] == "custom_page"
