from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.appointment_service import AppointmentService, AppointmentStatus
from app.services.patient_service import PatientService
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/appointments", tags=["appointments"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def list_appointments(request: Request, db: Session = Depends(get_db)):
    appointments = AppointmentService(db).get_all()
    return templates.TemplateResponse(
        "appointments/list.html", {"request": request, "appointments": appointments}
    )


@router.get("/create", response_class=HTMLResponse)
def create_form(
    request: Request,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    patients = PatientService(db).get_all()
    doctors = DoctorService(db).get_all()
    return templates.TemplateResponse(
        "appointments/create.html",
        {
            "request": request,
            "patients": patients,
            "doctors": doctors,
            "selected_patient_id": patient_id,
        },
    )


@router.post("/create")
def create_appointment(
    patient_id: int = Form(...),
    doctor_id: int = Form(...),
    appointment_date: str = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    appt_dt = datetime.fromisoformat(appointment_date)
    AppointmentService(db).create(patient_id, doctor_id, appt_dt, notes)
    return RedirectResponse(f"/patients/{patient_id}", status_code=303)


@router.post("/{appointment_id}/update-status")
def update_status(
    appointment_id: int,
    status: str = Form(...),
    diagnosis: str = Form(""),
    db: Session = Depends(get_db),
):
    service = AppointmentService(db)
    appt = service.get_by_id(appointment_id)
    if appt:
        service.update_status(appointment_id, AppointmentStatus(status), diagnosis)
        return RedirectResponse(f"/patients/{appt.patient_id}", status_code=303)
    return RedirectResponse("/appointments/", status_code=303)


@router.post("/{appointment_id}/delete")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    service = AppointmentService(db)
    appt = service.get_by_id(appointment_id)
    patient_id = appt.patient_id if appt else None
    service.delete(appointment_id)
    if patient_id:
        return RedirectResponse(f"/patients/{patient_id}", status_code=303)
    return RedirectResponse("/appointments/", status_code=303)
