import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import csv
import scipy.io



def read_csv(file_path):
    # Read the CSV file
    with open(file_path, 'r') as csvfile:
        # Create a CSV reader object
        csvreader = csv.reader(csvfile)
        # Get the header
        header = next(csvreader)
        # Create an empty list to store the result
        result = []
        # Iterate over each row in the csv file
        for row in csvreader:
            # Create an empty dictionary
            row_dict = {}
            # Iterate over each cell in the row and the corresponding header cell
            for cell, header_cell in zip(row, header):
                # Add the cell value to the dictionary with the header cell as the key
                row_dict[header_cell] = cell
            # Add the dictionary to the result list
            result.append([row_dict])
        # Return the result list
        return result

def convert_string_to_array(mystring, number):
    number = number-1

    # # Remove spaces between square brackets
    # mystring = mystring.replace(' ]', ']')
    # mystring = mystring.replace('] ', ']')
    # # mystring = mystring.replace(' [', '[')
    # # mystring = mystring.replace('[ ', '[')

    mystring = mystring[1:]
    mystring = mystring[:-1]
    # mystring = mystring.strip().split(" ")
    i = 0
    newstr = ""
    array = []
    smallarrays = []
    current_number = 0
    
    # print(mystring)
    while i < len(mystring):

        # if (mystring[i+1] == "]"):
        #     close = True
        
        # print(mystring[i], end = "")
        j = i
        while(j < len(mystring) and mystring[j] != ' ' ):
            if (mystring[j] == "]"):
                    # close = True
                    j = j+1
                    i = j
                    continue
            if (mystring[j] == "["or mystring[j] == "\n" or mystring[j] == ","):
                    j = j+1
                    i = j
                    continue
                
            newstr = newstr + mystring[j]
            j = j+1
            i = j

        

        

        if newstr != '':
            floaty = float(newstr)
            if current_number < number:
                smallarrays.append(floaty)
                # print(floaty)
                current_number = current_number+1
            else:
                smallarrays.append(floaty)
                array.append(smallarrays)
                smallarrays = []
                current_number = 0
                
                

        newstr = ""            
            
        i = i+1
    
    return array

def convert_string_to_array_cutedhere(mystring):
    mystring = mystring[1:]
    mystring  = mystring[:-1]
    # mystring = mystring.strip().split(" ")
    i = 0
    newstr = ""
    array = []
    smallarrays = []
    number = 0
    close = False

    while i < len(mystring):

        if (mystring[i] == "]"):
            close = True
        
        # print(mystring[i], end = "")
        j = i
        while(j < len(mystring) and mystring[j] != ' '):
            if (mystring[j] == "[" or mystring[j] == "]"):
                if (mystring[i] == "]"):
                    close = True
                j = j+1
                i = j
                continue
            newstr = newstr + mystring[j]
            j = j+1
            i = j

        

        if newstr != '':
            floaty = int(newstr)
            array.append(floaty)

        newstr = ""            
            
        i = i+1
    
    return array








# Points that describes a line

# 2 [343.029000000000,140.373000000000,581.989000000000,151.236000000000]
# [732.996000000000,214.867000000000,645.987000000000,217.565000000000]




# lines = [[353.6517446808511, 220.4936170212766, 378.19234042553194, 453.627914893617]]
# lines = lines[0]


def RhoThetaClac(lines):
    

    point1 = (lines[0],lines[1])
    point2 = (lines[2],lines[3])



    x1, y1 = point1
    x2, y2 = point2

    # Adjacent and Opposite calculated
    a = abs(x1-x2)
    o = abs(y1-y2)

    # To prevent zero division
    if(a == 0):
        angle_radians = 0
    # Calculate the angle in radians
    else:
        angle_radians = math.atan(o / a)


    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)

    # Convert float to int
    plus = math.ceil(angle_degrees)


    # determing which direction are we moving from the middle based on the position of the line 
    if((x1 > x2 and y2 > y1) or (x2 > x1 and y1 > y2)):
        theta = math.ceil(houghthetamiddle+plus/angle)
    else:
        theta = math.ceil(houghthetamiddle-plus/angle)

    if(a == 0):
        theta = 0





    ##### STANDART FORM


    if((x2 - x1) == 0):
        m = 180
    else:
        m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1

    # print(f"The equation of the line is: y = {m}x + {c}")

    b = -1
    a = m
    c = c



    def distance_to_line(x0, y0, A, B, C):
        # Calculate the distance
        distance = abs(A * x0 + B * y0 + C) / math.sqrt(A ** 2 + B ** 2)
        
        # Calculate the intersection point
        x_int = x0 - A * (A * x0 + B * y0 + C) / (A ** 2 + B ** 2)
        y_int = y0 - B * (A * x0 + B * y0 + C) / (A ** 2 + B ** 2)
        
        return distance, (x_int, y_int)

    # Example usage:
    A = a
    B = b
    C = c
    x0, y0 = middle_x, middle_y
    distance, intersection = distance_to_line(x0, y0, A, B, C)
    # print(f"Distance from ({x0}, {y0}) to the line: {distance}")
    # print(f"Intersection point: {intersection}")

    distance = round(distance)

    if (intersection[1] < middle_x):
        rho = houghrhomiddle+distance
        rho = math.ceil(rho)
    else:
        rho = houghrhomiddle-distance
        rho = math.ceil(rho)

    # print(f"({theta},{rho})")
    rhoTheta = [theta,rho]
    return rhoTheta




