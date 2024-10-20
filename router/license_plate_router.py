from fastapi import APIRouter, UploadFile, File
import gc
import shutil
import uuid
import tempfile
import os
from license_plate.license_plate import predict


router = APIRouter(
    prefix="/license_plate",
    tags=["license_plate"]
)


@router.post("/detect")
def get_license_plate_number(image: UploadFile = File(...), image2: UploadFile = File(...)):

    # Tạo tên tệp duy nhất cho mỗi yêu cầu API
    unique_id = str(uuid.uuid4())
    license_plate_frame = f"license_plate_image_{unique_id}.png"
    face_frame = f"face_image_{unique_id}.png"

    # Hoặc có thể sử dụng thư mục tạm thời
    temp_dir = tempfile.gettempdir()
    license_plate_frame_path = os.path.join(temp_dir, license_plate_frame)
    face_frame_path = os.path.join(temp_dir, face_frame)

    try:
        # Sử dụng with để đảm bảo tệp được đóng đúng cách sau khi xử lý xong
        with open(license_plate_frame_path, "w+b") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        with open(face_frame_path, "w+b") as buffer:
            shutil.copyfileobj(image2.file, buffer)

        # Đóng file upload ngay sau khi không sử dụng nữa
        image.file.close()
        image2.file.close()

        # Gọi hàm predict để xử lý ảnh
        result = predict(image=license_plate_frame_path, image2 = face_frame_path)
    
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