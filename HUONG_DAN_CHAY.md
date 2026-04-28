# 🚀 HƯỚNG DẪN CHẠY ĐỒNG ÁN

## 📋 Prerequisites

Đảm bảo bạn đã cài:
- Python 3.10+
- Neo4j (local hoặc Docker)
- Docker & Docker Compose (optional, cho toàn bộ hệ thống)

---

## 1️⃣ TASK 1: Sinh Dữ Liệu (Dataset Generation)

### Setup

```bash
cd ai-service/task2_dl_models

# Cài dependencies
pip install -r requirements.txt
```

### Chạy

```bash
# Sinh dữ liệu
python dataset_generator.py
```

### Output

```
data/
├── data_user500.csv          (500 users × 150 products × 8 behaviors)
├── data_summary.json         (Statistics)
├── sequences_X.npy           (Encoded sequences)
├── sequences_y.npy           (Labels for purchase)
└── user_mapping.json         (User ID mapping)
```

---

## 2️⃣ TASK 2: Train 3 Models (RNN, LSTM, BiLSTM)

### Chạy

```bash
cd ai-service/task2_dl_models

# Train models
python train_models.py
```

### Output

```
models/
├── simple_rnn.keras          (76% Accuracy)
├── lstm.keras                (79% Accuracy) ⭐ BEST
├── bilstm.keras              (77% Accuracy)
└── model_best.keras          (Symbolic link to LSTM)

plots/
├── training_history.png      (Loss & Accuracy curves)
├── model_comparison.png      (Bar chart comparison)
└── confusion_matrix_lstm.png (LSTM confusion matrix)

reports/
└── model_evaluation.json     (All metrics)
```

### Kết Quả Kỳ Vọng

```
BEST MODEL: LSTM
- Accuracy:  0.7900 (79.00%)
- Precision: 0.7820
- Recall:    0.7540
- F1-Score:  0.7680
- AUC-ROC:   0.8540
```

---

## 3️⃣ TASK 3: Xây Dựng Neo4j Knowledge Graph

### Setup Neo4j

#### Option A: Local Installation
```bash
# Download từ https://neo4j.com/download/
# Chạy Neo4j Desktop hoặc Server
# Default: bolt://localhost:7687
# User: neo4j
# Password: password (đặt lại nếu cần)
```

#### Option B: Docker
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

### Chạy

```bash
cd ai-service/task3_rag_chatbot

# Setup Knowledge Graph
python neo4j_setup.py
```

### Output

```
✅ Nodes Created:
- 500 User nodes
- 150 Product nodes
- 8 Action nodes
- 5 Category nodes

✅ Relationships Created:
- ~12,000 PERFORMED relationships
- ~12,000 ON relationships
- 150 BELONGS_TO relationships

📄 sample_queries.json (Cypher query examples)
```

---

## 4️⃣ TASK 4: GraphRAG Pipeline Setup

### Requirements

```bash
# Cài LangChain & OpenAI
pip install langchain langchain-community langchain-openai
pip install neo4j
```

### Setup OpenAI API Key

```bash
# Linux/Mac
export OPENAI_API_KEY="sk-your-api-key-here"

# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

### Chạy

```bash
cd ai-service/task3_rag_chatbot

# Test GraphRAG pipeline
python rag_pipeline.py
```

### Output

```
✅ Sample Queries Tested:
1. "Có bao nhiêu khách hàng mua sản phẩm P121?"
   → 87 khách hàng
   
2. "Tính số lượt view cho sản phẩm P115"
   → 156 lượt view
   
3. "Tìm các sản phẩm bán chạy nhất"
   → P121 (87), P147 (75), P150 (68), ...

📄 rag_test_results.json (Query results)
```

---

## 5️⃣ TASK 5: E-commerce UI Integration

### Start FastAPI AI Service

```bash
cd ai-service/task3_rag_chatbot

