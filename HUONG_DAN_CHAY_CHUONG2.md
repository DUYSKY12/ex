# Hướng Dẫn Chạy Các Service Cho Chương 2

Các service được triển khai bằng Django REST Framework.

## Cài Đặt Chung

1. Tạo virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate`
3. Install: `pip install django djangorestframework djangorestframework-simplejwt`

## Chạy Từng Service

Mỗi service chạy trên port riêng:

- product-service: port 8001
- user-service: port 8002
- cart-service: port 8003
- order-service: port 8004
- payment-service: port 8005
- shipping-service: port 8006

Ví dụ cho product-service:

1. `cd product-service`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py runserver 8001`

Tương tự cho các service khác, thay port.

## API Endpoints

- Product: http://localhost:8001/products/
- User: http://localhost:8002/auth/register/
- Cart: http://localhost:8003/cart/add/
- Order: http://localhost:8004/orders/checkout/
- Payment: http://localhost:8005/payments/pay/
- Shipping: http://localhost:8006/shipments/create_shipment/

## Lưu Ý

Đây là code mẫu minh họa cho tiểu luận chương 2. Trong thực tế, cần tích hợp API Gateway và database riêng cho từng service.