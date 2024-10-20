from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix="/app",
    tags=["app"]
)

# Định nghĩa đường dẫn tới tệp nén trên server
ZIP_FILE_PATH = "D:\\Project\\SmartParking\\file\\QSV.rar"

@router.get("/download/setup")
def download_file():
    # Kiểm tra xem tệp có tồn tại không
    if os.path.exists(ZIP_FILE_PATH):
        # Trả về file nén dưới dạng phản hồi file
        return FileResponse(path=ZIP_FILE_PATH, media_type='application/zip', filename="downloaded_file.zip")
    else:
        # Nếu file không tồn tại, trả về thông báo lỗi
        return Response(status_code=404, content="File not found")
