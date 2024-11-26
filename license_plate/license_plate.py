import string
import cv2
import time
import shutil
import asyncio
import os
import tempfile
from fastapi import UploadFile, HTTPException
from models.yolo_model import license_plate_detect_gpu
from models.ocr_model import detect_OCR
from fastapi import HTTPException
from file.save_file import save_image_license_plate
from file.check_image import check_image
from license_plate.forrmat_license_plate import dict_int_to_char, dict_char_to_int, dict_two


# Định dạng biển số xe máy sao cho đúng với định dạng biển số xe máy của Việt Nam hiện nay
def license_complies_format(license_plate):

    # Lấy độ dài của các kí tự biển số
    license_plate_size= len(license_plate)
    # example: 38-F7 3901
    # Nếu AI đọc được các ký tự có độ dài khác 9 và 11 thì đó không phải là biển số
    if license_plate_size not in [9, 11]:
        return False, license_plate
    
    # So sánh xem các ký tự đọc được có khớp với biển số xe không
    if license_plate_size == 9:
        if (license_plate[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[0] in dict_int_to_char.keys()) and \
        (license_plate[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[1] in dict_int_to_char.keys()) and \
        (license_plate[2] in ['-'] or license_plate[2]in dict_two.keys()) and \
        (license_plate[3] in string.ascii_uppercase or license_plate[3] in dict_char_to_int.keys()) and \
        (license_plate[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[4] in dict_int_to_char.keys()) and \
        (license_plate[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[5] in dict_int_to_char.keys()) and \
        (license_plate[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[6] in dict_int_to_char.keys()) and \
        (license_plate[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[7] in dict_int_to_char.keys()) and \
        (license_plate[8] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[8] in dict_int_to_char.keys()):
            
            license_plate_= license_plate_format(license_plate,license_plate_size)
            return True, license_plate_
        else:
            return False, license_plate
    
    if license_plate_size == 11: 
        # example: 38-F7 390.11
        if (license_plate[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[0] in dict_int_to_char.keys()) and \
        (license_plate[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[1] in dict_int_to_char.keys()) and \
        (license_plate[2] in ['-'] or license_plate[2] in dict_two.keys()) and \
        (license_plate[3] in string.ascii_uppercase or license_plate[3] in dict_char_to_int.keys()) and \
        (license_plate[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[4] in dict_int_to_char.keys()) and \
        (license_plate[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[5] in dict_int_to_char.keys()) and \
        (license_plate[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[6] in dict_int_to_char.keys()) and \
        (license_plate[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[7] in dict_int_to_char.keys()) and \
        (license_plate[8] in ['.']) and \
        (license_plate[9] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[9] in dict_int_to_char.keys()) and \
        (license_plate[10] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[10] in dict_int_to_char.keys()):
            
            license_plate_=license_plate_format(license_plate,license_plate_size)
            return True, license_plate_

        # example: 38-FA 390.11
        if (license_plate[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[0] in dict_int_to_char.keys()) and \
        (license_plate[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[1] in dict_int_to_char.keys()) and \
        (license_plate[2] in ['-'] or license_plate[2] in dict_two.keys()) and \
        (license_plate[3] in string.ascii_uppercase or license_plate[3] in dict_char_to_int.keys()) and \
        (license_plate[4] in string.ascii_uppercase or license_plate[3] in dict_char_to_int.keys()) and \
        (license_plate[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[4] in dict_int_to_char.keys()) and \
        (license_plate[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[5] in dict_int_to_char.keys()) and \
        (license_plate[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[6] in dict_int_to_char.keys()) and \
        (license_plate[8] in ['.']) and \
        (license_plate[9] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[9] in dict_int_to_char.keys()) and \
        (license_plate[10] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[10] in dict_int_to_char.keys()):
            
            license_plate_=license_plate_format(license_plate,license_plate_size)
            return True, license_plate_
        
    else:
        return False, license_plate

# Chuyển các ký tự có thể đọc nhầm về các ký tự chính xác
def license_plate_format(license_plate, license_plate_size):
    license_plate_ = ''

    #38-F7 3901
    mapping_9 = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_two, 3: dict_char_to_int, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char
               , 7: dict_int_to_char, 8: dict_int_to_char}

    #38-F7 390.01
    mapping_11 = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_two, 3: dict_char_to_int, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char
               , 7: dict_int_to_char, 8: dict_two, 9: dict_int_to_char, 10: dict_int_to_char}
    
    #38-FA 390.01
    mapping_11_new = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_two, 3: dict_char_to_int, 4: dict_char_to_int, 5: dict_int_to_char, 6: dict_int_to_char
                , 7: dict_int_to_char, 8: dict_two, 9: dict_int_to_char, 10: dict_int_to_char}
    
    mapping=[0,0,0,0,0,0,0,0,0,mapping_9,0,mapping_11,mapping_11_new]
    # So sánh từng ký tự một, nếu có sai sót thì chuyển nó về định dạng đúng
    for j in range(license_plate_size):
        if license_plate[j] in mapping[license_plate_size][j].keys():
            license_plate_ += mapping[license_plate_size][j][license_plate[j]]
        else:
            license_plate_ += license_plate[j]
    return license_plate_

# Tiến hành đọc các ký tự từ biển số đã được cắt từ hình ảnh gốc
async def get_license_plate(license_plate_crop):
    """
    Đọc các kí tự trong hình ảnh  
    - **license_plate_crop**: Là hình ảnh chứa các ký tự cần đọc
    """

    is_license_plate = False
    start_time = time.time()

    # Đọc tất cả các ký tự chứa trong hình ảnh vào một luồng phụ và có chế độ bất đồng bộ
    # sử dụng cls khi văn bản có góc xoay 180 độ, nếu không có văn bản nào 180 độ thì nên đặt False để tăng hiệu suất
    result_license_plate = await asyncio.to_thread(detect_OCR, license_plate_crop)
    # Tính thời gian đọc ký tự biển số
    ocr_model_time = time.time()
    # print(f"Thời gian paddleOCR đọc ký tự: {ocr_model_time - start_time}s")
    
    # Kiểm tra kết quả 
    if result_license_plate:
        # print(f"Các ký tự đọc được từ hình ảnh: {result_license_plate}")
        # Ghép từng ký tự ở hai hàng của biển số lại với nhau: 38-F7
                                                            # 390.01
        license_plate = [line[1][0] for line in result_license_plate]

        # Viết hoa các chữ cái, bỏ các khoảng trắng
        license_plate = [i.upper() for i in license_plate]
        license_plate =''.join(license_plate)
        # print(f"Các ký tự sau khi loại bỏ khoảng trắng và ghép lại: {license_plate}")

        # Định dạng lại tất cả ký tự xem nó có phải là biển số không, ví dụ: 38-F2 123456 thì nó thừa rất nhiều số, nên sẽ ko coi nó là biển số
        is_license_plate, license_plate=license_complies_format(license_plate)
        # print(f"Kết quả cuối cùng: {license_plate}")

    else:
        license_plate='000000000'

    # Tính thời gian định dạng các ký tự
    format_license_plate_time = time.time()
    # print(f"Thời gian định dạng các ký tự biển số: {format_license_plate_time - ocr_model_time}s")

    return  is_license_plate, license_plate # ,license_plate_crop_cvt

# Dự đoán và Cắt ảnh với hình ảnh bình thường
async def predict(image, image2, save=True):

    start_time = time.time()    
    is_license_plate= False   #default
    license_plate = "Không thấy biển số"   #default
    img_path = "None"    #default
    license_plate_crop = cv2.imread("assets\\image\\img_src\\not_found_license_plate.png")

    # Kiểm tra xem hình ảnh gửi đến api là frame từ camera hay hình ảnh có định dạng png, jpg, ...
    image = await asyncio.to_thread(check_image, image=image)
    image2 = await asyncio.to_thread(check_image, image=image2)

    # Tính thời gian kiểm tra ảnh có hợp lệ không
    check_image_time = time.time()
    # print(f"Thời gian kiểm tra hình ảnh: {check_image_time - start_time}s")

    # Kiểm tra nếu không thể đọc được ảnh
    if image is None:
        raise HTTPException(
            status_code=400,
            detail={
                    "error": f"Hình ảnh đầu vào không hợp lệ: {image}",
                    "is_license_plate": is_license_plate,
                    "license_plate": license_plate,
                    "license_plate_path": img_path,
                    "face_path": img_path
                    })
    # phát hiện khu vực có biển số, max_det là số lượng đối tượng phát hiện trên mỗi hình ảnh(max 300)
    results = await asyncio.to_thread(license_plate_detect_gpu, image)

    # Tính thời gian phát hiện khu vực có biển số
    license_plate_detect_time = time.time()
    # print(f"Thời gian yolo nhận diện biển số: {license_plate_detect_time - check_image_time}s")

    if results:
        # Trích xuất vị trí bounding box, là vị trí tọa độ chứa biển số
        boxes = results.boxes.xyxy.tolist()
        
        for i, box in enumerate(boxes):
            # lấy tọa độ (x1,y1) trên cùng bên trái và (x2,y2) cuối cùng bên phải
            x1, y1, x2, y2 = box

            # Cắt khu vực chứa biển số để đưa vào paddleocr
            license_plate_crop = image[int(y1):int(y2), int(x1):int(x2)]

            # Đọc các ký tự từ biển số với hàm async
            is_license_plate, license_plate = await get_license_plate(license_plate_crop)

            # Tính thời gian đọc các kí tự trong biển số
            ocr_license_plate_time = time.time()
            # print(f"Thời gian đọc các ký tự biển số: {ocr_license_plate_time - license_plate_detect_time}s")

            #lưu hình ảnh biển số vào thư mục
            if save:
                license_plate_path, face_path = await asyncio.to_thread(
                    save_image_license_plate,
                    license_plate_VN=license_plate,
                    license_plate_crop=license_plate_crop,
                    image_license_plate=image,
                    image_face=image2
                )
            
            # Tính thời gian lưu hình ảnh vào ổ đĩa
            save_image_to_disk_time = time.time()
            # print(f"Thời gian lưu hình ảnh là: {save_image_to_disk_time - license_plate_detect_time}s")

            # Sau khi xử lý xong hình ảnh, giải phóng bộ nhớ của hình ảnh
            del license_plate_crop
            del image
            del image2
            cv2.destroyAllWindows()

            return {
                "is_license_plate": is_license_plate,
                "license_plate": license_plate,
                "license_plate_path": license_plate_path,
                "face_path": face_path
            }
    
    # lưu hình ảnh biển số vào thư mục
    if save:
            license_plate_path, face_path = await asyncio.to_thread(
                save_image_license_plate,
                license_plate_VN=license_plate,
                license_plate_crop=license_plate_crop,
                image_license_plate=image,
                image_face=image2
            )

    # Giải phóng bộ nhớ của hình ảnh đầu vào
    # Nếu không phát hiện biển số
    del image
    del image2
    cv2.destroyAllWindows()
    # gc.collect()

    return {
                "is_license_plate": is_license_plate,
                "license_plate": license_plate,
                "license_plate_path": img_path,
                "face_path": img_path
        }


async def save_temp_image(upload_file: UploadFile, file_name: str):
    """
    Tạo file tạm để lưu hình ảnh khi người dùng gửi lên server  
    Sử dụng `await` để dùng bất đồng bộ  
    - **upload_file**: Là tệp tin được gửi kèm API  
    - **file_name**: Là tên tệp cho file tạm  
    """
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    upload_file.file.close()
    return file_path