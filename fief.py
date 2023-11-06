import uuid
from typing import Dict, Optional
from fastapi import HTTPException, Request, Response, status

from fastapi.security import APIKeyCookie
from fief_client import FiefAsync, FiefUserInfo
from fief_client.integrations.fastapi import FiefAuth
import os


class CustomFiefAuth(FiefAuth):
    client: FiefAsync

    async def get_unauthorized_response(self, request: Request, response: Response):
        redirect_uri = request.url_for("auth_callback")
        auth_url = await self.client.auth_url(redirect_uri, scope=["openid"])
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": str(auth_url)},
        )


class MemoryUserInfoCache:
    def __init__(self) -> None:
        self.storage: Dict[uuid.UUID, FiefUserInfo] = {}

    async def get(self, user_id: uuid.UUID) -> Optional[FiefUserInfo]:
        return self.storage.get(user_id)

    async def set(self, user_id: uuid.UUID, userinfo: FiefUserInfo) -> None:
        self.storage[user_id] = userinfo


memory_userinfo_cache = MemoryUserInfoCache()


async def get_memory_userinfo_cache() -> MemoryUserInfoCache:
    return memory_userinfo_cache


fief_url = os.getenv("FIEF_BASE_URL", "")
fief_client_id = os.getenv("FIEF_CLIENT_ID", "")
fief_client_secret = os.getenv("FIEF_clientSecret", "")
# encryption_key = os.getenv("FIEF_encryption_key", "")

fief = FiefAsync(
    fief_url,
    fief_client_id,
    fief_client_secret,
    # encryption_key=encryption_key,
)

SESSION_COOKIE_NAME = "user_session"
scheme = APIKeyCookie(name=SESSION_COOKIE_NAME, auto_error=False)
auth = CustomFiefAuth(
    fief, scheme, get_userinfo_cache=get_memory_userinfo_cache
)
