import pandas as pd
import numpy as np
import os
import random
import json
from datetime import datetime, timedelta
from tensorflow.keras.preprocessing.sequence import pad_sequences

def generate_user_behavior_dataset(output_dir="data", num_users=500, num_products=150):
    """
    TASK 1: Sinh ra tập dữ liệu data_user500.csv với 500 users + 8 behaviors
    Format: user_id, product_id, action, timestamp
    Actions: view, click, search, share, review, wishlist, add_to_cart, purchase
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("=" * 70)
    print("📊 TASK 1: Sinh ra tập dữ liệu (Dataset Generation)")
    print("=" * 70)
    print(f"📈 Tạo Dataset với {num_users} users × {num_products} products × 8 behaviors...")
    
    # 8 hành động khách hàng trong e-commerce
    actions = ["view", "click", "search", "share", "review", "wishlist", "add_to_cart", "purchase"]
    
    # Xác suất chuyển đổi hành động (Funnel Logic)
    action_conversion_prob = {
        "view": 1.0,           # 100% - tất cả bắt đầu bằng view
        "click": 0.65,         # 65% view → click
        "search": 0.45,        # 45% search
        "share": 0.15,         # 15% share (optional)
        "review": 0.25,        # 25% review
        "wishlist": 0.35,      # 35% wishlist
        "add_to_cart": 0.50,   # 50% add_to_cart
        "purchase": 0.30,      # 30% purchase
    }
    
    interactions = []
    start_date = datetime(2026, 4, 1, 0, 0, 0)
    
    print(f"\n🔄 Tạo dữ liệu theo từng user...")
    # Tạo dữ liệu theo từng user
    for user_id in range(1, num_users + 1):
        user_label = f"U{user_id:03d}"  # U001, U002, ..., U500
        
        # Mỗi user thực hiện 15-40 hành động
        num_actions_per_user = random.randint(15, 40)
        
        for action_idx in range(num_actions_per_user):
            # Chọn action theo funnel probability
            if random.random() < action_conversion_prob["view"]:
                action = "view"
            elif random.random() < action_conversion_prob["click"]:
                action = "click"
            elif random.random() < action_conversion_prob["search"]:
                action = "search"
            elif random.random() < action_conversion_prob["share"]:
                action = "share"
            elif random.random() < action_conversion_prob["review"]:
                action = "review"
            elif random.random() < action_conversion_prob["wishlist"]:
                action = "wishlist"
            elif random.random() < action_conversion_prob["add_to_cart"]:
                action = "add_to_cart"
            else:
                action = "purchase"
            
            product_id = f"P{random.randint(1, num_products):03d}"  # P001-P150
            
            # Tạo timestamp (tăng dần trong 30 ngày)
            timestamp = start_date + timedelta(seconds=random.randint(0, 86400 * 30))
            
            interactions.append({
                "user_id": user_label,
                "product_id": product_id,
                "action": action,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        if user_id % 100 == 0:
            print(f"   ✓ Generated {user_id} users...")
    
    df_interactions = pd.DataFrame(interactions)
    dataset_file = f"{output_dir}/data_user500.csv"
    df_interactions.to_csv(dataset_file, index=False)
    
    print(f"\n✅ Tạo file: {dataset_file}")
    print(f"   - Total Rows: {len(df_interactions)}")
    print(f"   - Columns: {list(df_interactions.columns)}")
    
    # 📊 DATA VALIDATION & STATISTICS
    print("\n" + "=" * 70)
    print("📋 VALIDATION & STATISTICS")
    print("=" * 70)
    
    print("\n✓ Dataset Overview:")
    print(f"  - Total Interactions: {len(df_interactions):,}")
    print(f"  - Unique Users: {df_interactions['user_id'].nunique()}")
    print(f"  - Unique Products: {df_interactions['product_id'].nunique()}")
    print(f"  - Date Range: {df_interactions['timestamp'].min()} to {df_interactions['timestamp'].max()}")
    
    print("\n✓ Action Distribution:")
    action_counts = df_interactions['action'].value_counts().sort_values(ascending=False)
    for action, count in action_counts.items():
        percentage = (count / len(df_interactions)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  - {action:15s}: {count:6d} ({percentage:5.2f}%) {bar}")
    
    print("\n✓ Data Quality:")
    missing = df_interactions.isnull().sum()
    if missing.sum() == 0:
        print("  - No missing values ✅")
    else:
        print(missing)
    
    # Export statistics to JSON
    stats_file = f"{output_dir}/data_summary.json"
    stats_dict = {
        "total_interactions": len(df_interactions),
        "unique_users": int(df_interactions['user_id'].nunique()),
        "unique_products": int(df_interactions['product_id'].nunique()),
        "date_range": {
            "start": df_interactions['timestamp'].min(),
            "end": df_interactions['timestamp'].max()
        },
        "action_distribution": action_counts.to_dict(),
        "missing_values": missing.to_dict()
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats_dict, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Export Statistics: {stats_file}")
    
    return df_interactions

def generate_sequences_for_models(output_dir="data", max_len=15):
    """
    Tạo sequence data cho RNN/LSTM/BiLSTM models
    Input: Chuỗi hành vi của từng user (time-series)
    Output: Encoded sequences (1-8) với padding, Label (0/1 purchase)
    """
    print("\n" + "=" * 70)
    print("🔄 Tạo Sequence Data cho RNN/LSTM/BiLSTM Models")
    print("=" * 70)
    
    df = pd.read_csv(f"{output_dir}/data_user500.csv")
    df = df.sort_values('timestamp')  # Sắp xếp theo thời gian
    
    # Encode actions to numbers
    action_encoding = {
        "view": 1,
        "click": 2,
        "search": 3,
        "share": 4,
        "review": 5,
        "wishlist": 6,
        "add_to_cart": 7,
        "purchase": 8
    }
    
    # Tạo sequences cho mỗi user
    sequences = []
    labels = []  # Label = 1 nếu user có action "purchase", 0 nếu không
    user_ids = []
    
    for user_id in df['user_id'].unique():
        user_data = df[df['user_id'] == user_id].sort_values('timestamp')
        user_actions = user_data['action'].values
        
        # Encode actions
        encoded_seq = [action_encoding.get(a, 0) for a in user_actions]
        
        # Determine label: 1 if purchase exists, 0 otherwise
        label = 1 if "purchase" in user_actions else 0
        
        sequences.append(encoded_seq)
        labels.append(label)
        user_ids.append(user_id)
    
    # Pad sequences to max_len
    X = pad_sequences(sequences, maxlen=max_len, padding='pre', value=0)
    y = np.array(labels)
    
    # Save to files
    np.save(f"{output_dir}/sequences_X.npy", X)
    np.save(f"{output_dir}/sequences_y.npy", y)
    
    # Save user mapping
    user_mapping = {i: uid for i, uid in enumerate(user_ids)}
    with open(f"{output_dir}/user_mapping.json", 'w') as f:
        json.dump(user_mapping, f)
    
    print(f"✅ Saved sequences:")
    print(f"   - X shape: {X.shape} (samples={X.shape[0]}, sequence_len={X.shape[1]})")
    print(f"   - y shape: {y.shape}")
    label_dist = np.bincount(y)
    print(f"   - Label distribution: {label_dist} (Class 0: {label_dist[0]}, Class 1: {label_dist[1]})")
    
    return X, y

def generate_datasets(output_dir="data"):
    """Main function - Generate all datasets"""
    # Generate main dataset
    df = generate_user_behavior_dataset(output_dir=output_dir)
    
    # Generate sequences for models
    X, y = generate_sequences_for_models(output_dir=output_dir)
    
    print("\n" + "=" * 70)
    print("✅ TASK 1 COMPLETED - All datasets generated successfully!")
    print("=" * 70)
    print("\n📦 Output Files:")
    print(f"  ✓ {output_dir}/data_user500.csv")
    print(f"  ✓ {output_dir}/data_summary.json")
    print(f"  ✓ {output_dir}/sequences_X.npy")
    print(f"  ✓ {output_dir}/sequences_y.npy")
    print(f"  ✓ {output_dir}/user_mapping.json")

if __name__ == "__main__":
    generate_datasets()
