
from scipy.io import savemat
import scipy.io
import numpy as np
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import scipy.io as sio
import csv


imagename = '0000000741'
imagesavepath = f'/Volumes/TIMKA/NEW_CNN/Images/LINES/{imagename}.png'
imagepath = f"/Volumes/TIMKA/NEW_CNN/Images/Kitti_360/orig/{imagename}.png"
# imagesavepath = f'/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/CODES/TEST/IMAGES/LINES/{imagename}.png'
# imagepath = f'/project/Datasets/KITTI_360/2013_05_28_drive_0000_sync/image_00/data_rect/{imagename}.png'


# Load the .mat file
#data = scipy.io.loadmat('/Users/timeanemet/Desktop/CNN/matfiles/subset_data.mat')
#data = scipy.io.loadmat("/home/bence/madTables/osszesitett.mat")
#data = scipy.io.loadmat("/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett_2.mat")
data = scipy.io.loadmat("/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/new_osszesitett_2.mat")
keys = data.keys()
osszesitett_data = data['new_osszesitett_2']
pusheddown = [0] * 1408

smallImageSize = 376
BigImageWidth = 1408
BigImageHeight = 376

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

            # lines = osszesitett_data[i][1][j].flatten().tolist()

            if (lines[0] <= lines[2]):
                linestart = math.floor(lines[0])
                lineend = math.ceil(lines[2])
            else:
                linestart = math.floor(lines[2])
                lineend = math.ceil(lines[0])

            for k in range(linestart, lineend):
                pusheddown[k] = 1




    print(imglines)
    return imglines, pusheddown


def drawlines (alllines, cuttedhere):

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
    line_color = (255, 255, 0)  # Red
    line_width = 5
    for line in lines:
        draw.line([line[0], line[1]], fill=line_color, width=line_width)
    
        # Draw vertical lines at each x point
    for x in cuttedhere:
        draw.line((x[0], 0, x[0], image.height), fill="red", width=2)
        draw.line((x[1], 0, x[1], image.height), fill="green", width=2)

    # Save the modified image
    image.save(imagesavepath)

imagelines, pusheddown = searchforimage(imagename)

def pusheddowntocutted (pusheddown):

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


    print(allsegment)
    smallImageStart = 0
    smallImageEnd = 0
    cuttedhere = []

    for segment in allsegment:
        start = segment[0]
        end = segment [1]
        size = segment[2]
        print(size)
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

    return cuttedhere

cuttedhere = pusheddowntocutted(pusheddown)
print("CUTTED", cuttedhere)
drawlines(imagelines, cuttedhere)