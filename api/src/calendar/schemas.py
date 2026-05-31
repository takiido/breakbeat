from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CalendarCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None


class CalendarUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


class CalendarOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_all_day: bool
    location: Optional[str] = None
    repeat_rule: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_all_day: Optional[bool] = None
    location: Optional[str] = None
    repeat_rule: Optional[str] = None
    calendar_id: Optional[int] = None


class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_all_day: bool
    location: Optional[str] = None
    repeat_rule: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
