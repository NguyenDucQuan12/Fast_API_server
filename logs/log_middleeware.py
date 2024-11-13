from fastapi import FastAPI, Request
from logging_config import logger
import json

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Lấy địa chỉ IP của người gọi API
    client_ip = request.client.host

    # Lấy tên endpoint và các tham số truyền vào
    api_name = request.url.path
    params = dict(request.query_params)  # Lấy query parameters nếu có

    # Gọi API và lấy kết quả
    response = await call_next(request)

    # Lấy nội dung trả về
    response_body = [section async for section in response.__dict__['body_iterator']]
    result = response_body[0].decode() if response_body else "No content"

    # Ghi log
    logger.info(
        "",
        extra={
            "ip": client_ip,
            "api_name": api_name,
            "params": json.dumps(params),
            "result": result,
        }
    )

    # Đưa lại nội dung vào response
    response.__setattr__('body_iterator', iter(response_body))
    
    return response
