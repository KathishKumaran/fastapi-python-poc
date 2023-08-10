# auth/routes.py
import datetime
import bcrypt
from fastapi import APIRouter, Depends,  HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError
from jsonschema import ValidationError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from jose import jwt, ExpiredSignatureError, JWTError

from auth.dependencies import get_db
from settings import ALGORITHM, SECRET_KEY
from .jwt import create_access_token
from models.models import User
from pydantic import BaseModel, EmailStr
from fastapi import Request
from fastapi import Response

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: str
    is_currently_logged_in: bool
    current_sign_in_at: datetime.datetime
    last_sign_in_at: datetime.datetime
    current_sign_in_ip: str
    last_sign_in_ip: str
    confirmed_at: datetime.datetime

@auth_router.post("/login", response_model=UserLoginResponse, tags=["Session"])
async def login(user_login: UserLogin, request: Request, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == user_login.email).first()
        if not user or not bcrypt.checkpw(user_login.password.encode('utf-8'), user.encrypted_password.encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # for expiration token
        # access_token_expires = datetime.timedelta(minutes=30)
        # access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

        access_token = create_access_token(data={"sub": user.email})

        # Update user information
        user.access_token = access_token
        user.is_currently_logged_in = True
        user.last_sign_in_at = user.current_sign_in_at
        user.current_sign_in_at = datetime.datetime.now()
        user.last_sign_in_ip = user.current_sign_in_ip
        user.current_sign_in_ip = request.client.host
        db.commit()

        # Create a response object
        response_model = UserLoginResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role,
            is_currently_logged_in=user.is_currently_logged_in,
            current_sign_in_at=datetime.datetime.now(),
            last_sign_in_at=user.last_sign_in_at,
            current_sign_in_ip=user.current_sign_in_ip,
            last_sign_in_ip=user.last_sign_in_ip,
            confirmed_at=user.confirmed_at,
        )
        # Set the token in the response headers
        response = Response(content=response_model.json())
        response.headers["Authorization"] = f"Bearer {access_token}"
        return response

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@auth_router.delete("/logout", tags=["Session"])
async def logout(authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token not present in Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Find the user and update user information
        user = db.query(User).filter(User.email == decoded_token['sub']).first()
        if user:
            user.access_token = None
            user.is_currently_logged_in = False
            db.commit()

            response = JSONResponse(content={"message": "Logged out successfully"})
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
