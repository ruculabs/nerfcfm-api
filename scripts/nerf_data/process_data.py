import os
import subprocess
import sys
import time
import json
import re
import psutil
from datetime import datetime
from threading import Thread
from pathlib import Path

LOG_FILE = "process_log.json"

def log_process(data_type, data_path, output_dir, time_taken, system_metrics, frames_info, run_folder):
    """
    Logs the details of the data processing step to a JSON file in the specific run folder.
    
    Args:
        data_type (str): Type of data processed (images/video).
        data_path (str): Path to the input data.
        output_dir (str): Path to the output directory.
        time_taken (float): Time taken for the process in seconds.
        system_metrics (list): List of GPU, CPU, and RAM metrics logged over time.
        frames_info (dict): Contains the number of frames in video and frames to extract.
        run_folder (Path): The path to the current run's folder where the log will be saved.
    
    Returns:
        None
    """
    log_data = {
        "date": str(datetime.now()),
        "data_type": data_type,
        "file_name": os.path.basename(data_path),
        "output_dir": output_dir,
        "time_taken": time_taken,
        "system_metrics": system_metrics,
        "frames_info": frames_info
    }
    
    # Define the path for the log file within the run folder
    log_file = run_folder / "process_log.json"

    # Read the existing log file or create a new list if the file doesn't exist
    if log_file.exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    # Append the new log
    logs.append(log_data)

    # Write the updated logs back to the JSON file in the run folder
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=4)

    print(f"Processing details, system metrics, and frame info logged to {log_file}")

def get_gpu_metrics():
    """
    Get GPU metrics using nvidia-smi, handling multiple GPUs or multiple readings.
    
    Returns:
        list: A list of dictionaries, each containing memory usage, GPU utilization, and power consumption for each GPU.
    """
    gpu_metrics_list = []
    
    try:
        # Capture the output of nvidia-smi for GPU utilization, memory usage, and power consumption
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,power.draw", "--format=csv,nounits,noheader"]
        ).decode('utf-8').strip()
        
        # Split the output into lines in case of multiple GPUs or readings
        output_lines = output.split("\n")
        
        for line in output_lines:
            output_values = line.split(", ")
            
            # Check if we have exactly 3 values per line (for each GPU)
            if len(output_values) == 3:
                gpu_utilization, memory_used, power_draw = output_values
                gpu_metrics = {
                    "gpu_utilization": f"{gpu_utilization}%",
                    "memory_used": f"{memory_used} MiB",
                    "power_draw": f"{power_draw} W"
                }
                gpu_metrics_list.append(gpu_metrics)
            else:
                print(f"Warning: Unexpected GPU metrics format: {output_values}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to retrieve GPU metrics: {e}")
    
    return gpu_metrics_list

def get_cpu_ram_metrics():
    """
    Get CPU and RAM usage metrics using psutil.
    
    Returns:
        dict: A dictionary containing CPU usage and RAM usage.
    """
    cpu_metrics = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_used": f"{psutil.virtual_memory().used / (1024 ** 2):.2f} MiB"
    }
    return cpu_metrics

def monitor_system_metrics(interval, system_metrics_list, stop_flag):
    """
    Continuously monitor and log GPU, CPU, and RAM metrics at regular intervals.
    
    Args:
        interval (int): The interval in seconds between logs.
        system_metrics_list (list): A list to store the system metrics over time.
        stop_flag (list): A flag to signal when to stop the monitoring.
    
    Returns:
        None
    """
    while not stop_flag[0]:
        gpu_metrics_list = get_gpu_metrics()  # List of GPU metrics for each GPU
        cpu_ram_metrics = get_cpu_ram_metrics()
        
        # Record the time along with system metrics
        system_metrics_list.append({
            "timestamp": str(datetime.now()),
            "gpu_metrics": gpu_metrics_list,
            "cpu_ram_metrics": cpu_ram_metrics
        })
        
        # Wait for the next interval
        time.sleep(interval)

