from typing import List

import psycopg2
from .. import schemas, oauth2, trans
from fastapi import Response, status, HTTPException, APIRouter, Depends
from ..main import cursor, conn

router = APIRouter(tags=["Vote"], 
                   prefix="/votes"
                   )

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, current_user: trans.TransUsers  = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * FROM votes WHERE post_id = %s AND user_id = %s""",(str(vote.post_id), str(current_user.id)))
    found_vote = cursor.fetchone()
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(vote.post_id),))
    post_exist = cursor.fetchone()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted post {vote.post_id}")
        elif not post_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")
        cursor.execute("""INSERT INTO votes (post_id, user_id) VALUES (%s,%s)""",(str(vote.post_id), str(current_user.id)))
        conn.commit()
        cursor.execute("""SELECT posts.id, COUNT(votes.post_id) as number_of_votes from posts LEFT JOIN votes ON posts.id = votes.post_id WHERE posts.id = %s GROUP By posts.id""",(str(vote.post_id),))
        number_of_vote = dict(cursor.fetchone())
        print(number_of_vote)
        print(number_of_vote['id'])
        return {"message": f"Successflly added vote! There is {number_of_vote['number_of_votes']} vote for post {vote.post_id}"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has not voted post {vote.post_id}")
        cursor.execute("""DELETE FROM votes WHERE post_id = %s AND user_id = %s""", (str(vote.post_id), str(current_user.id)))
        conn.commit()
        cursor.execute("""SELECT posts.id, COUNT(votes.post_id) as number_of_votes from posts LEFT JOIN votes ON posts.id = votes.post_id WHERE posts.id = %s GROUP By posts.id""",(str(vote.post_id),))
        number_of_vote = dict(cursor.fetchone())
        return {"message": f"Successfully deleted vote! There is {number_of_vote['number_of_votes']} vote for post {vote.post_id}"}
