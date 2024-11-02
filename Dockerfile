FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

# Cài đặt các gói cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    unixodbc \
    unixodbc-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    tzdata \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Thêm kho lưu trữ cho Python 3.10
RUN add-apt-repository ppa:deadsnakes/ppa

# Cài đặt Python 3.10 và pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-distutils \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt pip cho Python 3.10
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Tạo liên kết cho python và pip
RUN ln -s /usr/bin/python3.10 /usr/bin/python \
    && ln -s /usr/local/bin/pip /usr/bin/pip

# Cập nhật pip
RUN pip install --upgrade pip

# Sao chép requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt paddlepaddle-gpu từ URL dành cho Linux
RUN pip install --no-cache-dir paddlepaddle-gpu==2.4.2.post117 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

# Cài đặt torch với CUDA 11.6
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu116

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép mã nguồn vào container
COPY . .

# Mở cổng 80 để truy cập
EXPOSE 80

# Chạy ứng dụng khi container khởi động
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
