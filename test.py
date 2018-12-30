from Model.train import Trainer
from Model.run import Runner
import argparse

# Parse Mode
parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, default="run", required=True, help="Mode: 1) train 2) run")
args = parser.parse_args()

trainer = Trainer()
runner = Runner()

if args.mode == "train":
    trainer.train()
elif args.mode == "run":
    runner.run()
else:
    print("Please enter valid mode")