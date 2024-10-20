from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm.session import Session
from fastapi.responses import FileResponse
from typing import List
import os
from schemas.schemas import EmployeeDisplay, EmployeeBase, UserAuth
from db.database import get_db
from db import db_employee
from file.save_file import save_avatar_upload_from_user
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)

# Tạo thông tin nhân viên vào CSDL
@router.post("",response_model= EmployeeDisplay)
def create_user(request: EmployeeBase, db: Session = Depends(get_db)): # avatar: UploadFile = File(...): không thể vừa tải lên Json vừa uploadfile
    """
    Tạo thông tin nhân viên vào CSDL, việc tạo thông tin và cập nhật hình ảnh không thể thực hiện cùng lúc  

    """
    # avatar_path = save_avatar_upload_from_user(user_id_code= request.id_code, avatar= avatar)
    avatar_path = "None"
    
    return db_employee.create_employee(db= db, request= request, avatar_path = avatar_path)

# Cập nhật avatar cho nhân viên
@router.post("/{id_code}/upload_avatar")
def upload_avatar(id_code_employee: int, avatar: UploadFile = File(...), db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    """
    Người dùng cập nhật hình ảnh  
    Lưu hình ảnh vào server
    """
    # Lưu avatar và cập nhật đường dẫn vào cơ sở dữ liệu
    avatar_path = save_avatar_upload_from_user(user_id_code=id_code_employee, avatar=avatar)
    
    return db_employee.upload_avatar(db= db, id_code_employee= id_code_employee, avatar_path= avatar_path)

# Truy xuất tất cả thông tin của nhân viên
@router.get("/get_all_employee", response_model=list[ EmployeeDisplay])
def get_all_employee(db: Session = Depends(get_db)):
    """
    Truy xuất tất cả thông tin nhân viên trong CSDL
    """
    return db_employee.get_all_employee(db= db)

@router.get("/view/{name}", response_class= FileResponse )
def get_file(name: str):
    """
    API cho phép người dùng tải xuống tệp tin từ server  
    Yêu cầu trạng thái phản hồi là **response_class= FileResponse**  
    - **name**: là tệp tin mà người dùng muốn tải, nó yêu cầu cả đuôi như cat.png, requirements.txt
    ## Ví dụ
    ```python
    import requests

    # URL của API mà bạn muốn tải xuống tệp
    url_view_file = "http://localhost:8000/file/view/cat.png"

    # Gửi yêu cầu GET để tải xuống tệp
    response = requests.get(url_view_file)

    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        # Lưu tệp vào đĩa
        with open("downloaded_cat.png", "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    ```
    """

    path = f"files/{name}"

    # Kiểm tra xem tệp có tồn tại không
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return path

# Tải avatar nhân viên về máy tính local
@router.get("/download_avatar")
def download_avatar(id_code: int):

    """
    API tải hình ảnh nhân viên từ `server` về máy tính cục bộ  
    Chỉ cần cung cấp `id_code`: mã nhân viên là được  
    ## Ví dụ
    ```python
    import requests

    # URL của API mà bạn muốn tải xuống tệp
    url_view_file = "http://localhost:8000/employee/download_avatar?id_code=238299"

    # Gửi yêu cầu GET để tải xuống tệp
    response = requests.get(url_view_file)

    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        # Lưu tệp vào đĩa
        with open("downloaded_cat.png", "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    ```
    """

    file_path = f"data/employee/{id_code}/avatars/avatar.png"
    # Kiểm tra xem tệp có tồn tại trên server không
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Không có thư mục của nhân viên này")

    # Trả về tệp để tải xuống
    return FileResponse(file_path, media_type="image/jpeg", filename=os.path.basename(file_path))

# Truy xuất thông tin nhân viên dựa trên biển số xe
@router.get("/{license_plate}/information", response_model= EmployeeDisplay)
def get_employee_from_license_plate(license_plate: str, db: Session = Depends(get_db)):

    return db_employee.get_employee_from_license_plate(db= db, license_plate= license_plate)