from fastapi import APIRouter, UploadFile, File
import uuid
import asyncio
import os
import time
from license_plate.license_plate import predict, save_temp_image


router = APIRouter(
    prefix="/license_plate",
    tags=["license_plate"]
)


@router.post("/detect")
async def get_license_plate_number(image: UploadFile = File(...), image2: UploadFile = File(...)):

    # Tính toán quá trình thực hiện
    start_time = time.time()

    # Tạo tên tệp duy nhất cho mỗi yêu cầu API
    unique_id = str(uuid.uuid4())
    license_plate_frame = f"license_plate_image_{unique_id}.png"
    face_frame = f"face_image_{unique_id}.png"

    # Tạo file tạm cho hình ảnh gửi lên API
    license_plate_frame_path = await save_temp_image(upload_file= image, file_name= license_plate_frame)
    face_frame_path = await save_temp_image(upload_file= image2, file_name= face_frame)

    # Tính thời gian tạo file tạm
    create_temp_image_time = time.time()
    # print(f"Thời gian tạo thư mục tạm cho hình ảnh gửi đến server: {create_temp_image_time - start_time}s")

    try:
        # Gọi hàm predict trong luồng phụ để không làm chặn luồng chính
        result = await predict(image= license_plate_frame_path, image2= face_frame_path)

        # Tính thời gian dự đoán
        predict_time = time.time()
        # print(f"Tổng thời gian đọc ký tự biển số: {predict_time - create_temp_image_time}s")
    
    finally:
        # Dọn dẹp tài nguyên sau khi xử lý
        # Xóa tệp tạm thời nếu cần, đảm bảo tệp ảnh không lưu lại trên hệ thống
        if os.path.exists(license_plate_frame_path):
            os.remove(license_plate_frame_path)
        if os.path.exists(face_frame_path):
            os.remove(face_frame_path)

        # Tính thời gian dọn dẹp
        clean_trash = time.time()
        # print(f"Thời gian dọn dẹp sau khi đọc ký tự xong: {clean_trash - predict_time}s")
        
        # Thu hồi bộ nhớ không cần thiết
        # gc.collect()

    return result