from pydantic import BaseModel
from typing import List, Optional


class BlogBase(BaseModel):
    title: str
    body: str
    # published: Optional[bool]


class Blog(BlogBase):
    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        from_attributes = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str

    class Config():
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []

class message(BaseModel):
    role: str
    content: str
class Chat(BaseModel):
    messages: List[message] = []
    model: Optional[str] = "gpt-3.5-turbo"
    max_tokens: Optional[int] = 256