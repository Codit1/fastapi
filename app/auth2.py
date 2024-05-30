import jwt
from jwt.exceptions import PyJWKError, InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException,status
from datetime import datetime, timedelta, timezone
from . import Schema, models, database
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    econded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return econded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = Schema.TokenData(id = id)
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    
def get_users(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):

    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="coudld not authorize user", headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user

