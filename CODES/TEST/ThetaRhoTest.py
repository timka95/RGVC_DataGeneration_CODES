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



# ####################################HT########################################################
def hough_transform(rows, cols, theta_res, rho_res):
    theta = np.linspace(0, 180.0, int(np.ceil(180.0 / theta_res) + 1.0))
    theta_SIZE = len(theta)
    theta = theta[0:len(theta) - 1]
    theta_SIZE = len(theta)

    ###  Actually,the offset does not have to be this large, because the origin is located at the image center.
    D = np.sqrt((rows - 1) ** 2 + (cols - 1) ** 2)
    ###  replace the line above to reduce unnecessray computation (significantly).
    # D = np.sqrt((rows/2) ** 2 + (cols/2) ** 2)

    q = np.ceil(D / rho_res)
    nrho = 2 * q + 1
    rho = np.linspace(-q * rho_res, q * rho_res, int(nrho))
    rho_SIZE = len(rho)

    w = np.size(theta)
    h = np.size(rho)
    cos_value = np.cos(theta * np.pi / 180.0).astype(np.float32)
    sin_value = np.sin(theta * np.pi / 180.0).astype(np.float32)
    sin_cos = np.concatenate((sin_value[None, :], cos_value[None, :]), axis=0)

    ###  This is much more memory-efficient by shifting the coordinate ####
    coords_r, coords_w = np.ones((rows, cols)).nonzero()
    coords = np.concatenate((coords_r[:, None], coords_w[:, None]), axis=1).astype(np.float32)

    coords[:, 0] = rows - coords[:, 0] - rows // 2
    coords[:, 1] = coords[:, 1] + 1 - cols // 2

    vote_map = (coords @ sin_cos).astype(np.float32)

    print("FOR START", datetime.datetime.now())

    vote_index = np.zeros((rows * cols, h, w))
    for i in range(rows * cols):
        if(i % 100 == 0):
            print(rows * cols, "--------", i)
        for j in range(w):
            rhoVal = vote_map[i, j]
            rhoIdx = np.nonzero(np.abs(rho - rhoVal) == np.min(np.abs(rho - rhoVal)))[0]
            vote_map[i, j] = float(rhoIdx[0])
            vote_index[i, rhoIdx[0], j] = 1

    print("FOR END", datetime.datetime.now())

    vote_index_SIZE = vote_index.shape
    ### remove all-zero lines in the HT maps ####
    vote_rho_idx = vote_index.reshape(rows * cols, h, w).sum(axis=0).sum(axis=1)
    # vote_rho_idx_SIZE=vote_rho_idx.size()
    vote_index_SIZE = vote_index.shape
    vote_index = vote_index[:, vote_rho_idx > 0.0, :]
    vote_index_SIZE = vote_index.shape
    # vote_index_SIZE = vote_index.shape
    ### update h, since we remove those HT lines without any votes
    ### slightly different from the original paper, the HT size in this script is 182x60.
    h = (vote_rho_idx > 0.0).sum()
    vote_index_SIZE = vote_index.shape
    result = vote_index.reshape(rows, cols, h, w)
    vote_index_SIZE = result.shape
    

    

    return result






# Create a blank image with a white background
width, height = 128, 128
image = Image.new('RGB', (width, height), (0,0,0))
draw = ImageDraw.Draw(image)


#[633.737000000000,205.220000000000,133.070000000000,374.207000000000]

point1 = (132.996000000000,14.867000000000)
point2 = (45.987000000000,57.565000000000)

# middle = (64,64)

x1, y1 = point1
x2, y2 = point2

# Angle in degrees by which to rotate the line
rotation_angle_degrees = 0

# Calculate the rotation angle in radians
rotation_angle_radians = math.radians(rotation_angle_degrees)

# Calculate the coordinates of the new endpoints
i = int((x1 - 64) * math.cos(rotation_angle_radians) - (y1 - 64) * math.sin(rotation_angle_radians) + 64)
j = int((x1 - 64) * math.sin(rotation_angle_radians) + (y1 - 64) * math.cos(rotation_angle_radians) + 64)
x = int((x2 - 64) * math.cos(rotation_angle_radians) - (y2 - 64) * math.sin(rotation_angle_radians) + 64)
y = int((x2 - 64) * math.sin(rotation_angle_radians) + (y2 - 64) * math.cos(rotation_angle_radians) + 64)

