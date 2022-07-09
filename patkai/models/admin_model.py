from dataclasses import dataclass
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from patkai.database import Base


class Admin(Base):
    __tablename__ = "admin"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(String)
    updated_at = Column(String)

