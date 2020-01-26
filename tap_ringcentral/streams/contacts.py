from tap_ringcentral.streams.base import BaseStream
import tap_ringcentral.cache

import singer
import json

LOGGER = singer.get_logger()  # noqa


class ContactsStream(BaseStream):
    NAME = 'ContactsStream'
    KEY_PROPERTIES = ['id']
    API_METHOD = 'GET'
    TABLE = 'contacts'

    @property
    def api_path(self):
        return '/restapi/v1.0/account/~/directory/entries'

    def get_stream_data(self, result):
        contacts = [
            self.transform_record(record)
            for record in result['records']
        ]

        tap_ringcentral.cache.contacts.extend(contacts)
        return contacts
