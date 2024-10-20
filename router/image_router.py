from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
import os
import datetime
from sqlalchemy.orm.session import Session
from schemas.schemas import ImageDisplay, ImageBase, UserAuth
from db.database import get_db
from db import db_image


router = APIRouter(
    prefix="/image",
    tags=["image"]
)
# Lấy thời gian ngày tháng năm giờ phút giấy theo định dạng string
today = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) 
date_today = str(datetime.datetime.now().strftime("%d-%m-%y"))

# Tạo đường dẫn lưu hình ảnh: data/license_plate/14-09-24/38-F73901
save_dir_license_plate= "data/license_plate/"+ date_today



# Tạo thông tin nhân viên vào CSDL
@router.post("/create_new_image",response_model= ImageDisplay)
async def create_image(request: ImageBase, db: Session = Depends(get_db)): # avatar: UploadFile = File(...): không thể vừa tải lên Json vừa uploadfile
    
    return  await db_image.create_image(db= db, request= request)

# Truy vấn thông tin nhân viên đã vào nhà xe bằng mã nhân viên
@router.get("/employee/{id_employee}/in", response_model= ImageDisplay)
def get_latest_out_employee(id_employee: int, db: Session = Depends(get_db)):
    
    return db_image.get_latest_in_employee_from_id_employee(id_employee= id_employee, db= db)

# API cập nhật thông tin nhân viên đi ra thành công, không còn trạng thái in_out = in nữa
@router.put("/employee/{id_employee}/update", response_model= ImageDisplay)
def update_employee_success_out(id_employee: int, request: ImageBase, db: Session = Depends(get_db)):
    return db_image.update_employee_in_to_success(id_employee= id_employee, request= request, db= db)

# Định nghĩa API để lấy hình ảnh từ server
@router.get("/get/view")
def get_image(image_path: str):
    
    # Kiểm tra xem file có tồn tại không
    if os.path.isfile(image_path):
        # Trả về file hình ảnh
        return FileResponse(image_path, media_type="image/jpeg")
    else:
        # Nếu không tìm thấy file, trả về lỗi 404
        return Response(status_code=404, content="Image not found")