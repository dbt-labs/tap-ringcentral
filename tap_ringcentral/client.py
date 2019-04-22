import requests
import base64
import backoff

import singer
import singer.metrics

LOGGER = singer.get_logger()  # noqa


class RateLimitException(Exception):
    pass


class RingCentralClient:

    MAX_TRIES = 5

    def __init__(self, config):
        self.config = config
        self.base_url = self.config.get('api_url')

        self.refresh_token, self.access_token = self.get_authorization()

    def get_authorization(self):
        client_id = self.config.get('client_id')
        client_secret = self.config.get('client_secret')
        basic_auth = base64.b64encode("{}:{}".format(client_id, client_secret).encode())

        body = {
            'username': self.config.get('username'),
            'password': self.config.get('password'),
            'grant_type': 'password'
        }

        headers = {
            'Authorization': 'Basic {}'.format(basic_auth.decode()),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request(
            'POST',
            '{}/restapi/oauth/token'.format(self.base_url),
            headers=headers,
            data=body)

        response.raise_for_status()
        json = response.json()
        return json['refresh_token'], json['access_token']

    @backoff.on_exception(backoff.expo,
                          RateLimitException,
                          max_tries=MAX_TRIES)
    def make_request(self, url, method, params=None, body=None):
        LOGGER.info("Making {} request to {} ({})".format(method, url, params))

        response = requests.request(
            method,
            url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.access_token),
                'User-Agent': self.config.get('user_agent', 'tap-ringcentral')
            },
            params=params,
            json=body)

        LOGGER.info("Got status code {}".format(response.status_code))

        if response.status_code == 429:
            LOGGER.info("Rate limit status code received, waiting")
            raise RateLimitException()

        elif response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()
