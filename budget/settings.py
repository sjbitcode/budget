import os

# Plaid settings.
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENVIRONMENT = os.getenv('PLAID_ENVIRONMENT')

# Spreadsheet settings
SPREADSHEET_CREDS = os.getenv('SPREADSHEET_CREDS')  # creds.json
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_NAME = os.getenv('SHEET_NAME')

# Update interval
UPDATE_INTERVAL = os.getenv('UPDATE_INTERVAL')

DATA_PATH = os.getenv('DATA_PATH')  # accounts_data.json
