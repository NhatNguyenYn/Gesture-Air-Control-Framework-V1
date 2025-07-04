# modules/hand_tracker.py

import cv2
import mediapipe as mp

class HandTracker:
    """
    Lớp dùng để phát hiện và theo dõi bàn tay sử dụng MediaPipe.
    Nó đóng gói tất cả các logic liên quan đến việc khởi tạo MediaPipe,
    tìm kiếm bàn tay và trích xuất vị trí các điểm mốc.
    """
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        """
        Khởi tạo các tham số cho việc nhận diện bàn tay.
        """
        self.mode = mode
        self.max_hands = max_hands
        # Chuyển đổi sang float để đảm bảo MediaPipe chấp nhận
        self.detection_con = float(detection_con) 
        self.track_con = float(track_con)

        # Khởi tạo các đối tượng cần thiết từ MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands,
                                           min_detection_confidence=self.detection_con,
                                           min_tracking_confidence=self.track_con)
        self.mp_drawing = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img, draw=True):
        """
        Tìm kiếm các bàn tay trong một khung hình.
        :param img: Khung hình đầu vào (ở định dạng BGR).
        :param draw: Cờ để quyết định có vẽ các điểm mốc lên ảnh hay không.
        :return: Trả về khung hình đã được vẽ (nếu có).
        """
        # MediaPipe xử lý ảnh RGB, cần chuyển đổi
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(img, hand_landmarks,
                                               self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_landmarks_and_handedness(self, img):
        """
        Trích xuất vị trí các điểm mốc VÀ thông tin tay trái/phải cho TẤT CẢ các bàn tay.
        :param img: Khung hình đầu vào.
        :return: Một danh sách các tuple, mỗi tuple chứa (danh sách điểm mốc, nhãn tay 'Left'/'Right').
                 Ví dụ: [ ([...lm_list_hand_1...], 'Right'), ([...lm_list_hand_2...], 'Left') ]
        """
        all_hands_data = []
        if self.results and self.results.multi_hand_landmarks:
            h, w, c = img.shape
            
            # Lặp qua từng bàn tay được phát hiện
            # `enumerate` giúp lấy cả chỉ số (hand_idx) và dữ liệu (hand_landmarks)
            for hand_idx, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
                lm_list = []
                # Lấy nhãn 'Left' hoặc 'Right' từ kết quả
                # `multi_handedness` có cùng chỉ số với `multi_hand_landmarks`
                hand_label = self.results.multi_handedness[hand_idx].classification[0].label
                
                # Trích xuất các điểm mốc và chuyển về tọa độ pixel
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                
                all_hands_data.append((lm_list, hand_label))

        return all_hands_data