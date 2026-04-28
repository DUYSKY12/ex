# Project KiemTra01: Laptop & Mobile Store

## 🏗️ Kiến trúc Hệ thống (Architecture)
Hệ thống được thiết kế theo mô hình Microservices với 1 API Gateway điều phối và 4 services nghiệp vụ chuyên biệt.

### 🛡️ Danh sách Services & Databases (Polyglot Persistence)
| Service | Công nghệ | Database | Chức năng |
|---------|------------|----------|-----------|
| **API Gateway** | Django / Proxy | N/A | Điều phối, tổng hợp dữ liệu (Aggregation) |
| **customer-service** | DRF | **MySQL** | Quản lý khách hàng, Hồ sơ, Giỏ hàng |
| **staff-service** | DRF | **MySQL** | Xác thực nhân viên, Lưu nhật ký hành động |
| **laptop-service** | DRF | **PostgreSQL** | Danh mục Laptop, Tồn kho |
| **mobile-service** | DRF | **PostgreSQL** | Danh mục Mobile, Tồn kho |

## 🚀 Hướng dẫn khởi động (Quick Start)

### 1. Điều kiện tiên quyết
- Cài đặt Docker & Docker Compose.
- Python 3.10+ (để chạy script hỗ trợ nếu cần).

### 2. Khởi động toàn bộ hệ thống
Sử dụng docker-compose để build và chạy tất cả containers cùng database:
```bash
cd kiemtra01
docker-compose up --build
```

### 3. Truy cập
| Thành phần | URL |
|------------|------|
| **Frontend (React)** | http://localhost:3000 |
| **API Gateway** | http://localhost:8000 |
| **Customer Service** | http://localhost:8001 |
| **Staff Service** | http://localhost:8002 |
| **Laptop Service** | http://localhost:8003 |
| **Mobile Service** | http://localhost:8004 |

## 🛒 Luồng nghiệp vụ chính
- **Dành cho Khách hàng**: Đăng nhập riêng biệt -> Tìm kiếm (API Gateway sẽ gọi song song Laptop/Mobile service) -> Thêm vào giỏ hàng (Lưu tại Customer service).
- **Dành cho Nhân viên**: Đăng nhập portal Staff -> Thêm mới sản phẩm -> Cập nhật cấu hình (Laptop/Mobile).

## 🎨 Frontend Tech Stack
- **React.js + Vite** (Mạnh mẽ, tốc độ cao).
- **Tailwind CSS** (Thiết kế hiện đại, responsive).
- **Lucide Icons** (Biểu tượng cao cấp).
- **2 Luồng Login tách biệt**: Đảm bảo bảo mật và giao diện cá nhân hóa cho từng đối tượng.
