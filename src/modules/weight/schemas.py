import datetime
from src.modules.weight.models import WeightMeasurement
from src.schemas import CustomSchema


class WeightMeasurementBrief(CustomSchema):
    """Schema representing information about a weight measurement.

    Attributes:
        date (datetime.datetime): The date of the weight measurement.
        weight (float): The weight value recorded by the user.
    """

    date: datetime.datetime
    weight: float

    @staticmethod
    def from_model(measurement: WeightMeasurement) -> "WeightMeasurementBrief":
        """Convert a weight measurement model instance into a brief representation.

        Args:
            measurement (WeightMeasurement): The weight measurement model instance.

        Returns:
            WeightMeasurementBrief: A brief representation of the weight measurement.
        """
        return WeightMeasurementBrief(
            date=measurement.date,
            weight=measurement.weight,
        )


class WeightMeasurementCreate(CustomSchema):
    """Schema representing the creation of a new weight measurement.

    Attributes:
        date (datetime.datetime): The date of the weight measurement.
        weight (float): The weight value recorded by the user.
    """

    date: datetime.datetime
    weight: float
