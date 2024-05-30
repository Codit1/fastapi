from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Post_Create(PostBase):
    pass

class UserResponse(BaseModel):
    name: str 
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True

class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True

class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = True

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str


class User_Credentials(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token: str

class Votes(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore