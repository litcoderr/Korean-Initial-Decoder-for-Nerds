from Model.model import InitialPrediction
from Model.dataset import Dataset
import torch
import os
import hgtk

dir_path = os.path.dirname(os.path.realpath(__file__))+"/trained/model.ckpt"

model = InitialPrediction()
model.load_state_dict(torch.load(dir_path))

dataset = Dataset()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

embed_size = 26
hidden_size = 26
num_classes=53
batch_size=1

def extract_chosung(query):
    chosung = []
    for letter in query:
        raw = hgtk.letter.decompose(letter)[0]
        one_hot = dataset.korean_to_onehot(raw)
        chosung.append([raw,one_hot])
    return chosung


while(True):
    query = input("Insert Query : ")
    if query=="exist":
        break
    print("Query : {}".format(query))
    constructed = []
    # Extract cho sung
    chosung = extract_chosung(query)
    # For each word -> Feed Forward
    hx = torch.zeros(batch_size, hidden_size).to(device)
    cx = torch.zeros(batch_size, hidden_size).to(device)
    for letter in chosung:
        constructed.append(letter[0])
        x = torch.FloatTensor(letter[1]).unsqueeze(0)
        for seq in range(3):
            x,hx,cx = model(x,hx,cx)
            if seq<2:
                constructed.append(dataset.onehot_to_korean(x.view(-1)))
    print(constructed)

print("Run Finished")