import pandas as pd
import numpy as np
import csv
import scipy.io

data_to_save = []

# Load the .mat file
#data = scipy.io.loadmat('/Users/timeanemet/Desktop/CNN/matfiles/hibaertek_fromZita.mat')
data = scipy.io.loadmat('/project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/hibaertek_fromZita.mat')


# Access the data structure
osszesitett_data = data['hibaertek_fromZita']

lines_2D = []
lines_3D = []
mistakes = []
data = {}
alldata = []
number = 0

for i in range(len(osszesitett_data)):
    print(len(osszesitett_data), "---------", i, len(osszesitett_data[i][1]))
    image_id_1 = str(osszesitett_data[i][0][0])  # Convert to string
    imglines = []
    posematrix = osszesitett_data[i][3]
    calibmatrix = osszesitett_data[i][4]

    for j in range(len(osszesitett_data[i][1])):
        lines = osszesitett_data[i][1][j].flatten().tolist()
        lines = [array[0].tolist() for array in lines]
        lines = lines[0]

        lines3d = osszesitett_data[i][2][j].flatten().tolist()
        lines3d = [array[0].tolist() for array in lines3d]
        lines3d = lines3d[0]

        mistake = osszesitett_data[i][5][j].flatten().tolist()
        mistake = [array.tolist() for array in mistake]
        num1 = mistake[0][0]
        num1 = num1[0]
        num2 = mistake[0][1]
        num2 = num2[0]
        mistake = [num1, num2]

        if (((mistake[0] + mistake[1]) / 2) <= 2):
            lines_2D.append(lines)
            lines_3D.append(lines3d)
            mistakes.append(mistake)
        # else:
        #     number = number+1
        #     print(number)
        #     print(image_id_1)
        #     print((mistake[0] + mistake[1]) /2)

    if (len(lines_2D) > 0):
        data["ID"] = image_id_1
        data["lines_2D"] = lines_2D
        data["lines_3D"] = lines_3D
        data["PoseMatrix"] = posematrix
        data["CalibMatrix"] = calibmatrix
        data["Mistake"] = mistakes
        data_to_save.append(data)

    lines_2D = []
    lines_3D = []
    mistakes = []

    data = {}


output_data = {
    'new_osszesitett': data_to_save
}

# scipy.io.savemat('/Users/timeanemet/Desktop/CNN/matfiles/new_osszesitett.mat', output_data,  long_field_names=True, oned_as='column')
scipy.io.savemat('/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett.mat', output_data, long_field_names=True,
                 oned_as='column')