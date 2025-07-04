# 🖐️ Gesture Air-Control Framework – Framework Điều Khiển Máy Tính Bằng Cử Chỉ Tay

🎯 A real-time computer vision framework that enables users to interact with the computer using only hand gestures captured via webcam.  
🎯 Một framework thị giác máy tính thời gian thực, cho phép người dùng tương tác với máy tính hoàn toàn bằng cử chỉ tay thông qua webcam.

---

## ✅ Features / Tính năng đã hiện thực hóa

| Feature | Mô tả |
|--------|------|
| ✏️ **Virtual Air-Painter** | Draw on air by using your index finger like a pen. <br> Vẽ trực tiếp lên không khí bằng ngón tay trỏ như một cây bút. |
| 🖱️ **Virtual Air-Mouse** | Control the system cursor: move, click, drag using gestures. <br> Điều khiển con trỏ chuột: di chuyển, nhấp, kéo thả bằng tay. |
| 🔊 **Volume Air-Control** | Change system volume based on finger distance. <br> Điều chỉnh âm lượng bằng cách thay đổi khoảng cách giữa các ngón tay. |
| 🔍 **Gesture Inspector** | Display live recognition of hand (left/right), fingers up, and key points. <br> Chẩn đoán và hiển thị nhận diện chi tiết bàn tay (trái/phải, số ngón, vị trí...). |

---

## ⚙️ Technologies Used / Công nghệ sử dụng

| Technology | Purpose / Mục đích |
|-----------|---------------------|
| Python 3.x | Main language / Ngôn ngữ chính |
| OpenCV | Image processing / Xử lý hình ảnh từ webcam |
| MediaPipe | Hand tracking with 21 landmark points / Theo dõi 21 điểm tay |
| PyAutoGUI | Control OS mouse and keyboard / Điều khiển chuột, bàn phím hệ điều hành |
| PyCAW | Audio volume control (Windows) / Điều khiển âm lượng trên Windows |
| Tkinter | GUI interface / Giao diện người dùng |

---

## 🧠 Architecture Highlights / Kiến trúc nổi bật

- 🧩 **Modular Design**: Each function (hand tracking, mouse, paint...) is built as an independent module – scalable & maintainable.  
  🎯 Thiết kế module hóa – dễ bảo trì, mở rộng hoặc tái sử dụng.
  
- 🔄 **Multithreading**: Camera input, logic, and GUI run on separate threads for low-latency, smooth performance.  
  🚀 Áp dụng đa luồng để giảm độ trễ và tăng độ mượt khi chạy thời gian thực.

- 📐 **Vector-based Gesture Recognition**: Uses vector math instead of simple rules to analyze relative finger positions for robust detection.  
  🧠 Nhận diện cử chỉ bằng toán học vector để tăng độ chính xác ở nhiều góc tay khác nhau.

- 🎨 **Interactive Feedback**: Cursor color, button highlight, and gesture visualization to enhance user experience.  
  ✨ Phản hồi trực quan giúp người dùng dễ hiểu và kiểm soát tốt.

---

## 🚀 How to Run / Cách chạy chương trình

