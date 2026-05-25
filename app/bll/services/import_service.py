from datetime import datetime

from app.bll.interfaces.i_import_service import IImportService
from app.dal.interfaces.i_csv_repository import ICsvReader
from app.dal.interfaces.i_repository import IRepository
from app.dal.models.orm_models import Doctor, MedicalRecord, Patient, Room, User, Ward


def _parse_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


class ImportService(IImportService):

    def __init__(self, repository: IRepository, csv_reader: ICsvReader):
        self.repository = repository
        self.csv_reader = csv_reader

    def import_from_csv(self, file_path: str) -> dict:
        rows = self.csv_reader.read(file_path)

        patient_data: dict[str, dict] = {}
        doctor_data: dict[str, dict] = {}
        ward_data: dict[str, dict] = {}
        room_data: dict[tuple, dict] = {}
        patient_doctor_pairs: set[tuple] = set()
        patient_room: dict[str, tuple] = {}

        for row in rows:
            p_phone = row["patient_phone"]
            d_phone = row["doctor_phone"]
            ward_num = row["ward_number"]
            room_key = (ward_num, row["room_number"])

            if p_phone not in patient_data:
                patient_data[p_phone] = row
            if d_phone not in doctor_data:
                doctor_data[d_phone] = row
            if ward_num not in ward_data:
                ward_data[ward_num] = row
            if room_key not in room_data:
                room_data[room_key] = row

            patient_doctor_pairs.add((p_phone, d_phone))
            if p_phone not in patient_room:
                patient_room[p_phone] = room_key

        # Step 1: create User rows for patients and doctors, flush to get IDs
        patient_users: dict[str, User] = {
            phone: User(
                first_name=row["patient_first_name"],
                last_name=row["patient_last_name"],
                birth_date=_parse_date(row["patient_birth_date"]),
                phone=phone,
            )
            for phone, row in patient_data.items()
        }
        doctor_users: dict[str, User] = {
            phone: User(
                first_name=row["doctor_first_name"],
                last_name=row["doctor_last_name"],
                birth_date=_parse_date(row["doctor_birth_date"]),
                phone=phone,
            )
            for phone, row in doctor_data.items()
        }

        self.repository.add_all(list(patient_users.values()) + list(doctor_users.values()))
        self.repository.flush()

        # Step 2: create Patient and Doctor rows using the IDs from Step 1
        patients: dict[str, Patient] = {
            phone: Patient(id=user.id, insurance_policy=patient_data[phone]["patient_insurance"])
            for phone, user in patient_users.items()
        }
        doctors: dict[str, Doctor] = {
            phone: Doctor(id=user.id, specialization=doctor_data[phone]["doctor_specialization"])
            for phone, user in doctor_users.items()
        }

        self.repository.add_all(list(patients.values()) + list(doctors.values()))
        self.repository.flush()

        # Step 3: create Wards, flush to get IDs
        wards: dict[str, Ward] = {
            ward_num: Ward(
                capacity=int(row["ward_capacity"]),
                current_occupancy=int(row["ward_occupancy"]),
            )
            for ward_num, row in ward_data.items()
        }

        self.repository.add_all(list(wards.values()))
        self.repository.flush()

        # Step 4: create Rooms using ward IDs from Step 3
        rooms: dict[tuple, Room] = {
            room_key: Room(
                ward_id=wards[room_key[0]].ward_id,
                room_type=row["room_type"],
            )
            for room_key, row in room_data.items()
        }

        self.repository.add_all(list(rooms.values()))
        self.repository.flush()

        # Step 5: create MedicalRecords
        records = [
            MedicalRecord(
                patient_id=patients[row["patient_phone"]].id,
                doctor_id=doctors[row["doctor_phone"]].id,
                diagnosis=row["diagnosis"],
                date=_parse_date(row["record_date"]),
            )
            for row in rows
        ]

        self.repository.add_all(records)
        self.repository.flush()

        # Step 6: patient_doctors many-to-many
        for p_phone, d_phone in patient_doctor_pairs:
            patients[p_phone].doctors.append(doctors[d_phone])

        # Step 7: room_patients many-to-many (one room per patient)
        for p_phone, room_key in patient_room.items():
            rooms[room_key].patients.append(patients[p_phone])

        self.repository.commit()

        return {
            "patients": len(patients),
            "doctors": len(doctors),
            "wards": len(wards),
            "rooms": len(rooms),
            "medical_records": len(records),
            "patient_doctor_assignments": len(patient_doctor_pairs),
            "room_patient_assignments": len(patient_room),
        }
