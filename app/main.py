from fastapi import FastAPI
from .database import conn_database
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# from fastapi.params import Body
# from typing import Optional, List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from . import schemas, utils
# import time

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
cursor, conn = conn_database()
from .routers import post, user, auth, vote
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database = 'fastapi', user= 'postgres', password='abcd1005', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection is successful!")
#         break
#     except Exception as error:
#         print("Connection to Database failed!")
#         print(f"The error was: {error}")
#         time.sleep(3)

# my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1}, {"title" : "favourite food", "content" : "I like pizza", "id" : 2 }] 

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

# @app.get("/")
# async def root():
#     return{"message":"Welcome to my API!"}

# @app.get("/posts", response_model= List[schemas.Post])
# def get_post():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return posts 

# @app.post("/posts", status_code = status.HTTP_201_CREATED, response_model= schemas.Post)
# def create_posts(post : schemas.PostCreate):
#     """post_dict = post.dict()
#     post_dict["id"] = randrange(0,100000000)
#     my_posts.append(post_dict)"""
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
#                    tuple(post.dict().values()))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return new_post

# @app.get("/posts/{id}", response_model= schemas.Post)
# def get_post(id : int):
#     """post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
#         #response.status_code = status.HTTP_404_NOT_FOUND
#         #return{"message" : f"Post with id: {id} was not found"}"""
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
#     posts = cursor.fetchone()
#     if not posts:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not  found")
#     return posts

# @app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     """index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
#     my_posts.pop(index)"""
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if not deleted_post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {str(id)} does not exist")
#     return Response(status_code = status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}", response_model= schemas.Post)
# def update_post(id:int, post: schemas.PostCreate):
#     """index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
#     post_dict = post.dict()
#     post_dict["id"] = id
#     my_posts[index]= post_dict"""
#     temporary_post = list(post.dict().values())
#     temporary_post.append(str(id))
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (temporary_post))
#     updated_posts = cursor.fetchone()
#     if  updated_posts == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
#     conn.commit()
#     return updated_posts

# @app.post("/users", status_code = status.HTTP_201_CREATED, response_model= schemas.UserOut)
# def create_user(user: schemas.UserCreate):
#     user.password = utils.hash(user.password)
#     cursor.execute("""INSERT INTO users (email, password) VALUES (%s,%s) RETURNING * """,
#                    tuple(user.dict().values()))
#     new_user = cursor.fetchone()
#     conn.commit()
#     return new_user

# @app.get("/users/{id}", response_model= schemas.UserOut)
# def get_user(id : int):
#     cursor.execute("SELECT * FROM users WHERE id = %s", (str(id),))
#     user = cursor.fetchone()
#     if not user:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist")
#     return user