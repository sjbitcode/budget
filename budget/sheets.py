import datetime
import logging

from . import db


logger = logging.getLogger(__name__)


def update_sheet_cell(sheet, cell, value):
    """
    Update a single cell with a value in sheet.
    """
    data_range = sheet.get_range_from_a1(f'{cell}:{cell}')
    data_range.set_value(value)


def update_google_spreadsheet(sheet, account_results):
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
        update_sheet_cell(sheet, cell, account.balance)

    # update last update
    now = datetime.datetime.now().strftime('%B %d %Y - %I:%M:%S %p')
    logger.info(f'~ updating last updated time to {now}')
    update_sheet_cell(sheet, 'F4', now)
