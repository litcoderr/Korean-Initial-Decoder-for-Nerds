import torch
from torch.utils import data
import pandas as pd
import hgtk
import json

class Dataset(data.Dataset):
    def __init__(self):
        self.original_header = "./Data/original"
        self.config_data_path = "./Data/config.json"

        self.current_dataset = 1

        config_file = open(self.config_data_path, "r")
        self.config_data = json.load(config_file)
        self.original_file = self.load_file(self.original_header)

        self.all_korean_characters = self.get_korean_characters()

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

    def load_file(self,header):
        temp = pd.read_csv(self.generate_file_name(header),header=None)
        temp.columns = ["letter"]
        return temp

    def get_korean_characters(self):
        temp = []
        for index in range(44032,50814):
            temp_ch = chr(index)
            temp_ch = hgtk.letter.decompose(temp_ch)
            for letter in temp_ch:
                if not letter in temp:
                    temp.append(letter)
        temp.append("N")
        return temp

    def korean_to_index(self,letter):
        index = self.all_korean_characters.index(letter)
        return index

    def korean_to_onehot(self,letter):
        index = self.korean_to_index(letter)
        vector = [0 for _ in range(len(self.all_korean_characters))]
        vector[index] = 1
        return vector

if __name__ == "__main__":
    data = Dataset()
    print(data.original_file)