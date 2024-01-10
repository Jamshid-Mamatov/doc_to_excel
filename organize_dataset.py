import os
import random
import shutil

def split_data(input_folder, output_folder, split_ratio=0.8):
    # Create train and val folders
    train_folder = os.path.join(output_folder, 'images', 'train')
    val_folder = os.path.join(output_folder, 'images', 'val')
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)

    # Create train and val folders for labels
    train_label_folder = os.path.join(output_folder, 'labels', 'train')
    val_label_folder = os.path.join(output_folder, 'labels', 'val')
    os.makedirs(train_label_folder, exist_ok=True)
    os.makedirs(val_label_folder, exist_ok=True)

    # Get list of image files
    image_files = [f for f in os.listdir(os.path.join(input_folder, 'data')) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Calculate the number of images for training and validation
    num_images = len(image_files)
    num_train = int(num_images * split_ratio)
    num_val = num_images - num_train

    # Randomly shuffle the image files
    random.shuffle(image_files)

    # Copy images and labels to train and val folders
    for i, image_file in enumerate(image_files):
        src_image_path = os.path.join(input_folder, 'data', image_file)
        src_label_path = os.path.join(input_folder, 'labels', image_file.replace(os.path.splitext(image_file)[1], '.txt'))

        if i < num_train:
            dst_image_path = os.path.join(train_folder, image_file)
            dst_label_path = os.path.join(train_label_folder, image_file.replace(os.path.splitext(image_file)[1], '.txt'))
        else:
            dst_image_path = os.path.join(val_folder, image_file)
            dst_label_path = os.path.join(val_label_folder, image_file.replace(os.path.splitext(image_file)[1], '.txt'))

        shutil.copy(src_image_path, dst_image_path)
        shutil.copy(src_label_path, dst_label_path)

if __name__ == "__main__":
    input_folder = ""
    output_folder = "dataset"

    split_data(input_folder, output_folder)
