from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Couple(Base):
    __tablename__ = "couples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="couple", cascade="all, delete")
    memories = relationship("Memory", back_populates="couple", cascade="all, delete")
    goals = relationship("Goal", back_populates="couple", cascade="all, delete")
    expenses = relationship("Expense", back_populates="couple", cascade="all, delete")
    routines = relationship("RoutineItem", back_populates="couple", cascade="all, delete")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    couple_id = Column(Integer, ForeignKey("couples.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    couple = relationship("Couple", back_populates="users")


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    couple_id = Column(Integer, ForeignKey("couples.id"), nullable=False)

    couple = relationship("Couple", back_populates="memories")


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    couple_id = Column(Integer, ForeignKey("couples.id"), nullable=False)

    couple = relationship("Couple", back_populates="goals")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(120), default="general")
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    couple_id = Column(Integer, ForeignKey("couples.id"), nullable=False)

    couple = relationship("Couple", back_populates="expenses")


class RoutineItem(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    schedule = Column(String(120), nullable=True)
    active = Column(Boolean, default=True)
    couple_id = Column(Integer, ForeignKey("couples.id"), nullable=False)

    couple = relationship("Couple", back_populates="routines")
