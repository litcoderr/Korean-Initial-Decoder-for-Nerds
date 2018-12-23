import os
import hgtk
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup as BS

raw_data_path = "./Data/kowiki-latest-pages-articles.xml"
#raw_data_path = "./Data/small_sample.xml"
original_data_path = "./Data/original.txt"
initial_data_path = "./Data/initial.txt"

## Setup

# Check for raw data path
assert os.path.isfile(raw_data_path), "No Raw Data Found"
# Check for converted data path. If not exist, make one
if not os.path.isfile(original_data_path):
    converted_file = open(original_data_path,"w+")
if not os.path.isfile(initial_data_path):
    converted_file = open(initial_data_path,"w+")

def saveText(text):
    original_file = open(original_data_path,"a")
    initial_file = open(initial_data_path,"a")

    if not text == None:
        original_file.write(text)
        for letter in text:
            if hgtk.checker.is_hangul(letter):
                temp = hgtk.letter.decompose(letter)[0]
                print(temp)
            else:
                temp = letter
            initial_file.write(temp)

context = ET.iterparse(raw_data_path,events=("start","end"))

for event, element in context:
    if event == "start":
        if element.tag == '{http://www.mediawiki.org/xml/export-0.10/}mediawiki':
            root = element
    elif event == "end":
        if element.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
            revision = element.find('{http://www.mediawiki.org/xml/export-0.10/}revision')
            if revision is None: continue
            text_elem = revision.find('{http://www.mediawiki.org/xml/export-0.10/}text')
            if text_elem is None: continue
            text = text_elem.text
            saveText(text)
            if text is None: continue
        root.clear()