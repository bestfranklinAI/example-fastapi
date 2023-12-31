from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import schemas, trans
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .main import cursor, conn
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secrete_key
ALGORITHM =  settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTE = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id= id)
    except JWTError:
        raise credential_exception
    return token_data
    
def get_current_user(token:str = Depends(oath2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credential_exception)
    cursor.execute("""SELECT * FROM users WHERE id = %s""", (token.id,))
    user = trans.TransUsers(cursor.fetchone())
    return user