from ninja import Schema
from pydantic import Field
import datetime

class SomeModelUpdatePayload(Schema):
    """
    Schema for the payload when updating a SomeModel instance.
    """
    field_a: str = Field(..., max_length=10, example="text_val")
    field_b: int = Field(..., example=123)

class SomeModelResponse(Schema):
    """
    Schema for the response when returning a SomeModel instance.
    """
    id: int
    field_a: str
    field_b: int
    number_of_updates: int
    last_modified: datetime.datetime

    class Config:
        from_attributes = True
        