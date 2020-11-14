import os
import json
from singer import metadata

STREAMS = {
    'logs': {
        'key_properties': ['log_id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['log_id']
    }
}


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def get_schemas():
    schemas = {}
    schemas_metadata = {}

    for stream_name, stream_metadata in STREAMS.items():
        schema_path = get_abs_path('schemas/{}.json'.format(stream_name))

        with open(schema_path) as file:
            schema = json.load(file)

        meta = metadata.get_standard_metadata(
            schema=schema,
            schema_name=stream_name,
            key_properties=stream_metadata.get('key_properties', None),
            valid_replication_keys=stream_metadata.get('replication_keys', None),
            replication_method=stream_metadata.get('replication_method', None)
        )

        schemas[stream_name] = schema
        schemas_metadata[stream_name] = meta

    return schemas, schemas_metadata
