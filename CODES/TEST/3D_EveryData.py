import pandas as pd
import numpy as np
import csv
import scipy.io
import ast

# INPUT
#filename = '/Volumes/TIMKA/NEW_CNN/matfiles/Every_data_2.csv'
filename = ('/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/Every_data_2.csv')

# OUTPUT
#filepath = '/Volumes/TIMKA/NEW_CNN/matfiles/3D_EveryData.csv'
filepath = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/3D_EveryData.csv'


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


csvdata = read_csv(filename)

for i in range(len(csvdata)):
    csvdata[i] = csvdata[i][0]
    csvdata[i]["ThetaRho"] = ast.literal_eval(csvdata[i]["ThetaRho"])
    csvdata[i]["2D_orig"] = ast.literal_eval(csvdata[i]["2D_orig"])
    csvdata[i]["2D_376"] = ast.literal_eval(csvdata[i]["2D_376"])
    csvdata[i]["2D_512"] = ast.literal_eval(csvdata[i]["2D_512"])
    csvdata[i]["3D"] = ast.literal_eval(csvdata[i]["3D"])
    csvdata[i]["cuttedhere"] = ast.literal_eval(csvdata[i]["cuttedhere"])

array3d = []
number = 0
all3d = 0
listof3d = {}
datas = {}
listid = 0

for data in (csvdata):
    number = number + 1
    if (number % 10 == 0):
        print(len(csvdata), "-------", number)
    image3d = data["3D"]
    for elem in range(len(image3d)):

        mydata = [data["ID"], data["2D_512"][elem], data["ThetaRho"][elem]]
        benne = False
        all3d = all3d + 1
        for already in range(len(array3d)):
            check = image3d[elem]
            if (array3d[already][0] == check[0] and array3d[already][1] == check[1] and array3d[already][2] == check[
                2] and array3d[already][3] == check[3] and array3d[already][4] == check[4] and array3d[already][5] ==
                    check[5]):
                benne = True
                datas[already].append(mydata)
        if benne == False:
            array3d.append(image3d[elem])
            listof3d[listid] = []
            listof3d[listid].append(image3d[elem])
            datas[listid] = []
            datas[listid].append(mydata)
            listid = listid + 1

savelist = []
savedict = {}
print(len(csvdata), len(array3d))

for data in datas:
    namesarray = []
    data_2darray = []
    thetarhoarr = []
    for image in datas[data]:
        name = image[0]
        arr2d = image[1]
        theta = image[2]
        namesarray.append(name)
        data_2darray.append(arr2d)
        thetarhoarr.append(theta)
    savedict["id_3D"] = data
    savedict["3D"] = array3d[data]
    savedict["ID"] = namesarray
    savedict["2D_512"] = data_2darray
    savedict["ThetaRho"] = thetarhoarr

    savelist.append(savedict)
    savedict = {}


def write_data_to_csv(data_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id_3D', '3D', 'ID', '2D_512', 'ThetaRho']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)


# Replace this line with the actual name of your CSV file


write_data_to_csv(savelist, filepath)

