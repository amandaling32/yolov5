import detect
import os

os.system("python detect.py --weights ./best_100epoch.pt --img 640 --conf 0.25 --source ./images --data ../test-1/data.yaml")