################################## CODE STARTS ##################################




file_path = "/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/data.csv"
#file_path = "/Users/timeanemet/Desktop/CNN/matfiles/data.csv"


result = read_csv(file_path)

for i in range(len(result)):  
    result[i] = result[i][0]    

for i in range(len(result)):
    current = result[i]
    result[i]["2D"] = convert_string_to_array(result[i]["2D"], 4)
    result[i]["2D_orig"] = convert_string_to_array(result[i]["2D_orig"], 4)
    result[i]["3D"] = convert_string_to_array(result[i]["3D"],6)
    result[i]["cutedhere"] = convert_string_to_array_cutedhere(result[i]["cutedhere"])
    










# middle_y = 64
# middle_x = 64 # The middle of the 128*128 image. Everything is calculated respect to this
# houghrhomiddle = 91 # The middle of the rho values in our case sqrt(128** + 128**) --> 182
# houghthetamiddle = 30 # The middle of the theta values in our case (180 --> 3 degree --> 60) 



#1408, 376, 1458, 512
# middle_x = 64  # The middle of the 128*128 image. Everything is calculated with respect to this
# middle_y = 64
# houghrhomiddle = 91  # The middle of the rho values in our case sqrt(128**2 + 128**2) --> 182
# houghthetamiddle = 30  # The middle of the theta values in our case (180 --> 3 degrees --> 60)
# angle = 3
    



middle_x = 256  # The middle of the 512*512 image. Everything is calculated with respect to this
middle_y = 256
houghrhomiddle = 364  # The middle of the rho values in our case sqrt(128**2 + 128**2) --> 182
houghthetamiddle = 120  # The middle of the theta values in our case (180 --> 3 degrees --> 60)
angle = 0.75


orig_width = 376
orig_height = 376
new_width = 512
new_height = 512


new_coordinates = []
new_array = []
new_dict = {}
new_coordinates_all = []
rhotheta_array = []



for i in range(len(result)):
    print(len(result), "--------------" , i)
    current = result[i]
    lines = current["2D"]
    # print(len(lines))
    for line in lines:
        rhotheta = RhoThetaClac(line)
        rhotheta_array.append(rhotheta)
        rhotheta = []

        new_x1 = (line[0] / orig_width) * new_width
        new_y1 = (line[1] / orig_height) * new_height
        new_x2 = (line[2] / orig_width) * new_width
        new_y2 = (line[3] / orig_height) * new_height

        new_coordinates = [new_x1, new_y1, new_x2, new_y2]
        new_coordinates_all.append(new_coordinates)

        

    new_dict["ID"] = current["ID"]
    new_dict["2D"] = current["2D"]
    new_dict["2D_orig"] = current["2D_orig"]
    new_dict["3D"] = current["3D"]
    new_dict["cutedhere"] = current["cutedhere"]
    new_dict["2D_512"] = new_coordinates_all
    new_dict["ThetaRho"] = rhotheta_array
    rhotheta_array = []

    new_array.append(new_dict)
    new_dict = {}

    # Clear new_coordinates_all for the next iteration
    new_coordinates_all = []



def write_data_to_csv(data_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID','ThetaRho' ,'2D', '2D_orig' ,'2D_512','3D', 'cutedhere' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)

# Replace this line with the actual name of your CSV file
#filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/Every_data_2.csv'
#filename = '/Users/timeanemet/Desktop/CNN/matfiles/Every_data_2.csv'
filename = '/Volumes/TIMKA/NEW_CNN/Data_Generation/Matfiles/Every_data_2.csv'


write_data_to_csv(new_array, filename)



