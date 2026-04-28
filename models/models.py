from core.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.enum import Role
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    full_name: Mapped[str]
    role: Mapped[Role]
    is_active: Mapped[bool] = mapped_column(default=True)
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
