# Dmitry Kisler © 2020
# www.dkisler.com

from typing import Union, Tuple, List
from collections import namedtuple
from google.cloud import bigquery
import fastjsonschema


def json_representation(json_schema: dict) -> dict:
    """Function to convert json schema to Google Big Query schema in JSON representation.

    Args:
      json_schema: Json schema
                read https://json-schema.org/
                for details.

    Returns:
      Json schema as dict.
    
    Raises:
      fastjsonschema.JsonSchemaDefinitionException: Error occured if input json schema is invalid.
    """
    try:
        fastjsonschema.compile(json_schema)
    except fastjsonschema.JsonSchemaDefinitionException as ex:
        raise ex
    
    pass


def sdk_representation(json_schema: dict) -> List[bigquery.SchemaField]:
    """Function to convert json schema to Google Big Query schema in Google SDK representation.

    Args:
      json_schema: json schema
                read https://json-schema.org/
                for details.

    Returns:
      List of SchemaField objects.
    """
    pass
