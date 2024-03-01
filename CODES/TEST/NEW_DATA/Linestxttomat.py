import os
import numpy as np
from scipy.io import savemat

# Directory containing your .txt files
dir_path = '/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/data_rect/'

outpath = '/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/data_rect_GRAY/'


# Iterate over all files in the directory
for filename in os.listdir(dir_path):
    # Check if the file is a .txt file
    if filename.endswith('.txt'):
        # Construct the full .txt file path
        txt_file_path = os.path.join(dir_path, filename)

        # Read the data from the .txt file into a numpy array
        with open(txt_file_path, 'r') as f:
            data_array = np.array([list(map(float, line.split())) for line in f])

        # Remove the 'lines' prefix and '.jpeg' part from the filename
        new_filename = filename.replace('lines', '').replace('.jpeg', '')

        # Construct the .mat file path (same name as .txt file but with .mat extension)
        mat_file_path = os.path.join(outpath, os.path.splitext(new_filename)[0] + '.mat')

        # Save the numpy array to a .mat file
        savemat(mat_file_path, {'data': data_array})

