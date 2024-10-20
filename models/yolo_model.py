from ultralytics import YOLO
import torch
import logging

# Đầu tiên lên chạy câu lệnh `nvidia-smi` để xem phiên bản Cuda cần thiết là bao nhiêu, xong lên trang chủ nvidia tải về
# Tiếp theo tải CUDA tương ứng từ trang chủ, giải nén và cài đặt
# Thêm CUDA vào path nếu chưa có: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4\bin, lib và incude

logger = logging.getLogger(__name__)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
logger.info(f"Sử dụng {device}")

license_plate_detect_gpu = YOLO('assets/model/yolo/yolov8_pretrain/best.pt').to(device)

# Model yolo obb (có bounding box có thể xoay theo đối tượng)
# license_plate_detect_cpu = YOLO('assest/model/best-yolo-obb.pt')


