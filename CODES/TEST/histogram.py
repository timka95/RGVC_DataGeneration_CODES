from PIL import Image
import matplotlib.pyplot as plt

def plot_histogram(image_path):
    # Open the image file
    img = Image.open(image_path).convert('L')

    # Get the image histogram
    histogram = img.histogram()

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.bar(range(256), histogram)
    plt.title('Grayscale Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.show()

def get_histogram_dict(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Get the image histogram
    histogram = img.histogram()

    # Create a dictionary: pixel value -> frequency
    histogram_dict = {i: histogram[i] for i in range(256)}

    return histogram_dict


# Usage:
plot_histogram('/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/NewCutted_512GT/0000_0000006480_6.png')
hist_dict = get_histogram_dict('/project/ntimea/l2d2/IMAGE_PAIR_GT/IMAGES/NewCutted_512GT/0000_0000006480_6.png')
print(hist_dict)
