import concurrent.futures

from plaid.errors import PlaidError


class PlaidAccount:
    """
    This class represents a Plaid Account object,
    returned from the `/accounts/balance/get` endpoint.
    """
    def __init__(self, data={}):
        self.id = data.get('account_id', 'abcd')
        self.mask = data.get('mask', '0000')
        self.name = data.get('name', 'Unnamed Acc')
        self.type = data.get('subtype', '')
        self._available_balance = data.get('balances', {}).get('available', '0.00')
        self._current_balance = data.get('balances', {}).get('current', '0.00')

    @property
    def balance(self):
        """
        Current balance is the balance in an account with all transactions taken into account.
        Available balance is the balance in an account that can be withdrawn at the moment.
        """
        if self._available_balance == self._current_balance:
            return f'${self._available_balance}'

        if self.type in ['credit card', 'brokerage']:
            return f'${self._current_balance}'

        return f'${self._available_balance} -> ${self._current_balance}'

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.mask} - {self.name}>'


def get_balance_info(client, access_token):
    """
    Get all account balance info from Plaid client.
    """
    print(f'~ getting balance info: {access_token}')
    try:
        balance_response = client.Accounts.balance.get(access_token)
        accounts = {
            acc.id: acc
            for acc in map(lambda item: PlaidAccount(item), balance_response['accounts'])
        }
        return accounts
    except PlaidError as e:
        print(e)
        return None


def get_account_balances(client, access_tokens):
    accounts = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = [(client, token) for token in access_tokens]
        results = executor.map(lambda p: get_balance_info(*p), args)
        for result in results:
            accounts.update(result)
    return accounts
