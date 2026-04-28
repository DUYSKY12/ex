# Auth Service

Xác thực và phân quyền người dùng cho hệ thống đặt phòng khách sạn.

## Overview

- Đăng ký / đăng nhập tài khoản
- Phát và xác thực JWT token
- Quản lý thông tin người dùng
- Phân quyền: `guest` và `admin`

## Tech Stack

| Component  | Choice                  |
|------------|-------------------------|
| Language   | Python 3.12             |
| Framework  | FastAPI                 |
| Database   | PostgreSQL (`db-auth`)  |

## API Endpoints

| Method | Endpoint          | Auth  | Description                   |
|--------|-------------------|-------|-------------------------------|
| GET    | `/health`         | —     | Health check                  |
| POST   | `/auth/register`  | —     | Đăng ký tài khoản mới         |
| POST   | `/auth/login`     | —     | Đăng nhập, nhận JWT token     |
| POST   | `/auth/verify`    | —     | Xác thực JWT token (internal) |
| GET    | `/users/me`       | JWT   | Lấy thông tin bản thân        |
| PUT    | `/users/me`       | JWT   | Cập nhật thông tin cá nhân    |
| GET    | `/users`          | Admin | Danh sách tất cả user         |

> Full API spec: [`docs/api-specs/auth-service.yaml`](../../docs/api-specs/auth-service.yaml)

## Running Locally

```bash
docker compose up auth-service --build
```

## Project Structure

```
auth-service/
├── Dockerfile
├── readme.md
├── requirements.txt
└── src/
    ├── main.py         # FastAPI app, health check
    ├── config.py       # Biến môi trường
    ├── database.py     # SQLAlchemy engine, session
    ├── models.py       # User model
    ├── schemas.py      # Pydantic schemas
    ├── security.py     # Hash password, JWT encode/decode
    └── routers/
        ├── auth.py     # /auth/register, /auth/login, /auth/verify
        └── users.py    # /users/me, /users
```

## Environment Variables

| Variable         | Description               | Default                                              |
|------------------|---------------------------|------------------------------------------------------|
| `DATABASE_URL`   | PostgreSQL connection URL | `postgresql://admin:changeme@db-auth:5432/auth_db`   |
| `JWT_SECRET`     | Secret key để ký JWT      | `your-super-secret-jwt-key`                          |
| `JWT_EXPIRES_IN` | Thời hạn token            | `7d`                                                 |
