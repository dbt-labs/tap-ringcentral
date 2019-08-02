from tap_ringcentral.streams.base import ContactBaseStream
from tap_ringcentral.state import incorporate

import singer
import json

LOGGER = singer.get_logger()  # noqa


class CompanyCallLogStream(ContactBaseStream):
    NAME = 'CompanyCallLogStream'
    KEY_PROPERTIES = ['id']
    API_METHOD = 'GET'
    TABLE = 'company_call_log'

    @property
    def api_path(self):
        return '/restapi/v1.0/account/~/call-log'

    def sync_data_for_period(self, date, interval):
        self.sync_data_for_extension(date, interval, None)
        self.state = incorporate(self.state, self.TABLE, 'last_record', date.isoformat())
        return self.state