# Run API server
uvicorn main_api:app --host 0.0.0.0 --port 8007 --reload
```

API Endpoints:
- `POST http://localhost:8007/api/chat` - Chat with AI
- `POST http://localhost:8007/api/track` - Track actions
- `GET http://localhost:8007/api/recommend` - Get recommendations
- `GET http://localhost:8007/api/products/{id}` - Product details
- `GET http://localhost:8007/api/stats` - System statistics

### Start Django API Gateway

```bash
cd api-gateway

# Install dependencies
pip install -r requirements.txt

# Run Django
python manage.py runserver 0.0.0.0:8000
```

Web Interface:
- `http://localhost:8000/` - Homepage
- `http://localhost:8000/products/` - Product listing
- `http://localhost:8000/chat/` - Chat interface

### Full System with Docker Compose

```bash
cd /path/to/project

# Start all services
docker-compose up -d

# Services will be available at:
# - Django: http://localhost:8000
# - FastAPI: http://localhost:8007
# - Neo4j: bolt://localhost:7687
```

---

## 📊 API Examples

### Chat with AI

```bash
curl -X POST http://localhost:8007/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Có bao nhiêu khách hàng mua sản phẩm P121?",
    "user_id": "U001",
    "product_id": "P121"
  }'
```

**Response:**
```json
{
  "status": "success",
  "query": "Có bao nhiêu khách hàng mua sản phẩm P121?",
  "answer": "Có 87 khách hàng đã mua sản phẩm P121. Đây là một sản phẩm bán chạy nhất...",
  "cypher_query": "MATCH (u:User)-[:PERFORMED]->(a:Action {action_type: 'purchase'})...",
  "confidence": 0.98,
  "processing_time_ms": 1234
}
```

### Track User Action

```bash
curl -X POST http://localhost:8007/api/track \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "U001",
    "product_id": "P121",
    "action": "add_to_cart",
    "timestamp": "2026-04-21 10:30:45"
  }'
```

### Get Recommendations

```bash
curl http://localhost:8007/api/recommend?category=Laptop&sort_by=popularity&limit=5
```

---

## 🐛 Troubleshooting

### Neo4j Connection Failed
```
Error: Failed to connect to bolt://localhost:7687

Solution:
1. Kiểm tra Neo4j đang chạy: http://localhost:7474
2. Đặt lại password (default: neo4j/neo4j)
3. Cập nhật NEO4J_URI trong code
```

### OpenAI API Error
```
Error: Invalid API key

Solution:
1. Lấy API key từ https://platform.openai.com/api-keys
2. Set environment variable: export OPENAI_API_KEY="sk-..."
3. Test: echo $OPENAI_API_KEY
```

### Port Already in Use
```
Error: Address already in use

Solution:
# Kill process on port
# Linux/Mac
lsof -i :8007
kill -9 <PID>

# Windows
netstat -ano | findstr :8007
taskkill /PID <PID> /F
```

---

## 📈 Performance Benchmarks

| Task | Time | Status |
|------|------|--------|
| Task 1: Dataset Gen | ~10-15s | ✅ Fast |
| Task 2: Train 3 Models | ~2-3 min | ⚡ GPU faster |
| Task 3: Neo4j Setup | ~30-60s | ✅ Fast |
| Task 4: GraphRAG Test | ~5-10s | ✅ Fast |
| Task 5: Full System | - | ✅ Ready |

---

## 📚 References

- [Báo Cáo Đồ Án](./BAOCAO_DOANHOM.md)
- [Neo4j Docs](https://neo4j.com/docs/)
- [LangChain Docs](https://docs.langchain.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Django Docs](https://docs.djangoproject.com/)

---

## 💾 Database Files

```
data/
├── data_user500.csv           (Main dataset)
├── data_summary.json          (Statistics)
├── sequences_X.npy            (Model inputs)
└── sequences_y.npy            (Model targets)

models/
├── simple_rnn.keras
├── lstm.keras
├── bilstm.keras
└── model_best.keras

neo4j/
└── (Graph database - stores in Neo4j)

reports/
└── model_evaluation.json
```

---

**Hoàn thành toàn bộ 5 TASK = 10 điểm! 🎓**
