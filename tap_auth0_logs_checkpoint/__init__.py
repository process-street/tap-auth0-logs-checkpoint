#!/usr/bin/env python3
import singer
from singer import utils

from tap_auth0_logs_checkpoint.discover import discover
from tap_auth0_logs_checkpoint.schema import get_schemas, STREAMS
from tap_auth0_logs_checkpoint.sync import sync

DEFAULT_PER_PAGE = 100

REQUIRED_CONFIG_KEYS = [
    "domain",
    "non_interactive_client_id",
    "non_interactive_client_secret",
]
LOGGER = singer.get_logger()


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    config = {
        "domain": None,
        "non_interactive_client_id": None,
        "non_interactive_client_secret": None,
        "per_page": DEFAULT_PER_PAGE,
    }

    config.update(args.config)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()
        sync(config, args.state, catalog)


if __name__ == "__main__":
    main()
