import cv2
import numpy as np
import math

class EnhancedFingerCounterController:
    def __init__(self):
        self.finger_map = { 'Cai': (4, 2), 'Tro': (8, 6), 'Giua': (12, 10), 'Ap ut': (16, 14), 'Ut': (20, 18) }
        print("Enhanced Finger Counter Controller (FIXED) đã được khởi tạo.")

    def _is_long_finger_up(self, lm_list, tip_id, pip_id):
        wrist = lm_list[0]
        tip_pos = lm_list[tip_id]
        pip_pos = lm_list[pip_id]
        dist_tip_wrist = math.hypot(tip_pos[1] - wrist[1], tip_pos[2] - wrist[2])
        dist_pip_wrist = math.hypot(pip_pos[1] - wrist[1], pip_pos[2] - wrist[2])
        return dist_tip_wrist > dist_pip_wrist

    def process_hand(self, img, lm_list, hand_label_from_model):
        if not lm_list: return img

        img_width = img.shape[1]
        wrist_x = lm_list[0][1]
        display_hand_label = "Trai" if wrist_x < img_width / 2 else "Phai"

        fingers_up = []

        # Nhận diện 4 ngón dài
        for name, (tip_id, pip_id) in list(self.finger_map.items())[1:]:
            if self._is_long_finger_up(lm_list, tip_id, pip_id):
                fingers_up.append(name)

        # Nhận diện ngón cái: So sánh hướng nghiêng ngón cái với cổ tay
        thumb_tip = lm_list[self.finger_map['Cai'][0]]
        thumb_mcp = lm_list[self.finger_map['Cai'][1]]

        # Logic hướng X dựa vào vị trí cổ tay để xác định tay thật
        if display_hand_label == 'Trai':
            if thumb_tip[1] > thumb_mcp[1]:  # Ngón cái chìa ra ngoài bên trái
                fingers_up.append('Cai')
        else:  # 'Phai'
            if thumb_tip[1] < thumb_mcp[1]:  # Ngón cái chìa ra ngoài bên phải
                fingers_up.append('Cai')

        # Vẽ lên ảnh
        y_pos = 50
        cv2.putText(img, f"Ban tay: {display_hand_label}", (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        y_pos += 40
        cv2.putText(img, f"So ngon: {len(fingers_up)}", (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        y_pos += 50
        cv2.putText(img, "Ngon dang gio:", (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        y_pos += 35
        for finger_name in fingers_up:
            cv2.putText(img, f"- {finger_name}", (40, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_pos += 30

        return img
