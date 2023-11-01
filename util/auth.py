import httpx
from fastapi import Request, HTTPException
from settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET

headers = {
    'Accept': 'application/json'
}


async def validate_bearer(request: Request):
    # APIKeyHeader should be requiring this header to be present to reach this func
    auth = request.headers["authorization"]
    user = await get_github_user(auth)
    return user


async def get_github_user(access_token: str):
    async with httpx.AsyncClient() as client:
        headers.update({"Authorization": f'Bearer {access_token}'})
        response = await client.get(url=f'https://api.github.com/user', headers=headers)
        if response.status_code > 400:
            raise HTTPException(status_code=401, detail="Not authorized")
        if response.status_code != 200:
            raise Exception()
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
