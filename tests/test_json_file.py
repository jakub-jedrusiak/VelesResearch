"Test json file"
import os
from pathlib import Path
from shutil import rmtree
from velesresearch import survey, page, question

RSSI_items = """I feel that I am a person of worth, at least on an equal plane with others.
I feel that I have a number of good qualities.
All in all, I am inclined to feel that I am a failure.
I am able to do things as well as most other people.
I feel I do not have much to be proud of.
I take a positive attitude toward myself.
On the whole, I am satisfied with myself.
I wish I could have more respect for myself.
I certainly feel useless at times.
At times I think I am no good at all."""

RSSI_scale = """Strongly Agree
Agree
Disagree
Strongly Disagree"""


def test_creation():
    "Test that syrvey files are created"

    os.mkdir("build_dir")
    wd = Path(os.getcwd()) / "build_dir"

    survey(
        "RSSI",
        page("RSSI", question("RSSI", RSSI_items.split("\n"), RSSI_scale.split("; "))),
        create=wd,
    )

    # Check if the file was created

    for file in [
        "src",
        "public",
        "dist",
        "package.json",
        "package-lock.json",
        "node_modules",
        "src/survey.ts",
        "src/index.css",
        "src/SurveyComponent.tsx",
        "index.html",
    ]:
        assert os.path.exists(wd / file)

    rmtree(wd)
