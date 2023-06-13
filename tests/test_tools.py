"Test tools.py module"

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
    survey(
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
        create_file=True,
    )

    survey(
        page(
            "test",
            question(
                "q",
                "Question 1",
                ["Yes", "No"],
            ),
        ),
        create_file=False,
    )
