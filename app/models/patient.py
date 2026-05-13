from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone = Column(String(20), default="")
    email = Column(String(100), default="")
    address = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship(
        "Appointment", back_populates="patient", cascade="all, delete-orphan"
    )
