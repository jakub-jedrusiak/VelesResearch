from velesresearch.utils import *
from velesresearch.models import PageModel
from velesresearch import radio


def test_get_class_attributes():
    get_class_attributes(PageModel)


def test_get_class_attributes_assignments():
    get_class_attributes_assignments(PageModel)


def test_create_docs():
    create_docs(radio)
