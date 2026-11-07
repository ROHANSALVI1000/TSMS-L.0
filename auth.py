import jwt
from datetime import datetime,timezone,timedelta
from dotenv import load_dotenv
import os
load_dotenv()

SECURITY_KEY=os.getenv("security_key")

ALGORITHM="HS256"


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

