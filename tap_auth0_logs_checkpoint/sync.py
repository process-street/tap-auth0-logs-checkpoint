import singer

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

LOGGER = singer.get_logger()


def get_auth0_client(config):
    get_token = GetToken(config['domain'])
    token = get_token.client_credentials(config['non_interactive_client_id'],
                                         config['non_interactive_client_secret'],
                                         'https://{}/api/v2/'.format(config['domain']))
    mgmt_api_token = token['access_token']
    return Auth0(config['domain'], mgmt_api_token)


def sync(config, state, catalog):
    for stream in catalog.get_selected_streams(state):
        tap_stream_id = stream.tap_stream_id
        LOGGER.info("Syncing stream:" + tap_stream_id)

        singer.write_schema(
            stream_name=tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        params = {
            'take': config['per_page'],
            'from_param': singer.get_bookmark(state, tap_stream_id, 'last_log_id')
        }

        auth0 = get_auth0_client(config)

        with singer.metrics.record_counter(tap_stream_id) as counter:
            while True:
                LOGGER.info("SEARCH request with {params}".format(params=params))
                results = auth0.logs.search(**params)

                LOGGER.info('Found {} results'.format(len(results)))
                if len(results) == 0:
                    return

                max_bookmark = 0
                for item in results:
                    singer.write_records(tap_stream_id, [item])

                    max_bookmark = max(max_bookmark, int(item['log_id']))
                    counter.increment()

                state = singer.write_bookmark(state, tap_stream_id, 'last_log_id', max_bookmark)
                singer.write_state(state)

                if counter.value > 40000:
                    return

                params = {
                    'take': config['per_page'],
                    'from_param': max_bookmark
                }

    return
