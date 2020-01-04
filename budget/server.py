import concurrent.futures
import threading
import time

import requests
import schedule
from fastapi import FastAPI
from plaid import Client
from plaid.errors import PlaidError

from . import db, settings

scheduler_running = None

# -------------------------------------------------------------------


class PlaidAccount:
    """
    This class represents a Plaid Account object,
    returned from the `/accounts/balance/get` endpoint.
    """
    def __init__(self, data={}):
        self.mask = data.get('mask', '0000')
        self.name = data.get('name', 'Unnamed Acc')
        self.account_type = data.get('subtype', '')
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

        if self.account_type in ['credit card', 'brokerage']:
            return f'${self.current_balance}'

        return f'${self._available_balance} -> (${self._current_balance})'

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.mask} - {self.name}>'

# -------------------------------------------------------------------


# Init Plaid client.
client = Client(
    client_id=settings.PLAID_CLIENT_ID,
    secret=settings.PLAID_SECRET,
    public_key=settings.PLAID_PUBLIC_KEY,
    environment=settings.PLAID_ENVIRONMENT,
)

app = FastAPI()


def get_balance_info(access_token):
    """
    Get all account balance info from Plaid client.
    """
    print(f'~ getting balance info: {access_token}')
    try:
        balance_response = client.Accounts.balance.get(access_token)
        accounts = {
            acc.mask: acc
            for acc in map(lambda item: PlaidAccount(item), balance_response['accounts'])
        }
        return accounts
    except PlaidError as e:
        print(e)
        return None


def simple_get_balance_info(access_token):
    """
    Get all account balance info from Plaid client.
    """
    print(f'~ getting balance info: {access_token}')
    response = requests.get('https://httpbin.org/uuid')
    uuid = response.json()['uuid']
    return uuid
    # return Account({'name': f'Account {uuid[:7]}'})


def update_google_spreadsheet(some_token):
    import time
    print('~ update_google_spreadsheet')
    requests.get('https://httpbin.org/delay/2')
    return str(time.time())


def update():
    """
    This function updates the app's data by doing the following:
      - Get all account balances.
      - Push account data to google spreadsheet.
    """
    print('~ getting account results')

    tokens = db.get_access_tokens()
    accounts = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(get_balance_info, tokens)
        accounts = list(results)

    print('~ got account result', accounts)
    print('~ updating spreadsheet')
    result = update_google_spreadsheet(accounts)
    print('~ spreadsheet updated', result)


# ---


def setup_scheduler():
    global scheduler_running

    def run_continuously():
        while scheduler_running:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=run_continuously)
    thread.daemon = True
    print('~ starting continuous thread')
    scheduler_running = True
    thread.start()


def teardown_scheduler():
    global scheduler_running
    scheduler_running = False


@app.on_event('startup')
def startup():
    print('~ setting up jobs')
    setup_scheduler()
    schedule.every(2).minutes.do(update)
    # update()


@app.on_event('shutdown')
def shutdown():
    print('~ tearing down jobs')
    teardown_scheduler()


@app.get('/')
def index():
    return {'app': 'Budget API'}


# Run the server with:
#    uvicorn server:app --reload
