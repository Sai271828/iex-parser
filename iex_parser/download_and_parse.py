import os
from datetime import timedelta, datetime
from iex_parser.download_iex_pcaps import download_dates
import glob
import subprocess
import argparse
from datetime import datetime

# Path to the directory this package is installed in. Used for base path for running C++ binary files
dir_path = os.path.dirname(os.path.realpath(__file__))

def valid_date(s: str) -> str:
    """
    This function checks if a given string represents a valid date in the format YYYY-MM-DD.
    
    Parameters:
    s (str): The string to be checked.
    
    Returns:
    s (str): The input string if it represents a valid date, otherwise raises an error.
    """
    try:
        datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Use YYYY-MM-DD.")
    return s


def parse_file(file_path: str, parsed_folder: str, symbol: str, split: bool = False):
    """
    This function parses a file using the IEX parser and redirects the output to a specified folder.
    
    Parameters:
    file_path (str): The path to the file to be parsed.
    parsed_folder (str): The path to the folder where the parsed output should be saved.
    symbol (str): Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
    split (bool): Whether to split the output files. One file per letter of the anphabet is generated. Default is False.
    
    Returns:
    None
    """
    if split=="True":
        # Use compiled C++ binary to parse and split output files
        IEX_PARSER = os.path.join(dir_path, 'iex_parser_split.out')
    else:
        if symbol == "ALL":
            # Use compiled C++ binary to parse ALL symbols
            IEX_PARSER = os.path.join(dir_path, 'iex_parser_all_threaded.out')
        else:
            # Use compiled C++ binary to parse selected symbols
            IEX_PARSER =  os.path.join(dir_path, 'iex_parser_threaded.out')
        
    command2 =f"gunzip -d -c {file_path} | tcpdump -r - -w - -s 0 |  {IEX_PARSER} /dev/stdin {parsed_folder} {symbol}"
    subprocess.run(command2, shell=True)

def parse_date(date_str: str, download_dir: str, parsed_folder: str, symbol: str, download: bool = True, split: bool = False):
    """
    This function (can) download and parse the IEXTP1 DEEP1.0 pcap files for a given date.
    
    Parameters:
    date_str (str): The date string to be parsed. Format YYYY-MM-DD
    download_dir (str): The directory where the files are downloaded.
    parsed_folder (str): The directory where the parsed output should be saved.
    symbol (str): Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
    download (bool): Whether to download the files. Default is True.
    split (bool): Whether to split the output files. One file per letter of the anphabet is generated. Default is False.
    
    Returns:
    None
    """
    if valid_date(date_str) is None:
        return

    date_str_2 = date_str.replace("-","")
    file_pattern = f"data_feeds_{date_str_2}_{date_str_2}_IEXTP1_DEEP1.0.pcap.gz"

    if download:
        download_dates(download_dir, date_str, date_str, 'DEEP')

    matching_files = glob.glob(f"{download_dir}/DEEP/{file_pattern}")

    for file_path in matching_files:
        parse_file(file_path, parsed_folder, symbol,split=split)


def parse_dates(start_date: str, end_date: str, download_dir: str, parsed_folder: str, symbol: str, download: bool = False, split: bool = False):
    """
    This function parses a range of dates and (downloads and) parses the corresponding IEXTP1 DEEP1.0 pcap files.
    
    Parameters:
    start_date (str): The start date string in the format YYYY-MM-DD.
    end_date (str): The end date string in the format YYYY-MM-DD.
    download_dir (str): The directory where the files are downloaded.
    parsed_folder (str): The directory where the parsed output should be saved.
    symbol (str): Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
    download (bool): Whether to download the files. Default is False.
    split (bool): Whether to split the output files. One file per letter of the anphabet is generated. Default is False.
    
    Returns:
    None
    """
    if valid_date(start_date) is None or valid_date(end_date) is None:
        return

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date
    while current_date <= end_date:

        current_date_str = current_date.strftime("%Y-%m-%d")

        parse_date(current_date_str, download_dir, parsed_folder, symbol,download,split=split)

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