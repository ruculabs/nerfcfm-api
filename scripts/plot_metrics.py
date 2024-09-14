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

    for metrics in log_entry["system_metrics"]:
        timestamps.append(datetime.strptime(metrics["timestamp"], "%Y-%m-%d %H:%M:%S.%f"))
        gpu_utilization.append(float(metrics["gpu_metrics"][0]["gpu_utilization"].strip('%')))
        cpu_usage.append(metrics["cpu_ram_metrics"]["cpu_usage"])
        memory_usage.append(float(metrics["gpu_metrics"][0]["memory_used"].split()[0]))  # Extract MiB value
        power_draw.append(float(metrics["gpu_metrics"][0]["power_draw"].split()[0]))  # Extract W value
    
    return {
        "timestamps": timestamps,
        "gpu_utilization": gpu_utilization,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "power_draw": power_draw
    }

def plot_metrics(metrics):
    """
    Plot GPU utilization, CPU usage, memory usage, and power draw over time.
    
    Args:
        metrics (dict): A dictionary containing timestamps, GPU utilization, CPU usage, memory usage, and power draw.
    """
    timestamps = metrics["timestamps"]

    # Create subplots
    plt.figure(figsize=(10, 8))

    # GPU utilization
    plt.subplot(4, 1, 1)
    plt.plot(timestamps, metrics["gpu_utilization"], label='GPU Utilization (%)')
    plt.ylabel("GPU Util (%)")
    plt.grid(True)

    # CPU usage
    plt.subplot(4, 1, 2)
    plt.plot(timestamps, metrics["cpu_usage"], label='CPU Usage (%)', color='orange')
    plt.ylabel("CPU Usage (%)")
    plt.grid(True)

    # Memory usage
    plt.subplot(4, 1, 3)
    plt.plot(timestamps, metrics["memory_usage"], label='Memory Usage (MiB)', color='green')
    plt.ylabel("Memory (MiB)")
    plt.grid(True)

    # Power draw
    plt.subplot(4, 1, 4)
    plt.plot(timestamps, metrics["power_draw"], label='Power Draw (W)', color='red')
    plt.ylabel("Power (W)")
    plt.grid(True)
    plt.xlabel("Time")

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load the log data
    logs = load_log_data()

    if logs:
        # Extract the metrics from the first log entry (you can adjust this to select other logs)
        metrics = extract_metrics(logs[0])

        # Plot the extracted metrics
        plot_metrics(metrics)
