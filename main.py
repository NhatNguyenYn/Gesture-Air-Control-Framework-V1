# main.py

import tkinter as tk
from tkinter import ttk
import cv2
import threading
from PIL import Image, ImageTk
import time
import pyautogui
import numpy as np

from modules.hand_tracker import HandTracker
from modules.controllers.drawing_controller import DrawingController
from modules.controllers.mouse_controller import MouseController
from modules.controllers.enhanced_finger_counter_controller import EnhancedFingerCounterController
from modules.controllers.volume_controller import VolumeController # Thêm import

class HandGestureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gesture Control Framework - The Final Edition")
        self.geometry("1480x850")
        self.CAM_WIDTH, self.CAM_HEIGHT = 1280, 720
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pyautogui.size()
        self.current_mode = tk.StringVar(value="FingerCount")
        self.is_running = True
        self.show_skeleton = tk.BooleanVar(value=False)
        self.hand_tracker = HandTracker(max_hands=1, detection_con=0.7, track_con=0.7)
        self.drawing_controller = DrawingController(self.CAM_WIDTH, self.CAM_HEIGHT)
        self.mouse_controller = MouseController(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.CAM_WIDTH, self.CAM_HEIGHT)
        self.enhanced_finger_counter = EnhancedFingerCounterController()
        self.volume_controller = VolumeController() # Khởi tạo controller mới
        self.create_widgets()
        self.mouse_mode_image = self.create_static_image("Mouse Mode Active\nMinimize this window to use.")
        self.default_photo = self.create_static_image("Starting Camera...")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAM_HEIGHT)
        self.latest_frame = None
        self.processed_photo = self.default_photo
        self.frame_lock = threading.Lock()
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.capture_thread.start()
        self.processing_thread.start()
        self._update_gui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # ... (Không đổi) ...
        main_frame = ttk.Frame(self); main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.video_label = ttk.Label(main_frame); self.video_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        control_frame = ttk.Frame(main_frame, width=200); control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0)); control_frame.pack_propagate(False)
        feature_frame = ttk.LabelFrame(control_frame, text="TÍNH NĂNG"); feature_frame.pack(fill='x', padx=5, pady=5)
        modes = [("Vẽ Ảo", "Drawing"), ("Chuột Ảo", "Mouse"), ("Kiểm tra Cử chỉ", "FingerCount"), ("Âm Lượng", "Volume")]
        for text, mode in modes:
            rb = ttk.Radiobutton(feature_frame, text=text, variable=self.current_mode, value=mode)
            rb.pack(anchor=tk.W)
        drawing_frame = ttk.LabelFrame(control_frame, text="CÀI ĐẶT VẼ"); drawing_frame.pack(fill='x', padx=5, pady=5, ipady=5)
        ttk.Label(drawing_frame, text="Kích thước Cọ/Gôm").pack()
        self.size_var = tk.DoubleVar(value=15); size_slider = ttk.Scale(drawing_frame, from_=5, to=150, orient='horizontal', variable=self.size_var, command=self.on_size_change); size_slider.pack(fill='x', padx=5)
        self.size_label = ttk.Label(drawing_frame, text=f"Size: {int(self.size_var.get())}"); self.size_label.pack()
        mouse_frame = ttk.LabelFrame(control_frame, text="CÀI ĐẶT CHUỘT"); mouse_frame.pack(fill='x', padx=5, pady=5, ipady=5)
        ttk.Label(mouse_frame, text="Độ nhạy").pack()
        self.sensitivity_var = tk.DoubleVar(value=1.5); sens_slider = ttk.Scale(mouse_frame, from_=1.0, to=3.0, orient='horizontal', variable=self.sensitivity_var, command=self.on_sensitivity_change); sens_slider.pack(fill='x', padx=5)
        self.sensitivity_label = ttk.Label(mouse_frame, text=f"x{self.sensitivity_var.get():.1f}"); self.sensitivity_label.pack()
        ttk.Checkbutton(control_frame, text="Hiển thị khung xương", variable=self.show_skeleton).pack(pady=10)
        ttk.Button(control_frame, text="Thoát", command=self.on_closing).pack(side=tk.BOTTOM, pady=20)
    
    # ... (Các hàm còn lại không đổi) ...
    def on_size_change(self, value):
        size = int(float(value)); self.size_label.config(text=f"Size: {size}"); self.drawing_controller.set_brush_size(size); self.drawing_controller.set_eraser_size(size)
    def on_sensitivity_change(self, value):
        sens = float(value); self.sensitivity_label.config(text=f"x{sens:.1f}"); self.mouse_controller.set_sensitivity(sens)
    def create_static_image(self, text):
        img = np.zeros((self.CAM_HEIGHT, self.CAM_WIDTH, 3), dtype=np.uint8); img[:] = (235, 235, 235); lines = text.split('\n'); y0, dy = 300, 70
        for i, line in enumerate(lines):
            y = y0 + i * dy; (text_width, text_height), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 2, 3); x = (self.CAM_WIDTH - text_width) // 2
            cv2.putText(img, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 50, 50), 3)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB); return ImageTk.PhotoImage(image=Image.fromarray(img_rgb))
    def _capture_loop(self):
        while self.is_running:
            success, frame = self.cap.read()
            if success: frame = cv2.flip(frame, 1)
            with self.frame_lock: self.latest_frame = frame
            time.sleep(1/60)

    def _processing_loop(self):
        p_time = 0
        while self.is_running:
            with self.frame_lock: frame_to_process = self.latest_frame
            if frame_to_process is None: continue
            mode = self.current_mode.get()
            
            self.hand_tracker.find_hands(frame_to_process, draw=False)
            all_hands_data = self.hand_tracker.get_landmarks_and_handedness(frame_to_process)
            
            if mode == "Mouse":
                if all_hands_data: self.mouse_controller.update(all_hands_data[0][0])
                self.processed_photo = self.mouse_mode_image
                time.sleep(0.001)
                continue

            img_to_display = frame_to_process.copy()
            
            if all_hands_data:
                lm_list, hand_label_from_model = all_hands_data[0]
                
                if mode == "Drawing":
                    self.drawing_controller.update_logic(lm_list)
                elif mode == "FingerCount":
                    corrected_hand_label = "Phai" if hand_label_from_model == "Left" else "Trai"
                    img_to_display = self.enhanced_finger_counter.process_hand(img_to_display, lm_list, corrected_hand_label)
                # --- [TÍCH HỢP TÍNH NĂNG MỚI] ---
                elif mode == "Volume":
                    img_to_display = self.volume_controller.process_hand(img_to_display, lm_list)
            else:
                if mode == "Drawing":
                    self.drawing_controller.update_logic(None)
                # Vẫn gọi controller khi không có tay để giữ thanh âm lượng
                elif mode == "Volume":
                    img_to_display = self.volume_controller.process_hand(img_to_display, None)

            if mode == "Drawing":
                img_to_display = self.drawing_controller.render(img_to_display)
            
            if all_hands_data and self.show_skeleton.get():
                self.hand_tracker.mp_drawing.draw_landmarks(img_to_display, self.hand_tracker.results.multi_hand_landmarks[0], self.hand_tracker.mp_hands.HAND_CONNECTIONS)
            
            c_time = time.time(); fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0; p_time = c_time
            cv2.putText(img_to_display, f'FPS: {int(fps)}', (10, self.CAM_HEIGHT - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            
            img_rgb = cv2.cvtColor(img_to_display, cv2.COLOR_BGR2RGB)
            self.processed_photo = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))

    def _update_gui(self): # ... (Không đổi) ...
        if self.processed_photo: self.video_label.config(image=self.processed_photo); self.video_label.image = self.processed_photo
        self.after(15, self._update_gui)
    def on_closing(self): # ... (Không đổi) ...
        self.is_running = False
        if self.capture_thread.is_alive(): self.capture_thread.join()
        if self.processing_thread.is_alive(): self.processing_thread.join()
        self.cap.release(); self.destroy()

if __name__ == "__main__":
    app = HandGestureApp()
    app.mainloop()