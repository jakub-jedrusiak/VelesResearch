"""
This file contains some open, free-to-use questionnaires in English.
If you want to add your own questionnaire, go ahead and add it to this file.
For other languages, use appropriate folder.

Every questionnaire should be a function taking label, type, description and QuestionOptions objects as arguments.
The default label should be uppercase abbreviation of the questionnaire name. The function itself should be
lowercase abbreviation of the questionnaire name. Every function should have a docstring
with APA-style citation of the questionnaire and info what it measures. See the example below.

I'd be greatful if you could also write a documentation for the questionnaire.
See the repo: https://github.com/jakub-jedrusiak/VelesDocs
"""
from velesresearch.tools import question, QuestionOptions


def rse(
    label: str = "RSE",
    question_type: str = "radio",
    description: str | None = None,
    options: QuestionOptions | None = None,
):
    """
    Rosenberg Self-Esteem Scale (RSE)
    One of the most popular self-esteem scales. Measures global self-esteem.
    Rosenberg, M. (1965). Society and the adolescent self-image. Princeton, NJ: Princeton University Press.

    Reverse items: 3, 5, 8, 10
    """
    RSE_items = """I feel that I am a person of worth, at least on an equal plane with others.
I feel that I have a number of good qualities.
All in all, I am inclined to feel that I am a failure.
I am able to do things as well as most other people.
I feel I do not have much to be proud of.
I take a positive attitude toward myself.
On the whole, I am satisfied with myself.
I wish I could have more respect for myself.
I certainly feel useless at times.
At times I think I am no good at all.""".split(
        "\n"
    )

    RSE_scale = "Strongly Agree; Agree; Disagree; Strongly Disagree".split("; ")

    return question(
        label,
        RSE_items,
        RSE_scale,
        question_type=question_type,
        description=description,
        options=options,
    )
