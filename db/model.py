from sqlalchemy import Unicode
from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime

"""
Định nghĩa tất cả các bảng trong SQL Server
"""

class DbUser(Base):
    """
    Bảng người dùng  
    Bảng này chứa thông tin về thông tin đăng nhập như : `username`, `password`, `email`
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key= True, index= True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

class DbEmployee(Base):

    """
    Định nghĩa bảng nhân viên trong CSDL  
    - **tablename** là tên của bảng  
    - **id code employee**: Mã nhân viên  
    - **id card**: Mã code phía sau thẻ nhân viên  
    - **id vehicle**: Id phương tiện mà nhân viên đã đăng ký  
    - **username**: Họ tên nhân viên  
    - **avatar**: Đường link hình ảnh nhân viên đã đăng ký với hệ thống  
    - **email**: Email của nhân viên  
    - **phone_number**: SĐT của nhân viên  
    - **section**: Bộ phận của nhân viên  
    - **permission**: Quyền hạn  
    - **other**: các cột được bổ sung thông tin sau này  
    Bảng này sẽ được tạo nếu nó chưa tồn tại trong CSDL
    """
    __tablename__ = "employee"
    id_code_employee = Column(Integer, primary_key=True, unique=True)
    id_card = Column(Integer)
    id_vehicle = Column(Integer)
    username = Column(Unicode(100)) # Sử dụng kiểu Nvarchar: NVARCHAR
    avatar = Column(Unicode(100))
    email = Column(String(255), unique=True)
    phone_number = Column(String)
    section = Column(String)
    permission = Column(String)

    other1 = Column(String)
    other2 = Column(String)
    other3 = Column(String)
    other4 = Column(String)
    other5 = Column(String)
    
class DbImage_Employee(Base):

    """
    Định nghĩa bảng chứa hình ảnh về ảnh ra vào kèm thời gian ra vào của nhân viên  
    - **id employee**: Mã nhân viên vào/ra nhà xe  
    - **in_out**: Trạng thái vào/ra của nhân viên  
    - **time in**: Thời gian nhân viên vào nhà xe  
    - **license_image_path in**: Hình ảnh biển số xe nhân viên vào nhà xe  
    - **background_image_path in **: Hình ảnh toàn cảnh nhân viên vào nhà xe  
    - **face_image_path in**: Hình ảnh khuôn mặt nhân viên vào nhà xe  
    - **location in **: Vị trí làn vào của nhân viên  
    - **other**: các cột được bổ sung thông tin sau này  

    Bảng này sẽ được tạo nếu nó chưa tồn tại trong CSDL
    """
    __tablename__ = "image_employee"
    id = Column(Integer, primary_key=True, index=True)
    id_employee = Column(Integer)
    in_out = Column(String)
    time_in = Column(DateTime)
    license_image_path_in = Column(String)
    background_image_path_in = Column(String)
    face_image_path_in = Column(String)
    time_out = Column(DateTime)
    license_image_path_out = Column(String)
    background_image_path_out = Column(String)
    face_image_path_out = Column(String)
    location_in = Column(String)
    location_out = Column(String)
    other1 = Column(String)
    other2 = Column(String)
    other3 = Column(String)
    other4 = Column(String)
    other5 = Column(String)

class DbVehicle(Base):

    """
    Định nghĩa bảng chứa thông tin phương tiện của nhân viên  
    - **id_employee**: Mã nhân viên đã đăng ký phương tiện này  
    - **vehicle_name**: Tên phương tiện  
    - **model**: Phiên bản  
    - **color**: Màu sắc phương tiện  
    - **picture_vehicle**: Hình ảnh phương tiện  
    - **license_plate**: Biển số xe  

    Bảng này sẽ được tạo nếu nó chưa tồn tại trong CSDL
    """
    __tablename__ = "vehicle"
    id = Column(Integer, primary_key=True, index=True)
    id_employee = Column(Integer)
    vehicle_name = Column(String)
    model = Column(String)
    color = Column(String)
    license_plate = Column(String)
    picture_vehicle = Column(String)
    other1 = Column(String)
    other2 = Column(String)
    other3 = Column(String)
    other4 = Column(String)
    other5 = Column(String)

class DbEmployeeVehicle(Base):
    """
    Bảng trung gian lưu trữ mối quan hệ nhiều-nhiều giữa nhân viên và phương tiện  
    Khi cần truy vấn phương tiện cùng nhân viên thì chỉ cần truy vấn bảng này  
    Không phải truy vấn trực tiếp vào bảng nhân viên, nếu bảng nhân viên quá lớn thì có thể gây ra chậm  
    """
    __tablename__ = "employee_vehicle"
    id = Column(Integer, primary_key=True, index=True)
    id_employee = Column(Integer)  # ID của nhân viên (không cần ForeignKey)
    id_vehicle = Column(Integer)  # ID của phương tiện (không cần ForeignKey)

class DbModeLane(Base):
    """
    Bảng này diều chỉnh chế độ của làn là đang đi vào hay đi ra
    """
    __tablename__ = "mode_lane"
    id = Column(Integer, primary_key=True, index=True)
    mode = Column(Unicode(100))
    time = Column(DateTime)
    other1 = Column(String)
    other2 = Column(String)
    other3 = Column(String)
    other4 = Column(String)
    other5 = Column(String)
