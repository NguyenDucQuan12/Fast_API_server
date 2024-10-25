from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import jwt # pip install python-jose
from jose.exceptions import JWTError
from db.database import get_db
from db import db_user
 

# Khóa bí mật, nên tạo nó ngẫu nhiên bằng cách sau
# mở terminal và chạy lệnh: openssl rand -hex 32
# Khóa này chỉ dành cho việc phát triển API, không ai khác có thể sử dụng
# Chỉ những bên có SECRET_KEY mới có thể xác thực và giải mã token.
SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# chỉ định endpoint để lấy token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Tạo token với tiêu chuẩn JWT (RFC 7591)  
    - **data: dict**: Là dữ liệu mà bạn muốn mã hóa và lưu trữ trong JWT. 
    Nó thường chứa thông tin về người dùng như `user_id`, `username`, hoặc bất kỳ dữ liệu nào khác mà bạn muốn bao gồm trong token.  
    - **expires_delta**: Thời gian hết hạn của token, mặc định là 15 phút
    """
    # Tạo một bản sao data để thao tác, ko ảnh hưởng đến data gốc
    to_encode = data.copy()

    # Thêm thời gian tồn tại cho token, nếu không cung cấp thì mặc định nó sẽ là 15 phút
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Tạo token với khóa bí mật và phương thức tạo
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    """
    Lấy thông tin người dùng hiện tại dựa vào `token`  
    - `payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])` sẽ giải mã token dựa vào khóa bí mật và thuật toán đã sử dụng
    """
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Không thể xác thực đăng nhập",
        headers= {"WWW-Authenticate": "Bearer"}
    )
    try:
        # ví dụ ta có token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InR2Y19hZG1faXRAdGVydW1vLmNvLmpwIiwiZXhwIjoxNzI5ODcxMjQ2fQ.G-m2PjheT-zIQ7R9TkD9LWngHbZSeKF1LK8obtmE93k
        # Các giá trị ở giữa 2 dấu chấm sẽ là payload, từ đó ta có thể giải mã được giá trị ta đính kèm vào đó.
        # ta thu đưuọc email và thời gian token hết hạn, vì vậy không được để lộ token, vì khi đó người khác có thể giải mã và thu được thông tin từ token
        # Giải mã token dựa vào khóa bí mật và phương thức tạo
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])

        # Trích xuất email từ Payload của JWT, bắt buộc lúc tạo token phải cung cấp `data` là `email` thì khi giải mã mới truy xuất được
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Truy vấn thông tin người dùng thông qua email đã giải mã
    user = db_user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user