from Model.model import InitialPrediction
from Model.dataset import Dataset
import torch
import os
import hgtk

class Runner():
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))+"/trained/model.ckpt"

        self.model = InitialPrediction()
        self.model.load_state_dict(torch.load(self.dir_path))

        self.dataset = Dataset()

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.embed_size = 26
        self.hidden_size = 26
        self.num_classes=53
        self.batch_size=1

    def extract_chosung(self,query):
        chosung = []
        for letter in query:
            raw = hgtk.letter.decompose(letter)[0]
            one_hot = self.dataset.korean_to_onehot(raw)
            chosung.append([raw,one_hot])
        return chosung

    def run(self):
        while(True):
            query = input("Insert Query : ")
            if query=="exist":
                break
            print("Query : {}".format(query))
            constructed = []
            # Extract cho sung
            chosung = self.extract_chosung(query)
            # For each word -> Feed Forward
            hx = torch.zeros(self.batch_size, self.hidden_size).to(self.device)
            cx = torch.zeros(self.batch_size, self.hidden_size).to(self.device)
            for letter in chosung:
                constructed.append(letter[0])
                x = torch.FloatTensor(letter[1]).unsqueeze(0)
                for seq in range(3):
                    x,hx,cx = self.model(x,hx,cx)
                    if seq<2:
                        constructed.append(self.dataset.onehot_to_korean(x.view(-1)))
            print(constructed)

        print("Run Finished")