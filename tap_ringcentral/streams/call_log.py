from tap_ringcentral.streams.base import ContactBaseStream

import singer
import json

LOGGER = singer.get_logger()  # noqa


class CallLogStream(ContactBaseStream):
    NAME = 'CallLogStream'
    KEY_PROPERTIES = ['id']
    API_METHOD = 'GET'
    TABLE = 'call_log'

    @property
    def api_path(self):
        return '/restapi/v1.0/account/~/extension/{extensionId}/call-log'
