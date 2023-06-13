"Functions and wrappers for creating survey structure"
from collections.abc import Sequence
from pydantic import validate_arguments
import numpy as np
from .structure import Question, Page, Survey
from .options import QuestionOptions, PageOptions, SurveyOptions


def question(
    label: str,
    question_type: str,
    question_text: str,
    *answers: str | Sequence[str],
    description: str | None = None,
    options: QuestionOptions | None = None,
) -> Question:
    "Wrapper around Question class"
    answers_list = list(np.concatenate([answers]).flat)
    return Question(
        label=label,
        question_type=question_type,
        question_text=question_text,
        answers=answers_list,
        description=description,
        options=options,
    )


@validate_arguments
def questionnaire(
    label: str,
    items: Sequence[str],
    answers: Sequence[str] | str,
    question_type: str = "radio",
    description: str | None = None,
    options: QuestionOptions | None = None,
) -> list[Question]:
    "Convert whole questionnaire to Question objects list"
    q_list = []
    for i in enumerate(items):
        q_list.append(
            Question(
                label=f"{label}_{i[0] + 1}",
                question_type=question_type,
                question_text=i[1],
                answers=answers,
                description=description,
                options=options,
            )
        )
    return q_list


def page(
    label: str,
    *questions: Question | Sequence[Question],
    title: str | None = None,
    description: str | None = None,
    options: PageOptions | None = None,
) -> Page:
    "Wrapper around Page class"
    questions_list = list(np.concatenate([questions]).flat)
    return Page(
        label=label,
        questions=questions_list,
        title=title,
        description=description,
        options=options,
    )


def survey(
    *pages: Page | Sequence[Page],
    title: str | None = None,
    description: str | None = None,
    options: SurveyOptions | None = None,
    create_file: bool = True,
) -> Survey:
    "Create Survey object from pages, create json file"
    pages_list = list(np.concatenate([pages]).flat)
    survey_obj = Survey(
        pages=pages_list, title=title, description=description, options=options
    )
    if create_file:
        survey_obj.create()
    return survey_obj
