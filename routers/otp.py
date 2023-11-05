from fastapi import APIRouter, Depends, status
from repository import otp
from typing import Union
import fief

router = APIRouter(
    prefix="/opt",
    tags=["OTP"]
)


@router.get("/", status_code=status.HTTP_200_OK)
def main(platform: Union[str, None] = None, user: fief.FiefUserInfo = Depends(fief.auth.current_user())):
    return otp.get(platform)
