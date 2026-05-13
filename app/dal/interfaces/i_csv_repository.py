from abc import ABC, abstractmethod


class ICsvReader(ABC):

    @abstractmethod
    def read(self, file_path: str) -> list[dict]:
        pass
