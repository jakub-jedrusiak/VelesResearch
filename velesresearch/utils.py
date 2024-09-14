"""Additional utility functions for Veles"""

import itertools


def flatten(args: tuple) -> list:
    """Flatten a list of lists or touples"""
    args = [*args]
    args = [[arg] if not isinstance(arg, (list, tuple)) else arg for arg in args]
    return list(itertools.chain.from_iterable(args))


def dict_without_defaults(self) -> dict:
    "Return a dictionary of the changed object's attributes"
    # Values that are set to their default values differently from the SurveyJS default values
    # "attribute": "default value in SurveyJS"
    custom_defaults = {}

    return {
        k: v
        for k, v in vars(self).items()
        if (custom_defaults.get(k) is not None and v != custom_defaults.get(k))
        or (
            k not in ["questions", "pages", "validators", "addCode", "columns", "rows"]
            and v != self.model_fields[k].default
        )
        or (k == "type")
    }


def get_class_attributes(cls):
    attributes = []

    # Loop over the model fields, including inherited ones
    for name, field in cls.model_fields.items():
        # Get the type annotation from `field.annotation`
        attr_type = field.annotation

        # Handle None or optional types (Pydantic uses `NoneType` for fields with `None`)
        if hasattr(attr_type, "__name__"):
            attr_type_str = attr_type.__name__
        else:
            attr_type_str = str(attr_type).replace("typing.", "")

        # Handle the default value
        if field.default is not None:
            default = field.default
        elif field.default_factory is not None:
            default = field.default_factory()
        else:
            default = None

        # Append the attribute in the desired format
        if name not in [
            "type",
            "name",
            "title",
            "choices",
            "columns",
            "pages",
            "questions",
        ]:
            attributes.append(f"{name}: {attr_type_str} = {default!r}")

    # Join attributes as comma-separated values
    return ",".join(attributes) + ","


def get_class_attributes_assignments(cls):
    # Extract all field names from the model
    attribute_assignments = []
    for name in cls.model_fields:
        if name not in [
            "type",
            "name",
            "title",
            "choices",
            "columns",
            "pages",
            "questions",
        ]:
            attribute_assignments.append(f'"{name}": {name}')

    # Join them as a comma-separated string
    return "args = {" + ", ".join(attribute_assignments) + "}"
