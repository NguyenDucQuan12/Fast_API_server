from pydantic import BaseModel
from typing import List
from datetime import datetime

"""
Định nghĩa lược đồ từ người dùng đến API và từ API gửi đến người dùng  
Có nghĩa là các thông tin sẽ hiển thị khi gọi đến API, giới hạn một số thông tin bí mật không được phép cho người dùng xem khi gọi API
"""

class EmployeeBase(BaseModel):
    """
    Class này chứa thông tin cần được cung cấp để tạo một nhân viên mới
    - **id code**: Mã nhân viên  
    - **id card**: Mã thẻ từ của nhân viên  
    - **username**: Họ tên nhân viên  
    - **email**: Email của nhân viên  
    - **phone_number**: SĐT của nhân viên  
    - **section**: Bộ phận của nhân viên  
    - **permission**: Quyền hạn  
    - **other**: các cột được bổ sung thông tin sau này, khi nào thêm thông tin thì thêm vào  
    """
    id_code_employee: int
    id_card: int
    id_vehicle: int
    username: str
    email: str
    phone_number: str
    section: str
    permission: str

class EmployeeDisplay(BaseModel):
    """
    Trả về thông tin người dùng theo ý muốn, không trả về những thông tin quan trọng như password đã hash
    Lưu ý tên của các trường thông tin trả về phải giống nhau, nếu không gặp lỗi
    - **id code**: Mã nhân viên  
    - **username**: Họ tên nhân viên  
    - **avatar**: Ảnh đại diện của nhân viên
    - **vehicle**: Phương tiện di chuyển  
    - **email**: Email của nhân viên  
    - **phone_number**: SĐT của nhân viên  
    - **section**: Bộ phận của nhân viên  
    - **permission**: Quyền hạn  
    - **other**: các cột được bổ sung thông tin sau này  
    -  **Config**: cho phép tự động chuyển đổi dữ liệu type: Database quay trở về kiểu mà ta đã khai báo (str)
    """
    id_code_employee: int
    username: str
    avatar: str
    email:str
    section: str
    id_vehicle: int
    class Config():
        from_attributes  = True

class ImageBase(BaseModel):
    """
    Class này chứa thông tin về hình ảnh khi có người ra vào nhà xe khi tạo dữ liệu lên DB  
    - **in_out**: Vào hay ra nhà xe  
    - **time**: Thời gian vào/ra  
    - **license_image_path**: Đường dẫn hình ảnh biển số  
    - **background_image_path**: Đường dẫn hình ảnh toàn cảnh  
    - **face_image_path**: Đường dẫn hình ảnh khuồn mặt người lái  
    - **location**: vị trí  
    - **other**: thông tin thêm
    """
    id_employee: int
    in_out : str
    time_in: datetime
    license_image_path_in : str
    background_image_path_in : str
    face_image_path_in : str
    location_in : str
    time_out : datetime
    license_image_path_out : str
    background_image_path_out : str
    face_image_path_out : str
    location_out : str


class ImageDisplay(BaseModel):
    """
    Class này chứa thông tin hình ảnh ra vào nhà xe sẽ được hiển thị khi truy vấn
    Hiển thị trong ImageDisplay  
    - **in_out**: Ra/vào nhà xe  
    - **time**: Thời gian ra/vào  
    - **license_image_path**: Biển số xe lúc vào  
    - **background_image_path**: Hình ảnh toàn cảnh  
    - **face_image_path**: Hình ảnh khuôn mặt  
    - **employee**: Nhân viên đã đăng ký phương tiện  
    - **vehicle**: Thông tin phương tiện  
    """
    id_employee: int
    in_out : str
    time_in: datetime
    license_image_path_in : str
    background_image_path_in : str
    face_image_path_in : str
    location_in : str
    time_out : datetime
    license_image_path_out : str
    background_image_path_out : str
    face_image_path_out : str
    location_out : str
    
    class Config():
        from_attributes  = True

class VehicleBase(BaseModel):
    """
    Class này chứa thông tin về phương tiện nhân viên cần cung cấp để đăng ký lên DB  
    - **vehicle_name**: Tên phương tiện  
    - **model**: Phiên bản  
    - **color**: Màu sắc phương tiện  
    - **picture_vehicle**: Hình ảnh phương tiện   
    - **other**: các cột được bổ sung thông tin sau này  
    """
    id_employee: int
    vehicle_name: str
    model: str
    color: str
    license_plate: str
    picture_vehicle: str

class VehicleDisplay(BaseModel):
    """
    Class này chứa thông tin về phương tiện sẽ được hiển thị khi truy vấn
    Hiển thị trong VehicleDisplay
    - **vehicle_name**: Tên phương tiện  
    - **model**: Phiên bản  
    - **color**: Màu sắc phương tiện  
    - **picture_vehicle**: Hình ảnh phương tiện   
    - **employee**: Thông tin nhân viên đăng ký xe   
    - **image**: Hình ảnh phương tiện ra/vào nhà xe   
    - **other**: các cột được bổ sung thông tin sau này 
    """
    id_employee: int
    vehicle_name: str
    model: str
    color: str
    license_plate: str
    picture_vehicle: str
    class Config():
        from_attributes  = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str

class UserBase(BaseModel):
    username: str
    email:str
    password: str

class UserDisplay(BaseModel):
    username: str
    email:str
    class Config():
        from_attributes  = True

class ModeBase(BaseModel):
    mode : str

class ModeDisplay(BaseModel):
    mode: str
    time: datetime
    class Config():
        from_attributes  = True