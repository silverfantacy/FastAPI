from fastapi import APIRouter, Depends, status
from ..repository import otp
from typing import Union

router = APIRouter(
    prefix="/opt",
    tags=["OTP"]
)


@router.get("/", status_code=status.HTTP_200_OK)
def main(platform: Union[str, None] = None):
    return otp.get(platform)
