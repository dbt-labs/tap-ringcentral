# tap-ringcentral

Author: Drew Banin (drew@fishtownanalytics.com)

This is a [Singer](http://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

It:

- Generates a catalog of available data in the Amazon Advertising API
- Extracts the following resources:
    - [Contacts](https://developers.ringcentral.com/api-reference#Company-Contacts-listDirectoryEntries)
    - [Call Logs](https://developers.ringcentral.com/api-reference#Call-Log-loadUserCallLog)
    - [SMS/MMS/Voicemal/Fax](https://developers.ringcentral.com/api-reference#SMS-and-MMS-listMessages)
    - [Meetings](https://developers.ringcentral.com/api-reference#Upcoming-Meetings)

### Quick Start

1. Install

```bash
git clone git@github.com:fishtown-analytics/tap-ringcentral.git
cd tap-ringcentral
pip install .
```

2. Get credentials from RingCentral

- Create a new app and an associated sandbox account
- Note your `client_id`, `client_secret`, `username`, and `password` (used in the config.json file specified below)

3. Create the config file.

There is a template you can use at `config.json.example`, just copy it to `config.json` in the repo root and insert your credentials. You
will initially need to use the sandbox `api_url` (eg. `platform.devtest.ringcentral.com`), but after graduating from the dev requirements,
you will be able to switch this to use the production API endpoints.

4. Run the application to generate a catalog.

```bash
tap-ringcentral -c config.json --discover > catalog.json
```

5. Select the tables you'd like to replicate

Step 4 a file called `catalog.json` that specifies all the available endpoints and fields. You'll need to open the file and select the ones you'd like to replicate. See the [Singer guide on Catalog Format](https://github.com/singer-io/getting-started/blob/c3de2a10e10164689ddd6f24fee7289184682c1f/BEST_PRACTICES.md#catalog-format) for more information on how tables are selected.

6. Run it!

```bash
tap-ringcentral -c config.json --properties catalog.json
```

Copyright &copy; 2019 Fishtown Analytics
