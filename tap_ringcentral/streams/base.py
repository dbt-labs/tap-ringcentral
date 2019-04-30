import math
import pytz
import singer
import singer.utils
import singer.metrics

from datetime import timedelta, datetime

import tap_ringcentral.cache
from tap_ringcentral.config import get_config_start_date
from tap_ringcentral.state import incorporate, save_state, \
    get_last_record_value_for_table

from tap_framework.streams import BaseStream as base

LOGGER = singer.get_logger()


class BaseStream(base):
    KEY_PROPERTIES = ['id']

    def get_params(self, page=1):
        return {
            "page": page,
            "per_page": 1000
        }

    def get_body(self):
        return {}

    def get_url(self, path):
        return '{}{}'.format(BASE_URL, path)

    def sync_data(self):
        table = self.TABLE
        page = 1

        LOGGER.info('Syncing data for entity {} (page={})'.format(table, page))

        url = "{}{}".format(self.client.base_url, self.api_path)

        while True:
            params = self.get_params(page=page)
            body = self.get_body()

            result = self.client.make_request(
                url, self.API_METHOD, params=params, body=body)

            data = self.get_stream_data(result)

            with singer.metrics.record_counter(endpoint=table) as counter:
                for obj in data:
                    singer.write_records(
                        table,
                        [obj])

                    counter.increment()

            paging = result['paging']
            if page >= paging['totalPages']:
                break
            page += 1

        return self.state

class ContactBaseStream(BaseStream):
    KEY_PROPERTIES = ['id']

    def sync_data(self):
        table = self.TABLE
        LOGGER.info('Syncing data for entity {}'.format(table))

        date = get_last_record_value_for_table(self.state, table)

        if date is None:
            date = get_config_start_date(self.config)

        interval = timedelta(days=7)

        while date < datetime.now(pytz.utc):
            self.sync_data_for_period(date, interval)

            date = date + interval

        return self.state

    def sync_data_for_period(self, date, interval):
        for extension in tap_ringcentral.cache.contacts:
            extensionId = extension['id']
            self.sync_data_for_extension(date, interval, extensionId)

        return self.state

    def get_params(self, date_from, date_to, page):
        return {
            "page": page,
            "dateFrom": date_from,
            "dateTo": date_to,
            "showDeleted": True,
        }

    def sync_data_for_extension(self, date, interval, extensionId):
        table = self.TABLE
        page = 1

        date_from = date.isoformat()
        date_to = (date + interval).isoformat()

        while True:
            LOGGER.info('Syncing {}s for contact={} from {} to {}, page={}'.format(
                table,
                extensionId,
                date_from,
                date_to,
                page
            ))

            params = self.get_params(date_from, date_to, page)
            body = self.get_body()

            url = "{}{}".format(
                self.client.base_url,
                self.api_path.format(extensionId=extensionId)
            )

            result = self.client.make_request(
                url, self.API_METHOD, params=params, body=body)

            data = self.get_stream_data(result)

            if len(data) == 0:
                break

            with singer.metrics.record_counter(endpoint=table) as counter:
                for obj in data:
                    singer.write_records(
                        table,
                        [obj])

                    counter.increment()

            page += 1
