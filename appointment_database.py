import json
import os

APPOINTMENT_FILE = 'appointment_database.json'

def load_appointments():
    try:
        if os.path.exists(APPOINTMENT_FILE):
            with open(APPOINTMENT_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading appointments: {e}")
    
    # Return empty appointment list if file doesn't exist
    return []

def save_appointments(appointments):
    try:
        with open(APPOINTMENT_FILE, 'w') as f:
            json.dump(appointments, f, indent=4, default=str)  # default=str handles datetime objects
        return True
    except Exception as e:
        print(f"Error saving appointments: {e}")
        return False