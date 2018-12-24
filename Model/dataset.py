import torch
from torch.utils import data
import pandas as pd

class Dataset(data.Dataset):
    def __init__(self):
        self.original_header = "./Data/original"
        self.initial_header = "./Data/initial"

        self.dataset_num = 1
        self.data_num = 1

        self.original_file = pd.read_csv(self.generate_file_name(self.original_header),"a")
        self.initial_file = pd.read_csv(self.generate_file_name(self.initial_header),"a")

    def __len__(self):
        pass

    def __getitem__(self, index):
        arr = [1,2,3,4,5]
        return arr[index]

    def generate_file_name(self,header):
        return "{}-{}.csv".format(header,self.dataset_num)

if __name__ == "__main__":
    data = Dataset()
    print(data[0])
