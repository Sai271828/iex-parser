import os
from datetime import timedelta, datetime
from download_iex_pcaps import download_dates
import glob
import subprocess
import argparse
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))

def valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Use YYYY-MM-DD.")
    return s


def parse_file(file_path, parsed_folder, symbol,split=False):

    if split=="True":
        IEX_PARSER = os.path.join(dir_path, 'iex_parser_split.out')
    else:
        if symbol == "ALL":
            IEX_PARSER = os.path.join(dir_path, 'iex_parser_all_threaded.out')
        else:
            IEX_PARSER =  os.path.join(dir_path, 'iex_parser_threaded.out')
        
    command2 =f"gunzip -d -c {file_path} | tcpdump -r - -w - -s 0 |  {IEX_PARSER} /dev/stdin {parsed_folder} {symbol}"
    subprocess.run(command2, shell=True)

def parse_date(date_str, download_dir, parsed_folder, symbol,download=True,split=False):

    if valid_date(date_str) is None:
        return

    # Define the file pattern to search for
    date_str_2 = date_str.replace("-","")
    file_pattern = f"data_feeds_{date_str_2}_{date_str_2}_IEXTP1_DEEP1.0.pcap.gz"

    if download:
        # Call download_dates function for current date
        download_dates(download_dir, date_str, date_str, 'DEEP')

    # Search for files that match the pattern in the download directory
    matching_files = glob.glob(f"{download_dir}/DEEP/{file_pattern}")

    for file_path in matching_files:
        parse_file(file_path, parsed_folder, symbol,split=split)


def parse_dates(start_date, end_date, download_dir, parsed_folder, symbol,download=False, split=False):

    if valid_date(start_date) is None or valid_date(end_date) is None:
        return
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Iterate over each day between start and end date
    current_date = start_date
    while current_date <= end_date:
        # Convert current date to string in format YYYY-MM-DD
        current_date_str = current_date.strftime("%Y-%m-%d")

        # Parse the pcap file for the current date
        parse_date(current_date_str, download_dir, parsed_folder, symbol,download,split=split)

        # Increment current date by one day
        current_date += timedelta(days=1)


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Process start date, end date, and output directory")
    parser.add_argument("--start-date", required=True, type=valid_date, help="Start date (format: YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, type=valid_date, help="End date (format: YYYY-MM-DD)")
    parser.add_argument("--download-dir", required=True, help="Download directory")
    parser.add_argument("--parsed-dir", required=True, help="Parsed directory")
    parser.add_argument("--symbol", required=True, help="Symbols of interest")
    parser.add_argument("--download", default=False, help="Download pcap files")
    parser.add_argument("--split", default=False, help="Split pcap files")
    args = parser.parse_args()

    start_date_str = args.start_date
    end_date_str = args.end_date
    download_dir = args.download_dir
    parsed_folder = args.parsed_dir
    symbol = args.symbol
    download = args.download
    split = args.split

    print("Dumping command line arguments:")
    print("\t--start-date", start_date_str)
    print("\t--end-date", end_date_str)
    print("\t--download-dir", download_dir)
    print("\t--parsed-dir",parsed_folder)
    print("\t--symbol", symbol)
    print("\t--download", download)
    print("\t--split", split)

    parse_dates(start_date_str, end_date_str, download_dir, parsed_folder, symbol,download, split=split)