from singer.catalog import Catalog, CatalogEntry, Schema

from tap_auth0_logs_checkpoint.schema import get_schemas, STREAMS


def discover():
    schemas, schemas_metadata = get_schemas()

    streams = []
    for schema_name, schema_dict in schemas.items():
        schema = Schema.from_dict(schema_dict)
        schema_meta = schemas_metadata[schema_name]

        streams.append(
            CatalogEntry(
                tap_stream_id=schema_name,
                stream=schema_name,
                schema=schema,
                key_properties=STREAMS[schema_name]['key_properties'],
                metadata=schema_meta,
            )
        )
    return Catalog(streams)
