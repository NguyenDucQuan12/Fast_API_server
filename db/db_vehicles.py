from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status, UploadFile, File
from sqlalchemy import exc
from db.model import DbVehicle
from schemas.schemas import EmployeeBase
from sqlalchemy import desc


def create_vehicle(db: Session, request: DbVehicle):
    """
    Tạo thông tin nhân viên mới vào cơ sở dữ liệu  
    Các thông tin yêu cầu người dùng cung cấp phải đầy đủ như đã khai báo ở 
    
    """
    
    new_vehicle = DbVehicle(
        id_employee = request.id_employee,
        vehicle_name = request.vehicle_name,
        model = request.model,
        color = request.color,
        license_plate = request.license_plate,
        picture_vehicle=request.picture_vehicle,
        other1 = "Not use",
        other2 = "Not use",
        other3 = "Not use",
        other4 = "Not use",
        other5 = "Not use",
    )

    try:
        db.add(new_vehicle)
        db.commit()
        db.refresh(new_vehicle)
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(e)

        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Thêm phương tiện mới không thành công"
        )
    return new_vehicle

def get_all_vehicle(db: Session):
    vehicles = db.query(DbVehicle).all()
    return vehicles

def delete_employee(db: Session, license_plate: str):
    vehicle = db.query(DbVehicle).filter(DbVehicle.license_plate == license_plate).first()

    if not vehicle:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Không tìm thấy phương tiện có mã nhân viên: {license_plate}"
        )
    
    try:
        db.delete(vehicle)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(e)

        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Có lỗi trong quá trình xóa phương tiện"
        )
    return {
        "message": f"Đã xóa thành công phương tiện: {vehicle}"
    }



