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
#filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data.csv'
filename = '/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/data.csv'

keys = data.keys()
osszesitett_data = data['new_osszesitett_2']


imagename = "0000000084"
imgname = "0000_" + imagename
imagepath = f'/project/Datasets/KITTI_360/2013_05_28_drive_0000_sync/image_00/data_rect/{imagename}.png'
imagesavepath = f'/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/CODES/TEST/IMAGES/LINES/cutted_here{imagename}.png'

smallImageSize = 376
BigImageWidth = 1408
BigImageHeight = 376

for i in range(len(osszesitett_data)):
    image_id_1 = str(osszesitett_data[i][0][0])  # Convert to string
    pusheddown = [0] * BigImageWidth

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
                segments = [0] * 3
                size = 0

    smallImageStart = 0
    smallImageEnd = 0
    cuttedhere = []
    
    for segment in allsegment:
        start = segment[0]
        end = segment [1]
        size = segment[2]
        if(size <= smallImageSize):
            middle = start + (smallImageSize/2)
            if(start - (smallImageSize/2) < 0):
                smallImageStart = 0
                smallImageEnd = smallImageSize
            elif(end + (smallImageSize/2) > BigImageWidth):
                smallImageStart = BigImageWidth-smallImageSize
                smallImageEnd = BigImageWidth
            else:
                smallImageStart = middle - (smallImageSize/2)
                smallImageEnd = middle + (smallImageSize/2)

            smallImageStart = int(smallImageStart)
            smallImageEnd = int(smallImageEnd)
            cuttedhere.append([smallImageStart,smallImageEnd])
        else:
            # we will create two images where they overlap
            smallImageStart = start
            smallImageEnd = start + smallImageSize

            smallImageStart = int(smallImageStart)
            smallImageEnd = int(smallImageEnd)
            cuttedhere.append([smallImageStart,smallImageEnd])

            smallImageStart = end - smallImageSize
            smallImageEnd = end

            smallImageStart = int(smallImageStart)
            smallImageEnd = int(smallImageEnd)
            cuttedhere.append([smallImageStart,smallImageEnd])


            
            


        

    
    
            
        





