from tap_ringcentral.streams.base import ContactBaseStream

import singer
import json

LOGGER = singer.get_logger()  # noqa


class CallLogStream(ContactBaseStream):
    KEY_PROPERTIES = ['id']
    API_METHOD = 'GET'
    TABLE = 'call_log'

    @property
    def api_path(self):
        return '/restapi/v1.0/account/~/extension/{extensionId}/call-log'

    def get_stream_data(self, result):
        return [
            self.transform_record(record)
            for record in result['records']
        ]
