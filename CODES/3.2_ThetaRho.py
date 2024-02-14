import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import csv
import scipy.io
import ast

#INPUT
#file_path = "/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data.csv"
file_path = "/Volumes/TIMKA/NEW_CNN/matfiles/data_smallimg.csv"
#file_path = "/Users/timeanemet/Desktop/CNN/matfiles/data.csv"

#OUTPUT
#filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/Every_data_2.csv'
#filename = '/Users/timeanemet/Desktop/CNN/matfiles/Every_data_2.csv'
filename = '/Volumes/TIMKA/NEW_CNN/matfiles/Every_data_2.csv'

image_x = 512
image_y = 512
Hough_theta = 240
Hough_rho = 728
angle = 0.75

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



def RhoCalc(line):
    point1 = (line[0],line[1])
    point2 = (line[2],line[3])

    x1, y1 = point1
    x2, y2 = point2

    #STANDART FORM

    if((x2 - x1) == 0):
        m = 180
    else:
        #m = (y2 - y1) / (x2 - x1)
        m = math.atan2(y2 - y1, x2 - x1)
    c = y1 - m * x1

    # m is the slope and c is the intersection on the y axis
    # print(f"The equation of the line is: y = {m}x + {c}")


    def calculate_intersection_and_distance(A, B, C, x0, y0):
        # Calculate the distance
        distance = abs(A * x0 + B * y0 + C) / math.sqrt(A ** 2 + B ** 2)
        
        # Calculate the intersection point
        x_int = x0 - A * (A * x0 + B * y0 + C) / (A ** 2 + B ** 2)
        y_int = y0 - B * (A * x0 + B * y0 + C) / (A ** 2 + B ** 2)
        
        return distance,  y_int


    # def calculate_intersection_and_distance(A, B, C, x0, y0):
    #     # Calculate intersection with y-axis (x=0)
    #     y_intercept = C / B if B != 0 else None

    #     # Calculate distance from point to line
    #     distance = abs(A*x0 + B*y0 - C) / math.sqrt(A**2 + B**2)

    #     return distance, y_intercept
    
    # Origin
    x0 = int(image_x/2)
    y0 = int(image_y/2)

    # To convert this to the standard form Ax + By = C,
    # you can rearrange the equation y = mx + c to get mx - y = -c. 
    # Here, A would be m, B would be -1, and C would be -c.
    A = m
    B = -1
    C = c
   
    distance, intersection = calculate_intersection_and_distance(A, B, C, x0, y0)

    distance = round(distance)

    if (intersection < image_x/2):
        rho = Hough_rho/2+distance
        rho = math.ceil(rho)
    else:
        rho = Hough_rho/2-distance
        rho = math.ceil(rho)

    return rho























    

def ThetaCalc(line):
    point1 = (line[0],line[1])
    point2 = (line[2],line[3])

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


    # res = math.atan2(y2 - y1, x2 - x1)
    # resi = math.ceil(res * 180 / math.pi)
    # print("RES:", resi)

    if((x1 > x2 and y2 > y1) or (x2 > x1 and y1 > y2)):
        theta = math.ceil((Hough_theta/2)+plus/angle)
    else:
        theta = math.ceil((Hough_theta/2)-plus/angle)

    if(a == 0):
        theta = 0

    # print("THETA: ", theta)

    return theta










############################## CODE STARTS ##############################

csvdata = read_csv(file_path)


for i in range(len(csvdata)):  
    csvdata[i] = csvdata[i][0]

for i in range(len(csvdata)):
    current = csvdata[i] 

    csvdata[i]["2D_orig"] = ast.literal_eval(current["2D_orig"])
    csvdata[i]["2D_376"]  = ast.literal_eval(current["2D_376"])
    csvdata[i]["2D_512"]  = ast.literal_eval(current["2D_512"])
    csvdata[i]["cuttedhere"]  = ast.literal_eval(current["cuttedhere"])
    csvdata[i]["3D"]  = ast.literal_eval(current["3D"])


ThetaRho_array = []
ThetaRhoSmallimg_array = []

for i in range(len(csvdata)):
    smallimage = csvdata[i]["2D_512"]
    print("-------", len(smallimage))
    
    for line in smallimage:
        theta = ThetaCalc(line)
        rho = RhoCalc(line)
        thetarho = [theta,rho]
        ThetaRho_array.append(thetarho)
        thetarho = []

    #Test
    if(rho > 728 or rho < 0):
        print(csvdata[i]["ID"], "WTF RHO")
    if(theta > 240 or theta < 0):
        print(csvdata[i]["ID"], "WTF THETA")

        
    csvdata[i]["ThetaRho"] = ThetaRho_array
    # print(csvdata[i]["ID"])
    # print(ThetaRho_array)
    ThetaRho_array = []
    
def write_data_to_csv(data_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID','ThetaRho' ,'2D_orig', '2D_376' ,'2D_512','3D', 'cuttedhere' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)   

write_data_to_csv(csvdata, filename)
    

        
    
    






    
