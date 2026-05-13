from abc import ABC, abstractmethod


class IImportService(ABC):

    @abstractmethod
    def import_from_csv(self, file_path: str) -> dict:
        pass
