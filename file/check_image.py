import numpy as np
import cv2


def check_image(image):

    # Kiểm tra nếu đầu vào là đường dẫn tới tệp hình ảnh
    if isinstance(image, str):
        # Nếu image là đường dẫn đến file, dùng cv2.imread để đọc ảnh
        image = cv2.imread(image)

        # Kiểm tra nếu không thể đọc được ảnh
        if image is None:
            return None
        else:
            return image

    # Nếu image là một mảng NumPy, coi đó là frame từ camera
    elif isinstance(image, np.ndarray):
        # Đã là frame từ camera, không cần xử lý thêm
        return image
    else:
        # image là 1 định dạng không hợp lệ, nằm ngoài 2 định dạng trên
        return None