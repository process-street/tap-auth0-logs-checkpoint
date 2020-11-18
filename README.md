# tap-auth0-logs-checkpoint

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [Auth0](http://auth0.com)
- Extracts the following resources:
  - [Logs](https://auth0.com/docs/api/management/v2/#!/Logs/get_logs)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

---

Copyright &copy; 2020 Process Street
