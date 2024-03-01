import scipy.io
import numpy as np
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import scipy.io as sio
import csv
from ast import literal_eval
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import ast


#INPUT
filename = '/Volumes/TIMKA/NEW_CNN/matfiles/3D_EveryData.csv'
filename2 = '/Volumes/TIMKA/NEW_CNN/matfiles/3D_EveryDataOUTPUT.csv'

#OUTPUT
savemathere = '/Volumes/TIMKA/NEW_CNN/matfiles/Baches_3DTest.mat'

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



def arrangecsvdata(csvdata):
    for i in range(len(csvdata)):
        csvdata[i] = csvdata[i][0]
        csvdata[i]["id_3D"] = ast.literal_eval(csvdata[i]["id_3D"])
        csvdata[i]["ID"] = ast.literal_eval(csvdata[i]["ID"])
        csvdata[i]["ThetaRho"] = ast.literal_eval(csvdata[i]["ThetaRho"])
        csvdata[i]["2D_512"] = ast.literal_eval(csvdata[i]["2D_512"])
        csvdata[i]["3D"] = ast.literal_eval(csvdata[i]["3D"])


def arrangecsvdata2(csvdata):
    for i in range(len(csvdata)):
        csvdata[i] = csvdata[i][0]
        csvdata[i]["ThetaRho"] = ast.literal_eval(csvdata[i]["ThetaRho"])
        csvdata[i]["2D_512"] = ast.literal_eval(csvdata[i]["2D_512"])
        csvdata[i]["3D"] = ast.literal_eval(csvdata[i]["3D"])
        csvdata[i]["id_3D"] = ast.literal_eval(csvdata[i]["id_3D"])




def findimage(image, csvdata2):
    for data in csvdata2:
        ID = data["ID"]
        if (ID == image):
            return data


def extractdata(data):
    bachdataarr = []
    for line in range(len(data["ThetaRho"])):
        bachdataarr.append(data["ID"])
        bachdataarr.append(data["ThetaRho"][line])
        bachdataarr.append(data["id_3D"][line])
        bachdataarr.append(data["3D"][line])
        bachdataarr.append(data["2D_512"][line])
        if (data["id_3D"][line] not in check3dinbatch):
            check3dinbatch[data["id_3D"][line]] = 1
        else:
            check3dinbatch[data["id_3D"][line]] = check3dinbatch[data["id_3D"][line]] + 1
        batchdata.append(bachdataarr)
        bachdataarr = []


def biggestmach():
    max = 0
    for i in range(len(csvdata)):
        countmatch = len(csvdata[i]["ID"])

        if (countmatch > max):
            max = countmatch
            biggestid = csvdata[i]["id_3D"]
    return max, biggestid


# ID, ThetaRho, 3D, 3D_id
def creatematrix(allbatchdata):
    everymatrix = []
    for batch in allbatchdata:
        matrix = np.full((len(batch), len(batch)), 0)

        for index1, line1 in enumerate(batch):
            line1ID = line1[0].split("_")[0] + "_" + line1[0].split("_")[1]
            for index2, line2 in enumerate(batch):
                line2ID = line2[0].split("_")[0] + "_" + line2[0].split("_")[1]

                if (line1[2] == line2[2]):
                    if (line1ID == line2ID):
                        matrix[index1][index2] = -1
                        matrix[index2][index1] = -1
                    else:
                        matrix[index1][index2] = 1
                        matrix[index2][index1] = 1


        everymatrix.append(matrix)

    return everymatrix






######### CODE STARTS #########



csvdata = read_csv(filename)
csvdata2 = read_csv(filename2)
max = 0

arrangecsvdata(csvdata)
max, biggestid = biggestmach()
arrangecsvdata2(csvdata2)






print(biggestid)
print(max)

number = 0

now3d = biggestid
numberofimages = 0
imagesarray = []
bachimages = []
batchdata = []
check3dinbatch = {}
bachdatadicty = {}

allbatchdata = []

while len(csvdata) > 0:
    number = number+1
    if(number % 10 == 0):
        print(len(csvdata), "-------",number )

    for image in csvdata[biggestid]["ID"]:
        data = findimage(image, csvdata2)
        if(len(imagesarray) == 10):
            bachimages.append(imagesarray)
            imagesarray = []
            print("Len batchdata", len(batchdata))
            allbatchdata.append(batchdata)
            batchdata = []
            if(len(bachimages) == 2):
                break
        else:
            imagesarray.append(data)
            extractdata(data)
    
    csvdata.remove(csvdata[biggestid])
    if(len(check3dinbatch) > 0):
        max = 0 
        for data in check3dinbatch:
            if(check3dinbatch[data] > max):
                max = check3dinbatch[data] 
                biggestid = data
        del check3dinbatch[data]

    else:
        biggestid = biggestmach()



    if(len(bachimages) == 2):
                break


everymatrix = creatematrix(allbatchdata)
        
final_dict = {}

for index in range(len(allbatchdata)):
    numstr = str(index)

    batchydicty = {}
    matlab_cell = {f'Index_{i + 1}': str(allbatchdata[index][i]) for i in range(len(allbatchdata[index]))}
    # pairs_cell = {f'Images': str(everysmallpairs[index])}
    batchydicty["Matrix"] = everymatrix[index]
    batchydicty["datarray"] = matlab_cell
    # batchydicty["pairs"] = pairs_cell
    key = "B" + numstr
    final_dict[key] = batchydicty

scipy.io.savemat(savemathere, {'batches': final_dict})





