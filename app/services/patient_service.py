from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session
from app.models.patient import Patient


class PatientService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Patient]:
        return self.db.query(Patient).order_by(Patient.last_name, Patient.first_name).all()

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.db.query(Patient).filter(Patient.id == patient_id).first()

    def search(self, query: str) -> List[Patient]:
        q = f"%{query}%"
        return (
            self.db.query(Patient)
            .filter(
                Patient.first_name.ilike(q)
                | Patient.last_name.ilike(q)
                | Patient.phone.ilike(q)
                | Patient.email.ilike(q)
            )
            .order_by(Patient.last_name)
            .all()
        )

    def create(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        phone: str = "",
        email: str = "",
        address: str = "",
    ) -> Patient:
        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone=phone,
            email=email,
            address=address,
        )
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def update(
        self,
        patient_id: int,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        phone: str = "",
        email: str = "",
        address: str = "",
    ) -> Optional[Patient]:
        patient = self.get_by_id(patient_id)
        if not patient:
            return None
        patient.first_name = first_name
        patient.last_name = last_name
        patient.date_of_birth = date_of_birth
        patient.phone = phone
        patient.email = email
        patient.address = address
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def delete(self, patient_id: int) -> bool:
        patient = self.get_by_id(patient_id)
        if not patient:
            return False
        self.db.delete(patient)
        self.db.commit()
        return True
