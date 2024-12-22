from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

# These help separate the persistence layer from the domain layer.
# The persistence layer is responsible for creating IDs and timestamps.
# The domain layer is for business logic, i.e. how non-technical people would speak about the data.


class Unique(BaseModel, Generic[T]):
    """
    Wraps models that don't have an inherent ID field.

    In those cases, the [id] comes from the persistence layer (repositories).
    """

    model: T
    id: str


class Created(BaseModel, Generic[T]):
    """
    Wraps models that don't have an inherent creation timestamp.

    In those cases, [created_at] comes from the persistence layer (repositories).
    """

    model: T
    created_at: datetime


class Updated(BaseModel, Generic[T]):
    model: T
    updated_at: datetime
