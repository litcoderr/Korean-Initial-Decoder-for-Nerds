from Model.model import InitialPrediction
from Model.dataset import Dataset
import torch
import torch.nn as nn
import os

class Trainer():
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Hyper-parameters
        self.embed_size = 26
        self.hidden_size = 26
        self.num_classes=53
        self.batch_size=1
        self.num_epochs = 5
        self.learning_rate = 0.002

        # Dataset
        self.dataset = Dataset()

        # Model
        self.model = InitialPrediction(embed_size=self.embed_size,hidden_size=self.hidden_size,
                                       num_classes=self.num_classes).to(self.device)

        # Loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def train(self):
        for epoch in range(self.num_epochs):
            self.hx = torch.zeros(self.batch_size, self.hidden_size).to(self.device)
            self.cx = torch.zeros(self.batch_size, self.hidden_size).to(self.device)

            for index in range(len(self.dataset)):
                data = self.dataset[index]
                x = torch.FloatTensor(data[0]).unsqueeze(0) # Initial input

                # Forward
                for seq in range(3):
                    x,self.hx,self.cx = self.model(x,self.hx,self.cx)
                    if seq<2:
                        y = torch.LongTensor(data[seq+1]).max(0)[1].unsqueeze(0)
                        loss = self.criterion(x,y)

                        # Backward
                        self.optimizer.zero_grad()
                        loss.backward(retain_graph=True)
                        self.optimizer.step()

                if index % 100 == 0:
                    print("Epoch[{}/{}], Step[{}\{}], Loss:{:.4f}".format(
                        epoch, self.num_epochs, index, len(self.dataset), loss
                    ))
                    dir_path = os.path.dirname(os.path.realpath(__file__))
                    dir_path = dir_path+"/trained/model.ckpt"
                    torch.save(self.model.state_dict(), dir_path)
