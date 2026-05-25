from typing import Any
from sqlalchemy.orm import Session
from app.dal.interfaces.i_repository import IRepository


class SqlRepository(IRepository):

    def __init__(self, db: Session):
        self.db = db

    def add_all(self, items: list[Any]) -> None:
        self.db.add_all(items)

    def flush(self) -> None:
        self.db.flush()

    def commit(self) -> None:
        self.db.commit()
