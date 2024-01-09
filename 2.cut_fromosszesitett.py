from scipy.io import savemat
import scipy.io
import numpy as np
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import scipy.io as sio
import csv

# Load the .mat file
#data = scipy.io.loadmat('/Users/timeanemet/Desktop/CNN/matfiles/subset_data.mat')
#data = scipy.io.loadmat("/home/bence/madTables/osszesitett.mat")
data = scipy.io.loadmat("/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett_2.mat")


keys = data.keys()

# Access the data structure
osszesitett_data = data['new_osszesitett_2']


data_to_save = []
imglines = []
img3dlines = []
data = {}
dataarray = []
lines_2D = []
lines_3D = []
newdataarray = []
maxcuts = 0
maximage = ""

for i in range(len(osszesitett_data)):
    print(len(osszesitett_data), "---------", i, len(osszesitett_data[i][1]))
    image_id_1 = str(osszesitett_data[i][0][0])  # Convert to string
    imglines = []

    
    for j in range(len(osszesitett_data[i][1])):
        lines = osszesitett_data[i][1][j].flatten().tolist()




        lines3d = osszesitett_data[i][2][j].flatten().tolist()


        
        lines_2D.append(lines)
        lines_3D.append(lines3d)
        

        imglines.append(lines)
        

    data["ID"] = image_id_1
    data["2D"] = lines_2D
    data["3D"] = lines_3D

    lines_2D = []
    lines_3D = []
    
    dataarray.append(data)


    data= {}
           
    lines = imglines


    # Converting the list of lists to a list of dictionaries
    lines_with_keys = [{'x1': line[0], 'y1': line[1], 'x2': line[2], 'y2': line[3]} for line in lines]

    # Make them in order
    for lines in lines_with_keys:
        if(lines["x2"] < lines["x1"]):
            seged = lines["x1"]
            lines["x1"] = lines["x2"]
            lines["x2"] = seged

            seged = lines["y1"]
            lines["y1"] = lines["y2"]
            lines["y2"] = seged


    # Sort based on 'x1' value
    lines_with_keys = sorted(lines_with_keys, key=lambda line: line['x1'])

    smallimgsize=376
    img_width = 1408
    img_height = 376

    



    for line in lines_with_keys:
        line["x1"] = math.floor(line["x1"])
        line["x2"] = math.ceil(line["x2"])

        if(line["y1"] < line["y2"]):
            line["y1"] = math.floor(line["y1"])
            line["y2"] = math.ceil(line["y2"])
        else:
            line["y2"] = math.floor(line["y2"])
            line["y1"] = math.ceil(line["y1"])



    onesarray = [0] * img_width

    for line in lines_with_keys:
        for j in range(line["x1"], line["x2"]):
            onesarray[j] = onesarray[j] + 1

    linesegarray = []
    linesegments = {}

    
    

    k = 0
    while k < len(onesarray):
        if onesarray[k] != 0:
            linesegments = {"x1": k}
            while k < len(onesarray) and onesarray[k] != 0:
                k += 1
            linesegments["x2"] = k - 1  # Subtract 1 to get the endpoint
            linesegarray.append(linesegments)
        else:
            k += 1

    cutpoints = {}
    cutpointsarray = []

    


    

    for line in linesegarray:
        segmentlength = line["x2"] - line["x1"]
        if(segmentlength < 376):
            middle = line["x1"] + math.ceil(segmentlength/2)
            cutpoints = {"start": middle - 188, "end": middle + 188}

            if(cutpoints["start"] < 0):
                cutpoints["start"] = 0
                cutpoints["end"] = 376

            if(cutpoints["end"] > 1408):
                cutpoints["end"] = 1408
                cutpoints["start"] = 1408-376
            cutpointsarray.append(cutpoints)
        else:
            cutpoints = {"start": line["x1"], "end": line["x1"]+376}
            cutpointsarray.append(cutpoints)
            cutpoints = {"start": line["x2"] - 376, "end": line["x2"]}

            if(cutpoints["start"] < 0):
                cutpoints["start"] = 0
                cutpoints["end"] = 376

            if(cutpoints["end"] > 1408):
                cutpoints["end"] = 1408
                cutpoints["start"] = 1408-376

            cutpointsarray.append(cutpoints)


    arrayseg = [0] * 2
    savearray = []

    for lines in cutpointsarray:
        
        arrayseg[0] = lines["start"]
        arrayseg[1] = lines["end"]
        savearray.append(arrayseg)
        arrayseg = [0] * 2 # Reset arrayseg for the next iteration

    

    # if(maxcuts < len(savearray)):
    #     maxcuts = len(savearray)
    #     maximage = image_id_1

    list = dataarray[i]

    
    segedarray = dataarray[i].copy()
    linesinimage_2D = []
    linesinimage_3D = []
    linesinimage_2D_original = []
    newdata = {}
    numberofimages = 1


    LINE_2D = segedarray["2D"]

    for cuts in savearray:
        
        start = cuts[0]
        end = cuts[1]
        for lines in LINE_2D[:]:
            x1 = lines[0]
            y1 = lines[1]
            x2 = lines[2]
            y2 = lines[3]

            if(x1 < end):
                x1 = x1-start
                x2 = x2-start
                newline = (x1,y1,x2,y2)
                linein3D = segedarray["3D"][segedarray["2D"].index(lines)]
                linesinimage_3D.append(linein3D)
                linesinimage_2D.append(newline)
                linesinimage_2D_original.append(lines)
                if(x2<end-start):
                    LINE_2D.remove(lines)
                    segedarray["3D"].remove(linein3D)
                
                
        if linesinimage_2D != []:
            newname = image_id_1 + "_" + str(numberofimages)
            newdata["ID"] = newname
            newdata["2D"] = np.array(linesinimage_2D)
            newdata["2D_orig"] = np.array(linesinimage_2D_original)
            newdata["3D"] = np.array(linesinimage_3D)
            newdata["cutedhere"] = np.array(cuts)
            newdataarray.append(newdata)
            newdata = {}
            linesinimage_2D = []
            linesinimage_3D = []
            linesinimage_2D_original = []
            numberofimages = numberofimages + 1



# # Initialize an empty dictionary to hold all the data
# output_data = {
#     'data2': newdataarray
# }

# scipy.io.savemat('/Users/timeanemet/Desktop/CNN/matfiles/data_pairs_cutted2.mat', output_data,  long_field_names=True)
# numberofimages = 0
# for data in newdataarray:
#     numberofimages = numberofimages+1
# print("NUMBER OF IMAGES:", numberofimages)

def write_data_to_csv(data_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID', '2D', '2D_orig', '3D', 'cutedhere']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)

# Replace this line with the actual name of your CSV file
filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data.csv'

write_data_to_csv(newdataarray, filename)

