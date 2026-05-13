from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.models import Base, Patient, Doctor, Appointment  # noqa: registers models
from app.controllers import patient_controller, doctor_controller, appointment_controller

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Реєстратура клініки")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(patient_controller.router)
app.include_router(doctor_controller.router)
app.include_router(appointment_controller.router)


@app.get("/")
def index():
    return RedirectResponse("/patients/")
