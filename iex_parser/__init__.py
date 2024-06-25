import os
from datetime import timedelta, datetime
from .download import download_hist_file
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
        IEX_PARSER = os.path.join(dir_path, 'bin/iex_parser_split.out')
    else:
        if symbol == "ALL":
            # Use compiled C++ binary to parse ALL symbols
            IEX_PARSER = os.path.join(dir_path, 'bin/iex_parser_all_threaded.out')
        else:
            # Use compiled C++ binary to parse selected symbols
            IEX_PARSER =  os.path.join(dir_path, 'bin/iex_parser_threaded.out')
    
    parsed_prefix = os.path.join(parsed_folder, os.path.basename(file_path).replace(".pcap.gz", ""))
        
    command2 =f"gunzip -d -c {file_path} | tcpdump -r - -w - -s 0 |  {IEX_PARSER} /dev/stdin {parsed_prefix} {symbol}"
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
        download_hist_file(date_str_2, download_dir)

    matching_files = glob.glob(f"{download_dir}/{file_pattern}")

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
