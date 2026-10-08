#from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

import bcrypt
#password_context = CryptContext( schemes =["bcrypt"], deprecated ="auto")
from app.core.config import settings

def hash_password(password : str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode("utf-8")

def verify_password(plain_password : str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hash_bytes)

def create_access_token(user_id: int, role : str) -> str:
    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(hours = settings.ACCESS_TOKEN_EXPIRE_HOURS)

    payload = { "sub" : str(user_id), "role" : role, "iat" : now, "exp" : expires_at}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

def decode_access_token(token : str) -> dict | None:

    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
        return payload
    except JWTError:
        return None