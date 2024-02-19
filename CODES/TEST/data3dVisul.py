
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import csv
import scipy.io
import ast


filename = '/Volumes/TIMKA/NEW_CNN/matfiles/3D_EveryData.csv'


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

# for i in range(len(csvdata)):  
#     csvdata[i] = csvdata[i][0]

# for i in range(len(csvdata)):
#     current = csvdata[i] 

#     csvdata[i]["id_3D"] = ast.literal_eval(current["id_3D"])
#     csvdata[i]["3D"]  = ast.literal_eval(current["3D"])
#     csvdata[i]["image_id"]  = ast.literal_eval(current["image_id"])
#     csvdata[i]["2D"]  = ast.literal_eval(current["2D"])


listy = {}


for i in range(len(csvdata)):
    csvdata[i] = csvdata[i][0]
    csvdata[i]['2D_512'] =  ast.literal_eval(csvdata[i]['2D_512'])
    seen3d = len(csvdata[i]['2D_512'])
    seen3dstr = str(seen3d)
    if seen3dstr not in listy:
        listy[seen3dstr] = 1
    else:
        listy[seen3dstr] = listy[seen3dstr] + 1

# Convert keys to integers and sort the dictionary by keys
sorted_listy = {int(k): v for k, v in sorted(listy.items(), key=lambda item: int(item[0]))}

newlisty = {}

for key in sorted_listy:
    newkey = str(key)
    newlisty[newkey] = sorted_listy[key]


keys = list(newlisty.keys())
values = list(newlisty.values())

plt.bar(keys, values)

# Add labels and title
plt.xlabel('How many image sees the 3D line')
plt.ylabel('Number of 3D lines over the dataset')
plt.title('Cutted Images')

# Add values on top of the bars
for i in range(len(values)):
    plt.text(x = keys[i], y = values[i]+0.5, s = values[i], size = 10, ha = 'center')

# Show the plot
plt.show()