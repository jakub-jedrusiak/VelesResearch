"""
This file contains some open, free-to-use questionnaires in Polish.
If you want to add your own questionnaire, go ahead and add it to this file.
For other languages, use appropriate folder or the main file for English.

Every questionnaire should be a function taking label, description and QuestionOptions objects as arguments.
The default label should be uppercase abbreviation of the questionnaire name. The function itself should be
lowercase abbreviation of the questionnaire name. Every function should have a docstring
with APA-style citation of the questionnaire and info what it measures. See the example below.

I'd be greatful if you could also write a documentation for the questionnaire.
See the repo: https://github.com/jakub-jedrusiak/VelesDocs
"""

from velesresearch.structure import Question
from velesresearch import question, info, QuestionOptions


def tipi(
    label: str = "TIPI",
    question_type: str = "radio",
    description: str | None = None,
    options: QuestionOptions | None = None,
) -> list[Question]:
    """
    Ten Item Personality Inventory (TIPI)
    Ten item adaptation of Big Five. Measures five personality traits: Extraversion, Agreeableness, Conscientiousness, Emotional Stability and Openness to Experience.

    Original:
    Gosling, S. D., Rentfrow, P. J., Swann, W. B. Jr. (2003). A very brief measure of the Big-Five personality domains. Journal of Research in Personality, 37, 504–528.

    Adaptation:
    Sorokowska, A., Słowińska A., Zbieg A., Sorokowski, P. (2014). Polska adaptacja testu Ten Item Personality Inventory (TIPI) – TIPI-PL – wersja standardowa i internetowa. Wrocław: WrocLab.

    Reverse items: 2, 4, 6, 8, 10
    """

    items = """Lubiącą towarzystwo innych, aktywną i optymistyczną.
Krytyczną względem innych, konfliktową.
Sumienną, zdyscyplinowaną.
Pełną niepokoju, łatwo wpadającą w przygnębienie.
Otwartą na nowe doznania, w złożony sposób postrzegającą świat.
Zamkniętą w sobie, wycofaną i cichą.
Zgodną, życzliwą.
Źle zorganizowaną, niedbałą.
Niemartwiącą się, stabilną emocjonalnie.
Trzymającą się utartych schematów, biorącą rzeczy wprost.""".split(
        "\n"
    )

    scale = """Zdecydowanie się nie zgadzam
Raczej się nie zgadzam
W niewielkim stopniu się nie zgadzam
Ani się zgadzam, ani się nie zgadzam
W niewielkim stopniu się zgadzam
Raczej się zgadzam
Zdecydowanie się zgadzam""".split(
        "\n"
    )

    instruction = info(
        "TIPI_instruction",
        "Poniżej przedstawiona jest lista cech, które <u>są lub nie są</u> Twoimi charakterystykami. Zaznacz przy poszczególnych stwierdzeniach, do jakiego stopnia <u>zgadzasz się lub nie zgadzasz</u> z każdym z nich. Oceń stopień, w jakim każde z pytań odnosi się do Ciebie.",
    )

    intro = info("TIPI_intro", "**Spostrzegam siebie jako osobę:**")

    questionnaire = question(
        label,
        items,
        scale,
        question_type=question_type,
        description=description,
        options=options,
    )

    return [instruction, intro] + questionnaire
