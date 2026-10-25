
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from database import postgres_connection
from schema import UserGet, PostGet, FeedGet
from helpers import get_user, get_post, get_feed, get_recommended_feed


app = FastAPI()



def get_conn():

    conn = postgres_connection()
    try:
        yield conn  # отдаём соединение в обработчик запроса
    finally:
        conn.close()  # обязательно закрываем соединение после завершения


@app.get("/user/{id}", response_model=UserGet)
def handle_get_user(id: int, conn=Depends(get_conn)) -> UserGet:

    user = get_user(conn=conn, user_id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/post/{id}", response_model=PostGet)
def handle_get_post(id: int, conn=Depends(get_conn)) -> PostGet:

    post = get_post(conn=conn, post_id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def handle_get_user_feed(
    id: int, limit: int = 10, conn=Depends(get_conn)
) -> List[FeedGet]:

    feeded = get_feed(conn=conn, user_id=id, limit=limit)
    if not feeded:
        raise HTTPException(status_code=404, detail="Feed not found")
    return feeded


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def handle_get_post_feed(
    id: int, limit: int = 10, conn=Depends(get_conn)
) -> List[FeedGet]:

    get_feeded = get_feed(conn=conn, post_id=id, limit=limit)
    if not get_feeded:
        raise HTTPException(status_code=404, detail="Feed not found")
    return get_feeded


@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(
    id: int, limit: int = 10, conn=Depends(get_conn)
) -> List[PostGet]:

    rec = get_recommended_feed(conn=conn, id=id, limit=limit)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return rec
