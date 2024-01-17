from scipy.io import savemat
import scipy.io
import numpy as np
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import scipy.io as sio
import csv
import cv2

#INPUT
#data = scipy.io.loadmat('/Users/timeanemet/Desktop/CNN/matfiles/subset_data.mat')
#data = scipy.io.loadmat("/home/bence/madTables/osszesitett.mat")
#data = scipy.io.loadmat("/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett_2.mat")
#data = scipy.io.loadmat("/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/new_osszesitett_2.mat")

#OUTPUT
filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data.csv'
#filename = '/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/data.csv'

keys = data.keys()
osszesitett_data = data['new_osszesitett_2']


imagename = "0000000035"
imgname = "0000_" + imagename
# imagepath = f'/project/Datasets/KITTI_360/2013_05_28_drive_0000_sync/image_00/data_rect/{imagename}.png'
# imagesavepath = f'/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/CODES/TEST/IMAGES/LINES/cutted_here{imagename}.png'
imagesavepath = f'/Volumes/TIMKA/NEW_CNN/RGVC_DataGeneration_CODES/CODES/TEST/IMAGES/CUTTEST/'


smallImageSize = 376
BigImageWidth = 1408
BigImageHeight = 376


def newlinedata(cuttedhere, alllines, lines_3d):
    newlinesdata = []
    new3ddata = []
    neworigdata = []
    newlines3ddata = []
    newlinesorigdata = []
    newlinedata = []
    size = 0
    treshold = 15
    
    for cuts in cuttedhere:
        start = cuts[0]
        end = cuts[1]
        for i in range (len(alllines)):
            newline = [0] * 4
            line = alllines[i]
            xstart = line[0]
            xend = line[2]
            #CASE1
            if(xstart > start and xend < end):
                newline[0] = line[0] - start
                newline[2] = line[2] - start
                newline[1] = line[1]
                newline[3] = line[3]
                size = newline[2] - newline[0]
                if(size > treshold):
                    newlinedata.append(newline)
                    new3ddata.append(lines_3d[i])
                    neworigdata.append(alllines[i])
            #CASE2
            elif(xend < end and xend > start):
                newline[0] = 0
                newline[2] = line[2] - start
                newline[1] = line[1]
                newline[3] = line[3]
                size = newline[2] - newline[0]
                if(size > treshold):
                    newlinedata.append(newline)
                    new3ddata.append(lines_3d[i])
                    neworigdata.append(alllines[i])
            #CASE3
            elif(xstart < end and xstart > start):
                newline[0] = line[0] - start
                newline[2] = smallImageSize
                newline[1] = line[1]
                newline[3] = line[3]
                size = newline[2] - newline[0]
                if(size > treshold):
                    newlinedata.append(newline)
                    new3ddata.append(lines_3d[i])
                    neworigdata.append(alllines[i])
        newlinesdata.append(newlinedata)
        newlinedata = []
        newlines3ddata.append(new3ddata)
        newlinesorigdata.append(neworigdata)
        new3ddata = []
        neworigdata = []

    return newlinesdata, newlines3ddata, newlinesorigdata
                


def arrangelines(allines):
    for i in range(len(allines)):
        if(allines[i][2]<allines[i][0]):
            segedX = allines[i][0]
            allines[i][0] = allines[i][2]
            allines[i][2] = segedX

            segedY  = allines[i][1]
            allines[i][1] = allines[i][3]
            allines[i][3] = segedY
            
    return allines




def drawsmallblackimage(new2dlines, imagesavepath, size):
    index = 0
    for image in new2dlines:
        index = index+1
        img = np.zeros((size, size, 3), np.uint8)
        for line in image:
        # Define the coordinates of the line
            x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
            # Draw the line on the image
            img = cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 3)
        # Display the image
        imagesavepath2 = imagesavepath + imagename+ "_" +str(size)+ "_" + str(index) + ".png"
        cv2.imwrite(imagesavepath2, img)


def drawbigimage(lines2d, imagesavepath):
    img = np.zeros((376, 1408, 3), np.uint8)
    for line in lines2d:
        x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
            # Draw the line on the image
        img = cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 3)
    
    imagesavepath2 = imagesavepath + imagename + ".png"
    cv2.imwrite(imagesavepath2, img)




def resizeto512(lines2d):
    orig_width = 376
    orig_height = 376
    new_width = 512
    new_height = 512

    alllines_512 = []
    lines_512 = []

    for image in lines2d:
        for line in image:
            new_x1 = (line[0] / orig_width) * new_width
            new_y1 = (line[1] / orig_height) * new_height
            new_x2 = (line[2] / orig_width) * new_width
            new_y2 = (line[3] / orig_height) * new_height
            new_coordinates = [new_x1, new_y1, new_x2, new_y2]
            lines_512.append(new_coordinates)
        alllines_512.append(lines_512)
        lines_512 = []
    
    return alllines_512


def segmentstocutted(allsegment):

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

    return cuttedhere


def pushdowntosegments(pusheddown):

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
    return allsegment



def newimageids(cuttedhere, image_id_1):
    imageidlist = []

    for i in range(len(cuttedhere)):
        count = i+1
        newimageid = image_id_1 + "_"+ str(count)
        imageidlist.append(newimageid)
    
    return imageidlist





data = {}
all3dlines = []
dataarray = []
alllines =  []



for i in range(len(osszesitett_data)):
    if(i%100 == 0):
        print(len(osszesitett_data), "-------", i)
    image_id_1 = str(osszesitett_data[i][0][0])  # Convert to string
    pusheddown = [0] * BigImageWidth
    # if image_id_1 != imgname:
    #     continue
    for j in range(len(osszesitett_data[i][1])):
        lines = osszesitett_data[i][1][j].flatten().tolist()
        lines3d = osszesitett_data[i][2][j].flatten().tolist()
        alllines.append(lines)
        all3dlines.append(lines3d)

        if (lines[0] <= lines[2]):
            linestart = math.floor(lines[0])
            lineend = math.ceil(lines[2])
        else:
            linestart = math.floor(lines[2])
            lineend = math.ceil(lines[0])

        for k in range(linestart, lineend):
            pusheddown[k] = 1


    #We Have pusheddown which represents the image with 1 and 0 pushed down on the y axis

    allsegment = pushdowntosegments(pusheddown)
    cuttedhere = segmentstocutted(allsegment)
    alllines = arrangelines(alllines)
    #drawbigimage(alllines,imagesavepath)
    new2dlines, new3dlines, neworiglines = newlinedata(cuttedhere, alllines, all3dlines)
    #drawsmallblackimage(new2dlines, imagesavepath, 376)
    new512lines = resizeto512(new2dlines)
    #drawsmallblackimage(new512lines, imagesavepath, 512)

    # Save them as the small images 
    new_imageid = newimageids(cuttedhere, image_id_1)


    for i in range(len(cuttedhere)):
        data["ID"] = new_imageid[i]
        data["2D_orig"] = neworiglines[i]
        data["2D_376"] = new2dlines[i]
        data["2D_512"] = new512lines[i]
        data["3D"] = new3dlines[i]
        data["cuttedhere"] = cuttedhere[i]
        dataarray.append(data)
        data= {}

    alllines = []
    all3dlines = []

   


def write_data_to_csv(data_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID', '2D_orig', '2D_376', '2D_512',  '3D', 'cuttedhere']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)




write_data_to_csv(dataarray, filename)


    



    




            
            


        

    
    
            
        





