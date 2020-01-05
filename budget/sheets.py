from sheetfu import SpreadsheetApp

from . import settings


# Init Sheetfu client and get spreadsheet.
sheetfu_client = SpreadsheetApp(settings.SPREADSHEET_CREDS)
spreadsheet = sheetfu_client.open_by_id(spreadsheet_id=settings.SPREADSHEET_ID)
sheet = spreadsheet.get_sheet_by_name(settings.SHEET_NAME)


def update_sheet_cell(sheet, cell, value):
    """
    Update a single cell with a value in sheet.
    """
    data_range = sheet.get_range_from_a1(f'{cell}:{cell}')
    data_range.set_value(value)