def parse_process_output(output):
    """
    Parse the ns-process-data output to extract the number of frames in video and frames to extract.
    
    Args:
        output (str): The output from ns-process-data command.
        
    Returns:
        dict: A dictionary containing 'num_frames' and 'frames_to_extract'.
    """
    frames_info = {
        "num_frames": None,
        "frames_to_extract": None
    }

    # Use regex to extract the number of frames and frames to extract
    num_frames_match = re.search(r"Number of frames in video: (\d+)", output)
    frames_to_extract_match = re.search(r"Number of frames to extract: (\d+)", output)
    
    if num_frames_match:
        frames_info["num_frames"] = int(num_frames_match.group(1))
    
    if frames_to_extract_match:
        frames_info["frames_to_extract"] = int(frames_to_extract_match.group(1))
    
    return frames_info

def process_data(data_type, data_name, base_data_dir, base_results_dir):
    """
    Processes raw data using nerfstudio's ns-process-data command.
    
    Args:
        data_type (str): The type of data ('images' or 'video').
        data_name (str): The name of the input data file (e.g., 'video.mp4').
        base_data_dir (str): The base directory where the input data is located.
        base_results_dir (str): The base directory where the processed results should be saved.
        
    Returns:
        None
    """
    # Validate the data type
    if data_type not in ['images', 'video']:
        print(f"Error: Unsupported data type '{data_type}'. Supported types are 'images' or 'video'.")
        sys.exit(1)

    # Extract the video name (without extension) to use as a unique identifier
    data_path = Path(base_data_dir) / data_name
    video_name = data_path.stem  # Get the base name without extension (e.g., 'video1' from 'video1.mp4')

    # Create a separate directory for the video
    video_dir = Path(base_results_dir) / video_name

    # Create subdirectories for processing, training, and exporting results
    processed_data_dir = video_dir / "processed_data"
    processed_data_dir.mkdir(parents=True, exist_ok=True)

    # Construct the specific run folder name: run_<timestamp>
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = processed_data_dir / f"run_{timestamp}"

    output_dir = run_folder / video_name

    # Start tracking time
    start_time = time.time()

    # Initialize the system metrics list and stop flag
    system_metrics_list = []
    stop_flag = [False]  # This flag will be set to True to stop the monitoring

    # Start a separate thread to monitor system metrics (GPU, CPU, and RAM)
    monitor_thread = Thread(target=monitor_system_metrics, args=(2, system_metrics_list, stop_flag))
    monitor_thread.start()

    # Command to process data
    process_command = f"ns-process-data {data_type} --data {data_path} --output-dir {output_dir}"

    print(f"Processing {data_type} from {data_path}...")

    # Capture output in real-time while printing to the console
    try:
        process = subprocess.Popen(process_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Store the output for further parsing
        captured_output = ""

        # Read the output line by line
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # Print the line to the console
            captured_output += line  # Store the output for later use

        process.stdout.close()
        process.wait()  # Wait for the process to finish

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process_command)

        # Parse the output for frame information
        frames_info = parse_process_output(captured_output)

        # Calculate the time taken
        time_taken = time.time() - start_time
        print(f"Data processing complete. Time taken: {time_taken:.2f} seconds.")

        # Stop the monitoring thread
        stop_flag[0] = True
        monitor_thread.join()

        # Log the process details, system metrics, and frame information
        log_process(data_type, str(data_path), str(output_dir), time_taken, system_metrics_list, frames_info, run_folder)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Data processing failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    # Argument parsing
    parser = argparse.ArgumentParser(description="Process raw data into Nerfstudio format.")
    parser.add_argument('--data_type', type=str, required=True, help="Type of data ('images' or 'video').")
    parser.add_argument('--data_name', type=str, required=True, help="Name of the input data file (e.g., 'video.mp4').")
    parser.add_argument('--base_data_dir', type=str, default="./pipeline_data", help="Base directory where input data is stored.")
    parser.add_argument('--base_results_dir', type=str, default="./pipeline_results", help="Base directory where results will be stored.")
    
    args = parser.parse_args()
    
    # Call the process_data function with provided arguments
    process_data(args.data_type, args.data_name, args.base_data_dir, args.base_results_dir)
