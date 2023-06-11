"Test structure.py module"


import pytest
import velesresearch.structure as st


def test_calling():
    "Test calling all functions"
    st.Question(
        label="q",
        question_type="radio",
        question_text="Question 1",
        answers=["Yes", "No"],
    )
    st.Page(
        label="test",
        questions=st.Question(
            label="q",
            question_type="radio",
            question_text="Question 1",
            answers=["Yes", "No"],
        ),
    )
    st.Survey(
        pages=st.Page(
            label="test",
            questions=st.Question(
                label="q",
                question_type="radio",
                question_text="Question 1",
                answers=["Yes", "No"],
            ),
        )
    )


def test_printing():
    "Test printing all classes"
    q = st.Question(
        label="q",
        question_type="radio",
        question_text="Question 1",
        answers=["Yes", "No"],
    )

    p = st.Page(
        label="test",
        questions=st.Question(
            label="q",
            question_type="radio",
            question_text="Question 1",
            answers=["Yes", "No"],
        ),
    )

    s = st.Survey(
        pages=st.Page(
            label="test",
            questions=st.Question(
                label="q",
                question_type="radio",
                question_text="Question 1",
                answers=["Yes", "No"],
            ),
        )
    )

    print(q)
    print(p)
    print(s)
    print(p[0])
    print(s[0])
    print(p["q"])
    print(s["test"])
    print([q, q])
    print([p, p])
    print([s, s])


def test_unique_labels_questions():
    "Test that exception is raised when questions labels in page are not unique"
    with pytest.raises(ValueError):
        question = st.Question(
            label="q",
            question_type="radio",
            question_text="Question 1",
            answers=["Yes", "No"],
        )
        st.Page(label="test", questions=[question, question])


def test_unique_labels_pages():
    "Test that exception is raised when pages labels in survey are not unique"
    with pytest.raises(ValueError):
        question = st.Question(
            label="q",
            question_type="radio",
            question_text="Question 1",
            answers=["Yes", "No"],
        )
        page = st.Page(label="test", questions=question)
        st.Survey(pages=[page, page])


def test_subscripting_page():
    "Test subscripting in Page objects"
    page = st.Page(
        label="test",
        questions=st.Question(
            label="q",
            question_type="radio",
            question_text="Question 1",
            answers=["Yes", "No"],
        ),
    )
    print(page[0])
    print(page["q"])


def test_subscripting_survey():
    "Test subscripting in Survey objects"
    survey = st.Survey(
        pages=st.Page(
            label="test",
            questions=st.Question(
                label="q",
                question_type="radio",
                question_text="Question 1",
                answers=["Yes", "No"],
            ),
        )
    )
    print(survey[0])
    print(survey["test"])
