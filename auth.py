import jwt
from datetime import datetime,timezone,timedelta
from dotenv import load_dotenv
import os
load_dotenv()

SECURITY_KEY=os.getenv("security_key")

ALGORITHM="HS256"

if not SECURITY_KEY:
    raise RuntimeError("key not available")


def create_access_token(user_id:int):
    payload={
        "sub":str(user_id),
        "exp":datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token=jwt.encode(
        payload,
        SECURITY_KEY,
        algorithm=ALGORITHM
    )

    return token



def verifty_access_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECURITY_KEY,
            algorithms=ALGORITHM
        )

        return payload

    except jwt.InvalidTokenError:
        return None

