from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from sqlalchemy import exc
from schemas.schemas import UserBase
from db.model import DbUser
from db.hash import Hash

"""
Các câu lệnh truy vấn tới CSDL User
"""

def create_user(db: Session, request: UserBase):

    """
    Tạo thông tin người dùng vào CSDL  
    - `request`: Thông tin mà người dùng cần cung cấp  
    Mật khẩu sẽ được mã hóa sau đó.  
    Kết quả trả về:  
    200:  
    - `new_user`: Thông tin người dùng mới  
    500:  
    - `"message": "Lỗi khi thêm người dùng mới"`
    """
    
    new_user =  DbUser(
        username = request.username,
        email = request.email ,
        password = Hash.bcrypt(request.password)
    )
    try:
        db.add(new_user)
        db.commit()
        # refresh giúp nhận được giá trị ID của người dùng, vì nó là giá trị tự tăng
        db.refresh(new_user)
    except exc.SQLAlchemyError as e:   
        # Trong quá trình insert lỗi thì giá trị id (cột IDENTITY) vẫn tự tăng, đây là hành vi mặc định của SQL Server
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Lỗi khi thêm người dùng mới"
            }
        )
    return new_user 

def get_user_by_email(db: Session, email: str):
    """
    Truy vấn thông tin người dùng với `email` được cung cấp  
    
    """
    user = db.query(DbUser).filter(DbUser.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
                "message": f"Không tìm thấy người dùng có địa chỉ email:{email}"
            }
        )
    
    return user