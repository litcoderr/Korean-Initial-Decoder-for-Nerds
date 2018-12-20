import os

raw_data_path = "./Data/kowiki-latest-pages-articles.xml"
converted_data_path = "./Data/converted.txt"

## Setup

# Check for raw data path
assert os.path.isfile(raw_data_path), "No Raw Data Found"
# Check for converted data path. If not exist, make one
if not os.path.isfile(converted_data_path):
    converted_file = open(converted_data_path,"w+")



# End Program
converted_file.close()
