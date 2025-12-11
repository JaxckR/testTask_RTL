from dataclasses import dataclass
from typing import Generic, TypeVar

IdType = TypeVar("IdType")


@dataclass
class IDEntity(Generic[IdType]):
    id: IdType
