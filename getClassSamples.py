import os
import cv2
import matplotlib.pyplot as plt
import random

def plot_images_with_class(root_dir, class_label, num_images=10):
    label_path = os.path.join(root_dir, 'labels')
    image_path = os.path.join(root_dir, 'images')
    
    if not os.path.exists(label_path) or not os.path.exists(image_path):
        raise ValueError("Invalid YOLO root directory")
    
    matching_images = []
    # Iterate through all annotation files in the label directory
    for filename in os.listdir(label_path):
        if filename.endswith(".txt"):
            with open(os.path.join(label_path, filename), 'r') as file:
                boxes = []
                for line in file.readlines():
                    parts = line.strip().split()
                    if parts[0] == class_label:  # If the class label matches
                        boxes.append([float(part) for part in parts[1:]])
                if boxes:
                    matching_images.append((filename.replace('.txt', '.jpg'), boxes))
                    
    if len(matching_images) < num_images:
        raise ValueError(f"Not enough images with class {class_label}")
    
    # Randomly choose `num_images` files to plot
    chosen_images = random.sample(matching_images, num_images)
    
    fig, axs = plt.subplots(1, num_images, figsize=(15, 5))
    for i, (img_file, boxes) in enumerate(chosen_images):
        img = cv2.imread(os.path.join(image_path, img_file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
        
        h, w, _ = img.shape
        for box in boxes:
            x, y, bw, bh = box
            # Convert box coordinates from normalized to pixel values
            x = int((x - bw / 2) * w)
            y = int((y - bh / 2) * h)
            bw = int(bw * w)
            bh = int(bh * h)
            
            cv2.rectangle(img, (x, y), (x + bw, y + bh), (255, 0, 0), 2)
        
        axs[i].imshow(img)
        axs[i].axis('off')
    plt.show()


# Example usage
yolo_root_dir = "/home/lums/new_folder/vehicle_counting/data_orig/Vehicles-OpenImages/train"
class_label = "4"  # Change this to your desired class label
plot_images_with_class(yolo_root_dir, class_label)
