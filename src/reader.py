import csv
import json
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "311_Cases_20260513.csv"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "output.json"

FIELDS = [
    "CaseID", "Opened", "Closed", "Status",
    "Responsible Agency", "Category", "Request Type",
    "Request Details", "Address", "Neighborhood",
]


def read_dataset(limit: int = 100) -> list[dict]:
    records = []
    with open(DATASET_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            records.append({field: row.get(field, "") for field in FIELDS})
    return records


def save_to_file(records: list[dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"[Reader] Saved {len(records)} records to {OUTPUT_PATH}")
