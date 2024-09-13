import os
import subprocess
import sys
import time
import json
import psutil
from datetime import datetime
from threading import Thread
from pathlib import Path

LOG_FILE = "train_log.json"

def log_training(details, log_file):
    """ Logs training details to a JSON file. """
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(details)

    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=4)

def get_gpu_metrics():
    """ Get GPU metrics using nvidia-smi """
    gpu_metrics_list = []
    
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,power.draw", "--format=csv,nounits,noheader"]
        ).decode('utf-8').strip()
        
        output_lines = output.split("\n")
        
        for line in output_lines:
            output_values = line.split(", ")
            
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
    """ Get CPU and RAM usage metrics using psutil """
    cpu_metrics = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_used": f"{psutil.virtual_memory().used / (1024 ** 2):.2f} MiB"
    }
    return cpu_metrics

def monitor_system_metrics(interval, system_metrics_list, stop_flag):
    """ Continuously monitor and log GPU, CPU, and RAM metrics at regular intervals """
    while not stop_flag[0]:
        gpu_metrics_list = get_gpu_metrics()  # List of GPU metrics for each GPU
        cpu_ram_metrics = get_cpu_ram_metrics()
        
        system_metrics_list.append({
            "timestamp": str(datetime.now()),
            "gpu_metrics": gpu_metrics_list,
            "cpu_ram_metrics": cpu_ram_metrics
        })
        
        time.sleep(interval)

def train_model(variant, data_path, output_dir, gpu_count, system_metrics_file):
    """
    Trains a Nerfacto variant with normal calculation, logs system metrics, and follows folder structure.
    
    Args:
        variant (str): Nerfacto variant ('nerfacto', 'nerfacto-big', 'nerfacto-huge').
        data_path (str): Path to the processed data directory.
        output_dir (str): Directory to save training outputs.
        gpu_count (int): Number of GPUs to use.
        system_metrics_file (str): JSON file to log system metrics.
    """
    start_time = time.time()
    system_metrics_list = []
    stop_flag = [False]

    # Start system metrics monitoring in a separate thread
    monitor_thread = Thread(target=monitor_system_metrics, args=(2, system_metrics_list, stop_flag))
    monitor_thread.start()

    # Prepare run folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = Path(output_dir) / f"run_{timestamp}"
    run_folder.mkdir(parents=True, exist_ok=True)

    # Prepare command for training
    train_command = f"ns-train {variant} --data {data_path} --output-dir {run_folder} " \
                    f"--pipeline.model.predict-normals True --viewer.quit-on-train-completion True " \
                    f"--machine.num-devices {gpu_count}"

    print(f"Training {variant} with {gpu_count} GPUs...")
    try:
        subprocess.run(train_command, shell=True, check=True)
        time_taken = time.time() - start_time

        # Stop system metrics monitoring
        stop_flag[0] = True
        monitor_thread.join()

        # Log training details and system metrics
        log_training({
            "variant": variant,
            "data": data_path,
            "output_dir": str(run_folder),
            "time_taken": time_taken,
            "timestamp": str(datetime.now()),
            "system_metrics": system_metrics_list
        }, system_metrics_file)

        print(f"Training complete for {variant}. Time taken: {time_taken:.2f} seconds.")

    except subprocess.CalledProcessError as e:
        print(f"Error: Training failed for {variant} with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train Nerfacto variants.")
    parser.add_argument('--variant', type=str, required=True, choices=['nerfacto', 'nerfacto-big', 'nerfacto-huge'],
                        help="Nerfacto variant to train.")
    parser.add_argument('--data_path', type=str, required=True, help="Path to processed data directory.")
    parser.add_argument('--output_dir', type=str, required=True, help="Base directory for training results.")
    parser.add_argument('--gpu_count', type=int, default=2, help="Number of GPUs to use for training.")

    args = parser.parse_args()

    # Call the training function
    train_model(args.variant, args.data_path, args.output_dir, args.gpu_count, "train_log.json")
