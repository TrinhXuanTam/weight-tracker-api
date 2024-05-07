from datetime import date
from typing import List, Optional
from src.modules.weight.schemas import WeightMeasurementCreate, WeightMeasurementBrief
from src.modules.weight.repository import repository as weight_repository


class WeightService:
    async def get_weight_measurements(
        self,
        user_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[WeightMeasurementBrief]:
        """Retrieve weight measurements for a user, optionally filtered by a date range.

        Args:
            user_id (int): The unique ID of the user whose measurements are being retrieved.
            from_date (Optional[date]): The start date for filtering measurements.
            to_date (Optional[date]): The end date for filtering measurements.

        Returns:
            List[WeightMeasurementBrief]: A list of weight measurements for the user in the specified range.
        """
        # Fetch the weight measurements from the repository, optionally filtered by date range
        measurements = await weight_repository.get_weight_measurements(
            user_id, from_date, to_date
        )
        # Convert the retrieved models to brief Pydantic schema objects for consistent API responses
        return [WeightMeasurementBrief.from_model(m) for m in measurements]

    async def save_weight_measurement(
        self, user_id: int, data: WeightMeasurementCreate
    ) -> WeightMeasurementBrief:
        """Save a new weight measurement for a user.

        Args:
            user_id (int): The unique ID of the user for whom the measurement is being saved.
            data (WeightMeasurementCreate): The Pydantic schema object representing the new measurement data.

        Returns:
            WeightMeasurementBrief: The newly created weight measurement, formatted as a brief response.
        """
        # Save the weight measurement using the repository and return it as a brief schema object
        measurement = await weight_repository.save_weight_measurement(user_id, data)
        return WeightMeasurementBrief.from_model(measurement)


service = WeightService()
