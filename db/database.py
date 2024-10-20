from sqlalchemy import create_engine # pip install SQLAlchemy
import socket
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import URL

"""
Định nghĩa cơ sở dữ liệu 
"""

# connection_url = "sqlite:///./fastapi-practice.db" # Dùng để tạo DB sql lite
MY_HOSTNAME = socket.gethostname() # Tên laptop
MY_IP_ADDR = socket.gethostbyname(MY_HOSTNAME) # Địa chỉ IPV4

# Dùng để tạo DB SQL Server # pip install pyodbc
connection_url = URL.create(
    "mssql+pyodbc",
    username="sa",
    password="123456789",
    host=MY_IP_ADDR, #172.31.99.130  #192.168.0.102
    port=1433,
    database="Smart_Parking_Server",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes"
    },
)
engine = create_engine(
    connection_url
)

# Tạo một nhà máy (sessionmaker) tự động tạo các Session
# Khi sử dụng scoped_session, bạn sẽ có một session riêng biệt cho mỗi luồng hoặc yêu cầu,
# và chúng sẽ không bị xung đột với nhau. Đây là cách an toàn và hiệu quả để quản lý session trong các ứng dụng web đa luồng.
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Khai báo cơ sở dữ liệu với SQLAlchemy
Base = declarative_base()

# Hàm lấy session cho mỗi request (phải nhớ đóng session sau khi sử dụng)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()