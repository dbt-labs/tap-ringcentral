#!/usr/bin/env python3

import singer

import tap_framework
import argparse
import json

from tap_ringcentral.client import RingCentralClient
from tap_ringcentral.streams import AVAILABLE_STREAMS

LOGGER = singer.get_logger()  # noqa


class RingCentralRunner(tap_framework.Runner):
    pass

@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(required_config_keys=[
        'client_id',
        'client_secret',
        'username',
        'password',
        'api_url',
        'start_date'
    ])

    client = RingCentralClient(args.config)

    runner = RingCentralRunner(
        args, client, AVAILABLE_STREAMS)

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == '__main__':
    main()
