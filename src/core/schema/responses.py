from pydantic import BaseModel
from typing import (
    List,
    TypeVar,
    Generic,
    Optional
)
T = TypeVar('T', bound=BaseModel)


class GlobalResponseSchema(BaseModel, Generic[T]):
    count: Optional[int]
    next: Optional[str] = None
    result: List[T]

    class Config:
        from_attributes = True

