from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.doctor import Doctor


class DoctorService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Doctor]:
        return self.db.query(Doctor).order_by(Doctor.last_name, Doctor.first_name).all()

    def get_by_id(self, doctor_id: int) -> Optional[Doctor]:
        return self.db.query(Doctor).filter(Doctor.id == doctor_id).first()

    def create(
        self,
        first_name: str,
        last_name: str,
        specialization: str,
        phone: str = "",
    ) -> Doctor:
        doctor = Doctor(
            first_name=first_name,
            last_name=last_name,
            specialization=specialization,
            phone=phone,
        )
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        return doctor

    def delete(self, doctor_id: int) -> bool:
        doctor = self.get_by_id(doctor_id)
        if not doctor:
            return False
        self.db.delete(doctor)
        self.db.commit()
        return True
