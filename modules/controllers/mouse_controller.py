# modules/controllers/mouse_controller.py

import pyautogui
import numpy as np
import math
import time

class MouseController:
    """
    NÂNG CẤP V3.1: "CONSISTENT COORDINATES"
    - Hoạt động trên hệ tọa độ nhất quán (ảnh đã lật).
    - Loại bỏ các logic vá lỗi, di chuyển chuột trực quan hơn.
    - Giữ nguyên các cử chỉ và độ nhạy.
    """
    def __init__(self, screen_width, screen_height, cam_width, cam_height):
        self.screen_w, self.screen_h = screen_width, screen_height
        self.cam_w, self.cam_h = cam_width, cam_height
        
        self.frame_reduction = 100
        self.smoothing = 5
        self.mouse_sensitivity = 1.5

        self.ploc_x, self.ploc_y = 0, 0
        self.cloc_x, self.cloc_y = 0, 0
        self.last_action_time = 0
        self.action_cooldown = 0.4
        self.is_dragging = False

        print("Mouse Controller v3.1 (Consistent Coords) đã được khởi tạo.")

    def set_sensitivity(self, value):
        self.mouse_sensitivity = value

    def _get_distance(self, p1, p2):
        return math.hypot(p1[1] - p2[1], p1[2] - p2[2])

    def update(self, lm_list):
        if not lm_list: return

        thumb_tip = lm_list[4]
        index_tip = lm_list[8]
        middle_tip = lm_list[12]
        pinky_tip = lm_list[20]

        # --- [SỬA LỖI LỚN] ---
        # Logic ánh xạ tọa độ giờ đây đơn giản và trực tiếp hơn
        x_raw = np.interp(index_tip[1], (self.frame_reduction, self.cam_w - self.frame_reduction), (0, self.screen_w * self.mouse_sensitivity))
        y_raw = np.interp(index_tip[2], (self.frame_reduction, self.cam_h - self.frame_reduction), (0, self.screen_h * self.mouse_sensitivity))

        self.cloc_x = self.ploc_x + (x_raw - self.ploc_x) / self.smoothing
        self.cloc_y = self.ploc_y + (y_raw - self.ploc_y) / self.smoothing
        
        # Di chuyển chuột trực tiếp, không cần lật lại
        pyautogui.moveTo(self.cloc_x, self.cloc_y)
        
        self.ploc_x, self.ploc_y = self.cloc_x, self.cloc_y

        # --- Xử lý hành động (logic không đổi, nhưng giờ đáng tin cậy hơn) ---
        drag_distance = self._get_distance(index_tip, thumb_tip)
        left_click_distance = self._get_distance(index_tip, middle_tip)
        right_click_distance = self._get_distance(index_tip, pinky_tip)
        
        current_time = time.time()

        if drag_distance < 35:
            if not self.is_dragging:
                pyautogui.mouseDown()
                self.is_dragging = True
        else:
            if self.is_dragging:
                pyautogui.mouseUp()
                self.is_dragging = False
        
        if not self.is_dragging and (current_time - self.last_action_time > self.action_cooldown):
            if left_click_distance < 30:
                pyautogui.click(button='left')
                self.last_action_time = current_time
            elif right_click_distance < 30:
                pyautogui.click(button='right')
                self.last_action_time = current_time