from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import auth2, Schema, models, database

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: Schema.Votes, db: Session = Depends(database.get_db), current_user: int = Depends(auth2.get_users)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post id: {vote.post_id} could not be found")

    votes_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)

    found_votes = votes_query.first()

    if (vote.dir == 1):
        if found_votes:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"this post {found_votes} has been liked by you")
        
        new_votes = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_votes)
        db.commit()

        return {"message": "post vote was successfull"}
    
    else:
        if not found_votes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post id: {vote.post_id} does not exist")
        
        votes_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "post has been unvoted"}