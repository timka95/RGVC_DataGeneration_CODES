import pandas as pd
import numpy as np
import csv
import scipy.io
import ast


# csvpathfile = "/Volumes/TIMKA/NEW_CNN/matfiles/osszesitett_3D.csv" # The last image indicates how many images are in the batch
# filename = "/Volumes/TIMKA/NEW_CNN/matfiles/osszesitett_images.csv"

csvpathfile = "/home/bence/madTables/osszesitett.mat" # The last image indicates how many images are in the batch
filename = "/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/"




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
    

def convert_string_to_list(s):
    # Split the string into a list of strings
    str_list = s.strip('[]').split()
    
    # Convert each string to a float and return the list
    return [float(num_str) for num_str in str_list]

def asty(csvdata):
    for i in range(len(csvdata)):  
        csvdata[i] = csvdata[i][0]

    for i in range(len(csvdata)):
        current = csvdata[i] 

        csvdata[i]["id_3D"] = ast.literal_eval(current["id_3D"])
        csvdata[i]['3D'] = convert_string_to_list(current['3D'])
        csvdata[i]["image_id"]  = ast.literal_eval(current["image_id"])
        csvdata[i]["2D"]  = ast.literal_eval(current["2D"])

    return csvdata



######################### CODE STARTS #########################
csvdata = read_csv(csvpathfile)
csvdata = asty(csvdata)

imagesarray = []
dataarray = []
smalldata = []
data2darray = []
data3darray = []
datanum = 0

for data in csvdata:
    for image in data["image_id"]:
        if image not in imagesarray:
            imagesarray.append(image)
            dataarray.append([data["id_3D"]])
            data2darray.append([data["2D"]])
            data3darray.append([data["3D"]])
        else:
            index = imagesarray.index(image)
            dataarray[index].append(data["id_3D"])
            data2darray[index].append(data["2D"])
            data3darray[index].append(data["3D"])

alldata = []
dicty = {}

pairs = []
newdicty = {}
number = 0
print("here")

for i in range (len(imagesarray)):
    dicty['image_id'] = imagesarray[i]
    dicty['id_3D'] = dataarray[i]
    dicty['2D'] = data2darray[i]
    dicty['3D'] = data3darray[i]
    # dicty['pairs'] = newdicty[imagesarray[i]]

    alldata.append(dicty)
    dicty = {}


print("begin")
for data in alldata:
    number = number + 1
    image = data['image_id']
    pairs = []  # Move the initialization here
    for lines3d in data['id_3D']:
        for id in csvdata:
            if id['id_3D'] == lines3d:
                for images in id['image_id']:
                    if(images not in pairs):
                        pairs.append(images)
    newdicty[data['image_id']] = pairs

for key in newdicty:
    print(newdicty[key])

alldata = []

print("begin")
for i in range (len(imagesarray)):
    dicty['image_id'] = imagesarray[i]
    dicty['id_3D'] = dataarray[i]
    dicty['2D'] = data2darray[i]
    dicty['3D'] = data3darray[i]
    dicty['pairs'] = newdicty[imagesarray[i]]

    alldata.append(dicty)
    dicty = {}



def write_data_to_csv(data_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['image_id','id_3D' ,'2D', '3D', 'pairs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)   

write_data_to_csv(alldata, filename)





            
        



