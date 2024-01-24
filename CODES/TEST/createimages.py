from PIL import Image, ImageDraw
import os
import csv
import ast



#INPUT
# file_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/Every_data_2.csv'
# images_path = 'project/Datasets/KITTI_360/2013_05_28_drive_0000_sync/image_00/data_rect'
# newimages376_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/NewCutted_376'
# newimages512_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/NewCutted_512'
# newimagesGT_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/NewCutted_GT'

file_path = '/Volumes/TIMKA/NEW_CNN/matfiles/Every_data_2.csv'
images_path = '/Volumes/TIMKA/NEW_CNN/Images/Kitti_360/orig/'
newimages376_path = '/Volumes/TIMKA/NEW_CNN/Images/NewCutting/Newcutted_376/'
newimages512_path = '/Volumes/TIMKA/NEW_CNN/Images/NewCutting/NewCutted_512/'
newimages512GT_path = '/Volumes/TIMKA/NEW_CNN/Images/NewCutting/NewCutted_GT/'





def cutimage(img_path, cuttedhere, newimagname_path, new_size):

    new_size = (new_size,new_size)
    # Open the image file
    img = Image.open(img_path)  # Replace with your image path

    x1 = cuttedhere[0]  # Replace with your first x-coordinate
    x2 = cuttedhere[1]  # Replace with your second x-coordinate
    y1 = 0
    y2 = img.height  # We want the full height of the image

    # Crop the image
    cropped_img = img.crop((x1, y1, x2, y2))
    resized_img = cropped_img.resize(new_size)


    # Save the cropped image
    resized_img.save(newimagname_path)




def find_image(folder_path, image_name):

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.startswith(image_name) and file.endswith('.png'):
                return os.path.join(root, file)
    return None





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


def drawimage(size, lines, savepath):
   
    # Initialize a black image
    image = Image.new('RGB', (size, size), 'black')
    draw = ImageDraw.Draw(image)

    # Draw the lines
    for line in lines:
        draw.line(line, fill='white')

    # Save the image
    image.save(savepath)





####################### CODE STARTS ######################

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


# GOES THROUGH EVERY SMALL IMAGE
for i in range(1):
    current = csvdata[i]
    imagename = str(current["ID"])
    splitimagename =  imagename.split("_")  # Split the string into parts
    bigImageName = splitimagename[1]
    cuttedhere = current["cuttedhere"]
    data_2D_512 = current["2D_512"]


    newimagname_path = newimages512_path+"/"+imagename+".png"

    image_path = find_image(images_path, bigImageName)
    new_size = 512
    cutimage(image_path, cuttedhere, newimagname_path,new_size)

    # GT 512
    size = 512
    newimagname_path_512GT = newimages512GT_path+"/"+imagename+".png"
    drawimage(size, data_2D_512, newimagname_path_512GT)



