from datetime import datetime
from sqlalchemy import (
    String, DateTime, func,
    Boolean, Integer, ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Calendar(Base):
    __tablename__ = "calendars"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String, nullable=True)
    color: Mapped[str] = mapped_column(String(6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="calendar",
        cascade="all, delete-orphan",
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="calendars")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    is_all_day: Mapped[bool] = mapped_column(Boolean, default=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    repeat_rule: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    calendar_id: Mapped[int] = mapped_column(Integer, ForeignKey("calendars.id"))
    calendar: Mapped["Calendar"] = relationship(
        "Calendar",
        back_populates="events",
        lazy="joined",
    )