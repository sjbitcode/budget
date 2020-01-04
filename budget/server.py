import threading
import time

import requests
import schedule
from fastapi import FastAPI
from plaid import Client

from . import accounts, db, settings

scheduler_running = None

# -------------------------------------------------------------------
# -------------------------------------------------------------------


# Init Plaid client.
client = Client(
    client_id=settings.PLAID_CLIENT_ID,
    secret=settings.PLAID_SECRET,
    public_key=settings.PLAID_PUBLIC_KEY,
    environment=settings.PLAID_ENVIRONMENT,
)

app = FastAPI()


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
    account_results = accounts.get_account_balances(client, tokens)
    print('~ got account result', account_results)

    print('~ updating spreadsheet')
    result = update_google_spreadsheet(account_results)
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
