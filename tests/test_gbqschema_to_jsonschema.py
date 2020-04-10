# Dmitry Kisler © 2020
# www.dkisler.com

import pathlib
import pytest
import importlib.util
from types import ModuleType
from google.cloud.bigquery import SchemaField


DIR = pathlib.Path(__file__).parent
PACKAGE = "gbqschema_converter"
MODULE = "gbqschema_to_jsonschema"

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
    schema_in = [
        {
            "description": "Att 1",
            "name": "att_01",
            "type": "INT64",
            "mode": "NULLABLE"
        },
        {
            "name": "att_02",
            "type": "FFA",
            "mode": "REQUIRED"
        },
    ]

    try:
        module.json_representation(schema_in)
    except Exception as ex:
        assert "data[1].type must be one of" in str(ex),\
            "Input validation 1 doesn't work"

    schema_in = [
        {
            "description1": "Att 1",
            "name": "att_01",
            "type": "INT64",
            "mode": "NULLABLE"
        },
    ]

    try:
        module.json_representation(schema_in)
    except Exception as ex:
        assert "data[0] must not contain" in str(ex),\
            "Input validation 2 doesn't work"

    schema_in = [
        {
            "name": "att_01",
            "type": "INT64",
            "mode": "NULLABLE1"
        },
    ]

    try:
        module.json_representation(schema_in)
    except Exception as ex:
        assert "data[0].mode must be valid exactly by one of oneOf definition" in str(ex),\
            "Input validation 3 doesn't work"

    return


schema_out = {
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
                    "type": "number"
                },
                "att_04": {
                    "type": "string"
                },
                "att_05": {
                    "type": "boolean"
                },
                "att_06": {
                    "type": "boolean"
                },
                "att_07": {
                    "type": "string"
                },
                "att_08": {
                    "type": "string",
                    "format": "date"
                },
                "att_09": {
                    "type": "string",
                    "pattern": "^[0-9]{4}-((|0)[1-9]|1[0-2])-((|[0-2])[1-9]|3[0-1])(|T)((|[0-1])[0-9]|2[0-3]):((|[0-5])[0-9]):((|[0-5])[0-9])(|.[0-9]{1,6})$"
                },
                "att_10": {
                    "type": "string",
                    "format": "date-time"
                },
                "att_11": {
                    "type": "string",
                    "pattern": "^((|[0-1])[0-9]|2[0-3]):((|[0-5])[0-9]):((|[0-5])[0-9])(|.[0-9]{1,6})$"
                },
                "att_12": {
                    "type": "integer"
                },
                "att_13": {
                    "type": "integer"
                },
                "att_14": {
                    "type": "number"
                }
            },
            "additionalProperties": True,
            "required": [
                "att_02",
                "att_03",
                "att_04",
                "att_05",
                "att_06",
                "att_07",
                "att_08",
                "att_09",
                "att_10",
                "att_11",
                "att_12",
                "att_13",
                "att_14"
            ]
        }
    }
}


def test_json_representation_conversion() -> None:
    schema_in = [
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
            "type": "NUMERIC",
            "mode": "REQUIRED"
        },
        {
            "name": "att_04",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "att_05",
            "type": "BOOL",
            "mode": "REQUIRED"
        },
        {
            "name": "att_06",
            "type": "BOOLEAN",
            "mode": "REQUIRED"
        },
        {
            "name": "att_07",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "att_08",
            "type": "DATE",
            "mode": "REQUIRED"
        },
        {
            "name": "att_09",
            "type": "DATETIME",
            "mode": "REQUIRED"
        },
        {
            "name": "att_10",
            "type": "TIMESTAMP",
            "mode": "REQUIRED"
        },
        {
            "name": "att_11",
            "type": "TIME",
            "mode": "REQUIRED"
        },
        {
            "name": "att_12",
            "type": "INT",
            "mode": "REQUIRED"
        },
        {
            "name": "att_13",
            "type": "INTEGER",
            "mode": "REQUIRED"
        },
        {
            "name": "att_14",
            "type": "FLOAT",
            "mode": "REQUIRED"
        },
    ]

    schema_convert = module.json_representation(schema_in, True)

    assert schema_convert == schema_out,\
        "Convertion doesn't work"

    return


def test_sdk_representation_conversion() -> None:
    schema_in = [
        SchemaField('att_01', 'INT64', 'NULLABLE', 'Att 1', ()),
        SchemaField('att_02', 'FLOAT64', 'REQUIRED', 'Att 2', ()),
        SchemaField('att_03', 'NUMERIC', 'REQUIRED', None, ()),
        SchemaField('att_04', 'STRING', 'REQUIRED', None, ()),
        SchemaField('att_05', 'BOOL', 'REQUIRED', None, ()),
        SchemaField('att_06', 'BOOLEAN', 'REQUIRED', None, ()),
        SchemaField('att_07', 'STRING', 'REQUIRED', None, ()),
        SchemaField('att_08', 'DATE', 'REQUIRED', None, ()),
        SchemaField('att_09', 'DATETIME', 'REQUIRED', None, ()),
        SchemaField('att_10', 'TIMESTAMP', 'REQUIRED', None, ()),
        SchemaField('att_11', 'TIME', 'REQUIRED', None, ()),
        SchemaField('att_12', 'INT', 'REQUIRED', None, ()),
        SchemaField('att_13', 'INTEGER', 'REQUIRED', None, ()),
        SchemaField('att_14', 'FLOAT', 'REQUIRED', None, ())
    ]

    schema_convert = module.sdk_representation(schema_in, True)

    assert schema_convert == schema_out,\
        "Convertion doesn't work"

    return
