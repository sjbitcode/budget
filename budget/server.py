import logging

import schedule
from fastapi import FastAPI
from plaid import Client
from sheetfu import SpreadsheetApp

from . import accounts, db, events, settings, sheets


logger = logging.getLogger(__name__)
logging.getLogger('googleapiclient.discovery').setLevel(logging.WARNING)
logging.getLogger('oauth2client.client').setLevel(logging.WARNING)
logging.getLogger('oauth2client.transport').setLevel(logging.WARNING)

# Init Plaid client.
client = Client(client_id=settings.PLAID_CLIENT_ID,
                secret=settings.PLAID_SECRET,
                public_key=settings.PLAID_PUBLIC_KEY,
                environment=settings.PLAID_ENVIRONMENT)

# Init Sheetfu client and get spreadsheet.
sheet = (SpreadsheetApp(settings.SPREADSHEET_CREDS)
         .open_by_id(spreadsheet_id=settings.SPREADSHEET_ID)
         .get_sheet_by_name(settings.SHEET_NAME))

app = FastAPI()


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
    result = sheets.update_google_spreadsheet(sheet, account_results)
    logger.info(f'~ spreadsheet updated { result}')


# ---


@app.on_event('startup')
def startup():
    logger.info('~ setting up jobs')
    events.setup_scheduler()
    schedule.every(int(settings.UPDATE_INTERVAL)).minutes.do(update)


@app.on_event('shutdown')
def shutdown():
    logger.info('~ tearing down jobs')
    events.teardown_scheduler()


@app.get('/')
def index():
    return {'app': 'Budget API'}
