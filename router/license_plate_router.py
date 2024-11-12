from fastapi import APIRouter, UploadFile, File
import uuid
import asyncio
import os
from license_plate.license_plate import predict, save_temp_image


router = APIRouter(
    prefix="/license_plate",
    tags=["license_plate"]
)


@router.post("/detect")
async def get_license_plate_number(image: UploadFile = File(...), image2: UploadFile = File(...)):

    # Tạo tên tệp duy nhất cho mỗi yêu cầu API
    unique_id = str(uuid.uuid4())
    license_plate_frame = f"license_plate_image_{unique_id}.png"
    face_frame = f"face_image_{unique_id}.png"

    # Tạo file tạm cho hình ảnh gửi lên API
    license_plate_frame_path = await save_temp_image(upload_file= image, file_name= license_plate_frame)
    face_frame_path = await save_temp_image(upload_file= image2, file_name= face_frame)

    try:
        # Gọi hàm predict trong luồng phụ để không làm chặn luồng chính
        result = await predict(image= license_plate_frame_path, image2= face_frame_path)
    
    finally:
        # Dọn dẹp tài nguyên sau khi xử lý
        # Xóa tệp tạm thời nếu cần, đảm bảo tệp ảnh không lưu lại trên hệ thống
        if os.path.exists(license_plate_frame_path):
            os.remove(license_plate_frame_path)
        if os.path.exists(face_frame_path):
            os.remove(face_frame_path)
        
        # Thu hồi bộ nhớ không cần thiết
        # gc.collect()

    return result