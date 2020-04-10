# Google BigQuery Table Schema Converter

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](./LICENSE)
[![pyversion](https://img.shields.io/static/v1?label=python&color=blue&message=3.6%20|%203.7%20|%203.8)](./)
[![coverage](https://img.shields.io/static/v1?label=coverage&color=brightgreen&message=94%25)](./)
[![test](https://img.shields.io/static/v1?label=tests&color=success&message=100%25)](./)

Python library to convert [Google BigQuery table schema](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#datetime_type) into [draft-07](https://json-schema.org/draft-07/json-schema-release-notes.html) [json schema](https://json-schema.org/) and vice versa.

The library includes two main modules:

```bash
gbqschema_converter
├── gbqschema_to_jsonschema.py
└── jsonschema_to_gbqschema.py
```

Each of those modules has two main functions:

- `json_representation`: corresponds to json output (input for `gbqschema_to_jsonschema`).
- `sdk_representation`: corresponds to [Google Python SDK format](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.schema.SchemaField.html) output (input for `gbqschema_to_jsonschema`).

## Installation

```bash
python3 -m venv env && source ${PWD}/env/bin/activate
(env) pip install --no-cache-dir gbqschema_converter
```

## Usage: CLI

### Convert json-schema to GBQ table schema

```bash
(env) json2gbq -h
usage: json2gbq [-h] (-i INPUT | -f FILE)

Google BigQuery Table Schema Converter

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input object as string.
  -f FILE, --file FILE  Input object as file path.
```

#### Example: stdin

Execution:

```bash
(env) json2gbq -i '{
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
        }
      },
      "required": [
        "att_02"
      ]
    }
  }
}'
```

Output:

```bash
2020-04-08 21:42:51.700 [INFO ] [Google BigQuery Table Schema Converter] Output (5.52 ms elapsed):
[
  {
    "description": "Att 1",
    "name": "att_01",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "description": "Att 2",
    "name": "att_02",
    "type": "NUMERIC",
    "mode": "REQUIRED"
  },
  {
    "name": "att_03",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "att_04",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  },
  {
    "name": "att_05",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "att_06",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  },
  {
    "name": "att_07",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
```

#### Example: file

Execution:

```bash
(env) json2gbq -f ${PWD}/data/jsonschema.json
```

Output:

```bash
2020-04-08 21:57:25.516 [INFO ] [Google BigQuery Table Schema Converter] Output (6.39 ms elapsed):
[
  {
    "description": "Att 1",
    "name": "att_01",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "description": "Att 2",
    "name": "att_02",
    "type": "NUMERIC",
    "mode": "REQUIRED"
  },
  {
    "name": "att_03",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "att_04",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  },
  {
    "name": "att_05",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "att_06",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  },
  {
    "name": "att_07",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
```

### Convert GBQ table schema to json-schema

```bash
(env) gbq2json -h
usage: gbq2json [-h] (-i INPUT | -f FILE)

Google BigQuery Table Schema Converter

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input object as string.
  -f FILE, --file FILE  Input object as file path.
```

#### Example: stdin

Execution:

```bash
(env) gbq2json -i '[
  {
    "description": "Att 1",
    "name": "att_01",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "description": "Att 2",
    "name": "att_02",
    "type": "NUMERIC",
    "mode": "REQUIRED"
  },
  {
    "name": "att_03",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "att_04",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  },
  {
    "name": "att_05",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "att_06",
    "type": "DATETIME",
    "mode": "NULLABLE"
  },
  {
    "name": "att_07",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  }
]'
```

Output:

```bash
2020-04-08 21:51:05.370 [INFO ] [Google BigQuery Table Schema Converter] Output (1.08 ms elapsed):
{
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
          "pattern": "^[0-9]{4}-((|0)[1-9]|1[0-2])-((|[0-2])[1-9]|3[0-1])(|T)((|[0-1])[0-9]|2[0-3]):((|[0-5])[0-9]):((|[0-5])[0-9])(|.[0-9]{1,6})$"
        },
        "att_07": {
          "type": "string",
          "format": "date-time"
        }
      },
      "additionalProperties": false,
      "required": [
        "att_02"
      ]
    }
  }
}
```

#### Example: file

Execution:

```bash
(env) gbq2json -f ${PWD}/data/gbqschema.json
```

Output:

```bash
2020-04-08 21:55:20.275 [INFO ] [Google BigQuery Table Schema Converter] Output (1.72 ms elapsed):
{
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
          "pattern": "^[0-9]{4}-((|0)[1-9]|1[0-2])-((|[0-2])[1-9]|3[0-1])(|T)((|[0-1])[0-9]|2[0-3]):((|[0-5])[0-9]):((|[0-5])[0-9])(|.[0-9]{1,6})$"
        },
        "att_07": {
          "type": "string",
          "format": "date-time"
        }
      },
      "additionalProperties": false,
      "required": [
        "att_02"
      ]
    }
  }
}
```

## Usage: python program

### Convert json-schema to GBQ table schema

#### Example: output as json

```python
from gbqschema_converter.jsonschema_to_gbqschema import json_representation as converter

schema_in = {
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
          "description": "Att 1"
        },
        "att_02": {
          "type": "number",
        },
      }
      "required": [
        "att_02",
      ],
    },
  },
}

schema_out = converter(schema_in)
print(schema_out)
```

Output:

```bash
[{'description': 'Att 1', 'name': 'att_01', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'att_02', 'type': 'NUMERIC', 'mode': 'REQUIRED'}]
```

#### Example: output as list of SchemaField (SDK format)

```python
from gbqschema_converter.jsonschema_to_gbqschema import sdk_representation as converter

schema_in = {
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
          "description": "Att 1"
        },
        "att_02": {
          "type": "number",
        },
      },
      "required": [
        "att_02",
      ],
    },
  },
}

schema_out = converter(schema_in)
print(schema_out)
```

Output:

```bash
[SchemaField('att_01', 'INTEGER', 'NULLABLE', 'Att 1', ()), SchemaField('att_02', 'NUMERIC', 'REQUIRED', None, ())]
```

### Convert GBQ table schema to json-schema

#### Example: output as json

```python
from gbqschema_converter.gbqschema_to_jsonschema import json_representation as converter

schema_in = [
    {
        'description': 'Att 1',
        'name': 'att_01',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    },
    {
        'name': 'att_02',
        'type': 'NUMERIC',
        'mode': 'REQUIRED'
    }
]

schema_out = converter(schema_in)
print(schema_out)
```

Output:

```bash
{'$schema': 'http://json-schema.org/draft-07/schema#', 'type': 'array', 'items': {'$ref': '#/definitions/element'}, 'definitions': {'element': {'type': 'object', 'properties': {'att_01': {
'type': 'integer', 'description': 'Att 1'}, 'att_02': {'type': 'number'}}, 'additionalProperties': False, 'required': ['att_02']}}}
```

#### Example: output as list of SchemaField (SDK format)

```python
from gbqschema_converter.gbqschema_to_jsonschema import sdk_representation as converter
from google.cloud.bigquery import SchemaField

schema_in = [
    SchemaField('att_01', 'INTEGER', 'NULLABLE', 'Att 1', ()),
    SchemaField('att_02', 'NUMERIC', 'REQUIRED', None, ()),
]

schema_out = converter(schema_in)
print(schema_out)
```

Output:

```bash
{'$schema': 'http://json-schema.org/draft-07/schema#', 'type': 'array', 'items': {'$ref': '#/definitions/element'}, 'definitions': {'element': {'type': 'object', 'properties': {'att_01': {
'type': 'integer', 'description': 'Att 1'}, 'att_02': {'type': 'number'}}, 'additionalProperties': False, 'required': ['att_02']}}}
```
