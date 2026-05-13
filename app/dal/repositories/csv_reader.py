import csv
from app.dal.interfaces.i_csv_repository import ICsvReader


class CsvReader(ICsvReader):

    def read(self, file_path: str) -> list[dict]:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
