"""
Скрипт для заповнення бази даних тестовими даними.
Запуск: python seed_data.py
"""
from datetime import date, datetime
from app.database import SessionLocal, engine
from app.models import Base, Patient, Doctor, Appointment
from app.services.patient_service import PatientService
from app.services.doctor_service import DoctorService
from app.services.appointment_service import AppointmentService
from app.models.appointment import AppointmentStatus

Base.metadata.create_all(bind=engine)

db = SessionLocal()

print("Заповнення бази даних тестовими даними...\n")

# --- Лікарі ---
doctor_service = DoctorService(db)
doctors_raw = [
    ("Олександр", "Петренко", "Терапевт", "+380501234567"),
    ("Наталія",   "Коваленко", "Кардіолог", "+380502345678"),
    ("Василь",    "Мельник",   "Хірург",    "+380503456789"),
    ("Ірина",     "Шевченко",  "Невролог",  "+380504567890"),
    ("Дмитро",    "Бойко",     "Педіатр",   "+380505678901"),
]

doctors = []
for fn, ln, spec, phone in doctors_raw:
    d = doctor_service.create(fn, ln, spec, phone)
    doctors.append(d)
    print(f"  [Лікар] {d.last_name} {d.first_name} — {d.specialization}")

# --- Пацієнти ---
patient_service = PatientService(db)
patients_raw = [
    ("Микола",    "Іваненко",   date(1985, 3, 15),  "+380671111111", "mykola@gmail.com",   "м. Київ, вул. Хрещатик, 1"),
    ("Олена",     "Бондаренко", date(1992, 7, 22),  "+380672222222", "olena@gmail.com",    "м. Київ, вул. Лесі Українки, 5"),
    ("Андрій",    "Ткаченко",   date(1978, 11, 8),  "+380673333333", "",                   "м. Харків, просп. Науки, 12"),
    ("Ганна",     "Савченко",   date(2000, 1, 30),  "+380674444444", "hanna@ukr.net",      "м. Львів, вул. Франка, 3"),
    ("Богдан",    "Лисенко",    date(1965, 5, 12),  "+380675555555", "bohdan@ukr.net",     "м. Одеса, вул. Дерибасівська, 7"),
    ("Тетяна",    "Кравченко",  date(1990, 9, 4),   "+380676666666", "tetyana@gmail.com",  "м. Дніпро, вул. Гагаріна, 14"),
    ("Сергій",    "Мороз",      date(1972, 2, 18),  "+380677777777", "",                   "м. Запоріжжя, просп. Соборний, 33"),
]

patients = []
for fn, ln, dob, phone, email, addr in patients_raw:
    p = patient_service.create(fn, ln, dob, phone, email, addr)
    patients.append(p)
    print(f"  [Пацієнт] {p.last_name} {p.first_name}")

# --- Прийоми ---
appt_service = AppointmentService(db)
appointments_raw = [
    (patients[0], doctors[0], datetime(2024, 10, 5, 9, 0),   "Загальне нездужання, слабкість"),
    (patients[0], doctors[1], datetime(2024, 11, 12, 11, 0), "Болі в грудях"),
    (patients[1], doctors[0], datetime(2024, 11, 15, 10, 30), "Кашель, температура 38.2"),
    (patients[2], doctors[2], datetime(2024, 12, 3, 8, 0),   "Консультація перед операцією"),
    (patients[3], doctors[3], datetime(2024, 12, 8, 14, 0),  "Головний біль, запаморочення"),
    (patients[4], doctors[0], datetime(2024, 12, 10, 9, 30), "Профілактичний огляд"),
    (patients[5], doctors[1], datetime(2024, 12, 15, 13, 0), "Контроль тиску"),
    (patients[6], doctors[4], datetime(2024, 12, 18, 16, 0), "Запис на консультацію"),
]

appointments = []
for p, d, dt, notes in appointments_raw:
    a = appt_service.create(p.id, d.id, dt, notes)
    appointments.append(a)
    print(f"  [Прийом] {p.last_name} → {d.last_name} ({dt.strftime('%d.%m.%Y')})")

# Завершуємо деякі прийоми
appt_service.update_status(appointments[0].id, AppointmentStatus.completed, "Астенічний синдром, вітаміни")
appt_service.update_status(appointments[1].id, AppointmentStatus.completed, "Нейроциркуляторна дистонія")
appt_service.update_status(appointments[2].id, AppointmentStatus.completed, "ГРВІ, призначено лікування")
appt_service.update_status(appointments[4].id, AppointmentStatus.cancelled)

db.close()
print("\nТестові дані успішно завантажено!")
print("Запустіть сервер: uvicorn app.main:app --reload")
