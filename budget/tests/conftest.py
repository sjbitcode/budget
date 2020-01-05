import pytest


@pytest.fixture
def test_envs(monkeypatch):
    monkeypatch.setenv('DATA_PATH', 'accounts_data.example.json')


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
