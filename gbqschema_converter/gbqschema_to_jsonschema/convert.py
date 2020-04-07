# Dmitry Kisler © 2020
# www.dkisler.com

from typing import Union, Tuple, List
from collections import namedtuple
from google.cloud import bigquery
import fastjsonschema


gbq_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "required": [
            "name",
            "type",
            "mode"
        ],
        "properties": {
            "description": {
                "type": "string"
            },
            "name": {
                "type": "string",
                "examples": [
                    "att1"
                ]
            },
            "type": {
                "type": "string",
                "enum": [
                    "INT",
                    "INTEGER",
                    "INT64",
                    "FLOAT",
                    "FLOAT64",
                    "NUMERIC",
                    "BOOL",
                    "BOOLEAN",
                    "STRING",
                    "BYTES",
                    "DATE",
                    "DATETIME",
                    "TIME",
                    "TIMESTAMP"
                ]
            },
            "mode": {
                "type": "string",
                "enum": [
                    "REQUIRED",
                    "NULLABLE"
                ]
            }
        },
        "additionalProperties": False,
    },
}

validate = fastjsonschema.compile(gbq_schema)

TEMPLATE = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "$ref": "#/definitions/element"
    },
    "definitions": {
        "element": {
            "type": "object",
            "properties": {

            },
            "additionalProperties": False,
            "required": [
            ],
        },
    },
}

MapTypes = namedtuple("map_types",
                      gbq_schema['items']['properties']['type']['enum'])

map_types = MapTypes(
    INT={"type": "integer"},
    INTEGER={"type": "integer"},
    INT64={"type": "integer"},
    FLOAT={"type": "number"},
    FLOAT64={"type": "number"},
    NUMERIC={"type": "number"},
    BOOL={"type": "boolean"},
    BOOLEAN={"type": "boolean"},
    STRING={"type": "string"},
    BYTES={"type": "string"},
    DATE={"type": "string", "format": "date"},
    DATETIME={"type": "string", "format": "date-time"},
    TIME={"type": "string", "format": "time"},
    TIMESTAMP={"type": "string", "format": "time"}
)


def representation_json(gbq_schema: dict,
                        additional_properties: bool = False) -> dict:
    """Function to convert Google Big Query schema in JSON representation to json schema.

    Args:
      gbq_schema: Bigquery schema, JSON representation
                read https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file 
                for details.
      additional_properties: Json schema should contain "additionalProperties".

    Returns:
      Json schema as dict.
    
    Raises:
      fastjsonschema.JsonSchemaException: Error occured if input Google Big Query schema is invalid.
    """
    try:
        validate(gbq_schema)
    except fastjsonschema.JsonSchemaException as ex:
        raise ex

    output = TEMPLATE.copy()

    for element in gbq_schema:
        key = element['name']
        
        output['definitions']['element']['properties'][key] = getattr(map_types, element['type'])
        
        if 'description' in element:
            output['definitions']['element']['properties'][key]['description'] = element['description']
        
        if element['mode'] == "REQUIRED":
            output['definitions']['element']['required'].append(key)
    
    output['definitions']['element']['additionalProperties'] = additional_properties

    return output


def representation_google_sdk(gbq_schema: List[bigquery.SchemaField],
                              restrictive: bool = False) -> dict:
    """Function to convert Google Big Query schema in Google SDK representation to json schema.

    Args:
      gbq_schema: bigquery schema, SDK repsentation
                read https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.schema.SchemaField.html
                for details.
      additional_properties: jsonschema should contain "additionalProperties".

    Returns:
      json schema as dict.
    """
    pass
