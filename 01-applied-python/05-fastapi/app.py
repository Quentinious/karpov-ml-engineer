

import datetime
import os

import psycopg2
from fastapi import Depends, FastAPI, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: datetime.date


class PostResponse(BaseModel):
    id: int
    text: str
    topic: str


def get_db():
    conn = psycopg2.connect(
        dbname=os.environ["DB_NAME"],
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=int(os.environ["DB_PORT"]),
        cursor_factory=RealDictCursor,
    )

    try:
        yield conn
    finally:
        conn.close()


@app.post("/user/validate")
def validate_user(user: User):
    return (
        f"Will add user: {user.name} "
        f"{user.surname} with age {user.age}"
    )


@app.get("/user/{id}")
def get_user(id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT gender, age, city
            FROM "user"
            WHERE id = %(user_id)s
            """,
            {"user_id": id},
        )
        result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="user not found")

    return result


@app.get("/post/{id}", response_model=PostResponse)
def get_post(id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, text, topic
            FROM post
            WHERE id = %(post_id)s
            """,
            {"post_id": id},
        )
        result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="post not found")

    return PostResponse(**result)
