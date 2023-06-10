"Test structure.py module"

import pytest
import velesresearch.structure as st


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
