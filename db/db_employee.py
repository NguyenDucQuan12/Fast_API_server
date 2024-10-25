from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from sqlalchemy import exc
from db.model import DbEmployee, DbImage_Employee, DbVehicle, DbEmployeeVehicle
from schemas.schemas import EmployeeBase


def create_employee(db: Session, request: EmployeeBase, avatar_path):
    """
    Tạo thông tin nhân viên mới vào cơ sở dữ liệu  
    Các thông tin yêu cầu người dùng cung cấp phải đầy đủ như đã khai báo ở `DbEmployee`  
    Kết quả trả về:  
    200:  
    - `newemployee`: Thông tin nhân viên đã được tạo  
    500:  
    - `"message": f"Thêm dữ liệu mới không thành công: {e}"`    
    """
    # Tạo thông tin nhân viên mới từ request
    new_employee = DbEmployee(
        id_code_employee = request.id_code_employee,
        id_card = request.id_card,
        id_vehicle = request.id_vehicle,
        username = request.username,
        avatar = avatar_path,
        email = request.email,
        phone_number=request.phone_number,
        section = request.section,
        permission = request.permission,
        other1 = "Not use",
        other2 = "Not use",
        other3 = "Not use",
        other4 = "Not use",
        other5 = "Not use",
    )

    # Ghi dữ liệu lên CSDL
    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= {
                "message": f"Thêm dữ liệu mới không thành công: {e}"
            }
        )
    return new_employee

def upload_avatar(db: Session, id_code_employee: int, avatar_path: str):
    """
    Tải ảnh nhân viên lên sau khi đã tạo thông tin trước đó  
    200:  
    - `"message": avatar_path` : Trả về đường dẫn hình ảnh được lưu trên server  
    404:  
    - `"message":f"Không tìm thấy nhân viên có mã nhân viên: {id_code_employee}"`  
    500:  
    - `"message": f"Xảy ra lỗi trong quá trình cập nhật ảnh đại diện {e}"`
    """
    # Truy vấn thông tin nhân viên thông qua mã nhân viên (id_code_employee)
    employee = db.query(DbEmployee).filter(DbEmployee.id_code_employee == id_code_employee).first()

    if not employee:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= {
                    "message":f"Không tìm thấy nhân viên có mã nhân viên: {id_code_employee}"
            }
        )
    
    # Cập nhật lại đường dẫn avatar trong cơ sở dữ liệu
    employee.avatar = avatar_path

    # Lưu dữ liệu lên CSDL
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= {
                "message": f"Xảy ra lỗi trong quá trình cập nhật ảnh đại diện: {e}"
            }
        )

    return {
        "message": avatar_path
    }

def get_all_employee(db: Session):
    """
    Truy vấn tất cả thông tin nhân viên trong bảng `employee`  
    Kết quả trả về:  
    200:  
    - `employees`: Danh sách tất cả nhân viên  
    500:  
    - `"message": f"Xảy ra lỗi trong quá trình truy vấn thông tin nhân viên: {e}"`
    """
    try:
        employees = db.query(DbEmployee).all()
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= {
                "message": f"Xảy ra lỗi trong quá trình truy vấn thông tin nhân viên: {e}"
            }
        )
    return employees

def delete_employee(db: Session, id_code_employee: int, current_admin):
    """
    Xóa thông tin một nhân viên dựa vào mã nhân viên `(id_code_employee)`  
    Việc xóa thông tin nhân viên chỉ được phép thức thi với một số người nhất định, gọi là `admin`.  
    Kết quả trả về:  
    200:  
    - `"message": f"{current_admin} Đã xóa thành công nhân viên: {id_code_employee}"`  
    404:   
    - `"message": f"{current_admin}: Không tìm thấy nhân viên có mã nhân viên: {id_code_employee}"`  
    500:  
    - `"message": f"Có lỗi trong quá trình xóa nhân viên {id_code_employee}: {e}"`
    """
    employee = db.query(DbEmployee).filter(DbEmployee.id_code_employee == id_code_employee).first()

    if not employee:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= {
                "message": f"{current_admin}: Không tìm thấy nhân viên có mã nhân viên: {id_code_employee}"
            }
        )
    
    try:
        db.delete(employee)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= {
                "message": f"Có lỗi trong quá trình xóa nhân viên {id_code_employee}: {e}"
            }
        )
    return {
        "message": f"{current_admin} đã xóa thành công nhân viên: {id_code_employee}"
    }

