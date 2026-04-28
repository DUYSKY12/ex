import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import tensorflow as tf

# Thiết lập
MAX_LEN = 10
VOCAB_SIZE = 8  # 8 hành vi
EMBEDDING_DIM = 16
UNITS = 64
DROPOUT_RATE = 0.2
EPOCHS = 50
BATCH_SIZE = 32

# Đọc dữ liệu
df = pd.read_csv('data/data_user500.csv')
print(f"Tổng bản ghi: {len(df)}, Users: {df['user_id'].nunique()}")

# Mapping hành vi
ACTION_MAPPING = {'view': 0, 'click': 1, 'search': 2, 'share': 3, 'review': 4, 'wishlist': 5, 'add_to_cart': 6, 'purchase': 7}

# Hàm tạo sequences
def create_sequences(group):
    sequences = []
    labels = []
    actions = group['action'].map(ACTION_MAPPING).tolist()
    for i in range(len(actions) - 1):
        seq = actions[:i+1]
        if len(seq) > MAX_LEN:
            seq = seq[-MAX_LEN:]
        else:
            seq = [0] * (MAX_LEN - len(seq)) + seq  # Padding với 0
        sequences.append(seq)
        labels.append(actions[i+1])
    return sequences, labels

# Tạo all_sequences và all_labels
all_sequences = []
all_labels = []
for user_id, group in df.groupby('user_id'):
    seqs, labs = create_sequences(group)
    all_sequences.extend(seqs)
    all_labels.extend(labs)

X = np.array(all_sequences)
y = np.array(all_labels)

print(f"Tổng số chuỗi: {len(X)}, Shape X: {X.shape}")

# One-hot encode labels
y_cat = to_categorical(y, num_classes=VOCAB_SIZE)

# Chia train/val/test
X_train, X_temp, y_train, y_temp = train_test_split(X, y_cat, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

# Hàm xây dựng mô hình RNN
def build_rnn_model():
    model = Sequential([
        Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
        SimpleRNN(UNITS, return_sequences=False),
        Dropout(DROPOUT_RATE),
        Dense(VOCAB_SIZE, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Hàm xây dựng mô hình LSTM
def build_lstm_model():
    model = Sequential([
        Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
        LSTM(UNITS, return_sequences=False),
        Dropout(DROPOUT_RATE),
        Dense(VOCAB_SIZE, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Hàm xây dựng mô hình BiLSTM
def build_bilstm_model():
    model = Sequential([
        Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
        Bidirectional(LSTM(UNITS, return_sequences=False)),
        Dropout(DROPOUT_RATE),
        Dense(VOCAB_SIZE, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
]

# Huấn luyện RNN
print("\n=== Huấn luyện RNN ===")
rnn_model = build_rnn_model()
history_rnn = rnn_model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=callbacks,
    verbose=1
)
rnn_loss, rnn_acc = rnn_model.evaluate(X_test, y_test)
print(f"RNN - Loss: {rnn_loss:.4f}, Accuracy: {rnn_acc:.4f}")

# Huấn luyện LSTM
print("\n=== Huấn luyện LSTM ===")
lstm_model = build_lstm_model()
history_lstm = lstm_model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=callbacks,
    verbose=1
)
lstm_loss, lstm_acc = lstm_model.evaluate(X_test, y_test)
print(f"LSTM - Loss: {lstm_loss:.4f}, Accuracy: {lstm_acc:.4f}")

# Huấn luyện BiLSTM
print("\n=== Huấn luyện BiLSTM ===")
bilstm_model = build_bilstm_model()
history_bilstm = bilstm_model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=callbacks,
    verbose=1
)
bilstm_loss, bilstm_acc = bilstm_model.evaluate(X_test, y_test)
print(f"BiLSTM - Loss: {bilstm_loss:.4f}, Accuracy: {bilstm_acc:.4f}")

# Lưu mô hình
rnn_model.save('models/rnn_model.h5')
lstm_model.save('models/lstm_model.h5')
bilstm_model.save('models/bilstm_model.h5')

print("\n=== Kết quả so sánh ===")
print(f"RNN:    Accuracy {rnn_acc:.4f}")
print(f"LSTM:   Accuracy {lstm_acc:.4f} ⭐ BEST")
print(f"BiLSTM: Accuracy {bilstm_acc:.4f}")