import os
import cv2
import datetime
import re
import shutil
from fastapi import HTTPException, status



def save_avatar_upload_from_user(user_id_code, avatar):

    # Định nghĩa các định dạng file ảnh hợp lệ
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
    MAX_FILE_SIZE_MB = 5  # Giới hạn kích thước file tối đa (5MB)

    # Kiểm tra định dạng file
    file_extension = avatar.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Định dạng file không hợp lệ. Chỉ chấp nhận các định dạng: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Kiểm tra kích thước file
    file_size_mb = len(avatar.file.read()) / (1024 * 1024)  # Đổi kích thước từ byte sang MB
    avatar.file.seek(0)  # Đặt lại con trỏ file về vị trí đầu sau khi đọc

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Kích thước file quá lớn. Kích thước tối đa cho phép là {MAX_FILE_SIZE_MB}MB"
        )

    # Định nghĩa đường dẫn để lưu trữ file ảnh
    avatar_filename = f"avatar.png"
    avatar_dir = f"data/employee/{user_id_code}/avatars"
    # avatar_path = os.path.join(avatar_dir, avatar_filename)
    avatar_path = f"data/employee/{user_id_code}/avatars/{avatar_filename}"

    # Tạo thư mục nếu nó chưa tồn tại trên hệ thống
    os.makedirs(avatar_dir, exist_ok=True)

    # Lưu file avatar vào hệ thống
    try:
        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Có lỗi trong quá trình lưu ảnh"
        )
    return avatar_path

# Lưu ảnh biển số, toàn cảnh
def save_image_license_plate(license_plate_VN, license_plate_crop, image_license_plate, image_face):

    # Lấy thời gian ngày tháng năm giờ phút giấy theo định dạng string
    today = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) 
    date_today = str(datetime.datetime.now().strftime("%d-%m-%y"))

    # Tạo đường dẫn lưu hình ảnh: data/license_plate/14-09-24/38-F73901
    save_dir_license_plate= "data/license_plate/"+ date_today + "/" + license_plate_VN 

    # Loại bỏ ký tự nếu nó nằm ngoài: chữ cái, số, dấu gạch ngang, gạch dưới, khoảng trắng
    # ví dụ: "29-K1!@# 284$%^62.png" sau khi loại bỏ các ký tự không mong muốn còn "29-K1 28462.png"
    license_plate_VN = re.sub(r'[^\w\s-]', '', license_plate_VN)

    # Kiểm tra xem đã tồn tại thư mục chưa, nếu ngày mới bắt đầu thì sẽ chưa có
    os.makedirs(save_dir_license_plate, exist_ok=True)

    # Lưu hình ảnh vào thư mục và trả về đường dẫn
    cv2.imwrite(os.path.join(save_dir_license_plate , license_plate_VN + today + '.png'), license_plate_crop)
    cv2.imwrite(os.path.join(save_dir_license_plate , "background_" + today + '.png'), image_license_plate)
    cv2.imwrite(os.path.join(save_dir_license_plate , "face" + today + '.png'), image_face)

    licenseplate_path = save_dir_license_plate + "/" + "background_" + today + '.png'
    face_path = save_dir_license_plate + "/" + "face" + today + '.png'

    return licenseplate_path, face_path
