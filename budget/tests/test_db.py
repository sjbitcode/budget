def test__get_accounts():
    from budget import db
    accounts = db.get_accounts()
    assert accounts[0] == {'_name': 'Account 1', 'account_id': 'ab12', 'sheet_cell': 'B4'}
    assert accounts[1] == {'_name': 'Account 2', 'account_id': 'cd34', 'sheet_cell': 'F4'}
    assert accounts[2] == {'_name': 'Account 3', 'account_id': 'ef56', 'sheet_cell': 'D4'}


def test__get_account_ids():
    from budget import db
    account_ids = db.get_account_ids()
    assert account_ids == ['ab12', 'cd34', 'ef56']


def test__get_access_tokens():
    from budget import db
    access_tokens = db.get_access_tokens()
    assert access_tokens == ['access-token-123', 'access-token-456']


def test__get_sheet_cell():
    from budget import db
    assert db.get_account_cell('ab12') == 'B4'
