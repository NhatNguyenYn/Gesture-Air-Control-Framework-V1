# modules/gesture_recognizer.py

import numpy as np

class GestureRecognizer:
    """
    PHIÊN BẢN TIN CẬY NHẤT: Dựa trên nền tảng v3 ổn định, áp dụng một
    bản vá lỗi đơn giản và hiệu quả cho ngón cái. Logic này trực tiếp
    phân biệt ngón cái "chìa ra" và "gập vào" dựa trên vị trí tương đối
    của các khớp trên chính ngón tay đó.
    """
    def __init__(self, stability_threshold=5, up_threshold=0.75):
        self.finger_joints = {
            'thumb': (2, 4),
            'index': (5, 8),
            'middle': (9, 12),
            'ring': (13, 16),
            'pinky': (17, 20)
        }
        
        self.up_threshold = up_threshold

        # Bộ lọc ổn định
        self.stability_threshold = stability_threshold
        self.stable_gesture = None
        self.current_potential_gesture = None
        self.frame_counter = 0

    def _get_vector(self, lm_list, start_id, end_id):
        """Hàm trợ giúp tạo và chuẩn hóa vector."""
        if not lm_list or max(start_id, end_id) >= len(lm_list): return np.array([0, 0])
        start_point = np.array([lm_list[start_id][1], lm_list[start_id][2]])
        end_point = np.array([lm_list[end_id][1], lm_list[end_id][2]])
        vector = end_point - start_point
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else np.array([0, 0])

    def _get_gesture_from_vectors(self, lm_list, hand_label):
        """
        Logic chính: đếm ngón tay dựa trên hướng tương đối và quy tắc vị trí.
        """
        if not lm_list or len(lm_list) < 21:
            return None

        # 1. Xác định vector hướng chính của bàn tay (Logic từ v3)
        hand_direction_vector = self._get_vector(lm_list, 0, 9)

        fingers_up_count = 0

        # 2. Xử lý 4 ngón dài (Logic từ v3 - Không thay đổi)
        for finger_name in ['index', 'middle', 'ring', 'pinky']:
            start_id, end_id = self.finger_joints[finger_name]
            finger_vector = self._get_vector(lm_list, start_id, end_id)
            dot_product = np.dot(finger_vector, hand_direction_vector)
            if dot_product > self.up_threshold:
                fingers_up_count += 1
        
        # 3. Xử lý ngón cái (Logic vá lỗi đơn giản và hiệu quả)
        thumb_tip = lm_list[self.finger_joints['thumb'][1]] # Điểm #4
        thumb_mcp = lm_list[self.finger_joints['thumb'][0]] # Điểm #2 (khớp gốc)

        is_thumb_out = False
        if hand_label == 'Right':
            # Tay phải: ngón cái chìa ra khi đầu ngón ở bên trái khớp gốc (X nhỏ hơn)
            if thumb_tip[1] < thumb_mcp[1]:
                is_thumb_out = True
        elif hand_label == 'Left':
            # Tay trái: ngón cái chìa ra khi đầu ngón ở bên phải khớp gốc (X lớn hơn)
            if thumb_tip[1] > thumb_mcp[1]:
                is_thumb_out = True
        
        if is_thumb_out:
            fingers_up_count += 1
            
        return fingers_up_count

    def get_stable_gesture(self, lm_list, hand_label):
        """Hàm công khai, không thay đổi."""
        raw_gesture = self._get_gesture_from_vectors(lm_list, hand_label)
        
        if raw_gesture is None:
            self.frame_counter = 0
            self.current_potential_gesture = None
            return self.stable_gesture

        if raw_gesture == self.current_potential_gesture:
            self.frame_counter += 1
        else:
            self.current_potential_gesture = raw_gesture
            self.frame_counter = 1
        
        if self.frame_counter >= self.stability_threshold:
            if self.stable_gesture != self.current_potential_gesture:
                self.stable_gesture = self.current_potential_gesture
        
        return self.stable_gesture