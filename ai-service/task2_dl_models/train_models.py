import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Embedding, SimpleRNN, LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Configuration
MAX_LEN = 15
VOCAB_SIZE = 9  # 8 actions + 1 padding zero
EMBEDDING_DIM = 16
LSTM_UNITS = 32
DROPOUT_RATE = 0.2
EPOCHS = 20
BATCH_SIZE = 32
RANDOM_STATE = 42

def load_sequences(data_dir="data"):
    """Load sequences and labels"""
    X = np.load(f"{data_dir}/sequences_X.npy")
    y = np.load(f"{data_dir}/sequences_y.npy")
    return X, y

def build_rnn_model():
    """TASK 2: Model 1 - Simple RNN"""
    model = Sequential([
        Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
        SimpleRNN(LSTM_UNITS, return_sequences=False),
        Dropout(DROPOUT_RATE),
        Dense(1, activation='sigmoid')  # Binary classification
    ])
    return model

def build_lstm_model():
    """TASK 2: Model 2 - LSTM (Best Model)"""
    model = Sequential([
        Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
        LSTM(LSTM_UNITS, return_sequences=False),
        Dropout(DROPOUT_RATE),
        Dense(1, activation='sigmoid')
    ])
    return model

def build_bilstm_model():
    """TASK 2: Model 3 - BiLSTM"""
    model = Sequential([
        Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
        Bidirectional(LSTM(LSTM_UNITS, return_sequences=False)),
        Dropout(DROPOUT_RATE),
        Dense(1, activation='sigmoid')
    ])
    return model

def train_and_evaluate_model(model, model_name, X_train, X_test, y_train, y_test, save_dir="models"):
    """Train and evaluate a single model"""
    print(f"\n{'='*70}")
    print(f"📚 TRAINING: {model_name}")
    print(f"{'='*70}")
    
    # Compile
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # Train
    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate
    print(f"\n✅ {model_name} Evaluation:")
    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"  - Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  - Precision: {precision:.4f}")
    print(f"  - Recall:    {recall:.4f}")
    print(f"  - F1-Score:  {f1:.4f}")
    print(f"  - AUC-ROC:   {auc:.4f}")
    
    # Save model
    os.makedirs(save_dir, exist_ok=True)
    model_path = f"{save_dir}/{model_name.lower().replace(' ', '_')}.keras"
    model.save(model_path)
    print(f"  ✓ Model saved: {model_path}")
    
    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'auc_roc': float(auc)
    }
    
    return history, metrics, y_pred, y_pred_proba

def plot_training_history(histories, model_names, save_dir="plots"):
    """Plot training history for all models"""
    os.makedirs(save_dir, exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    for history, name in zip(histories, model_names):
        axes[0].plot(history.history['accuracy'], label=f"{name} - Train")
        axes[0].plot(history.history['val_accuracy'], label=f"{name} - Val", linestyle='--')
        
        axes[1].plot(history.history['loss'], label=f"{name} - Train")
        axes[1].plot(history.history['val_loss'], label=f"{name} - Val", linestyle='--')
    
    axes[0].set_title("Model Accuracy Comparison", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].set_title("Model Loss Comparison", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Loss")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = f"{save_dir}/training_history.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"✓ Plot saved: {plot_path}")
    plt.close()

def plot_model_comparison(metrics_dict, save_dir="plots"):
    """Plot comparison of all models"""
    os.makedirs(save_dir, exist_ok=True)
    
    models = list(metrics_dict.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(models))
    width = 0.2
    
    for i, metric in enumerate(metrics):
        values = [metrics_dict[model][metric] for model in models]
        ax.bar(x + i*width, values, width, label=metric.upper())
    
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Model Comparison (RNN vs LSTM vs BiLSTM)', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(True, axis='y', alpha=0.3)
    ax.set_ylim([0, 1])
    
    plt.tight_layout()
    plot_path = f"{save_dir}/model_comparison.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"✓ Plot saved: {plot_path}")
    plt.close()

def plot_confusion_matrix(y_test, y_pred, model_name, save_dir="plots"):
    """Plot confusion matrix"""
    os.makedirs(save_dir, exist_ok=True)
    
    cm = confusion_matrix(y_test, y_pred)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    
    ax.set_title(f'Confusion Matrix - {model_name}', fontsize=14, fontweight='bold')
    ax.set_ylabel('True Label')
    ax.set_xlabel('Predicted Label')
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        ax.text(j, i, format(cm[i, j], 'd'),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontsize=14, fontweight='bold')
    
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['No Purchase', 'Purchase'])
    ax.set_yticklabels(['No Purchase', 'Purchase'])
    
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    
    plot_path = f"{save_dir}/confusion_matrix_{model_name.lower()}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"✓ Confusion matrix saved: {plot_path}")
    plt.close()

