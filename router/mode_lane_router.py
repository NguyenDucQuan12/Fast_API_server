from fastapi import APIRouter, Depends, HTTPException, status
import threading
from sqlalchemy.orm.session import Session
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from schemas.schemas import ModeDisplay, ModeBase
from db.database import get_db
from db import db_mode


router = APIRouter(
    prefix="/modelane",
    tags=["modelane"]
)


# Khóa để đảm bảo các yêu cầu truy cập mode không bị xung đột
mode_lock = threading.Lock()

# Tạo thông tin nhân viên vào CSDL
@router.post("/create_new_mode",response_model= ModeDisplay)
def create_new_mode(request: ModeBase, db: Session = Depends(get_db)): # avatar: UploadFile = File(...): không thể vừa tải lên Json vừa uploadfile
    
    return db_mode.create_mode_lane(db= db, request= request)

# Biến lưu giá trị mode
mode_data = {"mode": "in"}

# API GET để lấy mode hiện tại
@router.get("/getmode", response_model= ModeDisplay)
async def get_mode(db: Session = Depends(get_db)):
    """
    API truy vấn giá trị mode lane hiện tại.  
    Sử dụng lock để đảm bảo tính toàn vẹn dữ liệu khi có nhiều truy vấn đồng thời.  
    """
    try:
        mode_lane = db_mode.get_latest_mode_lane(db= db)
        if not mode_lane:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông tin mode lane"
            )
        return mode_lane
        
    except Exception as e:
        print(f"Lỗi khi truy vấn mode lane: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể truy vấn mode lane"
        )

# API PUT để chỉnh sửa mode

@router.put("/change_mode_lane", response_model=ModeDisplay)
async def update_mode_lane(new_mode, db: Session = Depends(get_db)):
    """
    API cập nhật giá trị mode lane theo ID.
    Sử dụng lock để tránh xung đột khi nhiều yêu cầu cập nhật cùng lúc.
    """
    try:
        with mode_lock:  # Sử dụng lock để đảm bảo không có xung đột
            mode_lane = db_mode.update_mode_lane(db = db, new_mode= new_mode)
            if not mode_lane:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Mode lane với ID {id} không tồn tại"
                )
        # Xóa cache của endpoint getmode
        await FastAPICache.clear(namespace="getmode")
        # Làm mới cache bằng cách gọi lại API lấy dữ liệu
        await get_mode(db)
        return mode_lane

    except Exception as e:
        print(f"Lỗi khi cập nhật mode lane: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể cập nhật mode lane"
        )
