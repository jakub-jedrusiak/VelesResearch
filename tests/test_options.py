"Test options.py module"

from os import remove
import velesresearch.options as opt
from velesresearch.tools import question, page, survey


def test_calling():
    "Test calling all functions"
    opt.QuestionOptions()
    opt.PageOptions()
    opt.SurveyOptions()


def test_survey_opts():
    q_opt = opt.QuestionOptions(required=True)
    p_opt = opt.PageOptions(visible=False)
    s_opt = opt.SurveyOptions(language="pl")

    q = question("q1", "radio", "What is life?", "Yes", "No", "42", options=q_opt)
    p = page("p1", q, options=p_opt)
    s = survey(p, options=s_opt)

    remove("survey.json")
