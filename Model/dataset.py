from torch.utils import data
import torch
import pandas as pd
import hgtk
import json
import os

class Dataset(data.Dataset):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.original_header = dir_path+"/Data/original"
        self.config_data_path = dir_path+"/Data/config.json"

        self.current_dataset = 1

        config_file = open(self.config_data_path, "r")
        self.config_data = json.load(config_file)
        self.original_file = self.load_file(self.original_header)

        self.all_korean_characters = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ','ㄲ','ㄸ','ㅃ','ㅆ','ㅉ',
                                      'ㅆ','ㄳ','ㄵ','ㄶ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅄ','ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ',
                                      'ㅠ','ㅡ','ㅣ','ㅐ','ㅒ','ㅔ','ㅖ','ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ','N']

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
        # one hot encode
        letter = self.letter_to_onehot(character)
        # return
        return letter

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

    def onehot_to_korean(self,vec):
        # vec is a torch vector
        index = vec.max(0)[1]
        return self.all_korean_characters[index]

    def letter_to_onehot(self,letter):
        letter = hgtk.letter.decompose(letter)
        result = [[0] for _ in range(3)]
        for idx, char in enumerate(letter):
            result[idx] = self.korean_to_onehot(char)
        return result
