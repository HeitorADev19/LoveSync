from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.core.security import create_access_token, verify_password
from app.crud import create_couple, create_user, get_user_by_email
from app.schemas import Token, UserCreate

router = APIRouter()


@router.post("/signup", response_model=Token)
async def signup(data: UserCreate, db: AsyncSession = Depends(get_db_session)):
    existing_user = await get_user_by_email(db, email=data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    couple = await create_couple(db, name=data.couple_name)
    user = await create_user(
        db,
        email=data.email,
        password=data.password,
        full_name=data.full_name,
        couple_id=couple.id,
    )
    access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(data: UserCreate, db: AsyncSession = Depends(get_db_session)):
    user = await get_user_by_email(db, email=data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}
