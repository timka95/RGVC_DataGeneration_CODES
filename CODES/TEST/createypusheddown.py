import numpy
from scipy.io import savemat
import scipy.io
import numpy as np
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import scipy.io as sio
import csv

#INPUT
#data = scipy.io.loadmat('/Users/timeanemet/Desktop/CNN/matfiles/subset_data.mat')
#data = scipy.io.loadmat("/home/bence/madTables/osszesitett.mat")
#data = scipy.io.loadmat("/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett_2.mat")
data = scipy.io.loadmat("/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/new_osszesitett_2.mat")

#OUTPUT
filename = '/Matfiles/data.csv'
#filename = '/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/data.csv'

keys = data.keys()

# Access the data structure
osszesitett_data = data['new_osszesitett_2']

imagename = "0000000084"
imgname = "0000_" + imagename
#imagesavepath = f'/Volumes/TIMKA/NEW_CNN/Images/LINES/{imagename}.png'
imagesavepath = f'/Volumes/TIMKA/NEW_CNN/RGVC_DataGeneration_CODES/CODES/TEST/IMAGES/LINES/zeros_{imagename}.png'



for i in range(len(osszesitett_data)):
    print(len(osszesitett_data), "---------", i, len(osszesitett_data[i][1]))

    image_id_1 = str(osszesitett_data[i][0][0])  # Convert to string

    if (image_id_1 != imgname):
        continue

    # Describing the image if push it in the y axis
    pusheddown = [0] * 1408

    for j in range(len(osszesitett_data[i][1])):
        lines = osszesitett_data[i][1][j].flatten().tolist()
        lines3d = osszesitett_data[i][2][j].flatten().tolist()

        if(lines[0] <= lines[2]):
            linestart = math.floor(lines[0])
            lineend = math.ceil(lines[2])
        else:
            linestart = math.floor(lines[2])
            lineend = math.ceil(lines[0])

        for k in range(linestart, lineend):
            pusheddown[k] = 1


    ones_zeros_array = pusheddown

newarray = []
for i in range(10):
    newarray.append(ones_zeros_array)
array = numpy.array(newarray)
array = array.reshape((10, 1408))
image = Image.fromarray((255 * array).astype(np.uint8), mode='L')
image.save(imagesavepath)
