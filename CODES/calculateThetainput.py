import math

def max_distance_between_lines(width, angle_difference):
    angle_difference_rad = math.radians(angle_difference)  # convert angle to radians
    y_diff = math.tan(angle_difference_rad) * width  # calculate y difference
    return y_diff

def anglecalculatefrom_maxdiff(width, diff):
    angl = math.atan(diff / width)  # calculate y difference
    angle = math.degrees(angl)  # convert angle to radians
    return angle

# usage
width, height = 512, 512  # replace with your image size
angle_difference = 0.75  # replace with your angle difference in degrees
y_diff = max_distance_between_lines(width, angle_difference)
width = 1408
angle = anglecalculatefrom_maxdiff(width, y_diff)
print(y_diff)
print(angle)




