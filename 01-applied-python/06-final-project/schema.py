
from datetime import datetime
from pydantic import BaseModel


class UserGet(BaseModel):
    id: int
    gender: int
    age: int
    country: str
    city: str
    exp_group: int
    os: str
    source: str


class PostGet(BaseModel):

    id: int
    text: str
    topic: str


class FeedGet(BaseModel):
    user: UserGet
    post: PostGet
    user_id: int
    action: str
    time: datetime
    post_id: int
