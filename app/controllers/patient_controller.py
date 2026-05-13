from datetime import date
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.patient_service import PatientService
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/patients", tags=["patients"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def list_patients(request: Request, search: str = "", db: Session = Depends(get_db)):
    service = PatientService(db)
    patients = service.search(search) if search else service.get_all()
    return templates.TemplateResponse(
        "patients/list.html",
        {"request": request, "patients": patients, "search": search},
    )


@router.get("/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("patients/create.html", {"request": request})


@router.post("/create")
def create_patient(
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: date = Form(...),
    phone: str = Form(""),
    email: str = Form(""),
    address: str = Form(""),
    db: Session = Depends(get_db),
):
    PatientService(db).create(first_name, last_name, date_of_birth, phone, email, address)
    return RedirectResponse("/patients/", status_code=303)


@router.get("/{patient_id}", response_class=HTMLResponse)
def patient_detail(patient_id: int, request: Request, db: Session = Depends(get_db)):
    patient = PatientService(db).get_by_id(patient_id)
    if not patient:
        return RedirectResponse("/patients/", status_code=303)
    appointments = AppointmentService(db).get_by_patient(patient_id)
    return templates.TemplateResponse(
        "patients/detail.html",
        {"request": request, "patient": patient, "appointments": appointments},
    )


@router.get("/{patient_id}/edit", response_class=HTMLResponse)
def edit_form(patient_id: int, request: Request, db: Session = Depends(get_db)):
    patient = PatientService(db).get_by_id(patient_id)
    if not patient:
        return RedirectResponse("/patients/", status_code=303)
    return templates.TemplateResponse(
        "patients/edit.html", {"request": request, "patient": patient}
    )


@router.post("/{patient_id}/edit")
def edit_patient(
    patient_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: date = Form(...),
    phone: str = Form(""),
    email: str = Form(""),
    address: str = Form(""),
    db: Session = Depends(get_db),
):
    PatientService(db).update(patient_id, first_name, last_name, date_of_birth, phone, email, address)
    return RedirectResponse(f"/patients/{patient_id}", status_code=303)


@router.post("/{patient_id}/delete")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    PatientService(db).delete(patient_id)
    return RedirectResponse("/patients/", status_code=303)
