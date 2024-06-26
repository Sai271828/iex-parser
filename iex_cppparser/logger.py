import datetime
import os
import sys
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Log:
    def __init__(self):
        self.log_file_path = os.getenv('LOG_FILE_PATH', '/vagrant/logfile.log')

    def write(self, message):
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w'):
                pass  # Create an empty file if it doesn't exist
        with open(self.log_file_path, 'a') as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f'{timestamp} - {message}\n')

# Example usage
#logger = Log()
#logger.write('This is a log message.')
if __name__ == "__main__":
    log = Log()
    log.write(sys.argv[1])

