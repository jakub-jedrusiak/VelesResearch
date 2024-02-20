import velesresearch as vls

vls.survey(
    "Test_Survey",
    vls.page(
        "page_1",
        vls.question("name", "What is your name?", question_type="text"),
        vls.question("age", "How old are you?", question_type="text"),
        vls.question(
            "color",
            "What is your favorite color?",
            "Red",
            "Green",
            "Blue",
            question_type="radio",
            options=vls.QuestionOptions(visible_if="{group} = 1"),
        ),
    ),
    options=vls.SurveyOptions(number_of_groups=2),
).build_survey()
