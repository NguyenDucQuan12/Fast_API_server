from paddleocr import PaddleOCR
import paddle

# Kiểm tra xem paddle có nhận gpu không
# gpu_available  = paddle.device.is_compiled_with_cuda()
# print("GPU available:", gpu_available)



# rec_model_dir: đường dẫn recognition model là mô hình nhận dạng ký tự (Đọc các ký tự)  
# det_model_dir: đường dẫn detection model là mô hình nhận diện ký tự (Phát hiện vùng nào có các ký tự)  
# cls_model_dir: đường dẫn classification model là phân loại ký tự (Phân loại nó theo các nhóm)


# # sử dụng PaddleOCR ngôn ngữ tiếng Anh
# ocrEngine = PaddleOCR(
#             use_angle_cls=False,
#             lang='en',
#             show_log=False,
#             use_gpu=True,
#             rec_model_dir="assets/model/paddleocr/english/rec", # use in here
#             det_model_dir="assets/model/paddleocr/english/det", # use in here
        # )

# sử dụng PaddleOCR ngôn ngữ tiếng Trung
ocrEngine = PaddleOCR(
            use_angle_cls=False,
            lang='ch',
            show_log=False,
            use_gpu=True,
            rec_model_dir="assets/model/paddleocr/china/rec", # use in here
            det_model_dir="assets/model/paddleocr/china/det", # use in here
            cls_model_dir="assets/model/paddleocr/china/cls" # use in here
        )
