from database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.enum import Role, Status
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
    trips_as_passenger: Mapped[list["Trip"]] = relationship(back_populates="passenger", foreign_keys="[Trip.passenger_id]")
    trips_as_driver: Mapped[list["Trip"]] = relationship(back_populates="driver",foreign_keys="[Trip.driver_id]")


class Trip(Base):
    __tablename__ = "trips"
    id: Mapped[int] = mapped_column(primary_key=True)
    passenger_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[Status]
    pickup_address: Mapped[str]
    dropoff_address: Mapped[str]
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    passenger: Mapped["User"] = relationship(back_populates="trips_as_passenger", foreign_keys=[passenger_id])
    driver: Mapped["User"] = relationship(back_populates="trips_as_driver", foreign_keys=[driver_id])





