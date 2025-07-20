from sqlmodel import SQLModel
from typing import Optional


class UserCreate(SQLModel):
    username: str
    email: str
    password: str


class UserLogin(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: Optional[str] = "bearer"
    refresh_token: str


class RefreshToken(SQLModel):
    refresh_token: str


class AccessTokenOnly(SQLModel):
    access_token: str
