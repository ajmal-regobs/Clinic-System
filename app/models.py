from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: Optional[str] = None


class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    phone: Optional[str]
    created_at: datetime
