import json
import os
import time

import pytest


@pytest.fixture(autouse=True)
def test_envs(monkeypatch):
    data = {
        "access-token-123": {
            "accounts": [{
                    "_name": "Account 1",
                    "account_id": "ab12",
                    "sheet_cell": "B4"
                },
                {
                    "_name": "Account 2",
                    "account_id": "cd34",
                    "sheet_cell": "F4"
                }
            ]
        },
        "access-token-456": {
            "accounts": [{
                "_name": "Account 3",
                "account_id": "ef56",
                "sheet_cell": "D4"
            }]
        }
    }

    filename = f'/tmp/{time.time()}'

    with open(filename, 'w') as fp:
        json.dump(data, fp)

    monkeypatch.setenv('DATA_PATH', filename)
    yield

    os.remove(filename)


@pytest.fixture
def plaid_accounts_json():
    return [{
        'account_id': '1234',
        'balances': {
            'available': 1600,
            'current': 1600,
            'limit': None
        },
        'mask': '7001',
        'name': 'My Chk 1',
        'official_name': 'Personal Checking 1',
        'subtype': 'checking',
        'type': 'depository'
    }, {
        'account_id': '2345',
        'balances': {
            'available': 897,
            'current': 2174,
            'limit': None
        },
        'mask': '8234',
        'name': 'Misc expenses',
        'official_name': 'Personal Checking 2',
        'subtype': 'checking',
        'type': 'depository'
    }]
