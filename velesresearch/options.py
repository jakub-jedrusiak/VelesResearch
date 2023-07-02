"Options objects definitions"

from pydantic import BaseModel


class QuestionOptions(BaseModel):
    "Options for Question object"
    required: bool = False
    answers_order: str = "none"
    placeholder: str | None = None
    inherit_answers: str | None = None
    inherit_answers_mode: str | None = None
    comment: bool = False
    comment_text: str = "Other"
    comment_placeholder: str = ""
    visible: bool = True
    other: bool = False
    other_text: str = "Other"
    other_placeholder: str = ""
    none: bool = False
    none_text: str = "None"
    clear_button: bool = False
    visible_if: str | None = None
    editable_if: str | None = None
    requied_if: str | None = None
    show_number: bool = True


class PageOptions(BaseModel):
    "Options for Page object"
    read_only: bool = False
    time_limit: int | None = None
    visible: bool = True


class SurveyOptions(BaseModel):
    "Options for Survey object"
    language: str = "en"
    url_on_complete: str | None = None
