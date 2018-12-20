import os
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup as BS

#raw_data_path = "./Data/kowiki-latest-pages-articles.xml"
raw_data_path = "./Data/small_sample.xml"
converted_data_path = "./Data/converted.txt"

## Setup

# Check for raw data path
assert os.path.isfile(raw_data_path), "No Raw Data Found"
# Check for converted data path. If not exist, make one
if not os.path.isfile(converted_data_path):
    converted_file = open(converted_data_path,"w+")

print("Start Parsing")
xmlTree = ET.parse(raw_data_path)
xmlRoot = xmlTree.getroot()
xmlString = ET.tostring(xmlRoot,encoding='utf8',method='xml')
soup = BS(xmlString)
tag = soup.find_all("text")

for idx, element in enumerate(tag):
    print("{} : {}".format(idx,element.text))

print("Finished Parsing")
