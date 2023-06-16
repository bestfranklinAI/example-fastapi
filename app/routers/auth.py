from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import utils, oauth2, schemas
from ..main import cursor, conn

router = APIRouter(
    prefix = "/login",
    tags=["Authentication"]
)

@router.post("/",response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("SELECT * FROM users WHERE email = %s",(str(user_credentials.username),))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id" : user["id"]})

    return {"access_token": access_token, "token_type": "bearer"}
