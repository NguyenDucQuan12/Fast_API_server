# Cài đặt Torch phù hợp với phiên bản CUDA https://pytorch.org/
# Cài đặt ultralytics: pip install ultralytics
from ultralytics import YOLO
import torch
import cv2
import os
import gc
import datetime



device = 'cuda' if torch.cuda.is_available() else 'cpu'
license_plate_detect_GPU = YOLO('assets/model/best.pt').to(device)


img = "assets\\image\\image_test\\LÀN VÀO 52019_12_07_13_29_47.jpg"
image = cv2.imread(img)

# Cắt ảnh với hộp tọa độ xoay
# @profile
# # Dự đoán và Cắt ảnh với hình ảnh bình thường
def predict(image, save=True):
    
    is_license_plate= False   #default
    license_plate = "error_no_license_plate"   #default
    img_path = None    #default
    
    # phát hiện khu vực có biển số, max_det là số lượng đối tượng phát hiện trên mỗi hình ảnh(max 300)
    results= license_plate_detect_GPU(image, max_det = 1)[0]
    if results:
        # Trích xuất vị trí bounding box
        boxes = results.boxes.xyxy.tolist()
        
        for i, box in enumerate(boxes):
            # lấy tọa độ (x1,y1) trên cùng bên trái và (x2,y2) cuối cùng bên phải
            x1, y1, x2, y2 = box
            # Cắt khu vực chứa biển số để đưa vào paddleocr
            license_plate_crop = image[int(y1):int(y2), int(x1):int(x2)]
            # is_license_plate, license_plate_crop_cvt, license_plate = get_license_plate(license_plate_crop)
            #lưu hình ảnh biển số vào thu mục
            if save:
                img_path = save_image_license_plate(is_license_plate,license_plate_crop)
            return license_plate, is_license_plate, img_path
        
    return license_plate, is_license_plate, img_path

# Lưu ảnh biển số, toàn cảnh, ĐÃ TEST XONG (tkCamera, tkButton)
def save_image_license_plate(license_plate_VN, license_plate_crop):

    today = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) #chua ngay thang nam cung voi gio phut giay
    date_today = str(datetime.datetime.now().strftime("%d-%m-%y"))

    save_dir_license_plate = "license_plate"
    save_dir_license_plate_ok = "assets/image/image_result/"+ date_today + "/" + save_dir_license_plate
    save_dir_license_plate_fail = "assets/image/image_fail/"+ date_today + "/" + save_dir_license_plate
    
    if license_plate_VN:
        os.makedirs(save_dir_license_plate_ok, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir_license_plate_ok , save_dir_license_plate +today+'.png'), license_plate_crop)
        img_path = save_dir_license_plate_ok +"/"+save_dir_license_plate +today+'.png'
        return img_path
        
    else:
        os.makedirs(save_dir_license_plate_fail, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir_license_plate_fail , save_dir_license_plate +today+'.png'), license_plate_crop)
        img_path = save_dir_license_plate_fail + "/" +save_dir_license_plate +today+'.png'
        return img_path
    
predict(image=image)