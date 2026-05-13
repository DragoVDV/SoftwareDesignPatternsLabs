from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Table, CheckConstraint
from sqlalchemy.orm import relationship
from app.dal.database import Base


patient_doctors_table = Table(
    "patient_doctors",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
    Column("doctor_id", Integer, ForeignKey("doctors.id", ondelete="CASCADE"), primary_key=True),
)

room_patients_table = Table(
    "room_patients",
    Base.metadata,
    Column("room_id", Integer, ForeignKey("rooms.room_id", ondelete="CASCADE"), primary_key=True),
    Column("patient_id", Integer, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    phone = Column(String(20))


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    insurance_policy = Column(String(255))

    user = relationship("User", foreign_keys=[id])
    medical_records = relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan")
    doctors = relationship("Doctor", secondary=patient_doctors_table, back_populates="patients")
    rooms = relationship("Room", secondary=room_patients_table, back_populates="patients")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    specialization = Column(String(255))

    user = relationship("User", foreign_keys=[id])
    medical_records = relationship("MedicalRecord", back_populates="doctor")
    patients = relationship("Patient", secondary=patient_doctors_table, back_populates="doctors")


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True)
    diagnosis = Column(Text)
    date = Column(Date, nullable=False)

    patient = relationship("Patient", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")


class Ward(Base):
    __tablename__ = "wards"

    ward_id = Column(Integer, primary_key=True, autoincrement=True)
    capacity = Column(Integer, nullable=False)
    current_occupancy = Column(Integer, nullable=False, default=0)

    rooms = relationship("Room", back_populates="ward", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("capacity > 0", name="ck_ward_capacity"),
        CheckConstraint("current_occupancy >= 0", name="ck_ward_occupancy"),
    )


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    ward_id = Column(Integer, ForeignKey("wards.ward_id", ondelete="CASCADE"), nullable=False)
    room_type = Column(String(100))

    ward = relationship("Ward", back_populates="rooms")
    patients = relationship("Patient", secondary=room_patients_table, back_populates="rooms")
