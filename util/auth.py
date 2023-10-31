import httpx

from settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET

headers = {
    'Accept': 'application/json'
}


async def get_github_user(access_token: str):
    async with httpx.AsyncClient() as client:
        headers.update({"Authorization": f'Bearer {access_token}'})
        response = await client.get(url=f'https://api.github.com/user', headers=headers)
    return response.json()


async def get_github_access_token(code: str):
    params = {
        'client_id': OAUTH_CLIENT_ID,
        'client_secret': OAUTH_CLIENT_SECRET,
        'code': code
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=f'https://github.com/login/oauth/access_token', params=params, headers=headers)
    response_json = response.json()
    #  {'access_token': '', 'token_type': 'bearer', 'scope': ''}
    access_token = response_json["access_token"]
    return access_token
