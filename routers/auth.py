import httpx
from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse
from settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
from util.auth import get_github_access_token, get_github_user

router = APIRouter(prefix="/auth", tags=["system"])


@router.get("/login")
async def github_auth():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={OAUTH_CLIENT_ID}', status_code=302)


@router.get("/callback")
async def github_callback(code: str):
    access_token = await get_github_access_token(code)
    user = await get_github_user(access_token)
    # persist user to db? return bearer access token
    return user
