from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status, UploadFile, File
from sqlalchemy import exc
from db.model import DbModeLane
from schemas.schemas import ModeBase
import datetime
from sqlalchemy import desc


def create_mode_lane(db: Session, request: ModeBase):
    """
    Tạo thông tin nhân viên mới vào cơ sở dữ liệu  
    Các thông tin yêu cầu người dùng cung cấp phải đầy đủ như đã khai báo ở 
    
    """
    
    new_mode = DbModeLane(
        mode = request.mode,
        time = datetime.datetime.now(),
        other1 = "Not use",
        other2 = "Not use",
        other3 = "Not use",
        other4 = "Not use",
        other5 = "Not use",
    )

    try:
        db.add(new_mode)
        db.commit()
        db.refresh(new_mode)
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(e)

        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Thêm chế độ cho làn xe không thành công"
        )
    return new_mode

def get_latest_mode_lane(db: Session):
    """
    Truy vấn mode lane mới nhất từ cơ sở dữ liệu
    """
    return db.query(DbModeLane).order_by(desc(DbModeLane.time)).first()

def update_mode_lane(db: Session, new_mode: str, id: int = 1):
    """
    Cập nhật thông tin mode lane trong cơ sở dữ liệu
    - `id`: ID của mode lane cần cập nhật
    - `request`: Thông tin cập nhật từ người dùng
    """
    
    # Truy vấn mode lane từ cơ sở dữ liệu dựa trên ID
    mode_lane = db.query(DbModeLane).filter(DbModeLane.id == id).first()
    
    # Kiểm tra nếu không tìm thấy mode lane
    if not mode_lane:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mode lane với ID {id} không tồn tại"
        )
    
    try:
        # Cập nhật các trường thông tin của mode lane
        mode_lane.mode = new_mode
        mode_lane.time = datetime.datetime.now()  # Cập nhật thời gian hiện tại
        
        # Lưu thay đổi vào cơ sở dữ liệu
        db.commit()
        db.refresh(mode_lane)
        
    except exc.SQLAlchemyError as e:
        # Rollback nếu có lỗi xảy ra
        db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cập nhật chế độ cho làn xe không thành công"
        )
    
    return mode_lane
