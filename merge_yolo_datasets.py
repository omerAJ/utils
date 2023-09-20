import os
import argparse
import yaml
import shutil

def merge_yaml_files(yaml_files):
    all_classes = {}
    merged_classes = []
    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            names = data['names']
            for idx, name in enumerate(names):
                if name not in all_classes:
                    all_classes[name] = len(merged_classes)
                    merged_classes.append(name)
    return all_classes, {'names': merged_classes}

def merge_folders(src_folder, dest_folder, class_map):
    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)
        dest_path = os.path.join(dest_folder, filename)
        if filename.endswith(".txt"):
            with open(src_path, 'r') as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                parts = line.strip().split()
                old_class_id = int(parts[0])
                new_class_id = class_map[old_class_id]
                parts[0] = str(new_class_id)
                new_lines.append(" ".join(parts))
            with open(dest_path, 'w') as f:
                f.write("\n".join(new_lines))
        else:
            shutil.copy(src_path, dest_path)

def main(root_dirs, output_dir):
    yaml_files = [os.path.join(root_dir, 'data.yaml') for root_dir in root_dirs]
    
    class_map_list, merged_yaml_data = merge_yaml_files(yaml_files)
    
    os.makedirs(os.path.join(output_dir, 'train', 'labels'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'train', 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test', 'labels'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test', 'images'), exist_ok=True)
    
    with open(os.path.join(output_dir, 'data.yaml'), 'w') as f:
        yaml.dump(merged_yaml_data, f)

    for i, root_dir in enumerate(root_dirs):
        with open(os.path.join(root_dir, 'data.yaml'), 'r') as f:
            data = yaml.safe_load(f)
            names = data['names']

        class_map = {}
        for idx, name in enumerate(names):
            class_map[idx] = class_map_list[name]
        
        for data_type in ['train', 'test']:
            src_label_folder = os.path.join(root_dir, data_type, 'labels')
            dest_label_folder = os.path.join(output_dir, data_type, 'labels')
            merge_folders(src_label_folder, dest_label_folder, class_map)

            src_image_folder = os.path.join(root_dir, data_type, 'images')
            dest_image_folder = os.path.join(output_dir, data_type, 'images')
            merge_folders(src_image_folder, dest_image_folder, class_map)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple YOLO datasets into one.")
    parser.add_argument("root_dirs", type=str, nargs='+', help="Paths to the root directories of YOLO datasets")
    parser.add_argument("output_dir", type=str, help="Path to the output root directory")
    args = parser.parse_args()
    
    main(args.root_dirs, args.output_dir)
