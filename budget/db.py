import json

from . import settings


def _read_config_from_file():
    print(settings.DATA_PATH)
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


def get_account_cell(account_id):
    for account in get_accounts():
        if account['account_id'] == account_id:
            return account['sheet_cell']
