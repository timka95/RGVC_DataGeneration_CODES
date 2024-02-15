import scipy.io
import numpy as np
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import scipy.io as sio
import csv
from ast import literal_eval
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# INPUT
# file_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/Everything_2.mat'
# structname = 'Everything_2'
file_path = '/Volumes/TIMKA/NEW_CNN/matfiles/Everything_2.mat'
structname = 'Everything_2'

# OUTPUT
# savemathere = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/Baches_10ImageTest.mat'
# savecsvhere = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/Baches_.csv'
savemathere = '/Volumes/TIMKA/NEW_CNN/matfiles/Baches_10ImageTest.mat'
savecsvhere = '/Volumes/TIMKA/NEW_CNN/matfiles/Baches.csv'
index = 0

imagesavepath = f'/Volumes/TIMKA/NEW_CNN/Images/Matrixes/'
txtsavepath = f'/Volumes/TIMKA/NEW_CNN/Images/Matrixes/'
# imagesavepath = f'/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Images/Matrixes/'
# txtsavepath = f'/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Images/Matrixes/'

data_load = scipy.io.loadmat(file_path)
data = data_load[structname]


##### DATA STRUCTURE ####

# 1--'data1_imageid',
# 2--'data2_imageid',
# 3--'data1_ThetaRho'
# 4--'data2_ThetaRho'
# 5--'data1_2D_orig'
# 6--'data2_2D_orig'
# 7--'data1_2D_512'
# 8--'data2_2D_512'
# 9--'data1_2D_376'
# 10--'data2_2D_376'
# 11--'data1_cutedhere'
# 12--'data2_cutedhere'
# 13--'data_3D'


def arrangedata(data):
    newdata = []

    for i in range(len(data)):
        # first [0] column, second [0] so its not in an array box like ['0000_0000002975_4']
        if (i % 1000 == 0):
            print(len(data), "--------", i)

        data1_bigname = str(data[i][0][0])
        data1_bigname = data1_bigname.split("_")[0] + "_" + data1_bigname.split("_")[1]

        data2_bigname = str(data[i][1][0])
        data2_bigname = data2_bigname.split("_")[0] + "_" + data2_bigname.split("_")[1]

        data_dict = {
            'data1_bigname': data1_bigname,
            'data2_bigname': data2_bigname,
            'data1_imageid': str(data[i][0][0]),
            'data2_imageid': str(data[i][1][0]),
            'data1_ThetaRho': data[i][2][0],
            'data2_ThetaRho': data[i][3][0],
            'data1_2D_orig': data[i][4][0],
            'data2_2D_orig': data[i][5][0],
            'data1_2D_512': data[i][6][0],
            'data2_2D_512': data[i][7][0],
            'data1_2D_376': data[i][8][0],
            'data2_2D_376': data[i][9][0],
            'data1_cutedhere': data[i][10][0],
            'data2_cutedhere': data[i][11][0],
            'data_3D': data[i][12][0]
        }

        newdata.append(data_dict)
    return newdata



def findpair(searchingfor):
    global ihave100
    for pair in data:
        if (pair["data1_imageid"] == searchingfor):
            if pair["data2_imageid"] not in nomatch:
                return pair["data2_imageid"]

        elif (pair["data2_imageid"] == searchingfor):
            if pair["data1_imageid"] not in nomatch:
                return pair["data1_imageid"]

    return False


def findallbetweenpairs(searchingfor, pairsearchfor):
    global ihave100
    for pair in data[:]:
        if (pair["data1_imageid"] == searchingfor and pair["data2_imageid"] == pairsearchfor
                or pair["data2_imageid"] == searchingfor and pair["data1_imageid"] == pairsearchfor):
            
            batcharray.append(pair)
            data.remove(pair)
        

