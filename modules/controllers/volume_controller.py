# modules/controllers/volume_controller.py

import cv2
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeController:
    """
    Module chuyên biệt cho việc điều khiển âm lượng hệ thống.
    Sử dụng logic nhận diện 5 ngón ổn định để kích hoạt.
    """
    def __init__(self):
        # --- Khởi tạo pycaw để giao tiếp với hệ thống âm thanh ---
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.vol_range = self.volume.GetVolumeRange()
            self.min_vol, self.max_vol = self.vol_range[0], self.vol_range[1]
            self.pycaw_ready = True
        except Exception as e:
            print(f"Loi khi khoi tao pycaw: {e}. Tinh nang am luong se bi vo hieu hoa.")
            self.pycaw_ready = False

        # --- Trạng thái ---
        self.vol_bar = 400
        self.vol_percentage = 0
        print("Volume Controller đã được khởi tạo.")

    def _is_long_finger_up(self, lm_list, tip_id, pip_id):
        # Mượn logic ổn định nhất
        wrist = lm_list[0]
        dist_tip_wrist = math.hypot(lm_list[tip_id][1] - wrist[1], lm_list[tip_id][2] - wrist[2])
        dist_pip_wrist = math.hypot(lm_list[pip_id][1] - wrist[1], lm_list[pip_id][2] - wrist[2])
        return dist_tip_wrist > dist_pip_wrist

    def _is_five_fingers_up(self, lm_list):
        """Kiểm tra cử chỉ 5 ngón để kích hoạt."""
        if not lm_list: return False
        try:
            # 4 ngón dài phải giơ lên
            index_up = self._is_long_finger_up(lm_list, 8, 6)
            middle_up = self._is_long_finger_up(lm_list, 12, 10)
            ring_up = self._is_long_finger_up(lm_list, 16, 14)
            pinky_up = self._is_long_finger_up(lm_list, 20, 18)
            if not (index_up and middle_up and ring_up and pinky_up):
                return False

            # Logic ngón cái
            thumb_tip = lm_list[4]
            thumb_mcp = lm_list[2]
            wrist_x = lm_list[0][1]
            img_width = 1280 # Giả định chiều rộng ảnh
            display_hand_label = "Trai" if wrist_x < img_width / 2 else "Phai"
            
            if display_hand_label == 'Trai':
                if thumb_tip[1] > thumb_mcp[1]: return True
            else: # Phai
                if thumb_tip[1] < thumb_mcp[1]: return True

            return False
        except IndexError:
            return False

    def process_hand(self, img, lm_list):
        if not self.pycaw_ready: return img # Nếu pycaw lỗi, không làm gì cả

        # Luôn vẽ thanh âm lượng tĩnh trước
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(self.vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(self.vol_percentage)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        if not lm_list: return img

        # --- Kích hoạt điều khiển ---
        if self._is_five_fingers_up(lm_list):
            thumb_tip, index_tip = lm_list[4], lm_list[8]
            cx, cy = (thumb_tip[1] + index_tip[1]) // 2, (thumb_tip[2] + index_tip[2]) // 2

            cv2.circle(img, (thumb_tip[1], thumb_tip[2]), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (index_tip[1], index_tip[2]), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (thumb_tip[1], thumb_tip[2]), (index_tip[1], index_tip[2]), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            distance = math.hypot(index_tip[1] - thumb_tip[1], index_tip[2] - thumb_tip[2])
            
            # Ánh xạ khoảng cách
            vol_level = np.interp(distance, [20, 200], [self.min_vol, self.max_vol])
            self.vol_bar = np.interp(distance, [20, 200], [400, 150])
            self.vol_percentage = np.interp(distance, [20, 200], [0, 100])
            
            # Đặt âm lượng hệ thống
            self.volume.SetMasterVolumeLevel(vol_level, None)
            
            if distance < 20:
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        
        return img