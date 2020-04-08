import os
import pytest
import importlib.util
from types import ModuleType


DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE = "gbqschema_converter"
MODULE = "jsonschema_to_gbqschema"

FUNCTIONS = set(['json_representation', 'sdk_representation'])


def load_module(module_name: str) -> ModuleType:
    """Function to load the module.

    Args:
        module_name: module name

    Returns:
        module object
    """
    file_path = f"{DIR}/../{PACKAGE}/{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_module_exists():
    try:
        _ = load_module(MODULE)
    except Exception as ex:
        raise ex
    return


module = load_module(MODULE)


def test_module_miss_functions() -> None:
    missing = FUNCTIONS.difference(set(module.__dir__()))
    assert not missing, f"""Function(s) '{"', '".join(missing)}' is(are) missing."""
    return


def test_json_validator() -> None:
    schema_in = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "array1",
        "items": {
            "$ref": "#/definitions/element"
        },
        "definitions": {
            "element": {
                "type": "object",
                "properties": {
                    "att_01": {
                        "type": "integer",
                        "description": "Att 1"
                    },
                }
            }
        }
    }

    try:
        module.json_representation(schema_in)
    except Exception as ex:
        assert "Unknown type: 'array1'" in str(ex),\
            "Input validation doesn't work"
    
    schema_in = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "array",
        "items": {
            "$ref": "#/definitions/element"
        },
        "definitions": {
            "element": {
                "type": "objects",
                "properties": {
                    "att_01": {"type": "integer"}
                }
            }
        }
    }

    try:
        module.json_representation(schema_in)
    except Exception as ex:
        assert "Unknown type: 'objects'" in str(ex),\
            "Input validation doesn't work"