def get_employee_from_license_plate(db: Session, license_plate: str):
    """
    Truy vấn một nhân viên dựa trên biển số xe được cung cấp  
    Kết quả trả về:  
    200:  
    - `employees`: Thông tin nhân viên ứng với biển số xe đăng ký  
    400:  
    - `error và id_code_employee` : Chưa có thông tin phương tiện với biển số  
    404:  
    - `error và id_code_employee` : Chưa có thông tin nhân viên với biển số  
    """
    # Lấy đối tượng vehicle thông qua biển số
    vehicle = db.query(DbVehicle).filter(DbVehicle.license_plate == license_plate).first()

    if vehicle:
        # Từ phương tiện truy vấn thông tin nhân viên
        employees = db.query(DbEmployee).filter(DbEmployee.id_code_employee == vehicle.id_employee).first()

        if employees:
            return employees
        else:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= {   
                        "error": f"{vehicle.id_employee} chưa có thông tin đăng ký",
                        "id_code_employee": "Chưa có thông tin trên máy chủ"
                    }
        )
    else:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= {   
                        "error": f"{license_plate} chưa có thông tin đăng ký",
                        "id_code_employee": "Xe chưa đăng ký"
                    }
        )
    
def get_many_employees_from_license_plate(db: Session, license_plate: str):
    """
    Truy vấn danh sách nhân viên dựa trên biển số xe được cung cấp
    """
    # Lấy phương tiện qua biển số xe
    vehicle = db.query(DbVehicle).filter(DbVehicle.license_plate == license_plate).first()

    if vehicle:
        # Lấy danh sách id_employee từ bảng trung gian dựa trên id_vehicle
        employee_ids = db.query(DbEmployeeVehicle.id_employee).filter(DbEmployeeVehicle.id_vehicle == vehicle.id).all()

        # Truy vấn thông tin nhân viên dựa trên danh sách id_employee
        # Sử dụng in_ trong SQLAlchemy: Hàm filter(DbEmployee.id_code_employee.in_([...])) cho phép bạn truy vấn nhiều nhân viên dựa trên danh sách ID.
        employees = db.query(DbEmployee).filter(DbEmployee.id_code_employee.in_([emp[0] for emp in employee_ids])).all()

        if employees:
            return employees
        else:
            return {
                "message": f"Phương tiện {license_plate} chưa đăng ký với bất kỳ nhân viên nào"
            }
    else:
        return {
            "message": f"Phương tiện {license_plate} chưa đăng ký lên CSDL"
        }

def get_employee_with_latest_image(db: Session):
    """
    Truy vấn thông tin nhân viên với thời gian ra vào mới nhất  
    """
    # Truy vấn nhân viên với hình ảnh ra vào mới nhất
    employees_with_images = db.query(DbEmployee, DbImage_Employee).join(DbImage_Employee).order_by(
        DbImage_Employee.time.desc()).all()

    return employees_with_images

def get_latest_image_of_employee(db: Session, employee_id: int):
    # Truy vấn nhân viên với hình ảnh ra vào mới nhất
    latest_image = db.query(DbImage_Employee).filter(DbImage_Employee.employee_id == employee_id).order_by(
        DbImage_Employee.time.desc()).first()

    return latest_image

def get_latest_image_of_employee_by_in_out(db: Session, employee_id: int, in_out_status: str):
    # Truy vấn nhân viên với hình ảnh ra vào mới nhất dựa trên trạng thái in_out
    latest_image = db.query(DbImage_Employee).filter(
        DbImage_Employee.employee_id == employee_id,
        DbImage_Employee.in_out == in_out_status  # Điều kiện theo trạng thái "in" hoặc "out"
    ).order_by(DbImage_Employee.time.desc()).first()

    return latest_image

