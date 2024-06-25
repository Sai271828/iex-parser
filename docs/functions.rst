Package Functions
=================

.. automodule:: iex_parser
    :members:
    :undoc-members:
    :show-inheritance:

.. autofunction:: iex_parser.parse_file

`parse_file`
This function parses a file using the IEX parser and redirects the output to a specified folder.

Parameters

- `file_path (str)`: The path to the file to be parsed.
- `parsed_folder (str)`: The path to the folder where the parsed output should be saved.
- `symbol (str)`: Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
- `split (bool)`: Whether to split the output files. One file per letter of the alphabet is generated. Default is False.

Returns: None

### `parse_date` 
This function (can) download and parse the IEXTP1 DEEP1.0 pcap files for a given date.

Parameters

- `date_str (str)`: The date string to be parsed. Format YYYY-MM-DD.
- `download_dir (str)`: The directory where the files are downloaded.
- `parsed_folder (str)`: The directory where the parsed output should be saved.
- `symbol (str)`: Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
- `download (bool)`: Whether to download the files. Default is True.
- `split (bool)`: Whether to split the output files. One file per letter of the alphabet is generated. Default is False.

Returns: None

### `parse_dates`
This function parses a range of dates and (downloads and) parses the corresponding IEXTP1 DEEP1.0 pcap files.

Parameters
- `start_date (str)`: The start date string in the format YYYY-MM-DD.
- `end_date (str)`: The end date string in the format YYYY-MM-DD.
- `download_dir (str)`: The directory where the files are downloaded.
- `parsed_folder (str)`: The directory where the parsed output should be saved.
- `symbol (str)`: Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
- `download (bool)`: Whether to download the files. Default is False.
- `split (bool)`: Whether to split the output files. One file per letter of the alphabet is generated. Default is False.

Returns: None

### `download.get_hist_data`

This function retrieves the historical data available on IEX (https://iextrading.com/api/1.0/hist) and parses it as JSON.

Parameters:
- `date (str)`: The date in the format YYYYMMDD.

Returns:
- `dict`: The parsed JSON data for the required date.

If the data for the specified date is not found or the IEXTP1 1.0 DEEP file is not available, it raises an exception with an appropriate error message.

### `download.download_hist_file`

This function checks the hist_data JSON file for a specific file and downloads it if it doesn't exist.

Parameters:
- `date (str)`: The date in the format YYYYMMDD.
- `download_dir (str)`: The directory to download the file to.

Returns:
- `bool`: True if the file was downloaded or already existed, False otherwise.

The function first checks if the date is valid. It then retrieves the available files for the date from the IEX website using the `get_hist_data` function. It calculates the expected file size based on the retrieved data.
Next, it checks if the file already exists in the specified download directory. If the file exists and its size matches the expected size, it skips the download and returns True. If the file exists but the size doesn't match, it redownloads the file.
If the file doesn't exist or needs to be redownloaded, it proceeds to download the file using the requests library in a streaming fashion. Finally, it saves the downloaded file to the specified directory and returns True.
