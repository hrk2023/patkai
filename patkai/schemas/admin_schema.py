from pydantic import BaseModel
from uuid import uuid4
from typing import Optional
from datetime import datetime
import pytz

class Admin(BaseModel):
    id: Optional[str]
    username: str
    password: str
    is_active: Optional[bool] = True
    created_at: Optional[str] = datetime.now(pytz.timezone("Asia/Kolkata"))
    updated_at: Optional[str] = datetime.now(pytz.timezone("Asia/Kolkata"))

    class Config:
        orm_mode = True