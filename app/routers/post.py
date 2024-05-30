from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List, Optional

from sqlalchemy import func
from .. import Schema, models, auth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["POSTS"]
)

# to get all posts
# @router.get("/", response_model=List[Schema.PostResponse])
@router.get("/", response_model=List[Schema.PostVote])
def get_sqlalchemy(db: Session = Depends(get_db), get_current_user: int = Depends(auth2.get_users), limit: int = 10, skip: int = 2, search: Optional[str] = ""):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    votes_post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    print(votes_post)
    
    return votes_post

@router.get("/{id}", status_code=status.HTTP_404_NOT_FOUND, response_model=Schema.PostVote)
def get_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(auth2.get_users)):

    ind_post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()

    if not ind_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=fr"can't find a post with that ID: {id}")
    
    return ind_post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schema.PostResponse)
def create_posts(post: Schema.Post_Create, db: Session = Depends(get_db), get_current_user: int = Depends(auth2.get_users)):
    
    new_post = models.Post(owner_id = get_current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}")
def delete_posts(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(auth2.get_users)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=fr"the post id: {id} could not be found")
    
    deleted_post_data = deleted_post.first()

    if deleted_post_data.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorized to complete this action ")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Schema.PostResponse)
def update_post(id: int, post: Schema.Post_Create, db: Session = Depends(get_db), get_current_user: int = Depends(auth2.get_users)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post id: {id} could not be found")
    
    if updated_post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorized to complete this action")
    
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return updated_post


@router.patch("/{id}", response_model=Schema.PostResponse)
def update_particular_post(id: int, post: Schema.UpdatePost, db: Session = Depends(get_db), get_current_user: int = Depends(auth2.get_users)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_data = post_query.first()

    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post id:{id} was not found")
    
    if post.title == None:
        post.title = post_data.title
    
    if post.content == None:
        post.content = post_data.content

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_data