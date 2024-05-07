from typing import List, Optional
from datetime import date
from sqlalchemy import select
from src.modules.weight.models import WeightMeasurement
from src.modules.weight.schemas import WeightMeasurementCreate
from src.utils.db_utils import async_session


class WeightRepository:
    async def get_weight_measurements(
        self,
        user_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[WeightMeasurement]:
        """Retrieve weight measurements for a user, optionally filtered by a date range.

        Args:
            user_id (int): The unique ID of the user whose measurements are being retrieved.
            from_date (Optional[date]): The start date for filtering measurements.
            to_date (Optional[date]): The end date for filtering measurements.

        Returns:
            List[WeightMeasurement]: A list of weight measurement records that match the given criteria.
        """
        async with async_session() as session:
            # Construct the base query to retrieve weight measurements for a specific user
            query = select(WeightMeasurement).where(
                WeightMeasurement.user_id == user_id
            )
            # Apply optional date filters if provided
            if from_date:
                query = query.where(WeightMeasurement.date >= from_date)
            if to_date:
                query = query.where(WeightMeasurement.date <= to_date)

            # Execute the query and return the results
            result = await session.execute(query)
            return result.scalars().all()

    async def save_weight_measurement(
        self, user_id: int, data: WeightMeasurementCreate
    ) -> WeightMeasurement:
        """Save a new weight measurement for a user.

        Args:
            user_id (int): The unique ID of the user for whom the measurement is being saved.
            data (WeightMeasurementCreate): The Pydantic schema object representing the new measurement data.

        Returns:
            WeightMeasurement: The newly created weight measurement record.
        """
        async with async_session() as session:
            measurement = WeightMeasurement(
                user_id=user_id,
                date=data.date,
                weight=data.weight,
            )
            session.add(measurement)
            await session.commit()
            await session.refresh(measurement)
            return measurement


repository = WeightRepository()
