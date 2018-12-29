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
        # return file-index and index in that file
        which_file,which_index = self.which_file(index)
        # if file-index is different change if not do nothing
        if self.current_dataset != which_file:
            self.current_dataset = which_file
            self.original_file = self.load_file(self.original_header)
        # get letter of index
        character = self.original_file.at[which_index,"letter"]
        print(character)
        # one hot encode
        letter = self.letter_to_onehot(character)
        # return
        return letter
        pass

    def which_file(self,index):
        temp_file = 1
        temp_index = index

        for i in range(1,int(self.config_data["Dataset_Num"])+1):
            temp_index = temp_index - int(self.config_data["dataset-{}".format(i)])
            if temp_index < 0:
                temp_index = temp_index + int(self.config_data["dataset-{}".format(i)])
                temp_file = i
                break
        return (temp_file,temp_index)


    def generate_file_name(self,header):
        return "{}-{}.csv".format(header,self.current_dataset)

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
        if letter == '':
            letter = "N"
        index = self.all_korean_characters.index(letter)
        return index

    def korean_to_onehot(self,letter):
        index = self.korean_to_index(letter)
        vector = [0 for _ in range(len(self.all_korean_characters))]
        vector[index] = 1
        return vector

    def letter_to_onehot(self,letter):
        letter = hgtk.letter.decompose(letter)
        result = [[0] for _ in range(3)]
        for idx, char in enumerate(letter):
            result[idx] = self.korean_to_onehot(char)
        return result

if __name__ == "__main__":
    data = Dataset()
    print(data.original_file)
    print(data.__getitem__(5000000))