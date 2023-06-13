"Test tools.py module"

import os
from pathlib import Path
from shutil import rmtree
from velesresearch.tools import question, page, survey


def test_calling():
    "Test calling all functions"
    question(
        "q",
        "Question 1",
        ["Yes", "No"],
        description="This is a question",
    )
    page(
        "test",
        question(
            "q",
            "Question 1",
            ["Yes", "No"],
            description="This is a question",
        ),
        title="Test page",
        description="This is a page",
    )

    os.mkdir("build_dir")
    wd = Path(os.getcwd()) / "build_dir"

    survey(
        "test",
        page(
            "test",
            question(
                "q",
                "Question 1",
                ["Yes", "No"],
                description="This is a question",
            ),
            title="Test page",
            description="This is a page",
        ),
        title="Test survey",
        description="This is a survey",
        create=wd,
    )

    rmtree(wd)

    survey(
        "test",
        page(
            "test",
            question(
                "q",
                "Question 1",
                ["Yes", "No"],
            ),
        ),
        create=False,
    )
