from fastapi import Depends
from sqlalchemy.orm import Session

from app.bll.services.import_service import ImportService
from app.dal.database import get_db
from app.dal.repositories.csv_reader import CsvReader
from app.dal.repositories.sql_repository import SqlRepository


def get_import_service(db: Session = Depends(get_db)) -> ImportService:
    repository = SqlRepository(db)
    csv_reader = CsvReader()
    return ImportService(repository=repository, csv_reader=csv_reader)
