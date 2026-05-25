from abc import ABC, abstractmethod
from typing import Any


class IRepository(ABC):

    @abstractmethod
    def add_all(self, items: list[Any]) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass
