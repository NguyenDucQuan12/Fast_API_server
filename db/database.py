from sqlalchemy import create_engine # pip install SQLAlchemy
import socket
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import URL
from file import password

"""
Định nghĩa cơ sở dữ liệu 
"""

# connection_url = "sqlite:///./fastapi-practice.db" # Dùng để tạo DB sql lite
# Lấy địa chỉ IP của máy chủ bằng socket
MY_HOSTNAME = socket.gethostname()
MY_IP_ADDR = socket.gethostbyname(MY_HOSTNAME)

# "host.docker.internal" khi chạy bằng docker thì thay ip bằng câu này
# Cấu trúc chuỗi kết nối đến SQL Server
# pip install pyodbc
connection_url = URL.create(
    "mssql+pyodbc",
    username=password.DB_USER, # Tên đăng nhập 
    password=password.DB_PASSWORD, # mật khẩu đăng nhập
    host=MY_IP_ADDR, #Địa chỉ IP của máy tính lấy được
    port=1433, # cổng kết nối khi mở kết nối SQL server, xem them wor video youtube của bản thân
    database= password.DB_NAME, # Tên của database cần truy cập
    query={
        "driver": "ODBC Driver 18 for SQL Server", # Phiên bản driver của ODBC đã tải về từ microsoft
        "TrustServerCertificate": "yes"  
    },
)

# Kết nối đến SQL Server
engine = create_engine(
    connection_url
)

# Tạo một nhà máy (sessionmaker) tự động tạo các Session
# Khi sử dụng scoped_session, bạn sẽ có một session riêng biệt cho mỗi luồng hoặc yêu cầu,
# và chúng sẽ không bị xung đột với nhau. Đây là cách an toàn và hiệu quả để quản lý session trong các ứng dụng web đa luồng.
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Khai báo cơ sở dữ liệu với SQLAlchemy
Base = declarative_base()

# Hàm lấy session cho mỗi request, khi gọi các lệnh đến Database thì cần gọi hàm này để mở kết nối đến Database
# Hàm này sẽ tự động đóng kết nối sau khi sử dụng xong
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()