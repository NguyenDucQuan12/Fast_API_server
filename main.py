# import tensorflow as tf
from fastapi import FastAPI # pip install "fastapi[standard]"
import uvicorn
import os
from fastapi.responses import FileResponse
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
import logging
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from db import model
from router import employee_router, user_router, license_plate_router, vehicles_router, image_router, mode_lane_router, update_app_router, get_file_router
from auth import authentication
from update_app import update_app

# Tạo logging 
"""
Tạo logging để lưu lại những thông tin ra với các tham số cụ thể như: thời gian, chế độ, tên file, hàm gọi, dòng code, id và tên thread, và tin nhắn
Lưu ý có thêm tham số: force = True bởi vì xung đột giữa các trình ghi nhật ký cảu các thư viện hoặc file
Nếu đối số từ khóa này được chỉ định là đúng, mọi trình xử lý hiện có được gắn vào bộ ghi nhật ký gốc sẽ bị 
xóa và đóng trước khi thực hiện cấu hình như được chỉ định bởi các đối số khác
Đối với file main sẽ dùng: logger = logging.getLogger()
Còn các file khác sẽ dùng: logger = logging.getLogger(__name__) thì sẽ tự động cùng lưu vào 1 file, cùng 1 định dạng
"""
log_file_path = "log.txt"

logger = logging.getLogger()
# Dòng dưới sẽ ngăn chặn việc có những log không mong muốn từ thư viện PILLOW
# ví dụ: 2020-12-16 15:21:30,829 - DEBUG - PngImagePlugin - STREAM b'PLTE' 41 768
logging.getLogger("PIL.PngImagePlugin").propagate = False
logging.basicConfig(filename=log_file_path, filemode= 'a',
                    format='%(asctime)s %(levelname)s:\t %(filename)s: %(funcName)s()-Line: %(lineno)d\t message: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', encoding = 'utf-8', force=True)
logger.setLevel(logging.DEBUG)

app = FastAPI(
    docs_url="/myapi",  # Đặt đường dẫn Swagger UI thành "/myapi"
    redoc_url=None  # Tắt Redoc UI
)

# Khởi tạo in-memory cache trong event startup
@app.on_event("startup")
async def on_startup() -> None:
    in_memory_cache = InMemoryBackend()
    FastAPICache.init(in_memory_cache)



app.include_router(employee_router.router)
app.include_router(user_router.router)
app.include_router(authentication.router)
app.include_router(license_plate_router.router)
app.include_router(vehicles_router.router)
app.include_router(image_router.router)
app.include_router(mode_lane_router.router)
app.include_router(update_app_router.router)
app.include_router(get_file_router.router)
app.include_router(update_app.router)




@app.get("/")
def read_root():
    return {"Message": "World"}

# Tạo icon cho trang web api, nó sẽ hiển thị hình ảnh favicon ở thư mục `static/favicon.ico`
@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "static", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


# Tạo Bảng trong DB nếu nó chưa tồn tại
model.Base.metadata.create_all(engine)

"""
Cho phép các trang web, app, api trên cùng 1 máy tính có thể truy cập đến api này  
Mặc định các api trên cùng 1 máy không thể chia sẻ tài nguyên cho nhau  
Điều này phục vụ cho mục đích test, vì không thể lúc nào cũng có sẵn 2 máy tính khác nhau để test
"""
origins = [
    "http://localhost:3000",
    "http://192.168.0.145"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

if __name__ == "__main__":
    # Chạy file này bằng cách `python service\main.py`
    # sẽ lấy máy chạy file này làm máy chủ, các máy tính cùng dải mạng đều có thể truy cập API này
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Hoặc gõ trực tiếp lệnh `fastapi dev main.py` để vào chế độ developer
    # Hoặc gõ trực tiếp lệnh `fastapi run main.py` để vào chế độ lấy máy chạy làm server