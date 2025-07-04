# modules/action_controller.py

class ActionController:
    """
    Lớp này nhận vào một cử chỉ đã được xác định và thực hiện hành động tương ứng.
    Nó tách biệt hoàn toàn logic "nhận diện" và logic "hành động".
    """
    def __init__(self):
        # Bạn có thể khởi tạo các đối tượng cần thiết ở đây, ví dụ: thư viện điều khiển chuột
        # import pyautogui
        # self.screen_width, self.screen_height = pyautogui.size()
        pass

    def perform_action(self, gesture, hand_label=""):
        """
        Thực hiện hành động dựa trên cử chỉ được cung cấp.
        :param gesture: Cử chỉ đã được ổn định (ví dụ: số ngón tay, hoặc một chuỗi như "FIST").
        :param hand_label: Nhãn 'Left' hoặc 'Right' để có hành động khác nhau cho mỗi tay.
        """
        if gesture is None:
            return

        # Ví dụ về các hành động dựa trên số ngón tay
        if gesture == 0:
            print(f"[{hand_label}] Hành động: Nắm đấm!")
        elif gesture == 1:
            print(f"[{hand_label}] Hành động: Trỏ/Di chuyển!")
            # Logic điều khiển chuột có thể được gọi ở đây
        elif gesture == 2:
            print(f"[{hand_label}] Hành động: Victory!")
        elif gesture == 3:
            print(f"[{hand_label}] Hành động: OK!")
        elif gesture == 5:
            print(f"[{hand_label}] Hành động: Chào bạn/Dừng lại!")
        
        # Bạn có thể thêm các cử chỉ khác bằng chuỗi
        # elif gesture == "PINCH":
        #     print("Hanh dong: Click chuot!")