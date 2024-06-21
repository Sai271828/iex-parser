'''
Created on Apr 3, 2021

@author: jdoe
'''
import requests
import json
import datetime


from urllib.parse import unquote
import os.path
from os import path
from tqdm import tqdm
import sys

class IexMarketDataFile(object):
    def __init__(self, date_str, url, feed_type, feed_version, protocol, size):
        self.date = datetime.datetime.strptime(date_str, '%Y%m%d')
        self.url = url
        self.feed_type = feed_type
        self.feed_version = float(feed_version)
        self.protocol = protocol
        self.size = int(size)
        
        self.filename = unquote(self.url.split('/')[-1].split('?')[0]).replace('/', '_')
        # print(self.filename)
        pass
    
    def __str__(self):
        str_rep = ""
        str_rep = "%s %s %s %s %f %s %d bytes" % (self.date, self.url, self.filename, self.feed_type, self.feed_version, self.protocol, self.size)
        return str_rep
    
class IexAvailableFiles(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''

    @staticmethod
    def fetch_available_files(target_data_feed, start_date=None, end_date=None):
        if target_data_feed != "TOPS" and target_data_feed != "DEEP":
            raise Exception("Invalid target_data_feed_type (%s); must be either TOPS or DEEP" % (target_data_feed))
        
        # print("Fetching available files")
        available_files_url = "https://iextrading.com/api/1.0/hist"
        r = requests.get(available_files_url)
        # print(r.content)
        y = json.loads(r.content)
        # print(y)
        
        total_deep_size = 0.0
        all_files = []
        for date, value in y.items():
            for feed in value: #each date contains one or more feeds for TOPS and possibly DEEP
                # print(feed)
                market_data_file = IexMarketDataFile(feed['date'], feed['link'], feed['feed'], feed['version'], feed['protocol'], feed['size'])
                
                market_data_date = datetime.datetime.strptime(feed['date'], '%Y%m%d')
                
                if market_data_date >= start_date and market_data_date <= end_date and feed['feed'] == target_data_feed:
                    # print("Including %s" % (market_data_date))
                    all_files.append(market_data_file)
                    # print(market_data_file)
                    
                    if True or market_data_file.feed_type == target_data_feed:
                        total_deep_size = total_deep_size + market_data_file.size
                else:
                    # print("Filtering out %s" % (market_data_date))
                    pass
        
        deep_size_gigabytes = total_deep_size / (1024.0 * 1024.0 * 1024.0)
        print("Total file size of all pcap files files is %f GB" % deep_size_gigabytes)
        
        return all_files


class IexFileDownloader(object):
    def __init__(self, iex_files):
        self.iex_files = iex_files
        
    def download_all_files(self, base_download_path):
        print("Downloading files")
        
        total_download_size = 0
        for iex_file in self.iex_files:
            total_download_size = total_download_size + iex_file.size
            
        print("Total download size is expected to be %f GB" % (total_download_size / (1024.0 * 1024.0 * 1024.0)))
        
        #todo: use shtuil.disk_uage() to ensure sufficient filespace to actually download all intended files
        #see https://www.geeksforgeeks.org/python-shutil-disk_usage-method/
        
        for iex_file in self.iex_files:
            # base_download_path = download_path
            #base_download_path = "../../downloads"
            #base_download_path = "/run/media/jdoe/My Passport/market_data/IEX"
            download_path = "%s/%s/%s" % (base_download_path, iex_file.feed_type, iex_file.filename)
            
            # print("Downloading %s to %s" % (iex_file.url, download_path))
            IexFileDownloader.download_file(iex_file.url, download_path, iex_file.size)
            
    @staticmethod
    def download_file(file_url, local_path, expected_file_size):
        if path.exists(local_path):
            local_file_size = os.path.getsize(local_path)
            if local_file_size == expected_file_size:
                print("%s already exists and is fully downloaded; skipping download" % (local_path))
                # raise Exception("Invalid filesize %d vs expected %d" % (local_file_size, expected_file_size))
                return 
        
        print("%s doesnt already exist or isnt fully downloaded! downloading... " % (local_path))
        #return
        r = requests.get(file_url, stream=True, allow_redirects=True)
        total_size = int(r.headers.get('content-length'))
        initial_pos = 0
        with open(local_path,'wb') as f: 
            with tqdm(total=total_size, unit='B', 
                       unit_scale=True,desc=local_path,initial=initial_pos, ascii=True) as pbar:
              for ch in r.iter_content(chunk_size=1024):                             
                  if ch:
                      f.write(ch) 
                      pbar.update(len(ch))
                      
        local_file_size = os.path.getsize(local_path)
        print("Downloaded file size is %d vs expected %s" % (local_file_size, expected_file_size))


def download_dates(download_path, start_date_str, end_date_str, target_data_feed):
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date   = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    
    
    all_files = IexAvailableFiles.fetch_available_files(target_data_feed, start_date=start_date,end_date=end_date)
    # sys.exit(0)
   
    
    deep_files = list(filter(lambda x: (x.feed_type == target_data_feed), all_files))
    
    # for deep_file in deep_files:
        # print(deep_file)
    
    file_downloader = IexFileDownloader(deep_files)
    file_downloader.download_all_files(download_path)
    pass

if __name__ == "__main__":
    # target_data_feed = "TOPS"
    # target_data_feed = "DEEP"
    
    #below is the list of dates for which NASDAQ offers free data
    target_dates = [ '2019-03-27', 
                     '2019-07-30',
                     '2019-08-30',
                     '2019-10-30',
                     '2018-12-28',
                     '2021-04-19',
                     '2021-07-13',
                     '2021-08-13'
                    ]
    # target_dates = [ '2021-11-']
    # for target_date in target_dates:
        # download_dates(target_date, target_date, target_data_feed)
    
    download_path="/mnt/marketdata/market_data/IEX"
    
    #TODO this is really simple but very vulnerable command line parsing. later using an actual arg parsing library to do this properly
    
    #Dear students; DO NOT write code like this. Use a proper python command line parsing library with validation, etc. 
    
    if len(sys.argv) != 7:
        raise Exception("Invalid usage! need to specify startdate, enddate, text_tick_dir, and output dir")
    
    
    print("Dumping command line arguments: ")
    for count, arg in enumerate(sys.argv):
        print("\t", count, arg)
    
    if sys.argv[1] == "--start-date":
        start_date_str = sys.argv[2]
        #TODO: add date string validation, ensure in format of YYYY-MM-DD
    else:
        raise Exception("invalid arguments; first parameter should be --start-date <START_DATE>")
    
    if sys.argv[3] == "--end-date":
        end_date_str = sys.argv[4]
        #TODO: add date string validation, ensure in format of YYYY-MM-DD
    else:
        raise Exception("invalid arguments; second parameter should be --end-date <END_DATE>")
    
    if sys.argv[5] == "--download-dir":
        download_dir = sys.argv[6]
        #TODO: add date string validation, ensure in format of YYYY-MM-DD
    else:
        raise Exception("invalid arguments (%s); third parameter should be --download-dir <DOWNLOAD_DIR>" % (sys.argv[5]))
        
        
    #Print a summary
    
    print("Will download IEX DEEP pcap files from %s to %s and output them to %s"% (start_date_str, end_date_str, download_dir))
    
    download_dates(download_dir, start_date_str, end_date_str, 'DEEP')
    
    # for target_data_feed in ['DEEP', 'TOPS']:
        # download_dates(download_path, '2021-11-08', '2021-11-12', target_data_feed)
        #
    pass
    
    
