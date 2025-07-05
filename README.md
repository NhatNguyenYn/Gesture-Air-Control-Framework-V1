# 🖐️ Gesture Air-Control Framework

> 🇻🇳 Điều khiển máy tính không chạm bằng cử chỉ tay qua webcam
> 🇬🇧 Touchless gesture-based PC control using real-time hand tracking

---

## 🎯 Overview | Tổng quan

**Gesture Air-Control Framework** là một framework thị giác máy tính thời gian thực cho phép người dùng tương tác với máy tính chỉ bằng cử chỉ tay, sử dụng webcam. Dự án tập trung vào sự linh hoạt, hiệu suất và khả năng mở rộng, phục vụ mục đích học tập, trình diễn công nghệ và nghiên cứu giao diện người – máy (HCI).

This is a real-time computer vision framework that enables gesture-based PC interaction through webcam input. It is designed to be modular, performant, and extensible — perfect for learning, showcasing, and HCI experimentation.

---

## ✅ Features | Tính năng chính

| Feature                | Description                                                               |
| ---------------------- | ------------------------------------------------------------------------- |
| ✏️ Virtual Air-Painter | Draw in the air using your index finger like a pen                        |
| 🖱️ Virtual Air-Mouse  | Move cursor, click, drag using natural hand gestures                      |
| 🔊 Volume Air-Control  | Adjust system volume by measuring finger distance                         |
| 🔍 Gesture Inspector   | Display live hand recognition (left/right hand, fingers up, landmarks...) |

---

## ⚙️ Technologies Used | Công nghệ sử dụng

| Technology | Purpose                                |
| ---------- | -------------------------------------- |
| Python 3.x | Main programming language              |
| OpenCV     | Video capture and image processing     |
| MediaPipe  | 21-point hand tracking                 |
| PyAutoGUI  | Mouse and keyboard control             |
| PyCAW      | Audio volume adjustment (Windows only) |
| Tkinter    | GUI display (for menu/config)          |

---

## 🧠 Architecture Highlights | Kiến trúc nổi bật

* 🧩 **Modular Design** – Each function (hand tracking, mouse, volume...) is isolated in its own controller class → easier to scale.
* 🔄 **Multithreading** – Camera processing, GUI, and logic run on separate threads for low-latency performance.
* 📐 **Vector-based Gesture Recognition** – More precise and angle-independent than hard-coded heuristics.
* ✨ **Visual Feedback** – Live overlay, cursor color changes, gesture highlights, UI cues.

---

## 🚀 How to Run | Cách chạy chương trình

### 1. Cài đặt thư viện:

```bash
pip install opencv-python mediapipe pyautogui pycaw numpy
```

### 2. Chạy chương trình:

```bash
python main_app.py
```

Ensure your webcam is connected and active.

---

## 📂 Project Structure | Cấu trúc thư mục

```
Gesture-Control-Framework/
│
├── main.py                     # Main application entry (init UI, threading, routing)
├── modules/                    # Core logic modules
│   ├── __init__.py
│   ├── hand_tracker.py         # Hand detection & landmark tracking (MediaPipe)
│   └── controllers/
│       ├── __init__.py
│       ├── drawing_controller.py     # Logic for air drawing
│       ├── mouse_controller.py       # Gesture to mouse control
│       ├── volume_controller.py      # Gesture-based volume logic
│       └── enhanced_finger_counter_controller.py  # Diagnostic tool (hand label, finger count)
├── requirements.txt            # Dependency list
├── README.md                   # Project overview and usage
└── .gitignore                  # Ignore cache, venv, etc.
```

---

## 📈 Roadmap | Kế hoạch phát triển

* 🖐️ Custom gesture sets (swipe, circle...)
* 🎮 Control 3rd-party apps (PowerPoint, Media Player)
* 🧠 Trainable ML gesture classifier
* 🖥 Cross-platform OS support (Linux/macOS)
* ⚙️ Performance benchmark tools

---

## 📌 Notes & Credits

AI tools (like ChatGPT) were used for ideation and code generation. Architecture design, logic, integration, and bug fixing were done manually by the author.

Developed by **Ngô Nhật Nguyên (nnYunaXYZ)** 🇻🇳 – Built for personal learning, GitHub portfolio, and international research preparation (e.g., MIT).

---

## 🪪 License

Licensed under the **MIT License** – free for personal and academic use.
