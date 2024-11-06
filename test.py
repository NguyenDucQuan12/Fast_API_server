from PIL import Image
import cv2
import pillow_heif
import numpy as np

# pillow_heif.register_heif_opener()

image_path = 'assets\\image\\image_test\\20240425_061413796_iOS.heic'

try:
    heif_file = pillow_heif.read_heif(image_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode
    )
    # Chuyển đổi ảnh PIL thành NumPy array và chuyển sang định dạng BGR cho OpenCV
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    print(image)
    # image = Image.open(image_path)
    # image.show()
except Exception as e:
    print(f"Lỗi khi mở ảnh HEIC: {e}")
