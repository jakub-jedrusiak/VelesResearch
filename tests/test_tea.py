import os
from shutil import rmtree
import velesresearch as vls


def test_panels():
    "Test that panels are created"
    vls.survey(
        vls.page(
            "panel_page",
            vls.panel(
                "panel",
                vls.info("info", "This is a panel"),
            ),
        ),
        createStructure=False,
    )


def test_wrappers():
    "Test that questions are created"
    tea_kinds = ["Green", "Black", "Oolong", "White", "Herbal"]

    vls.survey(
        vls.page(
            "tea_page",
            vls.info(
                "info",
                "You will be asked a series of questions about tea. Be sure to think about your choices carefully. **It is a serious matter.**",
            ),
            vls.consent(),
            vls.dropdown("dropdown", "What is your favorite tea?", tea_kinds),
            vls.text("text", "What do you like about tea?"),
            vls.checkbox(
                "checkbox",
                "What do you like in your tea?",
                ["Sugar", "Milk", "Honey", "Lemon"],
                showNoneItem=True,
            ),
            vls.ranking(
                "ranking", "Rank these kinds of tea from best to worst", tea_kinds
            ),
            vls.radio(
                "radio",
                "If you were stranded on an island and had a chance to bring one kind of tea, which one would you choose?",
                tea_kinds,
            ),
            vls.dropdownMultiple(
                "dropdownMultiple",
                "Select 2 best kinds of tea for an autumn evening",
                tea_kinds,
                minSelectedChoices=2,
                maxSelectedChoices=2,
            ),
            vls.textLong(
                "textLong",
                "What is your favorite tea memory?",
                description="Describe in 2-3 sentences",
            ),
            vls.rating("rating", "Rate your tea experience", rateMin=1, rateMax=10),
            vls.yesno("yesno", "Are you certain that you may or may not love tea?"),
            vls.slider("slider", "Select your tea temperature", min=0, max=100),
            vls.image("image", vls.convertImage("figs/tea.jpg")),
        ),
        path="./build_dir",
        folderName="tea",
    )
    assert os.path.exists("./build_dir/tea/src/survey.js")
    rmtree("./build_dir")
