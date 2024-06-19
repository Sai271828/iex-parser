import sys
import os
from datetime import timedelta, datetime
from download_iex_pcaps import download_dates
import glob
import subprocess
import argparse
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Add the following lines to use logger.py
sys.path.append(str(Path(os.getenv('UTILS_DIR_PATH', '/vagrant'))))
from utils.logger import Log



if __name__ == "__main__":
    def valid_date(s):
        try:
            datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            raise argparse.ArgumentTypeError("Invalid date format. Use YYYY-MM-DD.")
        return s
    

    parser = argparse.ArgumentParser(description="Process start date, end date, and output directory")
    parser.add_argument("--start-date", required=True, type=valid_date, help="Start date (format: YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, type=valid_date, help="End date (format: YYYY-MM-DD)")
    parser.add_argument("--download-dir", required=True, help="Download directory")
    parser.add_argument("--symbol", required=True, help="Symbols of interest")
    parser.add_argument("--split", default=False, help="Split pcap files")
    args = parser.parse_args()

    start_date_str = args.start_date
    end_date_str = args.end_date
    download_dir = args.download_dir
    symbol = args.symbol
    split = args.split

    print("Dumping command line arguments:")
    print("\t--start-date", start_date_str)
    print("\t--end-date", end_date_str)
    print("\t--download-dir", download_dir)
    print("\t--symbol", symbol)
    print("\t--split", split)

    
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    # Initialize logger
    logger = Log()

    # Iterate over each day between start and end date
    current_date = start_date
    while current_date <= end_date:
        # Convert current date to string in format YYYY-MM-DD
        current_date_str = current_date.strftime("%Y-%m-%d")
        current_date_str_2 = current_date.strftime("%Y%m%d")

        # Write the current date to the log file
        logger.write(f"Downloading IEX DEEPs data from date: {current_date_str}\n")

        # Call download_dates function for current date
        download_dates(download_dir, current_date_str, current_date_str, 'DEEP')

        # Define the file pattern to search for
        file_pattern = f"data_feeds_{current_date_str_2}_{current_date_str_2}_IEXTP1_DEEP1.0.pcap.gz"

        # Search for files that match the pattern in the download directory
        matching_files = glob.glob(f"{download_dir}/DEEP/{file_pattern}")

        for file_path in matching_files:
            # Parse the pcap file
            logger.write(f"Parsing file: {file_path}\n")

            if split=="True":
                IEX_PARSER = os.getenv('IEX_PARSER_SPLIT', '/vagrant/src/iex_parser_split.out')
            else:
                if symbol == "ALL":
                    IEX_PARSER = os.getenv('IEX_PARSER_ALL', '/vagrant/src/iex_parser_all_threaded.out')
                else:
                    IEX_PARSER = os.getenv('IEX_PARSER_THREADED', '/vagrant/src/iex_parser_threaded.out')
            PARSED_FOLDER= os.getenv('PARSED_FOLDER', '/vagrant/data/parsed')
            command2 =f"gunzip -d -c {file_path} | tcpdump -r - -w - -s 0 |  {IEX_PARSER} /dev/stdin {PARSED_FOLDER}/{current_date_str_2} {symbol}"
            subprocess.run(command2, shell=True)

            # Remove the file
            # print(f"Removing file: {file_path}")
            # logger.write(f"Removing file: {file_path}\n")
            # command = f"rm -f {file_path}"
            # subprocess.run(command, shell=True)

        # Increment current date by one day
        current_date += timedelta(days=1)
