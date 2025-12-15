# main.py
import argparse
import os
from handlers import mask_text, mask_csv, mask_json, mask_hl7

def main():
    parser = argparse.ArgumentParser(description="Mask sensitive data in files using Microsoft Presidio.")
    parser.add_argument('file_type', choices=['csv', 'json', 'hl7', 'text'],
                        help="Type of the file to process.")
    parser.add_argument('input_file', help="Name of the input file in the 'Files' folder.")
    parser.add_argument('output_file', help="Name of the output masked file in the 'Files' folder.")
    parser.add_argument('--log', default='mask_log.txt', help="Path to the log file.")

    args = parser.parse_args()

    input_path = os.path.join('Files', args.input_file)
    output_path = os.path.join('Files', args.output_file)

    # Open log file once for the whole run
    with open(args.log, 'w', encoding='utf-8') as log_file:
        print(f"Starting masking of {args.input_file} → {args.output_file}")
        print(f"Log will be written to {args.log}")

        if args.file_type == 'text':
            mask_text(input_path, output_path, log_file)
        elif args.file_type == 'csv':
            mask_csv(input_path, output_path, log_file)
        elif args.file_type == 'json':
            mask_json(input_path, output_path, log_file)
        elif args.file_type == 'hl7':
            mask_hl7(input_path, output_path, log_file)

    print("Masking completed. Check the log file for details on what was anonymized.")

if __name__ == '__main__':
    main()