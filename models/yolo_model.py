from ultralytics import YOLO
import torch
import logging
import cv2
import time

# Đầu tiên chạy câu lệnh `nvidia-smi` để xem phiên bản Cuda cần thiết là bao nhiêu, xong lên trang chủ nvidia tải về
# Tiếp theo tải CUDA tương ứng từ trang chủ, giải nén và cài đặt
# Thêm CUDA vào path nếu chưa có: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4\bin, lib và include

logger = logging.getLogger(__name__)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
logger.info(f"Sử dụng {device} cho mô hình YOLO")

model = YOLO('assets/model/yolo/yolov8_pretrain/best.pt').to(device) # yolov8

def license_plate_detect_gpu(image):

    # verbose=False sẽ ko hiển thị log khi dự đoán: 
    # 0: 640x480 1 bien-so, 125.7ms
    # Speed: 0.0ms preprocess, 125.7ms inference, 15.6ms postprocess per image at shape (1, 3, 640, 480)
    result = model(image, verbose=False, max_det = 1)[0]

    return result
# license_plate_detect_gpu = YOLO("assets\\model\\yolo\\yolov11_pretrain\\last.pt").to(device= device) # yolov11

# Dự đoán thử
# image = im2 = cv2.imread("bus.jpg")
# results = license_plate_detect_gpu.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# results = license_plate_detect_gpu.predict("image.png")
# results[0].show()
# time.sleep(5)

# Model yolo obb (có bounding box có thể xoay theo đối tượng)
# license_plate_detect_cpu = YOLO('assest/model/best-yolo-obb.pt')


