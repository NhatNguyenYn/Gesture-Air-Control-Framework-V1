# 🖐️ Gesture Control Framework – Framework Điều Khiển Máy Tính Bằng Cử Chỉ Tay

🎯 A real-time computer vision framework that enables users to interact with the computer using only hand gestures captured via webcam.  
🎯 Một framework thị giác máy tính thời gian thực, cho phép người dùng tương tác với máy tính hoàn toàn bằng cử chỉ tay thông qua webcam.

---

## ✅ Features / Tính năng đã hiện thực hóa

| Feature | Mô tả |
|--------|------|
| ✏️ **Virtual Painter** | Draw on screen by using your index finger like a pen. <br> Vẽ trực tiếp lên màn hình bằng ngón tay trỏ như một cây bút. |
| 🖱️ **Virtual Mouse** | Control the system cursor: move, click, drag using gestures. <br> Điều khiển con trỏ chuột: di chuyển, nhấp, kéo thả bằng tay. |
| 🔊 **Volume Control** | Change system volume based on finger distance. <br> Điều chỉnh âm lượng bằng cách thay đổi khoảng cách giữa các ngón tay. |
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
```bash
pip install opencv-python mediapipe pyautogui pycaw numpy
2. Run / Chạy: python main_app.py
💡 Make sure your webcam is working.
💡 Đảm bảo webcam đang hoạt động.
```bash
📁 Folder Structure / Cấu trúc thư mục
gesture-control-framework/
├── main_app.py             # Main entry point / Điểm chạy chính
├── controllers/            # Gesture modules (mouse, painter, volume...)
├── hand_tracker/           # Hand tracking & gesture recognition
├── gui/                    # GUI & visual elements
├── assets/                 # Icons, images, sample data
├── utils/                  # Common helper functions
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```
---

📈 Roadmap (v1 → v2) / Kế hoạch nâng cấp
🖐️ Add custom gesture sets (swipe, rotate…)
📺 Control external applications (PowerPoint, media player)
🧠 Integrate ML gesture classifier (custom training)
🌐 Cross-platform support (Linux/Mac)
🧪 Performance benchmarking & optimization

---

⚠️ Notes / Ghi chú
This is a summer research project by a student entering university (HCMUS – University of Science).
Một dự án mùa hè cá nhân của học sinh chuẩn bị bước vào đại học (ĐH Khoa học Tự nhiên – ĐHQG TP.HCM).
AI (like ChatGPT) was used as a support tool for code generation. However, architecture design, testing, bug fixing, and idea formulation were done manually.

---

Author: nnYunaXYZ
