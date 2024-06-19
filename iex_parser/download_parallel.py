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
import re
load_dotenv()

if __name__ == "__main__":
    def valid_date(s):
        try:
            s = s.strip()
            datetime.strptime(str(s), "%Y-%m-%d")
        except ValueError as e:
            
            raise argparse.ArgumentTypeError("Invalid date format. Use YYYY-MM-DD.")
        return s
    
    
    
    parser = argparse.ArgumentParser(description="Process start date, end date, and output directory")
    parser.add_argument("--start-date", required=True, type=valid_date, help="Start date (format: YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, type=valid_date, help="End date (format: YYYY-MM-DD)")
    
    start_date_str = parser.parse_known_args()[0].start_date
    end_date_str = parser.parse_known_args()[0].end_date
    download_dir = os.getenv('IEX_DOWNLOADS')
    print(download_dir)
    download_dates(download_dir, start_date_str, end_date_str, 'DEEP')