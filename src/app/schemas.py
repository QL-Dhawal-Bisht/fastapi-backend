from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class Post(BaseModel):
    id: int
    title: str
    description: str
    author: User

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class PostCreate(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class CommentCreate(BaseModel):
    content: str

    class Config:
        from_attributes = True
