import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

USER_ID = "11111111-1111-1111-1111-111111111111"
ROOM_ID = "22222222-2222-2222-2222-222222222222"

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_my_bookings_unauthorized(client: TestClient):
    response = client.get("/bookings")
    assert response.status_code == 401

@patch("src.routers.bookings.get_room")
@patch("src.routers.bookings.update_room_status")
def test_create_booking_success(mock_update, mock_get_room, client: TestClient):
    # Mock behavior of Room Service
    mock_get_room.return_value = {
        "id": ROOM_ID,
        "status": "available",
        "price_per_night": 100
    }
    mock_update.return_value = True

    response = client.post(
        "/bookings",
        json={
            "room_id": ROOM_ID,
            "check_in": "2026-06-01",
            "check_out": "2026-06-03"
        },
        headers={"X-User-Id": USER_ID}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["room_id"] == ROOM_ID
    assert data["total_price"] == 200.0
    assert data["status"] == "pending"

def test_get_my_bookings_authorized(client: TestClient):
    response = client.get("/bookings", headers={"X-User-Id": USER_ID})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["data"][0]["status"] == "pending"

@patch("src.routers.bookings.send_notification")
def test_confirm_booking(mock_send, client: TestClient):
    # Get the booking first
    resp1 = client.get("/bookings", headers={"X-User-Id": USER_ID})
    booking_id = resp1.json()["data"][0]["id"]
    
    # Confirm it
    payment_id = "33333333-3333-3333-3333-333333333333"
    response = client.patch(
        f"/bookings/{booking_id}/confirm",
        json={"payment_id": payment_id}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"
    assert response.json()["payment_id"] == payment_id
    
    # Notification should be called
    mock_send.assert_called_once()

@patch("src.routers.bookings.update_room_status")
def test_cancel_booking(mock_update, client: TestClient):
    # Get the booking first
    resp1 = client.get("/bookings", headers={"X-User-Id": USER_ID})
    booking_id = resp1.json()["data"][0]["id"]
    
    # Cancel it
    mock_update.return_value = True
    response = client.patch(
        f"/bookings/{booking_id}/cancel",
        headers={"X-User-Id": USER_ID}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"

def test_get_all_bookings_admin(client: TestClient):
    response = client.get("/bookings/all", headers={"X-User-Role": "admin"})
    assert response.status_code == 200
    assert response.json()["total"] >= 1
