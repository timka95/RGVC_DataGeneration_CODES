



#INPUT
inputfolder = "/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/NewCutted_512"


#OUTPUT
outputfolder = "/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/NewCutted_512_GRAY"


import os
from PIL import Image

def convert_to_grayscale(input_folder, output_folder):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = Image.open(os.path.join(input_folder, filename)).convert("L")
            img.save(os.path.join(output_folder, filename))

# Usage
convert_to_grayscale(inputfolder, outputfolder)