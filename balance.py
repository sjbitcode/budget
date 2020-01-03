import asyncio

import aiohttp

PLAID_CLIENT_ID = '123'
PLAID_SECRET = '456'
PLAID_PUBLIC_KEY = '789'
PLAID_ENVIRONMENT = 'development'


async def get_balance(access_token):
    print(f'~ getting balance for {access_token.split("-")[-1]}')
    url = f'https://{PLAID_ENVIRONMENT}.plaid.com/accounts/balance/get'
    data = {
        'client_id': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
        'access_token': access_token,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response_json = await response.json()

            if 400 <= response.status < 600:
                print(f'Error: {response.reason} for url {response.url}, {response_json}')
                return None

            return response_json


async def update():
    balances = await asyncio.gather(
        get_balance('access-development-abc'),
        get_balance('access-development-def')
    )
    print(balances)


loop = asyncio.get_event_loop()
loop.run_until_complete(update())
