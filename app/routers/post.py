from typing import List
from .. import schemas, oauth2, trans
from fastapi import Response, status, HTTPException, APIRouter, Depends
from ..main import cursor, conn

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )


@router.get("/", response_model= List[schemas.PostOut])
def get_post(current_user: trans.TransUsers  = Depends(oauth2.get_current_user), limit: int = 10, skip: int =0, search: str = ""):
    cursor.execute("""SELECT posts.*, MAX(users.email) as email, COUNT(votes.post_id) as number_of_votes
FROM posts
LEFT JOIN users ON posts.owner_id = users.id
LEFT JOIN votes ON posts.id = votes.post_id
WHERE posts.title LIKE %s
GROUP BY posts.id LIMIT %s OFFSET %s"""
                   , ('%'+str(search)+'%', str(limit), str(skip)))
    posts = cursor.fetchall()
    return posts 

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostOut)
def create_posts(post : schemas.PostIn, current_user: trans.TransUsers = Depends(oauth2.get_current_user)):
    """post_dict = post.dict()
    post_dict["id"] = randrange(0,100000000)
    my_posts.append(post_dict)"""
    #print(current_user["email"])
    # post_detail = list(post.dict().values())
    # post_detail.append(str(current_user["id"]))
    cursor.execute("""INSERT INTO posts (title, content, published, owner_id) VALUES (%s,%s,%s,%s) RETURNING * """,
                   (current_user.append(post.list(),(str(current_user.id)))))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post

@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id : int, current_user: trans.TransUsers = Depends(oauth2.get_current_user)):
    """post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message" : f"Post with id: {id} was not found"}"""
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    cursor.execute("""SELECT posts.*, MAX(users.email) as email, COUNT(votes.post_id) as number_of_votes
FROM posts
LEFT JOIN users ON posts.owner_id = users.id
LEFT JOIN votes ON posts.id = votes.post_id
WHERE posts.id = %s
GROUP BY posts.id"""
                   , (str(id),))
    posts = cursor.fetchone()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not  found")
    return posts

@router.delete("/{post_id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int, current_user: trans.TransUsers = Depends(oauth2.get_current_user)):
    """index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
    my_posts.pop(index)"""
    try:
        cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(post_id),))
        user = trans.TransPosts(cursor.fetchone())
        if not current_user.id == user.owner_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Action is not authorized")
        cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
        deleted_post = cursor.fetchone()
        conn.commit()
    except TypeError:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {str(post_id)} does not exist")
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", response_model= schemas.PostOut)
def update_post(post_id: int, post: schemas.PostIn, current_user: trans.TransUsers = Depends(oauth2.get_current_user)):
    """index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index]= post_dict"""
    try:
        cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(post_id),))
        user = trans.TransPosts(cursor.fetchone())
        if not current_user.id == user.owner_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Action is not authorized")
        post_detail = list(post.dict().values())
        post_detail.append(str(post_id))
        cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post_detail))
        updated_posts = cursor.fetchone()
    except TypeError:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {post_id} does not exist")
    conn.commit()
    return updated_posts
