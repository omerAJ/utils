import os
import argparse
import yaml
import shutil

def add_class_from_yaml(src_yaml_file, dest_yaml_file, class_name):
    with open(src_yaml_file, 'r') as f_src:
        src_data = yaml.safe_load(f_src)
    with open(dest_yaml_file, 'r') as f_dest:
        dest_data = yaml.safe_load(f_dest)

    src_names = src_data.get('names', [])
    dest_names = dest_data.get('names', [])

    if class_name not in src_names:
        print(f"The class '{class_name}' is not present in the source dataset.")
        return None

    if class_name not in dest_names:
        dest_names.append(class_name)

    class_mapping = {src_names.index(class_name): dest_names.index(class_name)}

    return class_mapping, {'names': dest_names}

def add_class_from_folders(src_folder, dest_folder, class_map, existing_files):
    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)

        original_filename = filename
        counter = 1
        while filename in existing_files:
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}_{counter}{ext}"
            counter += 1
        existing_files.add(filename)

        dest_path = os.path.join(dest_folder, filename)

        if original_filename.endswith(".txt"):
            with open(src_path, 'r') as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                parts = line.strip().split()
                old_class_id = int(parts[0])
                if old_class_id in class_map:
                    new_class_id = class_map[old_class_id]
                    parts[0] = str(new_class_id)
                    new_lines.append(" ".join(parts))
            if new_lines:
                with open(dest_path, 'w') as f:
                    f.write("\n".join(new_lines))
        else:
            shutil.copy(src_path, dest_path)

def main(src_dir, dest_dir, class_name):
    src_yaml_file = os.path.join(src_dir, 'data.yaml')
    dest_yaml_file = os.path.join(dest_dir, 'data.yaml')

    class_map, merged_yaml_data = add_class_from_yaml(src_yaml_file, dest_yaml_file, class_name)

    if class_map is None:
        return

    with open(dest_yaml_file, 'w') as f:
        yaml.dump(merged_yaml_data, f)

    for data_type in ['train', 'valid']:
        existing_files = set(os.listdir(os.path.join(dest_dir, data_type, 'labels'))) | \
                         set(os.listdir(os.path.join(dest_dir, data_type, 'images')))

        src_label_folder = os.path.join(src_dir, data_type, 'labels')
        dest_label_folder = os.path.join(dest_dir, data_type, 'labels')
        add_class_from_folders(src_label_folder, dest_label_folder, class_map, existing_files)

        src_image_folder = os.path.join(src_dir, data_type, 'images')
        dest_image_folder = os.path.join(dest_dir, data_type, 'images')
        add_class_from_folders(src_image_folder, dest_image_folder, class_map, existing_files)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a specific class from dataset A to dataset B.")
    
    parser.add_argument("-s", "--src_dir", type=str, 
                        default='', 
                        help="Path to the source dataset (Dataset A)")
    
    parser.add_argument("-d", "--dest_dir", type=str, 
                        default='', 
                        help="Path to the destination dataset (Dataset B)")
    
    parser.add_argument("-c", "--class_name", type=str, 
                        default='className', 
                        help="Name of the class to be added from dataset A to dataset B")

    args = parser.parse_args()

    main(args.src_dir, args.dest_dir, args.class_name)
