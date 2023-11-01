from typing import Any

import httpx
from fastapi import APIRouter, Depends, Security, Request, Response
from fastapi.security import APIKeyHeader
from starlette.responses import RedirectResponse

from models.errors import UnAuthorizedError
from models.healthcheck import Check
from settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
from util.auth import get_github_access_token, get_github_user, validate_bearer

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/login")
async def github_auth():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={OAUTH_CLIENT_ID}', status_code=302)


@router.get("/callback", include_in_schema=False)
async def github_callback(code: str):
    access_token = await get_github_access_token(code)
    access_token = access_token
    print(access_token)
    user = await get_github_user(access_token)
    # persist user to db? return bearer access token
    return user

bearer_header = APIKeyHeader(name="Authorization")


# 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
@router.get("/test")
async def test_auth(bearer: str = Security(bearer_header), oauth_user_json=Depends(validate_bearer)):
    return bearer

