# Fast_API_server

# Hướng dẫn cách tạo API với FastAPI

# Mục lục

[I. FastAPI](#i-fastapi)
- [1. Cài đặt FastAPI](#1-cài-đặt-fastapi)
- [2. Khởi chạy FastAPI](#2-khởi-chạy-fastapi)

[II. Cách sử dụng](#ii-cách-sử-dụng)
- [1. Văn bản thuần](#1-văn-bản-thuần)
  - [1. Tiêu đề - Heading](#1-tiêu-đề---heading)
  - [2. Đoạn văn - Paragraph](#2-đoạn-văn---paragraph)
  - [3. Chữ in nghiêng - Italic](#3-chữ-in-nghiêng---italic)
  - [4. Chữ in đậm - Bold](#4-chữ-in-đậm---bold)
  - [5. In đậm và in nghiêng](#5-in-đậm-và-in-nghiêng)
  - [6. Chữ gạch giữa - Strikethrough](#6-chữ-gạch-giữa---strikethrough)
  - [7. Code trong dòng - Inline Code](#7-code-trong-dòng---inline-code)
- [2. Các khối](#2-các-khối)
  - [1. Trích dẫn - Blockquote](#1-trích-dẫn---blockquote)
  - [2. Danh sách có thứ tự - Ordered List](#2-danh-sách-có-thứ-tự---ordered-list)
  - [3. Danh sách không có thứ tự - Unordered List](#3-danh-sách-không-có-thứ-tự---unordered-list)
  - [4. Khối lệnh - Block Code](#4-khối-lệnh---block-code)
  - [5. Bảng - Table](#5-bảng---table)
- [3. Đặc biệt](#3-đặc-biệt)
  - [1. Đường kẻ ngang - Horizonal rules](#1-đường-kẻ-ngang---horizonal-rules)
  - [2. Liên kết - Link](#2-liên-kết---link)
  - [3. Hình ảnh - Image](#3-hình-ảnh---image)
  - [4. Biểu tượng cảm xúc - Icon](#4-biểu-tượng-cảm-xúc---icon)
  - [5. Checkbox](#5-checkbox)
  - [6. Escape markdown](#6-escape-markdown)

[III. Kết thúc](#iii-kết-thúc)

# I. FastAPI

## 1. Cài đặt FastAPI

Cài đặt `FastAPI` thông qua lệnh `pip` hoặc trực tiếp từ mã nguồn mở, xem chi tiết tại trang chủ [FastAPI](https://fastapi.tiangolo.com/):  

```python
pip install "fastapi[standard]"
```

## 2. Khởi chạy FastAPI

Để chạy `FastAPI` ta có thể sử dụng 2 câu lệnh thường xuyên như sau:  

```python
fastapi dev main.py
```
![chạy fastapi với câu lệnh dev](image_github/fast_api_run_dev.png)

Câu lệnh này sẽ chạy `FastAPI` trên môi trường `Developer`, có ngĩa là môi trường test, khi bạn đang chạy `server: là khởi chạy fastapi` và bạn thay đổi một số đoạn `code`, chỉnh sửa thêm một số file thì khi bạn lưu lại code nó sẽ tự động khởi động lại server, không cần ta phải chạy lại câu lệnh `fastapi dev main.py`.  

Và khi chạy lệnh này thì bạn chỉ có thể truy cập vào các địa chỉ có sẵn từ máy của bạn như:  
`http://127.0.0.1:8000/docs ` để xem toàn bộ api  
`http://127.0.0.1:8000/apixxx` truy cập api bạn tạo  

Và chỉ có duy nhất máy chủ có thể truy cập, các máy khác chưa thể truy cập được api này, vì vậy câu lệnh này chỉ chạy trên môi trường `dev`  

```python
fastapi run main.py
```

![alt text](image_github/fast_api_run.png)

Câu lệnh này sẽ lấy máy đang chạy làm máy chủ, và các máy tính khác trong cùng 1 dải mạng đều có thể truy cập api mà bạn tạo ra. Khi đó các máy khác sẽ truy cập được api của bạn thông qua địa chỉ:  

`http://IP:Port/apixxx`  
Trong đó `IP` sẽ là địa chỉ IP của máy tính đang làm server, port sẽ là: `8000` nếu bạn không cấu hình riêng, `apixxx` sẽ là địa chỉ api của bạn. Ví dụ:  
Để lấy địa chỉ ip của server thì bạn chạy lệnh sau trên CMD:
```
ipconfig
```

![Địa chỉ ip của server](image_github/ipconfig.png)

Ta có thể thấy được hai địa chỉ ip của máy tính như sau. Với `Ethernet: 192.168.0.100`, `Wifi: 172.31.99.131`, port thì mình không chỉnh sửa gì cả nên nó sẽ là `8000`, `apixxx: image/create_new_image`  
Như vậy ta có đường dẫn api cụ thể cho máy khác như sau:  
`http://192.168.0.100:8000/file/list_file_in_folder/` sẽ dành cho các máy tính kết nối với nhau thông qua `ethernet`.  

`http://172.31.99.131:8000/file/list_file_in_folder/` sẽ dành cho các máy tính kết nối cùng 1 mạng `wifi`.  

![alt text](image_github/api_list_file.png)