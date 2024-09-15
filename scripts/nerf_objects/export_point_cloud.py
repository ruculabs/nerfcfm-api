def export_pointcloud(data_path, output_dir, variant, system_metrics_file, num_points=1000000, remove_outliers=True):
    """
    Exports a point cloud for the trained model, tracks system metrics.
    
    Args:
        data_path (str): Path to training output directory.
        output_dir (str): Directory to save exported point cloud.
        variant (str): Nerfacto variant used for training.
        system_metrics_file (str): JSON file to log system metrics.
        num_points (int): Number of points to generate in the point cloud.
        remove_outliers (bool): Whether to remove outliers from the point cloud.
    """
    start_time = time.time()
    system_metrics_list = []
    stop_flag = [False]

    # Start system metrics monitoring in a separate thread
    monitor_thread = Thread(target=monitor_system_metrics, args=(2, system_metrics_list, stop_flag))
    monitor_thread.start()

    # Prepare run folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = Path(output_dir) / f"export_pointcloud_{timestamp}"
    run_folder.mkdir(parents=True, exist_ok=True)

    # Command for exporting point cloud
    export_command = f"ns-export pointcloud --load-config {data_path} --output-dir {run_folder} --num-points {num_points} --remove-outliers {remove_outliers}"

    print(f"Exporting point cloud for {variant}...")
    
    try:
        subprocess.run(export_command, shell=True, check=True)
        time_taken = time.time() - start_time

        # Stop system metrics monitoring
        stop_flag[0] = True
        monitor_thread.join()

        # Log export details and system metrics
        log_export({
            "variant": variant,
            "data": data_path,
            "output_dir": str(run_folder),
            "time_taken": time_taken,
            "timestamp": str(datetime.now()),
            "system_metrics": system_metrics_list
        }, system_metrics_file)

        print(f"Export complete for {variant}. Time taken: {time_taken:.2f} seconds.")

    except subprocess.CalledProcessError as e:
        print(f"Error: Export failed for {variant} with error: {e}")
        sys.exit(1)
