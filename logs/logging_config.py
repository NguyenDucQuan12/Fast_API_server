import logging
import datetime
import os
from logging.handlers import TimedRotatingFileHandler

# Định nghĩa CustomFilter
class CustomFilter(logging.Filter):
    def filter(self, record):
        record.ip = getattr(record, 'ip', '-')
        record.api_name = getattr(record, 'api_name', '-')
        record.params = getattr(record, 'params', '-')
        record.result = getattr(record, 'result', '-')
        return True

# Hàm tạo đường dẫn log theo ngày
def get_log_file_path():
    # Lấy ngày hiện tại theo định dạng DD-MM-YY
    today_date = datetime.datetime.now().strftime("%d-%m-%y")
    
    # Tạo đường dẫn thư mục cho ngày hiện tại
    log_dir = f"logs/{today_date}"
    os.makedirs(log_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
    
    # Trả về đường dẫn đầy đủ của tệp log
    return os.path.join(log_dir, "api_log.txt")

# Khởi tạo TimedRotatingFileHandler với đường dẫn tùy chỉnh
file_handler = TimedRotatingFileHandler(
    get_log_file_path(), when="midnight", interval=1, encoding="utf-8"
)
file_handler.suffix = ""  # Đặt suffix là chuỗi rỗng, vì đường dẫn đã bao gồm ngày

# Thêm CustomFilter vào handler
file_handler.addFilter(CustomFilter())

# Định dạng log theo yêu cầu
formatter = logging.Formatter(
    "%(asctime)s - %(ip)s - %(api_name)s - %(params)s - %(result)s"
)
file_handler.setFormatter(formatter)

# Cấu hình logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.propagate = False  # Tắt propagate để log không xuất hiện trên terminal
