import torch
import torch.nn as nn

class InitialPrediction(nn.Module):
    def __init__(self, embed_size=26, hidden_size=26, num_classes=53):
        super(InitialPrediction,self).__init__()
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.num_classes = num_classes

        self.encoder = nn.Linear(num_classes,embed_size)
        self.lstm = nn.LSTMCell(embed_size, hidden_size)
        self.decode = nn.Linear(hidden_size,num_classes)

    def forward(self, input, hidden, context):
        input = self.encoder(input)
        hidden, context = self.lstm(input,(hidden, context))
        output = self.decode(hidden)
        return (output,hidden,context)

'''
data = Dataset()
data = data[0][0]
data = torch.FloatTensor(data)
data = data.unsqueeze(0)

model = InitialPrediction()
hx = torch.randn(1, 26)
cx = torch.randn(1, 26)
print("{} , {} , {}".format(data,hx,cx))
output,hx,cx = model(data,hx,cx)
print("{} , {} , {}".format(output,hx,cx))
'''
