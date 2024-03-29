# -*- coding: utf-8 -*-
"""selfreformer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14rGIJpvpdypm4dPo22LGJ-cYaWR_Pzga
"""

!pip install opencv-python
!pip install importlib
!pip install timm

from google.colab import drive
drive.mount('/content/drive')

import torch
import matplotlib.pyplot as plt

!git clone https://github.com/BarCodeReader/SelfReformer.git

# Commented out IPython magic to ensure Python compatibility.
# %cd SelfReformer

class Options(object):
    def __init__(self, seed, pretrain, model, GPU_ID, pvt_path, dataset_root, dataset, test_dataset, lr, decay_step, img_size, batch_size, max_epoch, num_workers, gclip, lmbda, test_only, random_seed, save_every_ckpt, save_result, save_all, ckpt_root, save_root, save_msg, transformer):
        self.seed = seed
        self.pretrain = pretrain
        self.model = model
        self.GPU_ID = GPU_ID
        self.pvt_path = pvt_path
        self.dataset_root = dataset_root
        self.dataset = dataset
        self.test_dataset = test_dataset
        self.lr = lr
        self.decay_step = decay_step
        self.img_size = img_size
        self.batch_size = batch_size
        self.max_epoch = max_epoch
        self.num_worker = num_workers
        self.gclip = gclip
        self.lmbda = lmbda
        self.test_only = test_only
        self.random_seed = random_seed
        self.save_every_ckpt = save_every_ckpt
        self.save_result = save_result
        self.save_all = save_all
        self.ckpt_root = ckpt_root
        self.save_root = save_root
        self.save_msg = save_msg
        self.transformer= transformer

import numpy as np
import cv2
import importlib
import os
import skimage.io as io
import torch
import torch.nn.functional as F
from SelfReformer.augments import Augment
from SelfReformer.option import get_option
from SelfReformer.utils import LogWritter

opt = Options(1, "", "network", 0, "/content/drive/My Drive/best_DUTS-TE.pt", "../dataset/", "DUTSTR", "benchmark_DUTSTE", 1e-4, 40, 224, 16, 200, 8, 0, 5, "", "store_true", "store_true", "store_true", "store_true", "./ckpt", "./output", "abc", [[2, 1, 512, 3, 49],
                           [2, 1, 320, 3, 196],
                           [2, 1, 128, 3, 784],
                           [2, 1, 64, 3, 3136]])
torch.manual_seed(opt.seed)
module = importlib.import_module("model.{}".format(opt.model.lower()))
logger = LogWritter(opt)
dev =  torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = module.Net(opt)
net = net.to(dev)
msg = "# params:{}\n".format(
sum(map(lambda x: x.numel(), net.parameters())))
aug = Augment(opt)
if opt.save_result:
    save_root = os.path.join(opt.save_root, opt.save_msg)
    os.makedirs(save_root, exist_ok=True)

path = '/content/drive/My Drive/best_DUTS-TE.pt'
print('loading model from: {}'.format(path))
state_dict = torch.load(path, map_location=lambda storage, loc: storage)
net.load_state_dict(state_dict)

from PIL import Image
y = Image.open('/content/French toast_2.png')
y

image_path = "/content/French toast_2.png"
image = io.imread(image_path)

image = cv2.resize(image, (224,224))
image = image.astype(np.float32)/255.0

image = np.transpose(image, (2, 0, 1))
image_tensor = torch.from_numpy(image).unsqueeze(0)
image_tensor = image_tensor.to(dev)

with torch.no_grad():
    net.eval()
    output = net(image_tensor)
x = output[0].cpu().numpy()

x = x.astype('uint8')

plt.imshow(x.squeeze())

import matplotlib.pyplot as plt

plt.subplot(1, 2, 1)
plt.imshow(y)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(x.squeeze(), cmap='gray')
plt.title('Model Output')
plt.axis('off')


plt.show()

