
from datetime import datetime
from pydantic import BaseModel


class UserGet(BaseModel):
    """Модель данных пользователя для API-ответов."""
    id: int
    gender: int
    age: int
    country: str
    city: str
    exp_group: int
    os: str
    source: str


class PostGet(BaseModel):
    """Модель данных поста для API-ответов."""
    id: int
    text: str
    topic: str


class FeedGet(BaseModel):
    """Модель данных действия пользователя с постом для API-ответов."""
    user: UserGet
    post: PostGet
    user_id: int
    action: str
    time: datetime
    post_id: int
