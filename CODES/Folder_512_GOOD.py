from torch.nn import functional as F
import math
import numpy as np
import torch
import torch.nn as nn
from scipy import ndimage
import cv2
import sys
import scipy.io as sio
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image 
import datetime
from scipy.io import savemat


import os

# ####################################HT########################################################
def hough_transform(rows, cols, theta_res, rho_res, input_image_path):



    # ####### HT
    # r = 128
    # c = 128
    # h = 182
    # w = 60  # Use .shape instead of .size()

    r = 512
    c = 512
    h = 728
    w = 240  

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



    ########

    theta = np.linspace(0, 180.0, int(np.ceil(180.0 / theta_res) + 1.0))
    theta = theta[0:len(theta) - 1]

    D = np.sqrt((rows/2) ** 2 + (cols/2) ** 2)-1
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


    coords_r, coords_w = np.ones((rows, cols)).nonzero()
    coords = np.concatenate((coords_r[:,None], coords_w[:,None]), axis=1).astype(np.float16)

    
    coords[:,0] = rows-coords[:,0]-rows//2
    coords[:,1] = coords[:,1] +1 - cols//2

    vote_map = (coords @ sin_cos).astype(np.float16)
    print("FOR START", datetime.datetime.now())


    hough_space = np.zeros((h * w))
    for i in range(rows * cols):
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



    # HT_map = image @ self.vote_index
    # HT_map = HT_map / self.norm

    #print(vote_index[3][1][16])
        
    print("FOR END", datetime.datetime.now())
    #result = (vote_index.reshape(rows*cols, w*h))

    
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



# Rest of your imports and functions...

def process_folder(folder_path, output_folder):

    maximagewanted = 10
    imagecount = 0

    # List all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]

    for image_file in image_files:
        imagecount = imagecount+1

        if(imagecount >= maximagewanted):
            break


        image_path = os.path.join(folder_path, image_file)
        print("Processing:", image_path)

        # Generate the output image name
        output_image_name = image_file.replace(".png", "_HOUGH.png")
        output_image_path = os.path.join(output_folder, output_image_name)

        # Check if the output image already exists, if yes, skip processing
        # if os.path.exists(output_image_path):
        #     print("Output image already exists, skipping:", output_image_path)
        #     continue

        # Apply Hough Transform
        hough_space = hough_transform(rows=512, cols=512, theta_res=0.75, rho_res=1, input_image_path=image_path)

        # Save the Hough Transform image in the output folder
        plt.imsave(output_image_path, hough_space.squeeze(), cmap='gray', vmin=0, vmax=255)
        print("Hough Transform image saved at:", output_image_path)

if __name__ == "__main__":
    print("START", datetime.datetime.now())
    
    # input_folder = "/Users/timeanemet/Desktop/CNN/l2d2-main_2/Pictures/linetest/512"
    # output_folder = "/Users/timeanemet/Desktop/CNN/l2d2-main_2/Pictures/linetest/H512"

    input_folder ="/Volumes/TIMKA/NEW_CNN/Images/Kitti360_cuttedGT_512"
    output_folder = "/Volumes/TIMKA/NEW_CNN/Images/ThetaRho_TEST"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_folder(input_folder, output_folder)
    print("END", datetime.datetime.now())



