"Test structure.py module"


import pytest
import velesresearch.structure as st


def test_calling():
    "Test calling all functions"
    st.Question("q", "radio", "Question 1", "Yes", "No")
    st.Page("test", st.Question("q", "radio", "Question 1", "Yes", "No"))
    st.Survey(st.Page("test", st.Question("q", "radio", "Question 1", "Yes", "No")))


def test_printing():
    "Test printing all classes"
    print(st.Question("q", "radio", "Question 1", "Yes", "No"))
    print(st.Page("test", st.Question("q", "radio", "Question 1", "Yes", "No")))
    print(
        st.Survey(st.Page("test", st.Question("q", "radio", "Question 1", "Yes", "No")))
    )


def test_unique_labels_questions():
    "Test that exception is raised when questions labels in page are not unique"
    with pytest.raises(ValueError):
        question = st.Question("q", "radio", "Question 1", "Yes", "No")
        st.Page("test", question, question)


def test_unique_labels_pages():
    "Test that exception is raised when pages labels in survey are not unique"
    with pytest.raises(ValueError):
        question = st.Question("q", "radio", "Question 1", "Yes", "No")
        page = st.Page("test", question)
        st.Survey(page, page)


def test_subscripting_page():
    "Test subscripting in Page objects"
    page = st.Page("test", st.Question("q", "radio", "Question 1", "Yes", "No"))
    print(page[0])
    print(page["q"])


def test_subscripting_survey():
    "Test subscripting in Survey objects"
    survey = st.Survey(
        st.Page("test", st.Question("q", "radio", "Question 1", "Yes", "No"))
    )
    print(survey[0])
    print(survey["test"])
