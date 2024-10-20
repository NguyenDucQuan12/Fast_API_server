from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Dict
import hashlib
import os
import json

router = APIRouter(
    prefix="/update",
    tags=["update"]
)

# Đường dẫn tới thư mục hiện tại
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Đường dẫn tới thư mục chứa các phiên bản của phần mềm
VERSIONS_DIR = os.path.join(BASE_DIR, 'versions')
# Đường dẫn tới tệp json chứa thông tin của phiên bản cần cập nhật
VERSION_INFO_FILE = os.path.join(BASE_DIR, 'version_info.json')


@router.get("/latest-version")
def get_latest_version() -> Dict:
    try:
        with open(VERSION_INFO_FILE, 'r', encoding='utf-8') as f:
            version_info = json.load(f)
        return version_info
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail= {
                                "message": "Không thể truy cập nội dung từ tệp tin version_info",
                                "error": f"Chi tiết lỗi: {e}"
                            })

@router.get("/download/{version}")
def download_version(version: str):
    version_path = os.path.join(VERSIONS_DIR, version)

    if not os.path.exists(version_path):
        raise HTTPException(status_code=404,
                            detail= {
                                "message": f"Không tìm thấy phiên bản {version}",
                                "error": f"Đường dẫn không tồn tại trên server: {version_path} "
                            })
    
    # Giả sử tệp được nén có tên cố định, ví dụ 'Smartparking_v1.0.0.zip'
    file_name = f"Smartparking_v{version}.zip"
    file_path = os.path.join(version_path, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,
                            detail= {
                                "message": f"Không tìm thấy tệp zip: {file_name}",
                                "error": f"Đường dẫn không tồn tại trên server: {file_path} "
                            })

    return FileResponse(path=file_path, filename=file_name)

#  Tính checksum của file zip khi đã nén
@router.get("/checksum")
def calculate_checksum(file_path):

    # Loại bỏ dấu ngoặc kép bên ngoài nếu có
    file_path = file_path.strip('"').strip("'")

    # Kiểm tra xem tệp có tồn tại không
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    sha256_hash = hashlib.sha256()
    with open(file_path,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    calculated_checksum = sha256_hash.hexdigest()
    return {
        "message": calculated_checksum
    }
