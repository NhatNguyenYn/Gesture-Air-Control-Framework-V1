# modules/controllers/drawing_controller.py

import cv2
import numpy as np
import math

class DrawingController:
    """
    NÂNG CẤP V12.1: "BUG FIX"
    - Sửa lỗi nghiêm trọng IndexError do viết tắt code trong hàm tính toán tọa độ.
    - Đảm bảo code tường minh và chạy ổn định.
    """
    def __init__(self, width, height):
        self.canvas = np.zeros((height, width, 3), np.uint8)
        self.draw_color = (0, 0, 255)
        self.brush_thickness, self.eraser_thickness = 15, 50
        self.smoothed_cursor = (0, 0)
        self.last_draw_pos = (0, 0)
        self.current_action = "IDLE"
        self.is_hand_present = False
        self.potential_action = "IDLE"
        self.action_stabilization_counter = 0
        self.ACTION_CONFIRM_FRAMES = 3
        self.smoothing_factor = 0.4
        self.header_height = 85
        self.colors = {'red': (0, 0, 255), 'blue': (255, 0, 0), 'green': (0, 255, 0), 'yellow': (0, 255, 255)}
        self.color_boxes, self.eraser_box = {}, None
        self._calculate_toolbar_coords()
        print("Drawing Controller v12.1 (Bug Fix) đã được khởi tạo.")

    # --- [SỬA LỖI] ---
    # Viết lại hàm này một cách tường minh để tránh lỗi
    def _calculate_toolbar_coords(self):
        box_width = 100
        spacing = 20
        current_x = spacing
        for name in self.colors:
            self.color_boxes[name] = (current_x, 10, current_x + box_width, self.header_height - 10)
            current_x += box_width + spacing
        
        self.eraser_box = (current_x, 10, current_x + box_width, self.header_height - 10)

    def set_brush_size(self, size): self.brush_thickness = int(size)
    def set_eraser_size(self, size): self.eraser_thickness = int(size)

    def _is_finger_up(self, lm_list, tip_id, pip_id):
        dist_tip_wrist = math.hypot(lm_list[tip_id][1] - lm_list[0][1], lm_list[tip_id][2] - lm_list[0][2])
        dist_pip_wrist = math.hypot(lm_list[pip_id][1] - lm_list[0][1], lm_list[pip_id][2] - lm_list[0][2])
        return dist_tip_wrist > dist_pip_wrist

    def update_logic(self, lm_list):
        # ... (Hàm này không đổi) ...
        if not lm_list:
            self.is_hand_present = False
            self.current_action = "IDLE"
            return
        self.is_hand_present = True
        raw_x, raw_y = lm_list[8][1], lm_list[8][2]
        if self.smoothed_cursor == (0, 0): self.smoothed_cursor = (raw_x, raw_y)
        sx = int(self.smoothed_cursor[0] * (1 - self.smoothing_factor) + raw_x * self.smoothing_factor)
        sy = int(self.smoothed_cursor[1] * (1 - self.smoothing_factor) + raw_y * self.smoothing_factor)
        self.smoothed_cursor = (sx, sy)
        try:
            index_up = self._is_finger_up(lm_list, 8, 6)
            middle_up = self._is_finger_up(lm_list, 12, 10)
            if index_up and middle_up: self.potential_action = "HOVER"
            elif index_up and not middle_up: self.potential_action = "DRAW"
            else: self.potential_action = "IDLE"
        except IndexError: self.potential_action = "IDLE"
        if self.potential_action != self.current_action:
            self.action_stabilization_counter += 1
            if self.action_stabilization_counter >= self.ACTION_CONFIRM_FRAMES:
                self.current_action = self.potential_action
        else:
            self.action_stabilization_counter = 0
        if self.current_action == "DRAW":
            if self.smoothed_cursor[1] < self.header_height:
                for name, coords in self.color_boxes.items():
                    if coords[0] < self.smoothed_cursor[0] < coords[2]: self.draw_color = self.colors[name]
                if self.eraser_box[0] < self.smoothed_cursor[0] < self.eraser_box[2]: self.draw_color = (0, 0, 0)
            else:
                if self.last_draw_pos == (0, 0): self.last_draw_pos = self.smoothed_cursor
                thickness = self.eraser_thickness if self.draw_color == (0, 0, 0) else self.brush_thickness
                cv2.line(self.canvas, self.last_draw_pos, self.smoothed_cursor, self.draw_color, thickness)
        if self.current_action != "DRAW": self.last_draw_pos = (0, 0)
        self.last_draw_pos = self.smoothed_cursor

    def render(self, img):
        # ... (Hàm này không đổi) ...
        cv2.rectangle(img, (0, 0), (img.shape[1], self.header_height), (210, 210, 210), -1)
        for name, coords in self.color_boxes.items(): 
            cv2.rectangle(img, (coords[0], coords[1]), (coords[2], coords[3]), self.colors[name], -1)
        x1, y1, x2, y2 = self.eraser_box
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), -1)
        cv2.putText(img, "GOM", (x1 + 20, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        img_gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 10, 255, cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, img_inv)
        img = cv2.bitwise_or(img, self.canvas)
        if self.is_hand_present:
            cursor_pos = self.smoothed_cursor
            if cursor_pos[1] < self.header_height and self.current_action == "HOVER":
                for name, coords in self.color_boxes.items():
                    if coords[0] < cursor_pos[0] < coords[2]: cv2.rectangle(img, (coords[0]-3, coords[1]-3), (coords[2]+3, coords[3]+3), (255, 255, 255), 3)
                if self.eraser_box[0] < cursor_pos[0] < self.eraser_box[2]: cv2.rectangle(img, (self.eraser_box[0]-3, self.eraser_box[1]-3), (self.eraser_box[2]+3, self.eraser_box[3]+3), (255, 255, 255), 3)
            if self.current_action == "DRAW":
                effective_color = (255, 255, 255) if self.draw_color == (0,0,0) else self.draw_color
                cv2.circle(img, cursor_pos, self.brush_thickness // 2, effective_color, -1)
            elif self.current_action == "HOVER":
                cv2.circle(img, cursor_pos, 15, (255, 255, 255), 3)
        return img