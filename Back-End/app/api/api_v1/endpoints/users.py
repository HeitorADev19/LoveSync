from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.crud import (
    create_expense,
    create_goal,
    create_memory,
    create_routine,
    list_expenses,
    list_goals,
    list_memories,
    list_routines,
)
from app.schemas import (
    ExpenseCreate,
    ExpenseRead,
    GoalCreate,
    GoalRead,
    MemoryCreate,
    MemoryRead,
    RoutineCreate,
    RoutineRead,
    UserRead,
)
from app.db.models import User

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/memories", response_model=MemoryRead)
async def add_memory(
    payload: MemoryCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await create_memory(db, title=payload.title, description=payload.description or "", couple_id=current_user.couple_id)


@router.get("/memories", response_model=list[MemoryRead])
async def get_memories(db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await list_memories(db, couple_id=current_user.couple_id)


@router.post("/goals", response_model=GoalRead)
async def add_goal(
    payload: GoalCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await create_goal(
        db,
        title=payload.title,
        description=payload.description or "",
        due_date=payload.due_date,
        couple_id=current_user.couple_id,
    )


@router.get("/goals", response_model=list[GoalRead])
async def get_goals(db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await list_goals(db, couple_id=current_user.couple_id)


@router.post("/expenses", response_model=ExpenseRead)
async def add_expense(
    payload: ExpenseCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await create_expense(
        db,
        title=payload.title,
        amount=payload.amount,
        category=payload.category or "general",
        note=payload.note,
        couple_id=current_user.couple_id,
    )


@router.get("/expenses", response_model=list[ExpenseRead])
async def get_expenses(db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await list_expenses(db, couple_id=current_user.couple_id)


@router.post("/routines", response_model=RoutineRead)
async def add_routine(
    payload: RoutineCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await create_routine(
        db,
        title=payload.title,
        description=payload.description,
        schedule=payload.schedule,
        couple_id=current_user.couple_id,
    )


@router.get("/routines", response_model=list[RoutineRead])
async def get_routines(db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await list_routines(db, couple_id=current_user.couple_id)
