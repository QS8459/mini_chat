from pydantic.generics import GenericModel
from typing import List, TypeVar, Generic, Type, Optional
T = TypeVar('T', bound=GenericModel)


class GlobalResponseSchema(GenericModel, Generic[T]):
    count: Optional[int]
    next: Optional[str] = None
    result: List[T]

    class Config:
        from_attributes = True

