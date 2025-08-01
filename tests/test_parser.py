from iex_cppparser import parse_date

# Set your test parameters here
TEST_DATE = "2025-03-13"  # Example date
DOWNLOAD_FOLDER = "testing/"  # Update this path
PARSED_FOLDER = "testing/"      # Update this path
SYMBOLS_FILE = "ALL"                   # Update this path if needed

if __name__ == "__main__":
    try:
        print(f"Testing parser for date={TEST_DATE}, download_folder={DOWNLOAD_FOLDER}, parsed_folder={PARSED_FOLDER}, symbols_file={SYMBOLS_FILE}")
        parse_date(TEST_DATE, DOWNLOAD_FOLDER, PARSED_FOLDER, SYMBOLS_FILE)
        print("Parser ran successfully!")
    except Exception as e:
        print(f"Parser failed: {e}")
