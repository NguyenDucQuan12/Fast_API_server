from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
from fastapi.responses import FileResponse
import os
from pathlib import Path


router = APIRouter(
    prefix="/file",
    tags=["file"]
)

# Đường dẫn thư mục lưu trữ file
UPLOAD_DIRECTORY = "file/upload/"

# Tạo thư mục nếu chưa có
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Đường dẫn file sẽ lưu
        file_location = f"{UPLOAD_DIRECTORY}{file.filename}"

        # Mở file để lưu
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Trả về thông tin khi thành công
        return {"filename": file.filename, "message": "File uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/list_file_in_folder/")
async def list_files():
    """
    Liệt kê các file trong thư mục uploads
    ```python
    import requests

    # Gửi yêu cầu GET để liệt kê file
    response = requests.get("http://127.0.0.1:8000/files/")

    # Hiển thị danh sách các file có sẵn
    print(response.json())
    ```

    """
    try:
        # Liệt kê tất cả các file trong thư mục
        files = os.listdir(UPLOAD_DIRECTORY)
        # Nếu thư mục rỗng, thông báo không có file
        if not files:
            return {"message": "Không có file nào trong thư mục"}
        
        # Trả về danh sách các file
        return {"files": files}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi liệt kê file: {str(e)}")

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    """
    ```python
    import requests

    # Tên file muốn tải
    file_name = "example.txt"

    # Gửi yêu cầu tải file
    url = f"http://127.0.0.1:8000/download/{file_name}"
    response = requests.get(url)

    # Lưu file xuống máy client
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"Tải file {file_name} thành công!")
    else:
        print(f"Lỗi khi tải file: {response.status_code}")

    ```
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    
    # Kiểm tra nếu file tồn tại
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File không tồn tại")

    # Sử dụng FileResponse để gửi file cho client
    return FileResponse(path=file_path, filename=file_name)
