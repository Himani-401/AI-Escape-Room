import datetime as dt
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class SessionRecord(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    seed = Column(Integer, default=0)
    status = Column(String, default="active")
    narrative = Column(Text, default="")
    current_puzzle = Column(String, default="")
    score = Column(Integer, default=0)
    started_at = Column(DateTime, default=dt.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    attempts = relationship("AttemptRecord", back_populates="session")
    hints = relationship("HintRecord", back_populates="session")


class AttemptRecord(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True)
    puzzle_id = Column(String, index=True)
    answer_text = Column(Text, default="")
    correct = Column(Boolean, default=False)
    score_delta = Column(Integer, default=0)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    session = relationship("SessionRecord", back_populates="attempts")


class HintRecord(Base):
    __tablename__ = "hints"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True)
    puzzle_id = Column(String, index=True)
    level = Column(Integer, default=1)
    text = Column(Text, default="")
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    session = relationship("SessionRecord", back_populates="hints")


class PuzzleStateRecord(Base):
    __tablename__ = "puzzle_states"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True)
    puzzle_id = Column(String, index=True)
    solved = Column(Boolean, default=False)
    unlocked = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    last_answer = Column(Text, default="")


class LeaderboardRecord(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    score = Column(Integer, default=0)
    finished = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
