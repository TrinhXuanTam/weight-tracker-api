import datetime
from src.utils.db_utils import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class WeightMeasurement(Base):
    """Represents a weight measurement entry recorded by a user.

    Attributes:
        __tablename__ (str): Name of the SQL table that stores weight measurements.
        id (Mapped[int]): Unique identifier for the weight measurement entry.
        user_id (Mapped[int]): The ID of the user who recorded the weight.
        date (Mapped[datetime.datetime]): The date of the weight measurement entry.
        weight (Mapped[float]): The weight value recorded by the user.
    """

    __tablename__ = "weight_measurement"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
