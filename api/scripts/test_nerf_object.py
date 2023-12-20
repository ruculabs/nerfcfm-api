import sys
import random
import time
import os
import shutil

def main():
    if len(sys.argv) != 4:
        print("Usage: python test_nerf_object.py min_time max_time object_id")
        sys.exit(1)

    min_time = float(sys.argv[1])
    max_time = float(sys.argv[2])
    object_id = int(sys.argv[3])

    random_time = random.uniform(min_time, max_time)
    print(f"[TEST Exporting NeRF Object] {random_time} seconds")
    output_dir = f'media/nerf_objects/{object_id}/'
    
    try:
        time.sleep(random_time)
        exit_code = 0 if random.random() < 1 else 1

        if not exit_code:
            print("success")
            os.mkdir(output_dir)
            source_objs = 'sample_media/nerf_objects/'
            objs = os.listdir(source_objs)
            selected_obj = random.choice(objs)

            for file_name in os.listdir(os.path.join(source_objs, selected_obj)):
                source_file_path = os.path.join(source_objs, selected_obj, file_name)
                destination_file_path = os.path.join(output_dir, file_name)
                shutil.copy2(source_file_path, destination_file_path)
        else:
            print("failed")
        sys.exit(exit_code)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
