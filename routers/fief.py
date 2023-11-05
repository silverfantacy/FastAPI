import uuid

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fief_client import FiefUserInfo
import fief

router = APIRouter(
    # prefix="/",
    tags=["fief"],
)

app = FastAPI()


@router.get("/auth-callback", name="auth_callback")
async def auth_callback(
    request: Request,
    response: Response,
    code: str = Query(...),
    memory_userinfo_cache: fief.MemoryUserInfoCache = Depends(
        fief.get_memory_userinfo_cache
    ),
):
    redirect_uri = request.url_for("auth_callback")
    tokens, userinfo = await fief.auth_callback(code, redirect_uri)

    response = RedirectResponse(request.url_for("protected"))
    response.set_cookie(
        fief.SESSION_COOKIE_NAME,
        tokens["access_token"],
        max_age=tokens["expires_in"],
        httponly=True,
        secure=False,
    )

    print(userinfo)
    await memory_userinfo_cache.set(uuid.UUID(userinfo["sub"]), userinfo)

    return response


@router.get("/protected", name="protected")
async def protected(
    user: FiefUserInfo = Depends(fief.auth.current_user()),
):
    return HTMLResponse(
        f"<h1>You are authenticated. Your user email is {user['email']}</h1>"
    )
