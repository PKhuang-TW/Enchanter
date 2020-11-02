import socket
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
import torch.optim as optim
from torchvision import transforms
from PIL import Image

# from model import *
from SmallerModel import *

def pts2img(xs, ys):
	# imgPath = 'Assets/Gesture/RealTimeImg/'	
	imgPath = 'Gesture/'
	imgName = 'RealTimeImg.png'
	plt.figure(figsize=(3*80/60, 3*80/60), dpi=64)
	xlen = max(xs) - min(xs)
	ylen = max(ys) - min(ys)
	plt.axis('off')
	plt.xlim(min(xs)-0.05, max(xs)+0.05)
	plt.ylim(min(ys)-0.05, max(ys)+0.05)
	plt.plot(xs, ys, color='k', linewidth=15.0)
	plt.savefig(imgPath + imgName)
	plt.close()
	return imgPath + imgName

# Server mode socket, set to receive message
recv_address = ('127.0.0.1', 7000)
recv_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_s.bind(recv_address)

# Client mode socket, set to send message
send_address = ('127.0.0.1', 4000)
send_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


print('Loading Model...')
net = Net().to(device)
# net = torch.load('../Models/best.pt')
net.load_state_dict(torch.load('Gesture/best.pt'))
imgPath = pts2img([0], [0])
img = image_loader(imgPath)
pred = net(img)
print('Model Loaded Successfully!')

print('Server Started...')

xs = []
ys = []
while True:
	data, addr = recv_s.recvfrom(1024)
	data = data.decode("utf-8")
	
	if data == 'CloseSocket':
		break

	if data == 'MessageSent':
		imgPath = pts2img(xs, ys)
		# imgPath = '../Data/CollectedImgs/Funnel/Chenxy_2.png'
		img = image_loader(imgPath)
		pred = net(img)
		_, pred = torch.max(pred.data, 1)
		pred = pred.cpu().numpy()[0]
		send_s.sendto(str(pred).encode('utf-8'), send_address)
		print('Prediction :', labelDict[pred])
		xs = []
		ys = []

	else:
		xs.append(float(data.split(',')[0]))
		ys.append(float(data.split(',')[1]))

send_s.close()
recv_s.close()