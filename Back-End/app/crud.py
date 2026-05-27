from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Couple, User, Memory, Goal, Expense, RoutineItem
from app.core.security import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def create_couple(db: AsyncSession, name: str) -> Couple:
    couple = Couple(name=name)
    db.add(couple)
    await db.commit()
    await db.refresh(couple)
    return couple


async def create_user(db: AsyncSession, email: str, password: str, full_name: str, couple_id: int) -> User:
    user = User(
        email=email,
        full_name=full_name,
        hashed_password=get_password_hash(password),
        couple_id=couple_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_memory(db: AsyncSession, title: str, description: str, couple_id: int) -> Memory:
    memory = Memory(title=title, description=description, couple_id=couple_id)
    db.add(memory)
    await db.commit()
    await db.refresh(memory)
    return memory


async def create_goal(db: AsyncSession, title: str, description: str, due_date: Optional[datetime], couple_id: int) -> Goal:
    goal = Goal(title=title, description=description, due_date=due_date, couple_id=couple_id)
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


async def create_expense(db: AsyncSession, title: str, amount: float, category: str, note: Optional[str], couple_id: int) -> Expense:
    expense = Expense(title=title, amount=amount, category=category, note=note, couple_id=couple_id)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


async def create_routine(db: AsyncSession, title: str, description: Optional[str], schedule: Optional[str], couple_id: int) -> RoutineItem:
    routine = RoutineItem(title=title, description=description, schedule=schedule, couple_id=couple_id)
    db.add(routine)
    await db.commit()
    await db.refresh(routine)
    return routine


async def list_memories(db: AsyncSession, couple_id: int) -> List[Memory]:
    result = await db.execute(select(Memory).where(Memory.couple_id == couple_id).order_by(Memory.created_at.desc()))
    return result.scalars().all()


async def list_goals(db: AsyncSession, couple_id: int) -> List[Goal]:
    result = await db.execute(select(Goal).where(Goal.couple_id == couple_id).order_by(Goal.id.desc()))
    return result.scalars().all()


async def list_expenses(db: AsyncSession, couple_id: int) -> List[Expense]:
    result = await db.execute(select(Expense).where(Expense.couple_id == couple_id).order_by(Expense.created_at.desc()))
    return result.scalars().all()


async def list_routines(db: AsyncSession, couple_id: int) -> List[RoutineItem]:
    result = await db.execute(select(RoutineItem).where(RoutineItem.couple_id == couple_id).order_by(RoutineItem.id.desc()))
    return result.scalars().all()
