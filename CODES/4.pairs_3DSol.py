import pandas as pd
import numpy as np
import csv
import scipy.io
import ast


#INPUT



#data = scipy.io.loadmat('/home/bence/madTables/osszesitett.mat')
data = scipy.io.loadmat('/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/new_osszesitett.mat')

#data = scipy.io.loadmat('/Volumes/TIMKA/NEW_CNN/matfiles/new_osszesitett_2.mat')
#data = scipy.io.loadmat('/Volumes/TIMKA/NEW_CNN/matfiles/osszesitett.mat')

#OUTPUT
filename = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/osszesitett_3D_2.csv'
#filename = '/Volumes/TIMKA/NEW_CNN/matfiles/osszesitett_3D.csv'

#Name of the struct in the matfile (should be the same as the matfile's name)
osszesitett_data = data['osszesitett']

array3d = []
number = 0
all3d = 0
listof3d = {}
datas = {}
listid = 0

for data in (osszesitett_data):
    number = number + 1
    if(number % 10 == 0):
        print(len(osszesitett_data), "-------",number )
    image3d = data[2]
    for elem in range(len(image3d)):

        mydata = [data[0], data[1][elem]]
        benne = False
        all3d = all3d+1
        for already in range (len(array3d)):
            check = image3d[elem][0][0]
            if(array3d[already][0][0] == check[0] and array3d[already][0][1] == check[1] and array3d[already][0][2] == check[2] and array3d[already][0][3] == check[3] and array3d[already][0][4] == check[4] and array3d[already][0][5] == check[5]):
                benne = True
                datas[already].append(mydata)
        if benne == False:
            array3d.append(image3d[elem][0])
            listof3d[listid] = []
            listof3d[listid].append(image3d[elem][0])
            datas[listid] = []
            datas[listid].append(mydata)
            listid = listid+1
            

savelist = []
savedict = {}
print(len(osszesitett_data), len(array3d))

for data in datas:
    namesarray = []
    data_2darray = []
    for image in datas[data]:
       image[1] = image[1][0][0]
       image[0] = image[0][0]
       name = image[0].tolist()
       arr2d = image[1].tolist()
       namesarray.append(name)
       data_2darray.append(arr2d)
    savedict["id_3D"] = data
    savedict["3D"] = array3d[data][0]
    savedict["image_id"] = namesarray
    savedict["2D"] = data_2darray

    savelist.append(savedict)
    savedict = {}


def write_data_to_csv(data_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id_3D', '3D','image_id' ,'2D' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)

# Replace this line with the actual name of your CSV file



write_data_to_csv(savelist, filename)