### 1. Install dependencies / Cài đặt thư viện: 
pip install opencv-python mediapipe pyautogui pycaw numpy
### 2. Run / Chạy: 
python main_app.py
💡 Make sure your webcam is working.
💡 Đảm bảo webcam đang hoạt động.
## 📂 Project Structure / Cấu Trúc Thư Mục Dự Án
The project is organized with a modular architecture to ensure clarity, maintainability, and ease of future expansion.
Dự án được tổ chức theo kiến trúc module hóa để đảm bảo sự rõ ràng, dễ bảo trì và thuận tiện cho việc mở rộng trong tương lai.
```bash
Gesture-Control-Framework/
│
├── main.py
# 🇬🇧 The main entry point to run the application. It initializes the GUI (Tkinter),
#    starts the multithreading processes, and coordinates all controllers.
# 🇻🇳 File chính để chạy ứng dụng. Nó khởi tạo giao diện đồ họa (GUI),
#    bắt đầu các luồng xử lý và điều phối tất cả các controller.
│
├── modules/
│   # 🇬🇧 A Python package containing all the core logic of the application.
│   # 🇻🇳 Một package Python chứa toàn bộ logic cốt lõi của ứng dụng.
│   │
│   ├── __init__.py
│   │   # 🇬🇧 Marks 'modules' as a Python package.
│   # 🇻🇳 Đánh dấu thư mục 'modules' là một package Python.
│   │
│   ├── hand_tracker.py
│   │   # 🇬🇧 A dedicated module responsible for hand detection and tracking using MediaPipe.
│   │   #    It processes the camera feed and extracts hand landmarks.
│   # 🇻🇳 Module chuyên biệt chịu trách nhiệm phát hiện và theo dõi bàn tay bằng MediaPipe.
│   │   #    Nó xử lý luồng hình ảnh từ camera và trích xuất các điểm mốc của bàn tay.
│   │
│   └── controllers/
│       # 🇬🇧 A sub-package containing the logic for each specific feature.
│       # 🇻🇳 Một package con chứa logic cho từng tính năng cụ thể.
│       │
│       ├── __init__.py
│       │   # 🇬🇧 Marks 'controllers' as a Python sub-package.
│       # 🇻🇳 Đánh dấu thư mục 'controllers' là một package con của Python.
│       │
│       ├── drawing_controller.py
│       │   # 🇬🇧 Handles all logic for the "Virtual Painter" feature.
│       # 🇻🇳 Xử lý toàn bộ logic cho tính năng "Vẽ Ảo".
│       │
│       ├── mouse_controller.py
│       │   # 🇬🇧 Manages all logic for the "Virtual Mouse" feature, including cursor
│       │   #    movement and click actions.
│       # 🇻🇳 Quản lý toàn bộ logic cho tính năng "Chuột Ảo", bao gồm di chuyển
│       │   #    con trỏ và các hành động click.
│       │
│       ├── volume_controller.py
│       │   # 🇬🇧 Contains the logic for the "Volume Control" feature.
│       # 🇻🇳 Chứa logic cho tính năng "Điều Khiển Âm Lượng".
│       │
│       └── enhanced_finger_counter_controller.py
│           # 🇬🇧 A diagnostic tool to inspect gesture recognition, displaying
│           #    hand labels (Left/Right) and which fingers are up.
│       # 🇻🇳 Một công cụ chẩn đoán để kiểm tra khả năng nhận diện cử chỉ,
│           #    hiển thị nhãn tay (Trái/Phải) và các ngón tay đang giơ.
│
├── requirements.txt
# 🇬🇧 A file listing all the necessary Python libraries for the project.
#    Allows for easy one-step installation using `pip install -r requirements.txt`.
# 🇻🇳 File liệt kê tất cả các thư viện Python cần thiết cho dự án.
#    Cho phép cài đặt dễ dàng trong một bước bằng lệnh `pip install -r requirements.txt`.
│
├── README.md
# 🇬🇧 This file! It provides an overview of the project, setup instructions, and usage guide.
# 🇻🇳 Chính là file này! Cung cấp tổng quan về dự án, hướng dẫn cài đặt và sử dụng.
│
└── .gitignore (Optional / Tùy chọn)
    # 🇬🇧 A file that tells Git which files or folders to ignore in the project
    #    (e.g., __pycache__, virtual environment folders).
    # 🇻🇳 Một file để chỉ cho Git biết cần bỏ qua những file hoặc thư mục nào
    #    (ví dụ: __pycache__, thư mục môi trường ảo).
```
---

## 📈 Roadmap (v1 → v2) / Kế hoạch nâng cấp
- 🖐️ Add custom gesture sets (swipe, rotate…)
- 📺 Control external applications (PowerPoint, media player)
- 🧠 Integrate ML gesture classifier (custom training)
- 🌐 Cross-platform support (Linux/Mac)
- 🧪 Performance benchmarking & optimization

---

⚠️ Notes / Ghi chú
AI (like ChatGPT) was used as a support tool for code generation. However, architecture design, testing, bug fixing, and idea formulation were done manually.

---

Author: nnYunaXYZ
