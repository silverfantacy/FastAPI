import os
from fastapi import HTTPException, status
import pyotp


def get(platform: str):
    QRCODE = os.getenv(f"OTP_{platform}")
    if QRCODE:
        totp = pyotp.TOTP(QRCODE.replace(" ", ""))
        code = totp.now()
        return code
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"NO OTP")
