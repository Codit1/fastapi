from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List
from .. import Schema, models, utils
from sqlalchemy.orm import Session
from ..database import get_db

users_password_list = ["johndoe123", "singlenatty", "marysmithpaswrd", "jamessmith", "wiliamspassword"]


router = APIRouter(
    prefix="/users",
    tags=["USERS"]
)

# how to make or create fastapi for managing user sccounts

@router.get("/{id}", response_model=Schema.UserResponse)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the user id:{id} was not found")
    
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schema.UserResponse)
def create_user(user: Schema.CreateUser, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)

    new_user = models.Users(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="seems like the email address has been used")

    return new_user