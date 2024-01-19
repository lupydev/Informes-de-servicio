import uuid
from dotenv import load_dotenv
import os
from datetime import timedelta, datetime
from fastapi import Depends
from jose import jwt, JWTError
from db.security import oauth2_scheme

load_dotenv()

EXPIRES = int(os.getenv("TOKEN_EXPIRES"))
TOKEN_KEY = os.getenv("TOKEN_SECRET_KEY")
ALGORITHM = os.getenv("TOKEN_ALGORITHM")

access_token_expires = timedelta(weeks=EXPIRES)


def create_token(
    id: uuid.UUID,
    active: bool,
    verified: bool,
):
    encode = {
        "id": str(id),
        "active": active,
        "verified": verified,
    }

    expire = datetime.utcnow() + access_token_expires
    encode.update({"exp": expire})

    encode_jwt = jwt.encode(encode, TOKEN_KEY, algorithm=ALGORITHM)
    return encode_jwt


def decode_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, TOKEN_KEY, algorithms=ALGORITHM)
