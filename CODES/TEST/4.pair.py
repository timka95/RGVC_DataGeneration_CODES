import pandas as pd
import numpy as np
import csv
import scipy.io
import ast


#INPUT
#file_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/Every_data_2.csv'
file_path = '/Volumes/TIMKA/NEW_CNN/matfiles/Every_data_2.csv'

#OUTPUT
#filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/data_cutted_pairs_Everything.mat'
filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data_cutted_pairs_Everything.mat'

#Name of the struct in the matfile (should be the same as the matfile's name)
structname = 'data_cutted_pairs_Everything'


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
    










######################### CODE STARTS #########################
    

csvdata = read_csv(file_path)


for i in range(len(csvdata)):  
    csvdata[i] = csvdata[i][0]

for i in range(len(csvdata)):
    current = csvdata[i] 

    csvdata[i]["ThetaRho"] = ast.literal_eval(current["ThetaRho"])
    csvdata[i]["2D_orig"] = ast.literal_eval(current["2D_orig"])
    csvdata[i]["2D_376"]  = ast.literal_eval(current["2D_376"])
    csvdata[i]["2D_512"]  = ast.literal_eval(current["2D_512"])
    csvdata[i]["cuttedhere"]  = ast.literal_eval(current["cuttedhere"])
    csvdata[i]["3D"]  = ast.literal_eval(current["3D"])

match = 0

# GOES THROUGH EVERY SMALL IMAGE
for i in range(len(csvdata)):
    current = csvdata[i]
    if(i%100 == 0):
        print(len(csvdata), "--------", i, "--------", match)
    image_id_1 = str(current["ID"])

    #GOES THROUGH EVERY LINE IN THE IMAGE
    for j in range(len(current["3D"])):
        data1_line3D = current["3D"][j]



        #Go Through every image every line to see if there is mach
        for k in range(len(csvdata)):
            mach_current = csvdata[k]
            image_id_2 = str(mach_current["ID"])

            # THEY CANNOT MACH IF THEY ARE THE SAME IMAGE
            if(image_id_1 == image_id_2):
                continue

            #Every line
            for l in range(len(mach_current["3D"])):
                data2_line3D = mach_current["3D"][l]

                if np.array_equal(data1_line3D, data2_line3D):
                    match = match + 1
                    
                    data_row = {
                            'data1_imageid': image_id_1,
                            'data2_imageid': image_id_2,
                            'data1_ThetaRho': current["ThetaRho"][j],
                            'data2_ThetaRho': mach_current["ThetaRho"][l],
                            'data1_2D_orig': current["2D_orig"][j],
                            'data2_2D_orig':  mach_current["2D_orig"][l],
                            'data1_2D_512': current["2D_512"][j],
                            'data2_2D_512':  mach_current["2D_512"][l],
                            'data1_2D_376': current["2D_376"][j],
                            'data2_2D_376' : mach_current["2D_376"][l],
                            'data1_cutedhere' : current["cuttedhere"],
                            'data2_cutedhere' : mach_current["cuttedhere"],
                            'data_3D': current["3D"][j]
                        }