print("new coordinates", i, "," ,j, " ", x, "," ,y )


# Define coordinates for the lines
lines = [
   ((i,j),(x,y)) 
]

# Draw the lines on the image
line_color = (255, 255, 255)  # Black
for line in lines:
    draw.line(line, fill=line_color, width=2)

pathi = f'{i}_{j}__{x}_{y}.png'
path = f'/Users/timeanemet/Desktop/CNN/l2d2-main_2/Pictures/Coordinate/125_'+pathi
image.save(path)

print("START", datetime.datetime.now())
# Default settings for hough_transform
vote_index = hough_transform(rows=128, cols=128, theta_res=3, rho_res=1)


#loading vote index instead of calculating
#vote_index = np.load('vote_index.npy')


vote_index = torch.from_numpy(vote_index).float().contiguous()


# Load your binary input image (replace 'input_image_path' with the actual path)
input_image_path = path
#input_image_path = "/Users/timeanemet/Desktop/CNN/l2d2-main_2/Pictures/Ered128/004422_1.png"



class HT(nn.Module):
    def __init__(self, vote_index):
        super(HT, self).__init__()
        self.r, self.c, self.h, self.w = vote_index.size()  # Use .shape instead of .size()
        self.norm = max(self.r, self.c)
        SHAPE = vote_index.size()
        vote_type = type(vote_index)
        self.vote_index = vote_index.view(self.r * self.c, self.h * self.w)
        self.total = vote_index.sum(0).max()

    def forward(self, image):
        image_shape = image.size()
        image = image.unsqueeze(0)

        batch, channel, _, _ = image.size()

        image = image.view(batch, channel, -1).view(batch * channel, -1)

        image_shape = image.size()
        vote_index_shape = self.vote_index.size()
        image = F.relu(image)


        print(image.size(), self.vote_index.size())
        HT_map = image @ self.vote_index




        HT_map = HT_map / self.norm  # Removed self.total normalization
        HT_map = HT_map.view(batch, channel, -1).view(batch, channel, self.h, self.w)

        
        return HT_map

input_image = Image.open(input_image_path)

# Convert the image to grayscale mode
grayscale_image = input_image.convert('L')

# Convert the grayscale image to a NumPy array
binary_image = np.array(grayscale_image)

# Create a PyTorch tensor from the binary image
image_tensor = torch.tensor(binary_image).unsqueeze(0).float()  # Convert to float32 tensor

ht_module = HT(vote_index)

# Calculate the Hough Transform image using the HT module
ht_image = ht_module(image_tensor)

# Convert the Hough Transform image to a NumPy array
ht_image_np = ht_image.squeeze().detach().numpy()

print("MINMAX")
print(np.min(ht_image_np))
print(np.max(ht_image_np))

min_value = np.min(ht_image_np)


# ht_image_np = (ht_image_np - np.min(ht_image_np)) / (np.max(ht_image_np) - np.min(ht_image_np)) * 255
# ht_image_np = ht_image_np.astype(np.uint8)

# Save the Hough Transform image (replace 'output_image_path' with the desired output path)
pathi = f'H_{i}_{j}__{x}_{y}.png'
path = f'/Users/timeanemet/Desktop/CNN/l2d2-main_2/Pictures/Coordinate/'+pathi
image.save(path)




output_image_path = path
plt.imsave(output_image_path, ht_image_np, cmap='gray')

print("Hough Transform image saved at:", output_image_path)

print("END", datetime.datetime.now())


################# BRIHTEST #################

image = cv2.imread(path)  # Replace 'your_image.jpg' with the path to your image file

max_value = np.max(image)
brightest_point = np.argwhere(image == max_value)[0]

# Get the color of the brightest point
color = image[brightest_point[0], brightest_point[1]]



brightest_points = np.argwhere(image == max_value)

# Print the coordinates of the brightest points
for point in brightest_points:
    print(f'({point[1]}, {point[0]})')


