from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserIn(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    email:EmailStr
    created_at: datetime
    id: int

class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True
    def list(self):
        return list(self.dict().values())
    #rating : Optional[int] = None

class PostIn(PostBase):
    pass

class PostOut(PostBase):
    id:int
    created_at:datetime
    number_of_votes: int
    owner_id: int
    email: EmailStr
    # user: Optional[UserOut] = "Written by you"

# class UserLogin(BaseModel):
#     email:EmailStr
#     password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
 