def checksame(data1, data2, indexdata):
    [data["data1_bigname"], data["data1_imageid"], data["data1_ThetaRho"]]
    data1isin = False
    data2isin = False

    for i in range(len(indexdata)):
        check_bigname = indexdata[i][0]
        check_smallid = indexdata[i][1]
        s = indexdata[i][2]
        check_thetarho = np.array(s)

        data1_check_bigname = data1[0]
        data1_check_smallid = data1[1]
        data1s = data1[2]
        data1_check_thetarho = np.array(data1s)

        data2_check_bigname = data2[0]
        data2_check_smallid = data2[1]
        data2s = data2[2]
        data2_check_thetarho = np.array(data2s)

        if (data1_check_smallid == check_smallid and data1_check_thetarho[0] == check_thetarho[0] and
                data1_check_thetarho[1] == check_thetarho[1]):
            index1 = i
            data1isin = True
        if (data2_check_smallid == check_smallid and data2_check_thetarho[0] == check_thetarho[0] and
                data2_check_thetarho[1] == check_thetarho[1]):
            index2 = i
            data2isin = True

    if (data1isin == False and data2isin == False):
        indexdata.append(data1)
        index1 = len(indexdata) - 1
        indexdata.append(data2)
        index2 = len(indexdata) - 1

    elif (data1isin == False and data2isin == True):
        indexdata.append(data1)
        index1 = len(indexdata) - 1
    elif (data2isin == False and data1isin == True):
        indexdata.append(data2)
        index2 = len(indexdata) - 1

    return index1, index2


############# CODE STARTS ##########




data = arrangedata(data)

# The item we want to find the pairs for
searchingfor = data[0]["data1_imageid"]
# Bach array
batcharray = []
smallimagepairs = []
batchimagpairs = []
# The array that determines the next item we are looking for
havetosearch = []
nomatch = []

everybatch = []

ihave100 = 0
ihave100True = False
everypairs = []
searchnumber = 0



while len(data) > 0:
    if searchingfor not in nomatch:
        searchnumber = 0
        pairsearchfor = findpair(searchingfor)
        findallbetweenpairs(searchingfor, pairsearchfor)
        nomatch.append(searchingfor)
        nomatch.append(pairsearchfor)
        smallimagepairs = [searchingfor, pairsearchfor]
        batchimagpairs.append(smallimagepairs)
    else:
        searchnumber = searchnumber+1
        searchingfor = data[searchnumber]["data1_imageid"]


    if(len(batchimagpairs) == 10):
        everypairs.append(batchimagpairs)
        batchimagpairs = []
        nomatch = []
        searchingfor = data[0]["data1_imageid"]
        everybatch.append(batcharray)
        batcharray = []
        if (len(everybatch) == 1):
                break



print(everypairs)





indexdata = []
segedarr = []

matrix = np.full((200, 200), 0)

everymatrix = []
everyindexdata = []










for every in everybatch:

    matrix = np.full((200, 200), 0)
    indexdata = []
    everypair = []
    index1 = 0
    index2 = 1

    for data in every:
        data1 = [data["data1_bigname"], data["data1_imageid"], data["data1_ThetaRho"]]
        data2 = [data["data2_bigname"], data["data2_imageid"], data["data2_ThetaRho"]]

        everypair.append([data["data1_imageid"], data["data1_ThetaRho"], data["data2_imageid"], data["data2_ThetaRho"]])

        index1, index2 = checksame(data1, data2, indexdata)
        # indexdata.append(data1)
        # indexdata.append(data2)

        if (data["data1_bigname"] == data["data2_bigname"]):
            matrix[index1][index2] = -1
            matrix[index2][index1] = -1
        else:
            matrix[index1][index2] = 1
            matrix[index2][index1] = 1

    matrix = matrix[:, ~(matrix == 0).all(axis=0)]
    matrix = matrix[~(matrix == 0).all(axis=1)]

    #everypairs.append(everypair)
    everymatrix.append(matrix)
    everyindexdata.append(indexdata)

for i in range(len(everymatrix)):
    for j in range(len(everymatrix[i])):
        everymatrix[i][j][j] = -1
    #drawmatrix(i, everymatrix[i])
    #writepairs(i, everypairs[i], everyindexdata[i])

num = 0
final_dict = {}
dicty = {}

for index in range(len(everymatrix)):
    numstr = str(index)

    batchydicty = {}
    matlab_cell = {f'Index_{i + 1}': str(everyindexdata[index][i]) for i in range(len(everyindexdata[index]))}
    pairs_cell = {f'Index_{i + 1}': str(everypairs[index][i]) for i in range(len(everypairs[index]))}
    batchydicty["Matrix"] = everymatrix[index]
    batchydicty["datarray"] = matlab_cell
    batchydicty["pairs"] = pairs_cell
    key = "B" + numstr
    final_dict[key] = batchydicty

scipy.io.savemat(savemathere, {'batches': final_dict})





























