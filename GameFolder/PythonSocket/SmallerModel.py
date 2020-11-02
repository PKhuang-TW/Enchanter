import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
import torch.optim as optim
from torchvision import transforms
from PIL import Image
from tqdm import tqdm
from torch.autograd import Variable

device = 'cuda' if torch.cuda.is_available() else 'cpu'
TensorInputType = torch.FloatTensor

labelDict = {
    0 : 'Arc',
    1 : 'Lightning',
    2 : 'Fish',
    3 : 'Heart',
    4 : 'Funnel',
    5 : 'Background'
}

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 40, 5, 1)
        self.fc1 = nn.Linear(29*29*40, 250)
        self.fc2 = nn.Linear(250, 6)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 29*29*40)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

imgSize = 128
loader = transforms.Compose([transforms.Resize(imgSize), transforms.ToTensor()])
def image_loader(image_name):
    """load image, returns cuda tensor"""
    image = Image.open(image_name)
    image = loader(image)[0]
    image = torch.unsqueeze(image, 0)
    image = torch.unsqueeze(image, 0)
    image = image.type(TensorInputType)
    return image.to(device)  #assumes that you're using GPU