# Room Service

Quản lý thông tin phòng khách sạn.

## Overview

- CRUD đầy đủ cho phòng khách sạn
- Tìm phòng trống theo khoảng ngày check-in/check-out
- Cập nhật trạng thái phòng (available / booked / maintenance)
- Phân quyền Admin qua header `X-User-Role`

## Tech Stack

| Component  | Choice         |
|------------|----------------|
| Language   | Python 3.12    |
| Framework  | FastAPI        |
| Database   | PostgreSQL (`db-room`) |

## API Endpoints

| Method | Endpoint                    | Auth  | Description                          |
|--------|-----------------------------|-------|--------------------------------------|
| GET    | `/health`                   | —     | Health check                         |
| GET    | `/rooms`                    | —     | Danh sách phòng (filter status, type)|
| GET    | `/rooms/available`          | —     | Tìm phòng trống theo ngày            |
| GET    | `/rooms/{id}`               | —     | Chi tiết phòng                       |
| POST   | `/rooms`                    | Admin | Tạo phòng mới                        |
| PUT    | `/rooms/{id}`               | Admin | Cập nhật thông tin phòng             |
| DELETE | `/rooms/{id}`               | Admin | Xóa phòng                            |
| PATCH  | `/rooms/{id}/status`        | —     | Cập nhật trạng thái (internal)       |

> Full API spec: [`docs/api-specs/room-service.yaml`](../../docs/api-specs/room-service.yaml)

## Running Locally

```bash
docker compose up room-service --build
```

## Project Structure

```
room-service/
├── Dockerfile
├── readme.md
├── requirements.txt
└── src/
    ├── main.py         # FastAPI app, health check
    ├── config.py       # Biến môi trường
    ├── database.py     # SQLAlchemy engine, session
    ├── models.py       # Room model
    ├── schemas.py      # Pydantic schemas
    └── routers/
        └── rooms.py    # Tất cả endpoints /rooms
```

## Environment Variables

| Variable       | Description               | Default                                              |
|----------------|---------------------------|------------------------------------------------------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://admin:changeme@db-room:5432/room_db`   |
