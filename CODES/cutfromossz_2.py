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
data = scipy.io.loadmat("/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett_2.mat")
#data = scipy.io.loadmat("/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/new_osszesitett_2.mat")

#OUTPUT
filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data.csv'
#filename = '/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/data.csv'

keys = data.keys()
osszesitett_data = data['new_osszesitett_2']



imagename = "0000000035"
imgname = "0000_" + imagename

for i in range(len(osszesitett_data)):
    image_id_1 = str(osszesitett_data[i][0][0])  # Convert to string
    pusheddown = [0] * 1408

    if image_id_1 != imgname:
        continue

    for j in range(len(osszesitett_data[i][1])):
        lines = osszesitett_data[i][1][j].flatten().tolist()
        lines3d = osszesitett_data[i][2][j].flatten().tolist()

        if (lines[0] <= lines[2]):
            linestart = math.floor(lines[0])
            lineend = math.ceil(lines[2])
        else:
            linestart = math.floor(lines[2])
            lineend = math.ceil(lines[0])

        for k in range(linestart, lineend):
            pusheddown[k] = 1

    #We Have pusheddown which represents the image with 1 and 0 pushed down on the y axis

    #start,end,size
    segments = [0] * 3
    allsegment = []
    size = 0
    for i in range(len(pusheddown)):
        if(pusheddown[i] == 1):
            if(pusheddown[i-1] == 0):
                segments[0] = i
            size = size+1

        if (pusheddown[i] == 0):
            if(size != 0):
                segments[2] = size
                segments[1] = i
                allsegment.append(segments)
                size = 0


    print(allsegment)


