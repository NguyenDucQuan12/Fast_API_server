import torch

from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont

"""
Cách để chạy Paddle OCR trên GPU
Bước 1: Tải driver của card đồ họa
Bước 2: Tải CUDA và thêm path vào biến môi trường, paddle ocr yêu cầu cuda cao nhất hiện nay là 12.3
Bước 4: Tải cudnn và giải nén, sao chép các tệp trong cudnn vào thư mục tương ứng C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.4\\xxx
Lưu ý: Nếu cuda v12.4 (không phải v12.3) thì sao chép tệp `c:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.4\\bin\\cublas64_12.dll` vào thư mục "C:\\Windows\\System32\\cublas64_11.dll" Nhớ đổi tên _12 thành _11
Bước 5: pip install paddlepaddle-gpu
Bước 6: pip install "paddleocr>=2.0.1" # Recommend to use version 2.0.1+
Thế là xong
"""

# Initialize OCR engine
# sử dụng PaddleOCR ngôn ngữ tiếng Trung
ocr = PaddleOCR(
            use_angle_cls=False,
            lang='ch',
            show_log=False,
            use_gpu=True,
            rec_model_dir="assets/model/china/rec", # use in here
            det_model_dir="assets/model/china/det", # use in here
            cls_model_dir="assets/model/china/cls" # use in here
        )

img_path = "assets\\image\\image_test\\LÀN VÀO 52019_12_07_13_29_47.jpg"
slice = {'horizontal_stride': 300, 'vertical_stride': 500, 'merge_x_thres': 50, 'merge_y_thres': 35}
results = ocr.ocr(img_path, cls=True, slice=slice)

# Load image
image = Image.open(img_path).convert("RGB")
draw = ImageDraw.Draw(image)
# font = ImageFont.truetype("./doc/fonts/simfang.ttf", size=20)  # Adjust size as needed

# Process and draw results
for res in results:
    for line in res:
        box = [tuple(point) for point in line[0]]
        # Finding the bounding box
        box = [(min(point[0] for point in box), min(point[1] for point in box)),
               (max(point[0] for point in box), max(point[1] for point in box))]
        txt = line[1][0]
        draw.rectangle(box, outline="red", width=2)  # Draw rectangle
        draw.text((box[0][0], box[0][1] - 25), txt, fill="blue") # font = font # Draw text above the box

# Save result
image.save("result12.jpg")