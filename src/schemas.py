from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, model_validator


def convert_datetime_to_gmt(dt: datetime) -> str:
    """
    Convert a datetime object to a string formatted in GMT (UTC).

    :param dt: The datetime object to convert.
    :type dt: datetime

    :return: The formatted datetime string in the format "%Y-%m-%dT%H:%M:%S%z".
    :rtype: str
    """
    # If the datetime is naive (no timezone), convert it to UTC.
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    # Format the datetime object as a string with the required format.
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomSchema(BaseModel):
    """
    A base model schema that provides custom validation and encoding behavior.

    :cvar model_config: Configuration settings for JSON encoding and field population.
    :vartype model_config: ConfigDict
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

        :param data: A dictionary containing field names and values.
        :type data: dict[str, Any]

        :return: A new dictionary with datetime fields' microseconds set to zero.
        :rtype: dict[str, Any]
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

        :param kwargs: Additional arguments to pass to the encoder.
        :type kwargs: Any

        :return: A dictionary containing only serializable fields.
        :rtype: dict[str, Any]
        """
        # Get the default dictionary representation using Pydantic's model_dump.
        default_dict = self.model_dump()

        # Encode the dictionary using FastAPI's JSON encoder to ensure all fields are serializable.
        return jsonable_encoder(default_dict)
