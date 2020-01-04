import json

from . import settings


def _read_config_from_file():
    with open(settings.DATA_PATH, 'r') as fp:
        return json.load(fp)


_data = _read_config_from_file()


def get_accounts():
    """
    Get all account objects from all institutions.
    """
    accounts = []
    for institution in _data.values():
        accounts.extend(institution['accounts'])
    return accounts


def get_account_ids():
    accounts = get_accounts()
    return [account['account_id'] for account in accounts]


def get_access_tokens():
    return list(_data.keys())
