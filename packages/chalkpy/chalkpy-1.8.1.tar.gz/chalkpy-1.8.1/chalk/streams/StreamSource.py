from typing import Type, TypeVar

from pydantic import BaseModel
from typing_extensions import Protocol

T = TypeVar("T")


class StreamSource(Protocol[T]):
    Message: Type[T]
    consumer_config: BaseModel
