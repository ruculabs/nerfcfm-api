import argparse
from nerf_data.process_data import process_data
from nerf_models.train_model import train_model
from nerf_objects.export_object import export_object

def main():
    parser = argparse.ArgumentParser(description="Nerf Pipeline: Process data, train models, and export objects.")
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help="Available commands")

    # Data processing command
    data_parser = subparsers.add_parser('process_data', help="Process raw data using ns-process-data.")
    data_parser.add_argument('--data_type', type=str, required=True, help="Type of data ('images' or 'video').")
    data_parser.add_argument('--data_path', type=str, required=True, help="Path to the raw data directory (video or images).")
    data_parser.add_argument('--output_dir', type=str, required=True, help="Path to the output directory where processed data will be saved.")

    # Model training command
    train_parser = subparsers.add_parser('train_model', help="Train a NeRF model using ns-train.")
    train_parser.add_argument('--model_type', type=str, required=True, help="Type of NeRF model to train (e.g., 'nerfacto', 'instant-ngp', 'splatfacto').")
    train_parser.add_argument('--data_dir', type=str, required=True, help="Path to the processed data directory.")
    train_parser.add_argument('--output_dir', type=str, required=True, help="Path to the output directory where trained model will be saved.")
    train_parser.add_argument('--num_epochs', type=int, default=10, help="Number of epochs to train the model.")
    train_parser.add_argument('--other_args', type=str, default="", help="Other optional arguments to pass to the ns-train command.")

    # Object exporting command
    export_parser = subparsers.add_parser('export_object', help="Export a NeRF model to a 3D object using ns-export.")
    export_parser.add_argument('--export_type', type=str, required=True, help="Type of export ('tsdf', 'poisson', 'pointcloud').")
    export_parser.add_argument('--config_path', type=str, required=True, help="Path to the trained model config file (CONFIG.yml).")
    export_parser.add_argument('--output_dir', type=str, required=True, help="Path to the output directory where the exported object will be saved.")

    args = parser.parse_args()

    # Run the appropriate function based on the subcommand
    if args.command == 'process_data':
        process_data(args.data_type, args.data_path, args.output_dir)
    elif args.command == 'train_model':
        train_model(args.model_type, args.data_dir, args.output_dir, args.num_epochs, args.other_args)
    elif args.command == 'export_object':
        export_object(args.export_type, args.config_path, args.output_dir)
    else:
        print("Invalid command. Use --help for available commands.")

if __name__ == "__main__":
    main()
