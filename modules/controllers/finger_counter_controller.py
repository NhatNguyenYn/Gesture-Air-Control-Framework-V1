# modules/controllers/finger_counter_controller.py

import cv2
import numpy as np
import math

class FingerCounterController:
    """
    Module nền tảng: Chịu trách nhiệm nhận diện và hiển thị số ngón tay
    đang giơ lên một cách chính xác.
    """
    def __init__(self):
        # Sử dụng lại logic nhận diện vector ổn định nhất
        self.tip_ids = [4, 8, 12, 16, 20]
        self.up_threshold = 0.75 # Ngưỡng để coi là ngón tay duỗi
        print("Finger Counter Controller đã được khởi tạo.")

    def _get_vector(self, lm_list, start_id, end_id):
        """Hàm trợ giúp tạo và chuẩn hóa vector."""
        start_point = np.array([lm_list[start_id][1], lm_list[start_id][2]])
        end_point = np.array([lm_list[end_id][1], lm_list[end_id][2]])
        vector = end_point - start_point
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else np.array([0, 0])

    def process_hand(self, img, lm_list, hand_label):
        """
        Xử lý landmarks để đếm ngón tay và vẽ kết quả lên ảnh.
        """
        if not lm_list: return img

        # Xác định vector hướng chính của bàn tay
        hand_direction_vector = self._get_vector(lm_list, 0, 9)
        fingers_up_count = 0

        # Xử lý 4 ngón dài
        for tip_id in self.tip_ids[1:]: # Bỏ qua ngón cái
            pip_id = tip_id - 2
            finger_vector = self._get_vector(lm_list, pip_id, tip_id)
            dot_product = np.dot(finger_vector, hand_direction_vector)
            if dot_product > self.up_threshold:
                fingers_up_count += 1
        
        # Xử lý ngón cái (dùng logic so sánh X đơn giản và hiệu quả)
        thumb_tip = lm_list[self.tip_ids[0]]
        thumb_mcp = lm_list[self.tip_ids[0] - 2]
        if (hand_label == 'Right' and thumb_tip[1] < thumb_mcp[1]) or \
           (hand_label == 'Left' and thumb_tip[1] > thumb_mcp[1]):
            fingers_up_count += 1

        # Vẽ kết quả lên màn hình
        cv2.rectangle(img, (50, 350), (250, 450), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(fingers_up_count), (90, 440), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 10)

        return img