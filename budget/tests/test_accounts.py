import pytest

from budget.accounts import PlaidAccount


def test__plaid_account(plaid_accounts_json):
    account = PlaidAccount(plaid_accounts_json[0])
    assert account.id == '1234'
    assert account.mask == '7001'
    assert account.name == 'My Chk 1'
    assert account.type == 'checking'
    assert account._available_balance == 1600
    assert account._current_balance == 1600


def test__plaid_account__balance_when_available_and_current_is_the_same(plaid_accounts_json):
    account = PlaidAccount(plaid_accounts_json[0])
    assert account.balance == '$1600'


@pytest.mark.parametrize('account_type', ['credit card', 'brokerage', 'ira'])
def test__plaid_account__balance__when_account_is_of_different_type(account_type, plaid_accounts_json):
    account_json = plaid_accounts_json[1]
    account_json['subtype'] = account_type
    account = PlaidAccount(account_json)
    assert account.balance == '$2174'


def test__plaid_account__balance(plaid_accounts_json):
    account = PlaidAccount(plaid_accounts_json[1])
    assert account.balance == '$897 -> $2174'
