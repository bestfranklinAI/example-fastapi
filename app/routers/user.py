from fastapi import status, HTTPException, APIRouter
from .. import schemas, utils
from ..main import cursor, conn

router = APIRouter(
    prefix="/users",
    tags=["Users"]
    )


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserIn):
    try:
        user.password = utils.hash(user.password)
        cursor.execute("""INSERT INTO users (email, password) VALUES (%s,%s) RETURNING * """,
                    tuple(user.dict().values()))
        new_user = cursor.fetchone()
        conn.commit()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The error was {error}")
    return new_user

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id : int):
    cursor.execute("SELECT * FROM users WHERE id = %s", (str(id),))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist")
    return user