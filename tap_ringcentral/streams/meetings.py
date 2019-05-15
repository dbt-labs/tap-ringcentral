from tap_ringcentral.streams.base import ContactBaseStream

import singer
import json

LOGGER = singer.get_logger()  # noqa


class MeetingStream(ContactBaseStream):
    KEY_PROPERTIES = ['id']
    API_METHOD = 'GET'
    TABLE = 'meetings'

    @property
    def api_path(self):
        return '/restapi/v1.0/account/~/extension/{extensionId}/meeting'
