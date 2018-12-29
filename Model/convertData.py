import os
import hgtk
from xml.etree import ElementTree as ET
import json

raw_data_path = "./Data/kowiki-latest-pages-articles.xml"
original_data_path = "./Data/original"
config_data_path = "./Data/config.json"
dataset_num = 1
data_count = 1

## Setup
# Check for raw data path
assert os.path.isfile(raw_data_path), "No Raw Data Found"

def update_config(datacount):
    if os.path.isfile(config_data_path):
        file = open(config_data_path, "r+")
        data = json.load(file)
    else:
        file = open(config_data_path,"a")
        data = {
            "Dataset_Num": dataset_num,
            "dataset-1": 0
        }
    data["dataset-{}".format(dataset_num)] = datacount
    data["Dataset_Num"] = dataset_num
    file.seek(0)
    json.dump(data,file)
    file.truncate()
    file.close()

def saveText(text):
    global data_count
    global dataset_num
    original_file = open("{}-{}.csv".format(original_data_path,dataset_num),"a")

    if not text == None:
        for letter in text:
            if hgtk.checker.is_hangul(letter):
                original_file.write("{}\n".format(letter))

                data_count += 1
                if data_count == 5000001:
                    update_config(data_count-1)
                    print("dataset-{} done".format(dataset_num))
                    data_count = 1
                    dataset_num += 1
                    original_file = open("{}-{}.csv".format(original_data_path, dataset_num), "a")
            else:
                pass

print("start parsing")
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

print("done parsing")