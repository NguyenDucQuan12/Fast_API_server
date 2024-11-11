from test import password
import os

# Tải các biến môi trường từ tệp .env
# load_dotenv()

print(password.DB_USERNAME)
# Lấy giá trị biến môi trường
db_username = os.getenv("DB_USERNAME", "default")
db_password = os.getenv("DB_PASSWORD")
secret_key = os.getenv("SECRET_KEY")

