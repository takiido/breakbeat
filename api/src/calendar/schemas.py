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
