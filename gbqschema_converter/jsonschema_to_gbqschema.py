# Dmitry Kisler © 2020
# www.dkisler.com

from copy import deepcopy
from typing import Union, Tuple, List
from collections import namedtuple
from google.cloud.bigquery import SchemaField
import fastjsonschema


MapTypes = namedtuple("map_types",
                      ['integer', 'number', 'boolean', 'string', 'date'])

map_types = MapTypes(
    integer="INTEGER",
    number="NUMERIC",
    boolean="BOOLEAN",
    string="STRING",
    date="DATE"
)

TEMPLATE_GBQ_COLUMN = {
    "description": None,
    "name": "col_a",
    "type": "TYPE",
    "mode": "NULLABLE",
}


def _converter(json_schema: dict, 
               to_sdk_schema: bool = False) -> Union[List, List[SchemaField]]:
    """Base function to convert Google BigQuery table schema, JSON representation.
    
    Args:
      
      json_schema: Json schema
                 read https://json-schema.org/
                 for details.
    
    Returns:
      
      Google BigQuery table schema.
    """
    def __gbq_columns(properties: dict,
                      required: list = None) -> list:
        """Function to define Google BigQuery table columns in JSON schema format.

        Column format:
        [
            {
                "description": "columns description",
                "name": "col_a",
                "type": "TYPE",
                "mode": "NULLABLE",
            },
            {
                "description": "columns description",
                "name": "col_b",
                "type": "TYPE",
                "mode": "NULLABLE",
            },
        ]

        Args:
          
          properties: Json schema properties dictionary.
          
          required: List of required keys.

        Returns:
          
          List of column definition dict objects.
        """
        output = []
        for k, v in properties.items():
            gbq_column = deepcopy(TEMPLATE_GBQ_COLUMN)

            gbq_column['name'] = k

            if 'format' not in v:
                gbq_column['type'] = getattr(map_types, v['type'])
            else:
                gbq_column['type'] = "TIMESTAMP" if v['format'] == "date-time"\
                    else getattr(map_types, v['format']) if v['format'] in map_types.__dir__()\
                        else "STRING"

            if to_sdk_schema:
                gbq_column['field_type'] = gbq_column.pop('type')

            if required:
                if k in required:
                    gbq_column['mode'] = "REQUIRED"

            if 'description' in v:
                gbq_column['description'] = v['description']
            else:
                _ = gbq_column.pop('description')

            if to_sdk_schema:
                gbq_column = SchemaField(**gbq_column)
                
            output.append(gbq_column)
        return output

    output = []

    if 'definitions' in json_schema\
            or 'items' in json_schema:
        for prop in json_schema['definitions'].values():
            properties = prop['properties']
            required = prop['required'] if 'required' in prop else None
            output.extend(__gbq_columns(properties, required))
    else:
        properties = json_schema['properties']
        required = json_schema['required'] if 'required' in json_schema else None
        output.extend(__gbq_columns(properties, required))

    return output


def json_representation(json_schema: dict) -> list:
    """Function to convert json schema to Google BigQuery schema in JSON representation.

    Args:
      
      json_schema: Json schema
                 read https://json-schema.org/
                 for details.

    Returns:
      
      Google BigQuery table json schema as list of dict.

    Raises:
      
      fastjsonschema.JsonSchemaDefinitionException: Error occured if input json schema is invalid.
    """
    try:
        fastjsonschema.compile(json_schema)
    except fastjsonschema.JsonSchemaDefinitionException as ex:
        raise ex
    return _converter(json_schema)


def sdk_representation(json_schema: dict) -> List[SchemaField]:
    """Function to convert json schema to Google BigQuery schema in Google SDK representation.

    Args:
      
      json_schema: Json schema
                 read https://json-schema.org/
                 for details.

    Returns:
      
      List of SchemaField objects.
    """
    try:
        fastjsonschema.compile(json_schema)
    except fastjsonschema.JsonSchemaDefinitionException as ex:
        raise ex    
    return _converter(json_schema, to_sdk_schema=True)
