from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, model_validator


def convert_datetime_to_gmt(dt: datetime) -> str:
    """
    Convert a datetime object to a string formatted in GMT (UTC).

    Args:
        dt (datetime): The datetime object to convert.

    Returns:
        str: The formatted datetime string in the format "%Y-%m-%dT%H:%M:%S%z".
    """
    # If the datetime is naive (no timezone), convert it to UTC.
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    # Format the datetime object as a string with the required format.
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomSchema(BaseModel):
    """
    A base model schema that provides custom validation and encoding behavior.

    Attributes:
        model_config (ConfigDict): Configuration settings for JSON encoding and field population.
    """

    model_config = ConfigDict(
        json_encoders={datetime: convert_datetime_to_gmt},
        populate_by_name=True,
    )

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        """
        Remove microseconds from all datetime fields in the data dictionary.

        Args:
            data (dict[str, Any]): A dictionary containing field names and values.

        Returns:
            dict[str, Any]: A new dictionary with datetime fields' microseconds set to zero.
        """
        # Find and replace datetime fields' microseconds with zero to ensure consistency.
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(v, datetime)
        }

        # Return the modified data dictionary, merging changes.
        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs: Any) -> dict[str, Any]:
        """
        Return a dictionary representation of the model, including only serializable fields.

        Args:
            **kwargs (Any): Additional arguments to pass to the encoder.

        Returns:
            dict[str, Any]: A dictionary containing only serializable fields.
        """
        # Get the default dictionary representation using Pydantic's model_dump.
        default_dict = self.model_dump()

        # Encode the dictionary using FastAPI's JSON encoder to ensure all fields are serializable.
        return jsonable_encoder(default_dict)
