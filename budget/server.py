import datetime
import logging
import threading
import time

from fastapi import FastAPI
from plaid import Client
import schedule

from . import accounts, db, settings, sheets

logger = logging.getLogger(__name__)
scheduler_running = None

# Init Plaid client.
client = Client(
    client_id=settings.PLAID_CLIENT_ID,
    secret=settings.PLAID_SECRET,
    public_key=settings.PLAID_PUBLIC_KEY,
    environment=settings.PLAID_ENVIRONMENT,
)

# Sheetfu spreadsheet sheet.
sheet = sheets.sheet

app = FastAPI()


def update_google_spreadsheet(account_results, sheet):
    logger.info('~ update_google_spreadsheet')

    # filter the account_results
    account_ids = db.get_account_ids()
    accounts_to_update = {
        account_id: account_results[account_id]
        for account_id in account_ids
    }
    # update balance in cells
    for account in accounts_to_update.values():
        cell = db.get_account_cell(account.id)
        sheets.update_sheet_cell(sheet, cell, account.balance)

    # update last update
    now = datetime.datetime.now().strftime('%B %d %Y - %I:%M:%S %p')
    logger.info(f'~ updating last updated time to {now}')
    sheets.update_sheet_cell(sheet, 'F4', now)


def update():
    """
    This function updates the app's data by doing the following:
      - Get all account balances.
      - Push account data to google spreadsheet.
    """
    logger.info('~ getting account results')

    tokens = db.get_access_tokens()
    account_results = accounts.get_account_balances(client, tokens)
    logger.info(f'~ got account result {account_results}')

    logger.info('~ updating spreadsheet')
    result = update_google_spreadsheet(account_results, sheet)
    logger.info(f'~ spreadsheet updated { result}')


# ---


def setup_scheduler():
    global scheduler_running

    def run_continuously():
        while scheduler_running:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=run_continuously)
    thread.daemon = True
    logger.info('~ starting continuous thread')
    scheduler_running = True
    thread.start()


def teardown_scheduler():
    global scheduler_running
    scheduler_running = False


@app.on_event('startup')
def startup():
    logger.info('~ setting up jobs')
    setup_scheduler()
    schedule.every(int(settings.UPDATE_INTERVAL)).minutes.do(update)


@app.on_event('shutdown')
def shutdown():
    logger.info('~ tearing down jobs')
    teardown_scheduler()


@app.get('/')
def index():
    return {'app': 'Budget API'}


# Run the server with:
#    uvicorn server:app --reload
