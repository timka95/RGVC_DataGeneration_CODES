from scipy.io import savemat
import scipy.io
import numpy as np
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import scipy.io as sio
import csv



imagename = '0000000086'
#imagesavepath = f'/Volumes/TIMKA/NEW_CNN/Images/LINES/{imagename}.png'
imagesavepath = f'/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/CODES/TEST/IMAGES/LINES/{imagename}.png'
imagepath = f'/project/Datasets/KITTI_360/2013_05_28_drive_0000_sync/image_00/data_rect/{imagename}.png'


# Load the .mat file
#data = scipy.io.loadmat('/Users/timeanemet/Desktop/CNN/matfiles/subset_data.mat')
#data = scipy.io.loadmat("/home/bence/madTables/osszesitett.mat")
data = scipy.io.loadmat("/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett_2.mat")
#data = scipy.io.loadmat("/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/new_osszesitett_2.mat")
keys = data.keys()
osszesitett_data = data['new_osszesitett_2']


def drawlines (alllines):

    # Open the image
    image = Image.open(imagepath)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    lines = []

    for line in alllines:
        point1 = (line[0], line[1])
        point2 = (line[2], line[3])
        myline = [point1,point2]


        lines.append(myline)

    # Draw the line on the image
    line_color = (255, 0, 0)  # Red
    line_width = 5
    for line in lines:
        draw.line([line[0], line[1]], fill=line_color, width=line_width)

    # Save the modified image
    image.save(imagesavepath)


def searchforimage (imagename):
    imagename = "0000_" + imagename

    for i in range(len(osszesitett_data)):
        image_id_1 = str(osszesitett_data[i][0][0])  # Convert to string
        if image_id_1 != imagename:
            continue
        imglines = []

        for j in range(len(osszesitett_data[i][1])):
            lines = osszesitett_data[i][1][j].flatten().tolist()
            for line in range(len(lines)):
                lines[line] = math.floor(lines[line])

            imglines.append(lines)
    print(imglines)
    return imglines

imagelines = searchforimage(imagename)
drawlines(imagelines)