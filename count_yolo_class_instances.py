import os
import argparse
import yaml

def count_classes_in_folder(folder_path):
    class_count = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r") as f:
                lines = f.readlines()
                for line in lines:
                    class_id = int(line.strip().split()[0])
                    if class_id in class_count:
                        class_count[class_id] += 1
                    else:
                        class_count[class_id] = 1
    return class_count

def main(root_path):
    # Read data.yaml to get the class names
    with open(os.path.join(root_path, 'data.yaml'), 'r') as f:
        data = yaml.safe_load(f)
        names = data['names']
    
    # Count class instances in train folder
    train_path = os.path.join(root_path, 'train', 'labels')
    train_count = count_classes_in_folder(train_path)
    
    # Count class instances in test folder
    test_path = os.path.join(root_path, 'test', 'labels')
    test_count = count_classes_in_folder(test_path)

    print("Training data class instances:")
    for class_id, count in train_count.items():
        print(f"{names[class_id]}: {count}")
    
    print("\nTesting data class instances:")
    for class_id, count in test_count.items():
        print(f"{names[class_id]}: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count instances of each class in YOLO dataset")
    parser.add_argument("root", type=str, help="Path to the root directory of the YOLO dataset")
    args = parser.parse_args()
    
    main(args.root)
