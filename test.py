from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
import tempfile
import shutil
import cv2
import asyncio
from some_yolo_module import detect_license_plate
from paddleocr import PaddleOCR

router = APIRouter()

ocr_engine = PaddleOCR()

async def save_temp_image(upload_file: UploadFile, file_name: str):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    upload_file.file.close()
    return file_path

async def async_predict(image_path, image2_path):
    # Chạy hàm predict trong luồng phụ để không làm nghẽn luồng chính
    return await asyncio.to_thread(predict, image=image_path, image2=image2_path)

@router.post("/detect")
async def get_license_plate_number(image: UploadFile = File(...), image2: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    license_plate_file = f"license_plate_image_{unique_id}.png"
    face_file = f"face_image_{unique_id}.png"

    # Lưu ảnh vào thư mục tạm
    license_plate_path = await save_temp_image(image, license_plate_file)
    face_path = await save_temp_image(image2, face_file)

    try:
        # Gọi hàm xử lý ảnh không đồng bộ
        result = await async_predict(image=license_plate_path, image2=face_path)
    finally:
        # Dọn dẹp file tạm sau khi xử lý xong
        if os.path.exists(license_plate_path):
            os.remove(license_plate_path)
        if os.path.exists(face_path):
            os.remove(face_path)

    return result

# Hàm kiểm tra định dạng biển số
def license_complies_format(license_plate):
    if len(license_plate) not in [9, 11]:
        return False, license_plate
    # Xây dựng các biểu thức chính quy để kiểm tra định dạng biển số
    if len(license_plate) == 9:
        # Định dạng cho biển số 9 ký tự
        pattern = r'^\d{2}-[A-Z]\d\d{4}$'
    elif len(license_plate) == 11:
        # Định dạng cho biển số 11 ký tự
        pattern = r'^\d{2}-[A-Z]{1,2}\d{3}\.\d{2}$'
    match = re.match(pattern, license_plate)
    return bool(match), license_plate

# Định dạng lại ký tự biển số
def license_plate_format(license_plate):
    # Hàm định dạng biển số vào các chuẩn định dạng
    corrected_license_plate = ''
    for char in license_plate:
        corrected_license_plate += dict_int_to_char.get(char, char)
    return corrected_license_plate

# Hàm predict ảnh
def predict(image, image2):
    # Logic phát hiện biển số và xử lý hình ảnh
    # Trích xuất biển số, đọc ký tự và định dạng lại
    is_license_plate, license_plate = get_license_plate(cv2.imread(image))
    return {
        "is_license_plate": is_license_plate,
        "license_plate": license_plate,
    }


