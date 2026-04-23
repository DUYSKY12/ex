import os
import requests

ROOM_SERVICE_URL = os.getenv("ROOM_SERVICE_URL", "http://room-service:5000")

def get_room(room_id: str):
    response = requests.get(f"{ROOM_SERVICE_URL}/rooms/{room_id}")
    if response.status_code == 200:
        return response.json()
    return None

def update_room_status(room_id: str, status: str):
    response = requests.patch(
        f"{ROOM_SERVICE_URL}/rooms/{room_id}/status",
        json={"status": status}
    )
    return response.status_code == 200
