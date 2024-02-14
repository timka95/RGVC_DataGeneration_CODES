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
import csv
import ast
import cv2


#INPUT
input_image_path= "/Volumes/TIMKA/NEW_CNN/Images/Kitti360_cuttedGT_512/0000_0000000001_1.png"
inputcsv_path = "/Volumes/TIMKA/NEW_CNN/matfiles/Every_data_2.csv"
saveimagepath ="/Volumes/TIMKA/NEW_CNN/Images/ThetaRho_TEST/"



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

def read_csv(file_path):
    # Read the CSV file
    with open(file_path, 'r') as csvfile:
        # Create a CSV reader object
        csvreader = csv.reader(csvfile)
        # Get the header
        header = next(csvreader)
        # Create an empty list to store the csvdata
        csvdata = []
        # Iterate over each row in the csv file
        for row in csvreader:
            # Create an empty dictionary
            row_dict = {}
            # Iterate over each cell in the row and the corresponding header cell
            for cell, header_cell in zip(row, header):
                # Add the cell value to the dictionary with the header cell as the key
                row_dict[header_cell] = cell
            # Add the dictionary to the csvdata list
            csvdata.append([row_dict])
        # Return the csvdata list
        return csvdata




def editcsv (csvdata):

    for i in range(len(csvdata)):  
        csvdata[i] = csvdata[i][0]

    for i in range(len(csvdata)):
        current = csvdata[i] 

        csvdata[i]["ThetaRho"] = ast.literal_eval(current["ThetaRho"])
        csvdata[i]["2D_orig"] = ast.literal_eval(current["2D_orig"])
        csvdata[i]["2D_376"]  = ast.literal_eval(current["2D_376"])
        csvdata[i]["2D_512"]  = ast.literal_eval(current["2D_512"])
        csvdata[i]["cuttedhere"]  = ast.literal_eval(current["cuttedhere"])
        csvdata[i]["3D"]  = ast.literal_eval(current["3D"])

    return csvdata


def saveimageHough(ht_image, saveimagepath):
    # Create an image from the array
    plt.imsave(saveimagepath, ht_image.squeeze(), cmap='gray', vmin=0, vmax=255)



def saveimageFromCSV( ThetaRho, saveimagepath):
# Create a new black image
    img = Image.new('RGB', (240, 728), color = 'black')

    # Create a draw object
    d = ImageDraw.Draw(img)

    # List of coordinates for white dots
    coords = ThetaRho

    # Draw white dots at the specified coordinates
    for coord in coords:
        d.point(coord, fill='white')


    # Save the image
    img.save(saveimagepath)


def brightest (htimage):
    image = cv2.imread(htimage)
    # Find the coordinates of the brightest point
    max_value = np.max(image)
    brightest_point = np.argwhere(image == max_value)[0]

    # Get the color of the brightest point
    color = image[brightest_point[0], brightest_point[1]]

    brightest_points = np.argwhere(image == color)
    return_brightest = []

    # Print the coordinates of the brightest points
    for point in brightest_points:
        return_brightest.append([point[1], point[0]])
    
    return brightest_points




def drawbigimage(coordinates, path):

    image = np.zeros((512, 512), np.uint8)

    for coord in coordinates:
        x1, y1, x2, y2 = map(int, coord)
        cv2.line(image, (x1, y1), (x2, y2), (255), 1)

# Save the image
    cv2.imwrite(path, image)



















rows_orig = 512
cols_orig = 512
rows_hough = 728
cols_hough = 240
theta_res = 0.75
rho_res = 1


csvdata = read_csv(inputcsv_path)
csvdata = editcsv(csvdata)

# horizontallines = [ [[100,50,100,50]], [[50,100,50,100]], [[450,350,450,350]], [[350,450,350,450]]  ]
# horizontalnames = ["DUL", "DDL", "DDR", "DUR" ]

for i in range(3):
    saveimagepath_bigimg = ""
    saveimagepath_HoughCALC = ""

    current = csvdata[i]
    name = str(current["ID"])
    thetarho = current["ThetaRho"]
    data_512 = current["2D_512"]


    thetarho = thetarho

    # saveimagepath_CSV = saveimagepath + name + "_FROMCSV.png"
    # saveimageFromCSV( thetarho, saveimagepath_CSV)

    #TEST
    saveimagepath_bigimg= saveimagepath + name + "_ORIG.png"
    drawbigimage(data_512, saveimagepath_bigimg )

    ht_image = hough_transform( rows_orig, cols_orig,theta_res, rho_res, saveimagepath_bigimg )
    saveimagepath_HoughCALC = saveimagepath + name + "_CALC.png"
    saveimageHough(ht_image, saveimagepath_HoughCALC )

    # brightestdata = brightest(saveimagepath_CSV)
    print(data_512)
    print(name)
    # print("BRIGHTEST: ", brightestdata)
    print("----------")














