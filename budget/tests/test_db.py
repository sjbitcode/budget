def test__get_accounts():
    from budget import db
    accounts = db.get_accounts()
    assert accounts[0] == {'_name': 'Some Acc 123', 'account_id': '1234', 'sheet_cell': 'A1'}
    assert accounts[1] == {'_name': 'Some Acc 234', 'account_id': '2345', 'sheet_cell': 'A2'}
    assert accounts[2] == {'_name': 'Some Acc 345', 'account_id': '3456', 'sheet_cell': 'A3'}


def test__get_account_ids():
    from budget import db
    account_ids = db.get_account_ids()
    assert account_ids == ['1234', '2345', '3456']


def test__get_access_tokens():
    from budget import db
    access_tokens = db.get_access_tokens()
    assert access_tokens == ['access-development-abc', 'access-development-def']


def test__get_sheet_cell():
    from budget import db
    assert db.get_account_cell('1234') == 'A1'
