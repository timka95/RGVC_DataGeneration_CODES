import scipy.io
import numpy as np
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import scipy.io as sio
import csv

# WAGNER
# data = scipy.io.loadmat('/project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/cutted_pairs.mat')
# savemathere = 'project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/batches.mat'
# savecsvhere = 'project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/batches.csv'
# data_cutted_pairs = data['data2']

data = scipy.io.loadmat('/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data_cutted_pairs_Everything_2.mat')
data_cutted_pairs = data['Everything_2']
savemathere = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/batches.mat'
savecsvhere = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/batches.csv'




# MINE
# data = scipy.io.loadmat("/Users/timeanemet/Desktop/CNN/matfiles/cutted_pairs.mat")
# savemathere = '/Users/timeanemet/Desktop/CNN/matfiles/batches.mat'
# savecsvhere = '/Users/timeanemet/Desktop/CNN/matfiles/batches.csv'
# data_cutted_pairs = data['cutted_pairs']

# data = scipy.io.loadmat("/Volumes/ADATA_HDD/NEW_CNN/matfiles/cutted_pairs.mat")
# savemathere = '/Volumes/ADATA_HDD/NEW_CNN/matfiles/batches.mat'
# savecsvhere = '/Volumes/ADATA_HDD/NEW_CNN/matfiles/batches.csv'
# data_cutted_pairs = data['cutted_pairs']


# FOR WAGNER ITS data2 OTHERWISE cutted_pairs

allpairarray = []

for i in range(len(data_cutted_pairs)):
    if(i%1000 == 0):
        print(len(data_cutted_pairs), "---------", i)

    image_id_1 = str(data_cutted_pairs[i][0][0])  # Convert to string
    image_id_2 = str(data_cutted_pairs[i][1][0])  # Convert to string

    hough1 = (data_cutted_pairs[i][2][0])
    hough2 = (data_cutted_pairs[i][3][0])

    matchin3d = data_cutted_pairs[i][12][0]

    image_id_1_s = image_id_1.split("_")
    image_id_2_s = image_id_2.split("_")

    big_image_id_1 = image_id_1_s[1]
    small_image_id_1 = image_id_1_s[2]

    big_image_id_2 = image_id_2_s[1]
    small_image_id_2 = image_id_2_s[2]

    if (big_image_id_1 != big_image_id_2):
        allpairarray.append([big_image_id_1, big_image_id_2, image_id_1, image_id_2, hough1, hough2, matchin3d])

i = 0

db10 = []
ihave10 = 0
true10 = False
everything = []
havetosearch = []

print("start")
def findmypair(searchingfor, ihave10):
    for item in allpairarray[:]:
        # 0,1 bigname 2,3 smallname
        if (item[2] == searchingfor[2] or item[3] == searchingfor[3]):
            db10.append(item)
            havetosearch.append(item)
            allpairarray.remove(item)
            ihave10 += 1
            if (ihave10 == 100):
                return True, ihave10

    return False, ihave10


dataadded = []

searchingfor = allpairarray[0]
while len(allpairarray) > 0:
    if(len(allpairarray) % 100 == 0):
        print(len(allpairarray))
    if (true10 == True):
        dataadded.append(len(db10))
        everything.append(db10)
        ihave10 = 0
        db10 = []
        havetosearch = []
        searchingfor = allpairarray[0]
        db10.append(searchingfor)
        ihave10 = ihave10 + 1
        allpairarray.remove(searchingfor)

    if (true10 == False):
        if (len(havetosearch) == 0):
            searchingfor = allpairarray[0]
            allpairarray.remove(searchingfor)
            dataadded.append(len(db10))
            everything.append(db10)
            ihave10 = 0
            db10 = []
            db10.append(searchingfor)
            ihave10 = ihave10 + 1
            havetosearch = []
        else:
            if (ihave10 == 99):
                db10.append(havetosearch[0])
                everything.append(db10)
                ihave10 = 0
                db10 = []

                searchingfor = allpairarray[0]
                allpairarray.remove(searchingfor)
                dataadded.append(len(db10))
                db10.append(searchingfor)
                ihave10 = ihave10 + 1
                havetosearch = []




            else:
                searchingfor = havetosearch[0]
                havetosearch.remove(searchingfor)
                db10.append(searchingfor)
                ihave10 = ihave10 + 1

    true10, ihave10 = findmypair(searchingfor, ihave10)

print("hi")
batch = {}

num = 0
key = ""
final_array = []
batches_array = []
datas_array = []
dicty = {}
final_dict = {}
num2 = 0
batchydicty = {}

for everybatch in everything:
    num2 = 0
    num = num + 1
    key = "N" + str(num)
    batchydicty = {}
    for batch in everybatch:
        num2 = num2 + 1
        key2 = "B" + str(num2)
        dicty = {}  # Move the dicty definition here
        # dicty["image1"] = batch[0]
        # dicty["image2"] = batch[1]
        dicty["simage1"] = batch[2]
        dicty["simage2"] = batch[3]
        dicty["rho1"] = batch[4]
        dicty["rho2"] = batch[5]
        dicty["ThirdCol"] = batch[6]
        batchydicty[key2] = dicty

    final_dict[key] = batchydicty
print("hello")

scipy.io.savemat(savemathere, {'batches': final_dict})


def write_data_to_csv(data_array, filename, batchname):
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['simage1', 'simage2', 'rho1', 'rho2', 'ThirdCol']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for data in data_array:
            writer.writerow(data_array[data])

        # Write 'END' to the CSV file after all data has been written
        csvfile.write('\n' + batchname + '\n')


# Replace this line with the actual name of your CSV file

filename = savecsvhere

with open(filename, 'w'):
    pass

for batches in final_dict:
    write_data_to_csv(final_dict[batches], filename, batches)




