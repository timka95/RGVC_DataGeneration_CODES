from PIL import Image, ImageDraw

from torch.nn import functional as F

import torch
import torch.nn as nn

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
import datetime
from skimage import exposure
import torch
import numpy as np
import cv2
import math


#INPUT
input_image_path= "/Volumes/TIMKA/NEW_CNN/Images/Kitti360_cuttedGT_512/0000_0000000001_1.png"
inputcsv_path = "/Volumes/TIMKA/NEW_CNN/matfiles/Every_data_2.csv"



# ####################################HT########################################################
def hough_transform( rows_orig, cols_orig, rows_hough, cols_hough, theta_res, rho_res, input_image_path ):

    r = rows_orig
    c = cols_orig
    h = rows_hough
    w = cols_hough  

    norm = max(r, c)

    # Load your binary input image (replace 'input_image_path' with the actual path)
    input_image_path = input_image_path


    binary_image = np.array(Image.open(input_image_path).convert("L"))
    binary_image[binary_image != 0] = 1  # Convert non-zero values to 1
    
    # Create a PyTorch tensor from the binary image
    image = torch.tensor(binary_image).unsqueeze(0).float()

    image_shape = image.size()
    image = image.unsqueeze(0)

        
        
    batch, channel, _, _ = image.size()

    image = image.view(batch,channel, -1).view(batch*channel, -1)

    image = F.relu(image)


    theta = np.linspace(0, 180.0, int(np.ceil(180.0 / theta_res) + 1.0))
    theta = theta[0:len(theta) - 1]

    D = np.sqrt((rows_orig/2) ** 2 + (cols_orig/2) ** 2)-1
    #D = np.sqrt((rows - 1) ** 2 + (cols - 1) ** 2)
    
    q = np.ceil(D / rho_res)
    #nrho = 182
    nrho = 728
    #nrho = 2 *q + 1
    rho = np.linspace(-q * rho_res, q * rho_res, int(nrho))

    w = np.size(theta)
    h = np.size(rho)
    cos_value = np.cos(theta * np.pi / 180.0).astype(np.float32)
    sin_value = np.sin(theta * np.pi / 180.0).astype(np.float32)
    sin_cos = np.concatenate((sin_value[None, :], cos_value[None, :]), axis=0)


    coords_r, coords_w = np.ones((rows_orig, cols_orig)).nonzero()
    coords = np.concatenate((coords_r[:,None], coords_w[:,None]), axis=1).astype(np.float16)

    
    coords[:,0] = rows_orig-coords[:,0]-rows_orig//2
    coords[:,1] = coords[:,1] +1 - cols_orig//2

    vote_map = (coords @ sin_cos).astype(np.float16)
    print("FOR START", datetime.datetime.now())


    hough_space = np.zeros((h * w))
    for i in range(rows_orig * cols_orig):
        if( int(image[0,i]) == 0):
            continue
        for j in range(w):
            rhoVal = vote_map[i, j]
            rhoIdx = np.argmin(np.abs(rho - rhoVal))  # Use argmin instead of nonzero
            new_j = rhoIdx * w + j
            #vote_index[i, new_j] = 1 
            image_num = int(image[0,i])
            hough_num = hough_space[new_j]
            #hough_space[new_j] = hough_space[new_j] + image[i]
            hough_space[new_j] = hough_space[new_j] + image_num 
        
    print("FOR END", datetime.datetime.now())
    #result = (vote_index.reshape(rows_orig*cols_orig, w*h))

    
    #HOUGH_SIZE = hough_space.size()
    hough_space = hough_space / norm
    hough_space = torch.tensor(hough_space).view(1, -1)

    hough_space = hough_space.view(batch, channel, -1).view(batch, channel, h, w)
    #ht_image_np = hough_space.squeeze().detach().numpy()
    ht_image_np = hough_space
    hough_space_TYPE = hough_space.type()
    hough_space_SHAPE = hough_space.size()

    ht_image_np = hough_space.squeeze().detach().numpy()

    # Normalize Hough Transform values to [0, 255] and convert to uint8

    # Assuming ht_image_np is your 2D numpy array
    min_value = np.min(ht_image_np)
    max_value = np.max(ht_image_np)

    # Perform min-max normalization
    ht_image_np = (ht_image_np - min_value) / (max_value - min_value) * 255


    #ht_image_np = (ht_image_np - np.min(ht_image_np)) / (np.max(ht_image_np) - np.min(ht_image_np)) * 255
    ht_image_np = ht_image_np.astype(np.uint8)

    # Save the Hough Transform image (replace 'output_image_path' with the desired output path)


    return ht_image_np

rows_orig = 512
cols_orig = 512
rows_hough = 728
cols_hough = 240
theta_res = 0.75
rho_res = 1



ht_image = hough_transform( rows_orig, cols_orig, rows_hough, cols_hough, theta_res, rho_res, input_image_path )
print(ht_image[0][239])



