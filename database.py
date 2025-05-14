import json
import os

DATABASE_FILE = 'doctor_database.json'

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return {"Diabetes": [
        {"name": "Dr. Anshu Malli", "specialization": "Endocrinologist", "contact": "+977-9801234567",
         "available_hours": {"start": "09:00", "end": "14:00"}},
        {"name": "Dr. Bishnu Prasad", "specialization": "Diabetologist", "contact": "+977-9812345678",
         "available_hours": {"start": "10:00", "end": "16:00"}},
        {"name": "Dr. Meera Thapa", "specialization": "Internal Medicine Specialist", "contact": "+977-9841122334",
         "available_hours": {"start": "11:00", "end": "17:00"}},
        {"name": "Dr. Sita Ghimire", "specialization": "Endocrinologist", "contact": "+977-9807654321",
         "available_hours": {"start": "08:00", "end": "13:00"}},
        {"name": "Dr. Niraj Sharma", "specialization": "Diabetes Specialist", "contact": "+977-9865432109",
         "available_hours": {"start": "13:00", "end": "18:00"}}
    ]}

def save_database(database):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(database, f, indent=4)