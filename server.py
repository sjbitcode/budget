import asyncio
import os

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
# from plaid import Client
# from plaid.errors import PlaidError
# import requests

# Plaid settings.
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENVIRONMENT = os.getenv('PLAID_ENVIRONMENT')


# -------------------------------------------------------------------

class Account:
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


# # Init Plaid client.
# client = Client(
#     client_id=PLAID_CLIENT_ID,
#     secret=PLAID_SECRET,
#     public_key=PLAID_PUBLIC_KEY,
#     environment=PLAID_ENVIRONMENT,
# )

app = FastAPI()


# def original_get_balance_info(client, access_token):
#     """
#     Get all account balance info from Plaid client.
#     """
#     print('~ getting balance info')
#     try:
#         balance_response = client.Accounts.balance.get(access_token)
#         accounts = {
#             acc.mask: acc
#             for acc in map(lambda item: Account(item), balance_response['accounts'])
#         }
#         return accounts
#     except PlaidError as e:
#         print(e)
#         return None


# def get_balance_info(access_token):
#     """
#     Get all account balance info from Plaid client.
#     """
#     print(f'~ getting balance info: {access_token}')
#     response = requests.get('https://httpbin.org/uuid')
#     uuid = response.json()['uuid']
#     return uuid
#     # return Account({'name': f'Account {uuid[:7]}'})


async def aio_get_balance_info(access_token):
    print(f'~ getting balance info: {access_token}')
    await asyncio.sleep(2)
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/uuid') as response:
            response_json = await response.json()
            return {
                'status': response.status,
                'uuid': response_json['uuid'],
            }


def update_google_spreadsheet(some_token):
    import time
    print('~ update_google_spreadsheet')
    time.sleep(2)
    return str(time.time())


async def update():
    """
    This function updates the app's data by doing the following:
      - Get all account balances.
      - Push account data to google spreadsheet.
    """
    tasks = []
    for token in ['token-a', 'token-b', 'token-c', 'token-d']:
        tasks.append(aio_get_balance_info(token))

    print('~ tasks', tasks)
    account_results = await asyncio.gather(*tasks)
    print('~ got accounts', account_results)
    print('~ updating spreadsheet')
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, update_google_spreadsheet, 'some-token-123')
    print('~ spreadsheet updated', result)


@app.on_event('startup')
async def setup_jobs():
    print('~ setting up jobs')
    scheduler = AsyncIOScheduler()
    scheduler.start()
    # scheduler.add_job(get_balance_info, 'interval', [client, access_token], seconds=15)
    scheduler.add_job(update, 'interval', seconds=15)


@app.get('/')
async def index():
    return {'app': 'Budget API'}


# Run the server with:
#    uvicorn server:app --reload
