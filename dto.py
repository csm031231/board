from pydantic import BaseModel
from datetime import datetime

class AddUserDTO(BaseModel):
    username: str
    password: str
    nickname: str

class UpdateUserDTO(BaseModel):
    username: str
    password: str = None  
    nickname: str

class UserResponseDTO(BaseModel):
    id: int
    username: str
    nickname: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TokenDTO(BaseModel):
    access_token: str
    token_type: str

class PostCreateDTO(BaseModel):
    title: str
    content: str

class UpdatePost(BaseModel):
    title: str
    content: str

class PostResponseDTO(BaseModel):
    id: int
    title: str
    content: str
    view_count: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True

class CommentCreateDTO(BaseModel):
    post_id: int
    content: str

class CommentResponseDTO(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True
