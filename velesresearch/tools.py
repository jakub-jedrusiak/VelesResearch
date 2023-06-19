"Functions and wrappers for creating survey structure"
from collections.abc import Sequence
from pathlib import Path
from inspect import stack
from pydantic import validate_arguments
import numpy as np
from .structure import Question, Page, Survey
from .options import QuestionOptions, PageOptions, SurveyOptions


@validate_arguments
def question(
    label: str,
    question_text: str | Sequence[str],
    *answers: str | Sequence[str],
    question_type: str = "radio",
    description: str | None = None,
    options: QuestionOptions | None = None,
) -> Question | list[Question]:
    "Wrapper around Question class"
    answers_list = list(np.concatenate([answers]).flat)
    if isinstance(question_text, str):
        return Question(
            label=label,
            question_text=question_text,
            answers=answers_list,
            question_type=question_type,
            description=description,
            options=options,
        )
    question_list = list(np.concatenate([question_text]).flat)
    q_list = []
    for i in enumerate(question_list):
        q_list.append(
            Question(
                label=f"{label}_{i[0] + 1}",
                question_text=i[1],
                answers=answers_list,
                question_type=question_type,
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
    label: str,
    *pages: Page | Sequence[Page],
    title: str | None = None,
    description: str | None = None,
    options: SurveyOptions | None = None,
    create: bool | str | Path = True,
) -> Survey:
    "Create Survey object from pages, create json file"
    pages_list = list(np.concatenate([pages]).flat)
    survey_obj = Survey(
        label=label,
        pages=pages_list,
        title=title,
        description=description,
        options=options,
    )
    if create and isinstance(create, bool):
        survey_obj.create()
    elif isinstance(create, str) or isinstance(create, Path):
        survey_obj.create(Path(create))
    return survey_obj


def option(type: str | None = None, **kwargs):
    "Create options object for question, page or survey"
    if type is None:
        calling_function = stack()[1].function
    else:
        calling_function = type
    if calling_function in ["question", "Question"]:
        return QuestionOptions(**kwargs)
    elif calling_function in ["page", "Page"]:
        return PageOptions(**kwargs)
    elif calling_function in ["survey", "Survey"]:
        return SurveyOptions(**kwargs)
    else:
        raise ValueError('type must be "question", "page" or "survey"')
