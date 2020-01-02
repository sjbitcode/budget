import os

from fastapi import FastAPI
from plaid import Client
from plaid.errors import PlaidError

# Plaid settings.
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENVIRONMENT = os.getenv('PLAID_ENVIRONMENT')
# Access tokens for all accounts linked in Plaid.
PLAID_LINKED_ACCOUNTS = os.getenv('PLAID_LINKED_ACCOUNTS', '').split(',')


# -------------------------------------------------------------------

class PlaidAccount:
    """
    This class represents a Plaid Account object,
    returned from the `/accounts/balance/get` endpoint.
    """
    def __init__(self, data={}):
        self.mask = data.get('mask', '0000')
        self.name = data.get('name', 'Unnamed Acc')
        self.available_balance = data.get('balances', {}).get('available', '0.00')
        self.current_balance = data.get('balances', {}).get('current', '0.00')

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.mask} - {self.name}>'

# -------------------------------------------------------------------


# Init Plaid client.
client = Client(
    client_id=PLAID_CLIENT_ID,
    secret=PLAID_SECRET,
    public_key=PLAID_PUBLIC_KEY,
    environment=PLAID_ENVIRONMENT,
)

app = FastAPI()


def get_balance_info(client):
    """
    Get all account balance info from Plaid client.
    """
    try:
        balance_response = client.Accounts.balance.get()
        accounts = {
            acc.mask: acc
            for acc in map(lambda item: PlaidAccount(item), balance_response['accounts'])
        }
        return accounts
    except PlaidError as e:
        print(e)
        return None


@app.get('/')
async def index():
    return {'app': 'Budget API'}


# Run the server with:
#    uvicorn server:app --reload
