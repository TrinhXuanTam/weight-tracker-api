from datetime import date
from fastapi import APIRouter, Depends
from typing import Optional
from src.modules.weight.schemas import WeightMeasurementBrief, WeightMeasurementCreate
from src.schemas import ListResponse
from src.modules.auth.schemas import UserDetail
from src.modules.auth.dependencies import access_token_validation
from src.modules.weight.service import service as weight_service

router: APIRouter = APIRouter()


@router.get(
    "/",
    summary="Get weight measurements",
    description="Get weight measurements within an optionally specified date range.",
)
async def get_weight(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    user: UserDetail = Depends(access_token_validation()),
) -> ListResponse[WeightMeasurementBrief]:
    """Retrieve weight measurements for the authenticated user within an optional date range.

    Args:
        from_date (Optional[date]): The start date to filter weight measurements. Defaults to None.
        to_date (Optional[date]): The end date to filter weight measurements. Defaults to None.
        user (UserDetail): The authenticated user requesting their weight measurements.

    Returns:
        ListResponse[WeightMeasurementBrief]: A response containing a list of filtered weight measurements.
    """
    # Fetch the user's weight measurements using the weight service within the given date range
    measurement = await weight_service.get_weight_measurements(
        user.id, from_date, to_date
    )
    # Return the measurements in a standardized list response format
    return ListResponse(items=measurement)


@router.post(
    "/",
    summary="Create a weight measurement",
    description="Create a new weight measurement for the authenticated user.",
)
async def create_weight_measurement(
    measurement: WeightMeasurementCreate,
    user: UserDetail = Depends(access_token_validation()),
) -> WeightMeasurementBrief:
    """Create a new weight measurement for the authenticated user.

    Args:
        measurement (WeightMeasurementCreate): The weight measurement data to be saved.
        user (UserDetail): The authenticated user creating the weight measurement.

    Returns:
        WeightMeasurementBrief: A response containing the created weight measurement.
    """
    # Save the weight measurement using the weight service
    return await weight_service.save_weight_measurement(user.id, measurement)
