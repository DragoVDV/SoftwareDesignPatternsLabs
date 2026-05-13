from abc import ABC, abstractmethod


class IImportRouter(ABC):

    @abstractmethod
    def import_data(self):
        pass

    @abstractmethod
    def health_check(self):
        pass
