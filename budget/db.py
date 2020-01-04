import json

from . import settings


def _read_config_from_file():
    with open(settings.DATA_PATH, 'r') as fp:
        return json.load(fp)


_data = _read_config_from_file()


def get_accounts(access_token):
    return _data[access_token]


def get_account_masks(access_token):
    accounts = get_accounts(access_token)
    return [account['mask'] for account in accounts]


def get_access_tokens():
    return _data.keys()
