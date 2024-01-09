import pandas as pd
import numpy as np
import csv
import scipy.io



#INPUT
# Use the function to read a csv file and print the result
file_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/Every_data_2.csv'
file_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/Every_data_2.csv'
#file_path = '/Users/timeanemet/Desktop/CNN/matfiles/Every_data_2.csv'

#OUTPUT
#filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/data_cutted_pairs_Descr.mat'
filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data_cutted_pairs_Descr.mat'
#filename = '/Volumes/ADATA_HDD/NEW_CNN/matfiles/data_cutted_pairs_2.mat'

# This function reads the csv file and stores it in the desired format
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
            if (mystring[j] == "[" or mystring[j] == "]" or mystring[j] == ","):
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





result = read_csv(file_path)

for i in range(len(result)):  
    result[i] = result[i][0]
    


for i in range(len(result)):
    current = result[i]

    result[i]["2D"] = convert_string_to_array(result[i]["2D"], 4)
    result[i]["2D_orig"] = convert_string_to_array(result[i]["2D_orig"], 4)
    result[i]["2D_512"] = convert_string_to_array(result[i]["2D_512"], 4)
    result[i]["3D"] = convert_string_to_array(result[i]["3D"],6)
    result[i]["cutedhere"] = convert_string_to_array_cutedhere(result[i]["cutedhere"])
    result[i]["ThetaRho"] = convert_string_to_array(result[i]["ThetaRho"], 2)



data_to_save = []


for i in range(len(result)):
    current = result[i]
    print(len(result), "--------", i)
    image_id_1 = str(current["ID"])
    data1_cutedhere = current["cutedhere"]

    for j in range(len(current["2D"])):
        third_col_data_1 = current["3D"][j]
        second_col_data_1 = current["2D"][j]

        data1_2D_512 = current["2D_512"][j]
        data1_ThetaRho = current["ThetaRho"][j]
        data1_2D_orig = current["2D_orig"][j]



        for k in range(len(result)):
            k_current = result[k]
            image_id_2 = str(result[k]["ID"])
            data2_cutedhere = k_current["cutedhere"]
            if image_id_1 == image_id_2:
                continue
            for l in range(len(k_current["2D_orig"])):
                third_col_data_2 = k_current["3D"][l]
                second_col_data_2 = k_current["2D"][l]

                data2_2D_512 = k_current["2D_512"][l]
                data2_ThetaRho = k_current["ThetaRho"][l]
                data2_2D_orig = k_current["2D_orig"][l]

            if np.array_equal(third_col_data_1, third_col_data_2):
                    


                    data_row = {
                        'image_id_1': image_id_1,
                        'image_id_2': image_id_2,
                        'data1_ThetaRho': data1_ThetaRho,
                        'data2_ThetaRho': data2_ThetaRho,
                    }

                    
                    



                    data_to_save.append(data_row)



# 'second_col_data_1': second_col_data_1,
# 'second_col_data_2': second_col_data_2,
# 'data1_2D_512': data1_2D_512,
# 'data2_2D_512': data2_2D_512,
# 'data1_2D_orig': data1_2D_orig,
# 'data2_2D_orig' :data2_2D_orig,
# 'data1_cutedhere' :data1_cutedhere,
# 'data2_cutedhere' :data2_cutedhere,
# 'third_col_data_2': third_col_data_2

output_data = {
    'data_cutted_pairs_Descr': data_to_save
}


scipy.io.savemat(filename, output_data,  long_field_names=True, oned_as='column')