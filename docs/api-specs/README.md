# 🌐 Hotel Booking API Specifications (OpenAPI 3.0)

Thư mục này chứa toàn bộ thiết kế giao diện lập trình ứng dụng (API) cho hệ thống Microservices **Hotel Booking**. Tất cả các file được viết theo chuẩn **OpenAPI 3.0.3**.

## 📑 Danh sách Services

1. **Auth Service** (`auth-service.yaml`): Xử lý đăng ký, đăng nhập và quản lý User. Xác thực bằng JWT.
2. **Room Service** (`room-service.yaml`): Tìm kiếm và quản lý thông tin phòng khách sạn. Cung cấp API nội bộ để khóa phòng.
3. **Booking Service** (`booking-service.yaml`): Xử lý luồng đặt phòng, hủy phòng (Orchestrator trong Saga pattern).
4. **Payment Service** (`payment-service.yaml`): Xử lý thanh toán, hoàn tiền và thông báo xác nhận giao dịch.
5. **Notification Service** (`notification-service.yaml`): Xử lý gửi email xác nhận đặt phòng qua SMTP (Mailhog).

## 🚀 Hướng dẫn xem API với Swagger UI (Review với nhóm)

Thay vì phải đọc file `.yaml` dưới dạng văn bản (rất khó nhìn), bạn có thể chạy một giao diện **Swagger UI** chuyên nghiệp ngay trên máy cá nhân bằng Docker để Review cùng với nhóm.

### Bước 1: Khởi động Swagger UI
Mở Terminal, trỏ vào thư mục `docs/api-specs` này và chạy lệnh:
```bash
docker compose up -d
```

### Bước 2: Truy cập Giao diện
Mở trình duyệt và truy cập:
👉 **[http://localhost:8081](http://localhost:8081)**

Tại góc trên cùng bên phải của giao diện Swagger UI, bạn sẽ thấy một danh sách thả xuống (Dropdown). Hãy bấm vào đó để chọn và xem API của từng Service (Auth, Room, Booking, Payment, Notification).

### Bước 3: Tắt Swagger UI
Sau khi xem xong, chạy lệnh sau để dọn dẹp:
```bash
docker compose down
```

---

## 🔒 Quy chuẩn API chung của Hệ thống

Để đảm bảo tính nhất quán giữa các Microservices, toàn bộ hệ thống tuân thủ các quy tắc sau:

### 1. Phân trang (Pagination)
Các API lấy danh sách (VD: `/rooms`, `/bookings`) đều phải sử dụng `page` và `limit` qua Query Parameters. Dữ liệu trả về luôn bọc trong object `data` kèm metadata:
```json
{
  "data": [ ... ],
  "total": 100,
  "page": 1,
  "limit": 20
}
```

### 2. Xác thực nội bộ (Identity Translation)
- **Từ Client đến Gateway**: Gửi `Authorization: Bearer <JWT>`.
- **Từ Gateway đến các Services (Room, Booking, Payment)**: Gateway tự động giải mã JWT, bóc thông tin user và truyền xuống qua Headers nội bộ:
  - `X-User-Id`: ID của user đang đăng nhập.
  - `X-User-Role`: `guest` hoặc `admin`.
- Do đó, trong các file YAML của Room, Booking, Payment... scheme bảo mật không dùng `BearerAuth` mà dùng `InternalHeader` (`X-User-Id` / `X-User-Role`).

### 3. Cấu trúc Lỗi (Error Response)
Bất kỳ lỗi HTTP nào (400, 401, 403, 404, 409...) cũng đều phải trả về cấu trúc JSON đồng nhất:
```json
{
  "error": "Tên lỗi ngắn gọn (VD: Validation Failed)",
  "message": "Mô tả chi tiết lỗi bằng tiếng Việt để hiển thị lên Frontend"
}
```
