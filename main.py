# import tensorflow as tf
from fastapi import FastAPI, Request, Response# pip install "fastapi[standard]"
import uvicorn
import os
import datetime
import json
from fastapi.responses import FileResponse, JSONResponse
from starlette.concurrency import iterate_in_threadpool
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from db import model
from router import employee_router, user_router, license_plate_router, vehicles_router, image_router, mode_lane_router, update_app_router, get_file_router
from auth import authentication
from update_app import update_app
from logs.logging_config import logger

app = FastAPI(
    docs_url="/myapi",  # Đặt đường dẫn Swagger UI thành "/myapi"
    redoc_url=None  # Tắt Redoc UI
)

# Các đường dẫn cần bỏ qua khi log
# Vì các api này kết quả trả về không phải json mà là html, dẫn đến lỗi 
EXCLUDED_PATHS = ["/myapi", "/redoc", "/openapi.json", "/modelane/getmode"]
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware để ghi log mỗi khi có API được gọi.
    Cấu trúc log: `time - IP - API Name - Params - Result`
    Ví dụ: 2024-11-13 10:24:54,615 - 192.168.0.100 - / - {} - {"Message":"World"}
    """
    # Lấy thời gian hiện tại
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

    # Lấy địa chỉ IP của người gọi API
    client_ip = request.client.host

    # Lấy tên endpoint và các tham số truyền vào
    api_name = request.url.path
    params = dict(request.query_params)  # Lấy query parameters nếu có

    # Bỏ qua log nếu đường dẫn nằm trong danh sách EXCLUDED_PATHS
    if api_name in EXCLUDED_PATHS:
        # Ghi log với thông tin "nothing"
        logger.info(
            "",
            extra={
                "ip": client_ip,
                "api_name": api_name,
                "params": "nothing",
                "result": "nothing",
            }
        )
        return await call_next(request)

    # Gọi API và lấy kết quả
    response = await call_next(request)

    # Lấy Content-Type của phản hồi
    content_type = response.headers.get("Content-Type", "")

    # Đọc nội dung phản hồi
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    # Đặt lại body_iterator để phản hồi có thể được gửi lại cho client
    response.body_iterator = iterate_in_threadpool(iter([response_body]))

    # Xử lý và ghi log dựa trên Content-Type
    if "application/json" in content_type:
        try:
            result = response_body.decode()
            json_result = json.loads(result)
            log_result = json.dumps(json_result)
        except json.JSONDecodeError:
            # Nếu không phải JSON hợp lệ
            result = response_body.decode(errors='ignore')
            log_result = f"Invalid JSON: {result}"
    elif "text" in content_type:
        # Đối với các nội dung văn bản
        result = response_body.decode(errors='ignore')
        log_result = result
    else:
        # Đối với nội dung nhị phân (ví dụ: hình ảnh)
        log_result = f"Binary data of length {len(response_body)}"

    # Ghi log
    logger.info(
        "",
        extra={
            "ip": client_ip,
            "api_name": api_name,
            "params": json.dumps(params),
            "result": log_result,
        }
    )

    # Trả về phản hồi gốc mà không thay đổi
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=content_type
    )

# Khởi tạo in-memory cache trong event startup
@app.on_event("startup")
async def on_startup() -> None:
    in_memory_cache = InMemoryBackend()
    FastAPICache.init(in_memory_cache)
    print("Thông báo: FastAPI đã khởi chạy thành công!")

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
    #Thêm tham số log_config= "logs\\logging_config.json" để chuyển các log của uvicorn vào tệp
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, log_level= "error", log_config= "logs\\logging_config.json")  # log_config= "logs\\logging_config.json"

    # Hoặc gõ trực tiếp lệnh `fastapi dev main.py` để vào chế độ developer
    # Hoặc gõ trực tiếp lệnh `fastapi run main.py` để vào chế độ lấy máy chạy làm server