def main():
    """Main training pipeline"""
    print("\n" + "="*70)
    print("🚀 TASK 2: Build & Train RNN, LSTM, BiLSTM Models")
    print("="*70)
    
    # Load data
    print("\n📥 Loading data...")
    X, y = load_sequences(data_dir="data")
    print(f"  - X shape: {X.shape}")
    print(f"  - y shape: {y.shape}")
    print(f"  - Class distribution: {np.bincount(y)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"\n  - Train: {X_train.shape[0]} samples")
    print(f"  - Test: {X_test.shape[0]} samples")
    
    # Build and train models
    models = [
        (build_rnn_model(), "Simple RNN"),
        (build_lstm_model(), "LSTM"),
        (build_bilstm_model(), "BiLSTM")
    ]
    
    histories = []
    metrics_dict = {}
    predictions_dict = {}
    
    for model, model_name in models:
        history, metrics, y_pred, y_pred_proba = train_and_evaluate_model(
            model, model_name, X_train, X_test, y_train, y_test
        )
        histories.append(history)
        metrics_dict[model_name] = metrics
        predictions_dict[model_name] = {'pred': y_pred, 'proba': y_pred_proba}
    
    # Determine best model
    best_model = max(metrics_dict.items(), key=lambda x: x[1]['accuracy'])
    print(f"\n{'='*70}")
    print(f"🏆 BEST MODEL: {best_model[0]}")
    print(f"   Accuracy: {best_model[1]['accuracy']:.4f}")
    print(f"{'='*70}")
    
    # Save best model as symbolic best
    os.makedirs("models", exist_ok=True)
    best_model_path = f"models/{best_model[0].lower().replace(' ', '_')}.keras"
    os.system(f"copy {best_model_path} models/model_best.keras")
    
    # Generate plots
    print("\n📊 Generating plots...")
    plot_training_history(histories, [m[1] for m in models])
    plot_model_comparison(metrics_dict)
    plot_confusion_matrix(y_test, predictions_dict["LSTM"]['pred'], "LSTM")
    
    # Save evaluation report
    report = {
        'model_configurations': {
            'max_len': MAX_LEN,
            'vocab_size': VOCAB_SIZE,
            'embedding_dim': EMBEDDING_DIM,
            'lstm_units': LSTM_UNITS,
            'dropout_rate': DROPOUT_RATE,
            'epochs': EPOCHS,
            'batch_size': BATCH_SIZE
        },
        'models_evaluation': metrics_dict,
        'best_model': best_model[0],
        'best_model_metrics': best_model[1]
    }
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/model_evaluation.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("✓ Evaluation report saved: reports/model_evaluation.json")
    
    print("\n" + "="*70)
    print("✅ TASK 2 COMPLETED!")
    print("="*70)

if __name__ == "__main__":
    main()
    
    user_input = Input(shape=(1,), name="user_input")
    user_embed = Embedding(num_users, 16, name="user_embedding")(user_input)
    user_vec = Flatten()(user_embed)
    
    prod_input = Input(shape=(1,), name="product_input")
    prod_embed = Embedding(num_products, 16, name="product_embedding")(prod_input)
    prod_vec = Flatten()(prod_embed)
    
    # NCF
    concat = Concatenate()([user_vec, prod_vec])
    dense_1 = Dense(32, activation='relu')(concat)
    dense_2 = Dense(16, activation='relu')(dense_1)
    output = Dense(1, activation='linear', name="rating_output")(dense_2) # Dự đoán Rating 1->5
    
    model = Model(inputs=[user_input, prod_input], outputs=output)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    X_user = df['user_id'].values
    X_prod = df['product_id'].values
    y = df['interaction_score'].values
    
    model.fit([X_user, X_prod], y, epochs=5, batch_size=64, validation_split=0.2, verbose=1)
    
    model.save(save_path)
    print(f"Lưu Model 2 tại {save_path}")

# 3. MODEL 3: CUSTOMER SEGMENTATION (AUTOENCODER + KMeans)
def build_and_train_segmentation(data_path="data/user_product_matrix.csv", save_path="models/autoencoder.keras"):
    print("\n--- TRAIN MODEL 3: AUTOENCODER SEGMENTATION ---")
    if not os.path.exists(data_path): return print("Dataset not found!")
    
    df = pd.read_csv(data_path)
    user_stats = df.groupby('user_id').agg({
        'interaction_score': 'mean',
        'user_age': 'first',
        'total_spend': 'first'
    }).reset_index()
    
    X = user_stats[['interaction_score', 'user_age', 'total_spend']].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Kiến trúc Autoencoder để nén dữ liệu
    input_dim = X_scaled.shape[1]
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(2, activation='relu')(input_layer) # Latent space: 2 chiều
    decoded = Dense(input_dim, activation='linear')(encoded)
    
    autoencoder = Model(inputs=input_layer, outputs=decoded)
    encoder = Model(inputs=input_layer, outputs=encoded) # Lấy riêng encoder
    
    autoencoder.compile(optimizer='adam', loss='mse')
    autoencoder.fit(X_scaled, X_scaled, epochs=10, batch_size=16, verbose=1)
    
    autoencoder.save(save_path)
    print(f"Lưu Model 3 (Autoencoder) tại {save_path}")
    
    # Kết hợp KMeans trên Latent Space (Không gian nén rút gọn chiều nhiễu)
    compressed_features = encoder.predict(X_scaled)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(compressed_features)
    
    user_stats['segment_cluster'] = clusters
    user_stats.to_csv("data/user_segments_result.csv", index=False)
    print("Đã phân loại xong hệ thống KMeans và xuất ra data/user_segments_result.csv")

if __name__ == "__main__":
    build_and_train_purchase_model()
    build_and_train_recommender()
    build_and_train_segmentation()
