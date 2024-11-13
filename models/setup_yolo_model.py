from ultralytics import YOLO

if __name__ == "__main__":
    # Load a model
    model = YOLO("yolov8m.pt")  # load a pretrained model (recommended for training)

    # Train the model
    # results = model.train(data="assets\\License_plate_VN\\data.yaml", epochs=100, imgsz=640, device = 0)

    # Continue train model with new data
    results = model.train(data="assets\\License_plate_VN\\data.yaml", epochs=100, imgsz=640, device = 0)


    # Predict after train
    # model = YOLO("assets\\model\\yolo\\yolov11_pretrain\\last.pt")
    # results = model.predict(source= "assets\\image\\image_test\\choang-ngop-bo-suu-tap-500-xe-no-bien-khung-tai-an-giang-hinh-2.png", save = True, show = True, verbose = False)