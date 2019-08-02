#!/usr/bin/env python3

import singer

import tap_framework
from tap_framework.state import save_state
import argparse
import json

from tap_ringcentral.client import RingCentralClient
from tap_ringcentral.streams import AVAILABLE_STREAMS

LOGGER = singer.get_logger()  # noqa


class RingCentralRunner(tap_framework.Runner):
    # Sync the streams in the order specified in the
    # streams/__init__.py list of AVAILABLE_STREAMS
    def do_sync(self):
        LOGGER.info("Starting sync.")

        streams = self.get_streams_to_replicate()
        stream_map = {s.NAME: s for s in streams}

        for available_stream in AVAILABLE_STREAMS:
            if available_stream.NAME not in stream_map:
                continue

            stream = stream_map[available_stream.NAME]
            try:
                stream.state = self.state
                stream.sync()
                self.state = stream.state
            except OSError as e:
                LOGGER.error(str(e))
                exit(e.errno)

            except Exception as e:
                LOGGER.error(str(e))
                LOGGER.error('Failed to sync endpoint {}, moving on!'
                             .format(stream.TABLE))
                raise e

        save_state(self.state)


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
