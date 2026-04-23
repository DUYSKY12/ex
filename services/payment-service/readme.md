# Payment Service

Xử lý thanh toán và hoàn tiền cho hệ thống đặt phòng khách sạn.

## Overview

- Tạo giao dịch thanh toán cho booking
- Xác nhận thanh toán thành công → gọi Booking Service confirm
- Hoàn tiền khi booking bị hủy
- Lưu lịch sử toàn bộ giao dịch

## Tech Stack

| Component  | Choice |
|------------|--------|
| Language   | *(your choice)* |
| Framework  | *(your choice)* |
| Database   | PostgreSQL (`db-payment`) |

## API Endpoints

| Method | Endpoint                 | Auth  | Description                        |
|--------|--------------------------|-------|------------------------------------|
| GET    | `/health`                | —     | Health check                       |
| POST   | `/payments`              | JWT   | Tạo thanh toán cho booking         |
| GET    | `/payments/{id}`         | JWT   | Chi tiết giao dịch                 |
| GET    | `/payments/my`           | JWT   | Lịch sử thanh toán của user        |
| POST   | `/payments/{id}/refund`  | JWT   | Hoàn tiền cho giao dịch            |
| GET    | `/payments`              | Admin | Tất cả giao dịch trong hệ thống    |

> Full API spec: [`docs/api-specs/payment-service.yaml`](../../docs/api-specs/payment-service.yaml)

## Inter-service Calls

| Gọi tới         | Mục đích                                        |
|-----------------|-------------------------------------------------|
| Booking Service | Xác nhận booking sau khi thanh toán thành công  |
| Auth Service    | Xác thực JWT token (qua Gateway)                |

## Running Locally

```bash
docker compose up payment-service --build
```

## Project Structure

```
payment-service/
├── Dockerfile
├── readme.md
└── src/
```

## Environment Variables

| Variable               | Description                   |
|------------------------|-------------------------------|
| `DATABASE_URL`         | PostgreSQL connection URL     |
| `BOOKING_SERVICE_URL`  | `http://booking-service:5000` |
| `AUTH_SERVICE_URL`     | `http://auth-service:5000`    |
