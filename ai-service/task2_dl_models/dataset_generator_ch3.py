import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Thiết lập seed để tái tạo
np.random.seed(42)
random.seed(42)

# Số lượng
NUM_USERS = 500
NUM_PRODUCTS = 50
ACTIONS = ['view', 'click', 'search', 'share', 'review', 'wishlist', 'add_to_cart', 'purchase']

# Mapping hành vi
ACTION_MAPPING = {action: i for i, action in enumerate(ACTIONS)}

# Sinh dữ liệu
data = []
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 3, 31)

for user_id in range(1, NUM_USERS + 1):
    user_actions = []
    num_actions = random.randint(10, 25)  # Trung bình 16 hành vi/user

    current_date = start_date
    for _ in range(num_actions):
        product_id = random.randint(1, NUM_PRODUCTS)
        action = random.choice(ACTIONS)
        timestamp = current_date + timedelta(days=random.randint(0, 89))
        user_actions.append({
            'user_id': f'U{user_id:03d}',
            'product_id': f'LP{product_id:03d}',
            'action': action,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
        current_date = timestamp

    # Sắp xếp theo thời gian
    user_actions.sort(key=lambda x: x['timestamp'])
    data.extend(user_actions)

# Tạo DataFrame
df = pd.DataFrame(data)

# Lưu file
df.to_csv('data/data_user500.csv', index=False)

# Thống kê
print(f"Tổng số bản ghi: {len(df)}")
print(f"Số người dùng: {df['user_id'].nunique()}")
print(f"Số sản phẩm: {df['product_id'].nunique()}")
print(f"Phân bố hành vi:\n{df['action'].value_counts()}")

# Xuất 20 dòng mẫu
print("\n20 dòng mẫu:")
print(df.head(20).to_string(index=False))