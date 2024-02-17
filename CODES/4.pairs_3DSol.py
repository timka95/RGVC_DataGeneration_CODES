import pandas as pd
import numpy as np
import csv
import scipy.io
import ast


#INPUT



data = scipy.io.loadmat('/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett_2.mat')
#file_path = '/Volumes/TIMKA/NEW_CNN/matfiles/Every_data_2.csv'

#OUTPUT
filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/data_cutted_pairs_Everything_2.mat'
#filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data_cutted_pairs_Everything.mat'

#Name of the struct in the matfile (should be the same as the matfile's name)
osszesitett_data = data['new_osszesitett_2']

print(len(osszesitett_data))
array3d = []


for data in range(len(osszesitett_data)):
    for i in range(len(osszesitett_data[data][2])):
        print(osszesitett_data[data][2][i])
        if(osszesitett_data[data][i] not in array3d):
            array3d.append((osszesitett_data[data][i]))

print(len(array3d))









    #     currentdata = csvdata[i]
    #     current3D = csvdata[i]["3D"]
    #
    #
    #
    #     data["ThetaRho"] = currentdata["ThetaRho"]
    #     data["2D_orig"] = currentdata["2D_orig"]
    #     data["2D_376"] = currentdata["2D_376"]
    #     data["2D_512"] = currentdata["2D_512"]
    #     data["cuttedhere"] = currentdata["cuttedhere"]
    #
    #     if(index not in dicty):
    #         dicty[index] = []
    #         dicty[index].append(data)
    #     else:
    #         dicty[index].append(data)
    #
    # for data in dicty:
    #     print(data)
