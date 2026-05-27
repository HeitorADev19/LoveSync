from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    couple_name: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    couple_id: int
    is_active: bool

    class Config:
        orm_mode = True


class CoupleRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class MemoryCreate(BaseModel):
    title: str
    description: Optional[str] = None


class MemoryRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class GoalRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[datetime]

    class Config:
        orm_mode = True


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: Optional[str] = "general"
    note: Optional[str] = None


class ExpenseRead(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    note: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class RoutineCreate(BaseModel):
    title: str
    description: Optional[str] = None
    schedule: Optional[str] = None


class RoutineRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    schedule: Optional[str]
    active: bool

    class Config:
        orm_mode = True
