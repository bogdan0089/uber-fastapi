from database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.enum import Role, Status
from datetime import datetime
from sqlalchemy import Enum as SAEnum


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    full_name: Mapped[str]
    role: Mapped[Role] = mapped_column(SAEnum(Role, values_callable=lambda x: [e.value for e in x]), default=Role.PASSENGER)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    trips_as_passenger: Mapped[list["Trip"]] = relationship(back_populates="passenger", foreign_keys="[Trip.passenger_id]")
    trips_as_driver: Mapped[list["Trip"]] = relationship(back_populates="driver",foreign_keys="[Trip.driver_id]")
    avg_rating: Mapped[float] = mapped_column(default=0.0)
    ratings_as_passenger: Mapped[list["Rating"]] = relationship(back_populates="passenger", foreign_keys="[Rating.passenger_id]")
    ratings_as_driver: Mapped[list["Rating"]] = relationship(back_populates="driver", foreign_keys="[Rating.driver_id]")    


class Trip(Base):
    __tablename__ = "trips"
    id: Mapped[int] = mapped_column(primary_key=True)
    passenger_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[Status] = mapped_column(default=Status.WAITING)
    pickup_address: Mapped[str]
    dropoff_address: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    passenger: Mapped["User"] = relationship(back_populates="trips_as_passenger", foreign_keys=[passenger_id])
    driver: Mapped["User"] = relationship(back_populates="trips_as_driver", foreign_keys=[driver_id])
    ratings: Mapped[list["Rating"]] = relationship(back_populates="trip")
    pickup_lat: Mapped[float] = mapped_column(nullable=True)
    pickup_lon: Mapped[float] = mapped_column(nullable=True)
    dropoff_lat: Mapped[float] = mapped_column(nullable=True)
    dropoff_lon: Mapped[float] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(default=0.0)


class Rating(Base):
    __tablename__ = "rating"
    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"))
    passenger_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    score: Mapped[int] 
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    trip: Mapped["Trip"] = relationship(back_populates="ratings")
    passenger: Mapped["User"] = relationship(back_populates="ratings_as_passenger", foreign_keys=[passenger_id])
    driver: Mapped["User"] = relationship(back_populates="ratings_as_driver", foreign_keys=[driver_id])


