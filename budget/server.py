import datetime
import threading
import time

from fastapi import FastAPI
from plaid import Client
import requests
import schedule
from sheetfu import SpreadsheetApp

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

# Init Sheetfu client and get spreadsheet.
sheetfu_client = SpreadsheetApp(settings.SPREADSHEET_CREDS)
spreadsheet = sheetfu_client.open_by_id(spreadsheet_id=settings.SPREADSHEET_ID)
sheet = spreadsheet.get_sheet_by_name(settings.SHEET_NAME)

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


def update_sheet_cell(sheet, cell, value):
    """
    Update a single cell with a value in sheet.
    """
    data_range = sheet.get_range_from_a1(f'{cell}:{cell}')
    data_range.set_value(value)


def update_google_spreadsheet(account_results, sheet):
    print('~ update_google_spreadsheet')

    # filter the account_results
    account_ids = db.get_account_ids()
    accounts_to_update = {
        account_id: account_results[account_id]
        for account_id in account_ids
    }
    # update balance in cells
    for account in accounts_to_update.values():
        cell = db.get_account_cell(account.id)
        update_sheet_cell(sheet, cell, account.balance)

    # update last update
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
    update_sheet_cell(sheet, 'F4', now)


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
    result = update_google_spreadsheet(account_results, sheet)
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
    schedule.every(int(settings.UPDATE_INTERVAL)).minutes.do(update)
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
