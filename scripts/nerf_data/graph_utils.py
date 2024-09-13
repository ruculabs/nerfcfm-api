import json
import matplotlib.pyplot as plt
from datetime import datetime

LOG_FILE = "process_log.json"

def load_log_data():
    """
    Load the process log data from the JSON log file.
    
    Returns:
        list: A list of logs containing GPU/CPU metrics over time.
    """
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
        return logs
    except FileNotFoundError:
        print(f"Error: Log file {LOG_FILE} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from {LOG_FILE}.")
        return []

def extract_metrics(log_entry):
    """
    Extract GPU and CPU metrics over time from a single log entry.
    
    Args:
        log_entry (dict): A single log entry from the process log.
    
    Returns:
        dict: A dictionary containing lists of timestamps, GPU utilization, CPU usage, memory usage, and power draw.
    """
    timestamps = []
    gpu_utilization = []
    cpu_usage = []
    memory_usage = []
    power_draw = []

    for metrics in log_entry["gpu_cpu_metrics"]:
        timestamps.append(datetime.strptime(metrics["timestamp"], "%Y-%m-%d %H:%M:%S.%f"))
        gpu_utilization.append(float(metrics["gpu_metrics"]["gpu_utilization"].strip('%')))
        cpu_usage.append(metrics["cpu_metrics"]["cpu_usage"])
        memory_usage.append(float(metrics["gpu_metrics"]["memory_used"].split()[0]))  # Extract MiB value
        power_draw.append(float(metrics["gpu_metrics"]["power_draw"].split()[0]))  # Extract W value
    
    return {
        "timestamps": timestamps,
        "gpu_utilization":
