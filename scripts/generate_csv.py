import csv
import os
import random
from datetime import date, timedelta

SPECIALIZATIONS = [
    "Cardiology", "Neurology", "Orthopedics", "Pediatrics",
    "General Practice", "Surgery", "Oncology", "Psychiatry",
    "Radiology", "Dermatology",
]

DIAGNOSES = [
    "Hypertension", "Type 2 Diabetes", "Acute Respiratory Infection",
    "Coronary Artery Disease", "Chronic Back Pain", "Migraine",
    "Asthma", "Pneumonia", "Appendicitis", "Fracture",
    "Depression", "Anxiety Disorder", "Hypothyroidism", "Anemia",
    "Urinary Tract Infection", "Gastroenteritis", "Arthritis",
    "Stroke", "Epilepsy", "GERD",
]

ROOM_TYPES = ["Standard", "ICU", "Emergency", "Recovery", "Isolation"]

WARDS = [
    {"ward_number": "1", "ward_capacity": 20, "ward_occupancy": 15},
    {"ward_number": "2", "ward_capacity": 15, "ward_occupancy": 12},
    {"ward_number": "3", "ward_capacity": 25, "ward_occupancy": 20},
    {"ward_number": "4", "ward_capacity": 10, "ward_occupancy": 8},
    {"ward_number": "5", "ward_capacity": 30, "ward_occupancy": 25},
]

ROOMS = [
    {
        "ward_number": w["ward_number"],
        "room_number": str(r),
        "room_type": ROOM_TYPES[(int(str(w["ward_number"])) + r) % len(ROOM_TYPES)],
    }
    for w in WARDS
    for r in range(1, 5)
]

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer",
    "Michael", "Linda", "Olena", "Mykola", "Ivan", "Tetiana",
    "Andriy", "Natalia", "Dmytro", "Oksana", "Volodymyr", "Iryna",
    "Bohdan", "Yulia", "Serhiy", "Maryna", "Vasyl", "Halyna",
    "Oleg", "Svitlana", "Viktor", "Larysa", "Artem", "Daryna",
]

LAST_NAMES = [
    "Kovalenko", "Shevchenko", "Bondarenko", "Tkachenko", "Kravchenko",
    "Melnyk", "Lysenko", "Petrenko", "Savchenko", "Kovalchuk",
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Marchenko", "Moroz", "Litvinenko", "Yakovenko", "Zinchenko",
]


def _random_date(start_year: int = 2022, end_year: int = 2025) -> str:
    start = date(start_year, 1, 1)
    delta = date(end_year, 12, 31) - start
    return (start + timedelta(days=random.randint(0, delta.days))).isoformat()


def _random_birth_date() -> str:
    start = date(1950, 1, 1)
    delta = date(2000, 12, 31) - start
    return (start + timedelta(days=random.randint(0, delta.days))).isoformat()


def _build_people(count: int, phone_prefix: str) -> list[dict]:
    people = []
    used_phones = set()
    for i in range(count):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        phone = f"+380{phone_prefix}{str(i).zfill(7)}"
        while phone in used_phones:
            suffix = str(i + random.randint(1000, 9999)).zfill(7)
            phone = f"+380{phone_prefix}{suffix}"
        used_phones.add(phone)
        people.append({
            "first_name": first,
            "last_name": last,
            "birth_date": _random_birth_date(),
            "phone": phone,
        })
    return people


def generate_csv(output_path: str, num_records: int = 1000) -> None:
    dir_name = os.path.dirname(output_path) or "."
    os.makedirs(dir_name, exist_ok=True)

    patients = _build_people(100, "50")
    doctors = _build_people(20, "67")

    for i, d in enumerate(doctors):
        d["specialization"] = SPECIALIZATIONS[i % len(SPECIALIZATIONS)]

    for i, p in enumerate(patients):
        p["insurance_policy"] = f"INS-{str(i + 1).zfill(6)}"
        p["room"] = ROOMS[i % len(ROOMS)]

    fieldnames = [
        "record_date", "diagnosis",
        "patient_phone", "patient_first_name", "patient_last_name",
        "patient_birth_date", "patient_insurance",
        "doctor_phone", "doctor_first_name", "doctor_last_name",
        "doctor_birth_date", "doctor_specialization",
        "ward_number", "ward_capacity", "ward_occupancy",
        "room_number", "room_type",
    ]

    ward_lookup = {w["ward_number"]: w for w in WARDS}
    rows = []

    for _ in range(num_records):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        room = patient["room"]
        ward = ward_lookup[room["ward_number"]]

        rows.append({
            "record_date": _random_date(),
            "diagnosis": random.choice(DIAGNOSES),
            "patient_phone": patient["phone"],
            "patient_first_name": patient["first_name"],
            "patient_last_name": patient["last_name"],
            "patient_birth_date": patient["birth_date"],
            "patient_insurance": patient["insurance_policy"],
            "doctor_phone": doctor["phone"],
            "doctor_first_name": doctor["first_name"],
            "doctor_last_name": doctor["last_name"],
            "doctor_birth_date": doctor["birth_date"],
            "doctor_specialization": doctor["specialization"],
            "ward_number": ward["ward_number"],
            "ward_capacity": ward["ward_capacity"],
            "ward_occupancy": ward["ward_occupancy"],
            "room_number": room["room_number"],
            "room_type": room["room_type"],
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows -> {output_path}")


if __name__ == "__main__":
    generate_csv("data/data.csv")
