"Test json file"
import os
from velesresearch import survey, page, questionnaire

RSSI_items = """I feel that I am a person of worth, at least on an equal plane with others.
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

RSSI_scale = """Strongly Agree
Agree
Disagree
Strongly Disagree""".split(
    "\n"
)


def test_json_creation():
    "Test that json file is created"

    # Run the survey command
    survey(page("RSSI", questionnaire("RSSI", RSSI_items, RSSI_scale)))

    # Check if the file was created
    assert os.path.exists("survey.json")
    os.remove("survey.json")
