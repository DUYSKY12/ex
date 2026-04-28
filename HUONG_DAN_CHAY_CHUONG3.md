# Hướng Dẫn Chạy Chương 3: AI Service

## 1. Sinh Dữ Liệu

Chạy file `dataset_generator_ch3.py` để sinh tập dữ liệu 500 users, 50 laptops, 8 hành vi.

```bash
cd ai-service/task2_dl_models
python dataset_generator_ch3.py
```

Output: Tạo file `data/data_user500.csv` với ~8,000 bản ghi.

## 2. Huấn Luyện Mô Hình

Từ cùng thư mục `ai-service/task2_dl_models`, chạy file `train_models_ch3.py` để xây dựng và huấn luyện 3 mô hình RNN, LSTM, BiLSTM.

```bash
cd ai-service/task2_dl_models
python train_models_ch3.py
```

Quá trình huấn luyện sẽ mất thời gian. Output: Accuracy của từng mô hình, lưu mô hình vào `models/`.

## 3. Kết Quả Kỳ Vọng

- RNN: Accuracy ~70-75%
- LSTM: Accuracy ~75-80% ⭐ BEST
- BiLSTM: Accuracy ~73-78%

## 4. Phân Tích

Mô hình LSTM thường cho kết quả tốt nhất vì xử lý tốt phụ thuộc dài hạn trong chuỗi hành vi người dùng.

## Lưu Ý

- Cần cài đặt các thư viện trước khi chạy: `pip install -r ai-service/requirements.txt`
- Nếu chỉ muốn chạy chương 3, đảm bảo có ít nhất: `pip install tensorflow pandas scikit-learn`
- Đảm bảo thư mục `ai-service/task2_dl_models/data/` và `ai-service/task2_dl_models/models/` tồn tại trước khi chạy.
- Chạy từ đúng thư mục:

```powershell
cd d:\kiemtra01\ai-service\task2_dl_models
python train_models_ch3.py
```
