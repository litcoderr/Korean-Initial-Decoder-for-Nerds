import torch
from torch.utils import data
import pandas as pd
import json

class Dataset(data.Dataset):
    def __init__(self):
        self.original_header = "./Data/original"
        self.initial_header = "./Data/initial"
        self.config_data_path = "./Data/config.json"

        self.dataset_num = 1
        self.data_num = 1

        config_file = open(self.config_data_path, "r")
        self.config_data = json.load(config_file)

        self.original_file = pd.read_csv(self.generate_file_name(self.original_header),header=None)
        self.original_file.columns = ['letter']
        self.initial_file = pd.read_csv(self.generate_file_name(self.initial_header),header=None)
        self.original_file.columns = ['letter']

    def __len__(self):
        length = 0
        for i in range(1,int(self.config_data["Dataset_Num"])+1):
            length += int(self.config_data["dataset-{}".format(i)])
        return length

    def __getitem__(self, index):
        #TODO create one data based on index --> one_hot_encode --> return
        pass

    def generate_file_name(self,header):
        return "{}-{}.csv".format(header,self.dataset_num)

if __name__ == "__main__":
    data = Dataset()
    print(len(data))
