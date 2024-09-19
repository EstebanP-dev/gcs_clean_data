from src import *
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Generic, TypeVar

T = TypeVar('T')


class ValueObject(ABC, Generic[T], BaseModel):
    value: T

    @abstractmethod
    def validate(self, value: T) -> Result[Success]:
        pass

    @abstractmethod
    def equals(self, other: T) -> bool:
        pass
