from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status, UploadFile, File
from sqlalchemy import exc, desc
from db.model import DbImage_Employee
from schemas.schemas import ImageBase
import datetime


async def create_image(db: Session, request: ImageBase):
    """
    Tạo thông tin nhân viên mới vào cơ sở dữ liệu  
    Các thông tin yêu cầu người dùng cung cấp phải đầy đủ như đã khai báo ở 
    
    """
    # Tìm kiếm bản ghi hiện có với id_employee và in_out = 'in'
    existing_image = db.query(DbImage_Employee).filter(
        DbImage_Employee.id_employee == request.id_employee,
        DbImage_Employee.in_out == 'in'
    ).first()

    # Nếu đã tồn tại thông tin và trạng thái đã vào thì chỉ cập nhật không tạo mới
    if existing_image:
        # Cập nhật thông tin bản ghi hiện có
        existing_image.time_in = request.time_in
        existing_image.license_image_path_in = request.license_image_path_in
        existing_image.background_image_path_in = request.background_image_path_in
        existing_image.face_image_path_in = request.face_image_path_in
        existing_image.time_out = request.time_out
        existing_image.license_image_path_out = request.license_image_path_out
        existing_image.background_image_path_out = request.background_image_path_out
        existing_image.face_image_path_out = request.face_image_path_out
        existing_image.location_in = request.location_in
        existing_image.location_out = request.location_out
        # Cập nhật các trường khác nếu cần

        db.commit()
        db.refresh(existing_image)
        return existing_image
    else:
        # time = datetime.datetime.now()
        new_image = DbImage_Employee(
            id_employee = request.id_employee,
            in_out = request.in_out,
            time_in = request.time_in,
            license_image_path_in = request.license_image_path_in,
            background_image_path_in = request.background_image_path_in,
            face_image_path_in = request.face_image_path_in,
            time_out = request.time_out,
            license_image_path_out = request.license_image_path_out,
            background_image_path_out = request.background_image_path_out,
            face_image_path_out = request.face_image_path_out,
            location_in=request.location_in,
            location_out=request.location_out,
            other1 = "Not use",
            other2 = "Not use",
            other3 = "Not use",
            other4 = "Not use",
            other5 = "Not use",
        )

        try:
            db.add(new_image)
            db.commit()
            db.refresh(new_image)
        except exc.SQLAlchemyError as e:
            db.rollback()
            print(e)

            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Thêm hình ảnh mới không thành công"
            )
    return new_image

def get_latest_in_employee_from_id_employee(id_employee: int, db: Session):

    # Truy vấn để tìm record thỏa mãn id_employee, in_out = "in", và thời gian gần đây nhất
    employee_image = db.query(DbImage_Employee).filter(
        DbImage_Employee.id_employee == id_employee,
        DbImage_Employee.in_out == "in"
    ).order_by(desc(DbImage_Employee.time_in)).first()

    # Nếu không tìm thấy record nào
    if not employee_image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={   
                        "error": f"Phương tiện chưa có thông tin lúc đi vào, vui lòng kiểm tra lại"
                    })

    # Trả về kết quả dưới dạng JSON
    return employee_image

def update_employee_in_to_success(id_employee: int, db: Session, request: ImageBase):
    # Truy vấn để tìm record thỏa mãn id_employee, in_out = "in", và thời gian gần đây nhất
    employee_image = db.query(DbImage_Employee).filter(
        DbImage_Employee.id_employee == id_employee,
        DbImage_Employee.in_out == "in"
    ).order_by(desc(DbImage_Employee.time_in)).first()

    # Nếu không tìm thấy record nào
    if not employee_image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không tìm thấy thông tin lúc vào")
    
    # Cập nhật trạng thái in_out thành 'success'
    employee_image.in_out = request.in_out
    employee_image.time_out = request.time_out
    employee_image.license_image_path_out = request.license_image_path_out
    employee_image.background_image_path_out = request.background_image_path_out
    employee_image.face_image_path_out = request.face_image_path_out
    employee_image.location_out=request.location_out
    
    # Commit thay đổi vào database
    db.commit()

    # Refresh để cập nhật thông tin mới nhất của employee_image từ database
    db.refresh(employee_image)
    
    # Trả về kết quả cập nhật dưới dạng JSON hoặc một thông điệp thành công
    return employee_image