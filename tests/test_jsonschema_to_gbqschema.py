# Dmitry Kisler © 2020
# www.dkisler.com

import pathlib
import importlib.util
from types import ModuleType
from google.cloud.bigquery import SchemaField


DIR = pathlib.Path(__file__).parent
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


schema_in = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
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
                "att_02": {
                    "type": "number",
                    "description": "Att 2"
                },
                "att_03": {
                    "type": "string"
                },
                "att_04": {
                    "type": "boolean"
                },
                "att_05": {
                    "type": "string",
                    "format": "date"
                },
                "att_06": {
                    "type": "string",
                    "format": "date-time"
                },
                "att_07": {
                    "type": "string",
                    "format": "time"
                },
            },
            "additionalProperties": True,
            "required": [
                "att_02",
                "att_03",
                "att_04",
                "att_05",
                "att_06",
                "att_07",
            ]
        }
    }
}


def test_json_representation_conversion() -> None:
    schema_out = [
        {
            "description": "Att 1",
            "name": "att_01",
            "type": "INT64",
            "mode": "NULLABLE"
        },
        {
            "description": "Att 2",
            "name": "att_02",
            "type": "FLOAT64",
            "mode": "REQUIRED"
        },
        {
            "name": "att_03",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "att_04",
            "type": "BOOLEAN",
            "mode": "REQUIRED"
        },
        {
            "name": "att_05",
            "type": "DATE",
            "mode": "REQUIRED"
        },
        {
            "name": "att_06",
            "type": "TIMESTAMP",
            "mode": "REQUIRED"
        },
        {
            "name": "att_07",
            "type": "STRING",
            "mode": "REQUIRED"
        },
    ]

    schema_convert = module.json_representation(schema_in)

    assert schema_convert == schema_out,\
        "Convertion doesn't work"

    return


def test_sdk_representation_conversion() -> None:
    schema_out = [
        SchemaField('att_01', 'INT64', 'NULLABLE', 'Att 1', ()),
        SchemaField('att_02', 'FLOAT64', 'REQUIRED', 'Att 2', ()),
        SchemaField('att_03', 'STRING', 'REQUIRED', None, ()),
        SchemaField('att_04', 'BOOLEAN', 'REQUIRED', None, ()),
        SchemaField('att_05', 'DATE', 'REQUIRED', None, ()),
        SchemaField('att_06', 'TIMESTAMP', 'REQUIRED', None, ()),
        SchemaField('att_07', 'STRING', 'REQUIRED', None, ()),
    ]

    schema_convert = module.sdk_representation(schema_in)

    assert schema_convert == schema_out,\
        "Convertion doesn't work"

    return


schema_in_record = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
            "$ref": "#/definitions/element",
    },
    "definitions": {
        "element": {
            "type": "object",
            "properties": {
                "att_01": {
                    "type": "integer",
                    "description": "Att 1",
                },
                "att_02": {
                    "type": "object",
                    "description": "Att 2",
                    "properties": {
                        "att_11": {
                            "type": "number",
                        },
                        "att_12": {
                            "type": "string",
                        },
                    },
                    "additionalProperties": False,
                    "required": [
                        "att_11",
                    ],
                },
            },
            "additionalProperties": False,
            "required": [
                "att_01",
            ],
        },
    },
}


def test_json_representation_conversion_record() -> None:
    schema_out = [
        {
            "description": "Att 1",
            "name": "att_01",
            "type": "INT64",
            "mode": "REQUIRED"
        },
        {
            "description": "Att 2",
            "name": "att_02",
            "type": "RECORD",
            "mode": "NULLABLE",
            "fields": [
                {
                    "name": "att_11",
                    "type": "FLOAT64",
                    "mode": "REQUIRED"
                },
                {
                    "name": "att_12",
                    "type": "STRING",
                    "mode": "NULLABLE"
                }
            ]
        },
    ]

    schema_convert = module.json_representation(schema_in_record)

    assert schema_convert == schema_out,\
        "Convertion doesn't work"

    return


def test_sdk_representation_conversion_record() -> None:
    schema_out = [
        SchemaField('att_01', 'INT64', 'REQUIRED', 'Att 1', ()),
        SchemaField('att_02', 'RECORD', 'NULLABLE', 'Att 2', (
            SchemaField('att_11', 'FLOAT64', 'REQUIRED', None, ()),
            SchemaField('att_12', 'STRING', 'NULLABLE', None, ()))
        )
    ]

    schema_convert = module.sdk_representation(schema_in_record)

    assert schema_convert == schema_out,\
        "Convertion doesn't work"

    return
