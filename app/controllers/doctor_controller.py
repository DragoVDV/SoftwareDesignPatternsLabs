from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["doctors"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def list_doctors(request: Request, db: Session = Depends(get_db)):
    doctors = DoctorService(db).get_all()
    return templates.TemplateResponse(
        "doctors/list.html", {"request": request, "doctors": doctors}
    )


@router.get("/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("doctors/create.html", {"request": request})


@router.post("/create")
def create_doctor(
    first_name: str = Form(...),
    last_name: str = Form(...),
    specialization: str = Form(...),
    phone: str = Form(""),
    db: Session = Depends(get_db),
):
    DoctorService(db).create(first_name, last_name, specialization, phone)
    return RedirectResponse("/doctors/", status_code=303)


@router.post("/{doctor_id}/delete")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    DoctorService(db).delete(doctor_id)
    return RedirectResponse("/doctors/", status_code=303)
