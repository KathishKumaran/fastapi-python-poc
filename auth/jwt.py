# auth/jwt.py
import datetime
from jose import jwt, JWTError
from settings import ALGORITHM, SECRET_KEY  # Import your secret key

# For no expiration
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def create_access_token(data: dict, expires_delta: datetime.timedelta):
#     to_encode = data.copy()
#     expire = datetime.datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
