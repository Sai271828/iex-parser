import requests
import os
from tqdm import tqdm
from datetime import datetime

def get_hist_data(date: str):
    """
    Retrieves the historical data available on IEX (https://iextrading.com/api/1.0/hist) and parses it as JSON.
    
    Parameters:

        date (str): The date in the format YYYYMMDD.

    Returns:

        dict: The parsed JSON data for the required date.
    """
    url = "https://iextrading.com/api/1.0/hist"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(f"Error retrieving data: {response.status_code} - {response.text}")
    

    date_data = data.get(date)

    # Check if data for the date is available
    if not date_data:
        raise Exception(f"Data for date {date} not found on IEX website")
    
    # Check if the required file is available
    for file in date_data:
        if file.get("feed") == "DEEP" and file.get("date") == date and file.get("version") == "1.0" and file.get("protocol") == "IEXTP1":
            return file
    
    raise Exception(f"IEXTP1 1.0 DEEP file for date {date} not found on IEX website")


    
def download_hist_file(date: str, download_dir: str) -> bool:
    """
    Checks the hist_data JSON file for a specific file and downloads it if it doesn't exist.
    
    Parameters:
        date (str): The date in the format YYYYMMDD.
        download_dir (str): The directory to download the file to.
        
    Returns:
        bool: True if the file was downloaded or already existed, False otherwise.
    """

    # Check if the date is valid
    try:
        datetime.strptime(date, "%Y%m%d")
    except:
        print(f"Invalid date format: {date}. Must be in the format YYYYMMDD")
        return False

    # Get available files for the date from IEX website
    date_file = get_hist_data(date)
    expected_file_size = date_file.get("size")

    file_name = f"data_feeds_{date}_{date}_IEXTP1_DEEP1.0.pcap.gz"

    # Check if the file already exists
    file_path = f"{download_dir}/{file_name}"
    if os.path.exists(file_path):
        if int(os.path.getsize(file_path)) == int(expected_file_size):
            print(f"File {file_name} already exists. Skipping download")
            return True
        else:
            print(f"Expected file size {expected_file_size}. Current file size {os.path.getsize(file_path)}. Redownloading...")
    
    # Download the file
    print(f"Downloading {file_name} to {download_dir}")
    download_url = date_file.get("link")
    response = requests.get(download_url, stream=True)
    
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    
    with open(file_path, "wb") as f, tqdm(total=total_size, unit="iB", unit_scale=True) as pbar:
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                pbar.update(len(chunk))
                f.write(chunk)
    
    print(f"Downloaded {file_name}")
    return True
    
if __name__ == "__main__":
    date = "20231002"
    download_hist_file(date, "C:\\Users\\karth\\Code\\iex-parser\\iex_parser")