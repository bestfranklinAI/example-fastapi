from fastapi.testclient import TestClient
from app.main import app
import pytest
from pydantic import EmailStr
import re
from app import schemas

client = TestClient(app)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@pytest.mark.parametrize("id",[(20)])
def test_get_users(id):
    response = client.get(f"/users/{id}")
    new_user = schemas.UserOut(**response.json())
    

def test_create_users():
    response = client.post("/users/",json={"email":"feraaaaaaaaaaaa@gmail.com","password":"password123"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "feraaaaaaaaaaaa@gmail.com"
    assert response.status_code == 201

def test_get_post():
    client.headers = {**client.headers,"Authorization":f"bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozMSwiZXhwIjoxNjg3MjQ0NDc3fQ.GSQ4EvM6AAiOIhctDBr77u6yTXHlUA87ynHls0ax44M"}
    response = client.get("/posts/")
    def trans(dict):
        post = schemas.PostOut(**dict)
        return post
    list_of_posts = map(trans,list(response.json()))
    print(list(list_of_posts))





# from typing import get_type_hints

# def type_hinted(func):
#     hints = get_type_hints(func)
#     def wrapper(*args, **kwars):
#         new_args = []
#         for arg, hint in zip(args, hints.values()):
#             if not isinstance(arg, hint):
#                 arg = hint(arg)
#             new_args.append(arg)
#         return func(*new_args, **kwars)
#     return wrapper

# @type_hinted
# def add_numbers(a: int,b :int) -> int:
#     return str(a + b)

# print(type(add_numbers(2,3)))


