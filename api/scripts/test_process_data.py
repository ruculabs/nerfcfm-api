import sys
import random
import time
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: python test_process_data.py min_time max_time processed_data_id")
        sys.exit(1)

    min_time = float(sys.argv[1])
    max_time = float(sys.argv[2])
    processed_data_id = float(sys.argv[3])

    random_time = random.uniform(min_time, max_time)
    print(f"[TEST Process Data] {random_time} seconds")
    os.mkdir(f'media/processed_data/{int(processed_data_id)}/')
    
    try:
        time.sleep(random_time)
        exit_code = 0 if random.random() < 0.95 else 1
        if not exit_code:
            pass
        sys.exit(exit_code)
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == "__main__":
    main()
