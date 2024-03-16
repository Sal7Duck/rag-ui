import datetime
import glob
import os.path
import pickle
import urllib.request
from bs4 import BeautifulSoup
import requests

home_dir = "/Users/saloni/Desktop/rag-ui/data/"
dir_data_path = home_dir + "{}/"
file_name = "{}.html"
output_filename = "final_output_text.pkl"
all_directories = ["notification_1991_2023", "notifications_not_in_toc", "rbi_notification_2023_1991"]
verbose = 100

def get_text_from_html(html_file_path):
    html_file = open(html_file_path, 'r')
    html = html_file.read()
    #using BeautifulSoup to scrape text
    soup = BeautifulSoup(html)
    
    #kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    #get text
    text = soup.get_text()
    #break into lines and remmove leading and trailing spaces on each
    lines = (line.strip() for line in text.splitlines())
    #break multi headlines into a line each
    chunks = [phrase.strip() for line in lines for phrase in line.split(" ")]
    #drop blank lines
    text = '\n'.join([chunk for chunk in chunks])
    return text

if __name__ == '__main__':
    extracted_text_all_dirs = {}
    for directory_name in all_directories:
        extracted_text_all_dirs[directory_name] = {}

    #for all html files in all three directories, extract text and store in above object
    for directory_name in all_directories:
        dir_data_path_current = dir_data_path.format(directory_name)

        print(f"\n====== Current Directory : {directory_name} ======")
        start_time = datetime.datetime.now()
            
        #iterate over all nested pkl files
        for counter, html_file_path in enumerate(glob.glob(dir_data_path_current + "*.html")):
            text = get_text_from_html(html_file_path)
            file_name = html_file_path.split("/")[-1].split(".")[0]
            extracted_text_all_dirs[directory_name][file_name] = text

            if counter%verbose == 0:
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                elapsed_seconds = elapsed_time.total_seconds()
                print(f"Total files completed : {counter + 1} in {elapsed_seconds} s")

            if os.path.exists(home_dir + output_filename):
                os.remove(home_dir + output_filename)

            with open(home_dir + output_filename, 'wb') as f:
                pickle.dump(extracted_text_all_dirs, f)

print("Completed!")
