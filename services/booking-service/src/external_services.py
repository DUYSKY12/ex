import os
import requests
import threading

ROOM_SERVICE_URL = os.getenv("ROOM_SERVICE_URL", "http://room-service:5000")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:5000")

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

def _send_notification_async(booking_id: str, user_id: str):
    try:
        requests.post(
            f"{NOTIFICATION_SERVICE_URL}/notifications",
            json={"booking_id": booking_id, "user_id": user_id, "type": "BOOKING_CONFIRMED"},
            timeout=5
        )
    except Exception as e:
        print(f"Async notification error: {e}")

def send_notification(booking_id: str, user_id: str):
    # Chạy ngầm trong một thread khác để không block request hiện tại (Fire-and-forget)
    thread = threading.Thread(target=_send_notification_async, args=(booking_id, user_id))
    thread.start()
