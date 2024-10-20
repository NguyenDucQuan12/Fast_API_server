from paddleocr import PaddleOCR
import threading


"""
Cách 1:
đoạn mã này về cơ bản sẽ nhận tối đa 3 yêu cầu đồng thời để xử lý và thực hiện luân chuyển giữa 3 đối tượng ocr.
"""
ocr1 = PaddleOCR(lang='en', use_gpu=True)
ocr2 = PaddleOCR(lang='en', use_gpu=True)
ocr3 = PaddleOCR(lang='en', use_gpu=True)

parallel_thread_counter = 0
parallel_thread_counter_lock = threading.Lock()

ocr_objects = [ocr1, ocr2, ocr3] 
ocr_parallel_count = len(ocr_objects)

ocr_semaphore = threading.Semaphore(value=ocr_parallel_count)

with ocr_semaphore:
    current_thread_counter = 0
    try:
        parallel_thread_counter_lock.acquire()
        parallel_thread_counter += 1
        current_thread_counter = parallel_thread_counter % ocr_parallel_count
    finally:
        parallel_thread_counter_lock.release()

    selected_ocr = ocr_objects[current_thread_counter]
    ocr_dump  = selected_ocr.ocr("image")


def lock_ocr():
    """
    Cách 2:
    Nếu một luồng đang dùng OCR thì các luồng khác phải đợi luồng này xong trước đã
    """
    ocr = PaddleOCR(lang='en', use_gpu=True)
    ocr_lock = threading.Lock()

    ocr_lock.acquire()
    try:
        ocr_dump  = ocr.ocr("image")  
    finally:
        ocr_lock.release()