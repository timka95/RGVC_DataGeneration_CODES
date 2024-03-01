import numpy as np
from numba import cuda


@cuda.jit
def sobel_filter(input_image, output_image):
    x, y = cuda.grid(2)

    if x < input_image.shape[0] - 2 and y < input_image.shape[1] - 2:
        gx = (input_image[x, y] - input_image[x + 2, y] +
              2 * input_image[x, y + 1] - 2 * input_image[x + 2, y + 1] +
              input_image[x, y + 2] - input_image[x + 2, y + 2])

        gy = (input_image[x, y] - input_image[x, y + 2] +
              2 * input_image[x + 1, y] - 2 * input_image[x + 1, y + 2] +
              input_image[x + 2, y] - input_image[x + 2, y + 2])

        output_image[x + 1, y + 1] = np.sqrt(gx ** 2 + gy ** 2)


# Load an example image (replace with your image)
image = np.array([[1, 2, 1],
                  [0, 0, 0],
                  [-1, -2, -1]])

# Create CUDA device array for the image
d_image = cuda.to_device(image)

# Allocate memory for the output image
output_image = np.zeros_like(image)

# Define block and grid dimensions
threadsperblock = (16, 16)
blockspergrid_x = (image.shape[0] + threadsperblock[0] - 1) // threadsperblock[0]
blockspergrid_y = (image.shape[1] + threadsperblock[1] - 1) // threadsperblock[1]
blockspergrid = (blockspergrid_x, blockspergrid_y)

# Apply Sobel filter using CUDA
sobel_filter[blockspergrid, threadsperblock](d_image, output_image)

# Copy the result back to the CPU
output_image = d_image.copy_to_host()

print("Sobel Filter Result:")
print(output_image)


