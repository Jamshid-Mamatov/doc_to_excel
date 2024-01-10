from ultralytics import YOLO

# Load a model
model = YOLO('yolov8s-seg.pt')  # load a pretrained model (recommended for training)

# Train the model48
results = model.train(data='custom.yaml', epochs=100, imgsz=640,batch=32)