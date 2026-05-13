from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.models.appointment import Appointment, AppointmentStatus


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Appointment]:
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.patient), joinedload(Appointment.doctor))
            .order_by(Appointment.appointment_date.desc())
            .all()
        )

    def get_by_patient(self, patient_id: int) -> List[Appointment]:
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.doctor))
            .filter(Appointment.patient_id == patient_id)
            .order_by(Appointment.appointment_date.desc())
            .all()
        )

    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.patient), joinedload(Appointment.doctor))
            .filter(Appointment.id == appointment_id)
            .first()
        )

    def create(
        self,
        patient_id: int,
        doctor_id: int,
        appointment_date: datetime,
        notes: str = "",
    ) -> Appointment:
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            notes=notes,
            status=AppointmentStatus.scheduled,
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def update_status(
        self,
        appointment_id: int,
        status: AppointmentStatus,
        diagnosis: str = "",
    ) -> Optional[Appointment]:
        appt = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appt:
            return None
        appt.status = status
        if diagnosis:
            appt.diagnosis = diagnosis
        self.db.commit()
        self.db.refresh(appt)
        return appt

    def delete(self, appointment_id: int) -> bool:
        appt = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appt:
            return False
        self.db.delete(appt)
        self.db.commit()
        return True
