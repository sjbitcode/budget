from plaid import Client
from sheetfu import SpreadsheetApp

from budget import db, accounts, settings


# Init Plaid client.
client = Client(
    client_id=settings.PLAID_CLIENT_ID,
    secret=settings.PLAID_SECRET,
    public_key=settings.PLAID_PUBLIC_KEY,
    environment=settings.PLAID_ENVIRONMENT,
)

tokens = db.get_access_tokens()
account_results = accounts.get_account_balances(client, tokens)
account_ids = db.get_account_ids()

# filter the account_results
accounts_to_update = {account_id: account_results[account_id] for account_id in account_ids}

# filter
account_id_cell_mapping = {account['account_id']: account['sheet_cell'] for account in db.get_accounts()}

# Sheetfu stuff
sheetfu_client = SpreadsheetApp(settings.SPREADSHEET_CREDS)
spreadsheet = sheetfu_client.open_by_id(spreadsheet_id=settings.SPREADSHEET_ID)
sheet1 = spreadsheet.get_sheet_by_name(settings.SHEET_NAME)

data_range = sheet1.get_data_range()
values = data_range.get_values()
