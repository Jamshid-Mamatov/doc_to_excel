from ultralytics import YOLO
from PIL import Image
from pathlib import Path
import torch
import cv2
import numpy as np

import os

# Create a directory for cropped images
os.makedirs('cropped', exist_ok=True)

# Load your model
model = YOLO("best.pt")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
path="test_image/대조군10.jpg"

def draw_points(img_path):
    image=cv2.imread(str(img_path))
    results = model(img_path, device=device)

    # Save predictions
    # results.save(Path("results") / img_path.name)
    for r in results:
      
        points=r.cpu().keypoints.xy.numpy()
        count=0
        for point in points[0]:

            x,y=int(point[0]),int(point[1])
            image = cv2.circle(image, (x,y), radius=30, color=(0, 0, 255), thickness=-1)
            image = cv2.putText(image, f'{count}', (x,y), cv2.FONT_HERSHEY_SIMPLEX,  
                        5, (255, 0, 0), 3, cv2.LINE_AA)
            count+=1
    cv2.imwrite("result.jpg",image)
# draw_points(path)
    
def testing(folder_path):
    for img_path in Path(folder_path).glob('*.jpg'):  # Assuming images are in JPG format
        # img = Image.open(img_path)
        print(img_path)
        image=cv2.imread(str(img_path))
        results = model(img_path, device=device)

        # Save predictions
        # results.save(Path("results") / img_path.name)
        for r in results:
            points=r.cpu().keypoints.xy.numpy()
            count=0
            for point in points[0]:

                x,y=int(point[0]),int(point[1])
                image = cv2.circle(image, (x,y), radius=30, color=(0, 0, 255), thickness=-1)
                image = cv2.putText(image, f'{count}', (x,y), cv2.FONT_HERSHEY_SIMPLEX,  
                            5, (255, 0, 0), 3, cv2.LINE_AA)
                count+=1

        result_img_path = Path('results') / img_path.name
        cv2.imwrite(str(result_img_path), image)

# testing("test")
def inference(path):

    results=model(path)
    points=results[0].cpu().keypoints.xy.numpy()[0]
    print(points)
    return points

def crop_doc(path):

    img=cv2.imread(path)
    template=np.ones((1500,2000))

    width,height=template.shape
    print(height,width)
    pts1 = inference(path=path).reshape(4,2)


    pts2 = np.float32([[0,0],[width,0],[width,height],[0,height]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    print(img.shape[:2][-1::-1])
    dst = cv2.warpPerspective(img,M,template.shape)
    print(dst.shape)
    cropped_img_path = f"cropped/crop_{Path(path).name}"
    cv2.imwrite(cropped_img_path, dst)

# def process_directory(directory_path):
#     for img_path in Path(directory_path).glob('*.jpg'):  # Assuming images are in JPG format
#         crop_doc(str(img_path))

# # Replace 'path_to_directory' with your directory path
# directory_path = 'test'
# process_directory(directory_path)
# # crop_doc(path=path)


