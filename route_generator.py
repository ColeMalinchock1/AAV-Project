# Intended Process:
# When the system begins it creates a loading screen for connecting to the boat and an option to disable the program
# Then when the boat is located, you are asked to select the body of water desired to route plan around
# Select a button to develop the route on the selected body of water
# Goes into autonomous mode as you are able to follow the body of water but able to disable this mode by selecting a button and use the arrow keys to move

import cv2 as cv
import numpy as np
from PIL import Image
import math

image = cv.imread("map.png")

# Resize factor
resizeFactor = 7

height, width, _ = image.shape

image = cv.resize(image, (int(width/resizeFactor), int(height/resizeFactor)))

start = [90, 300]

invalid_colors = [[223, 223, 224], [140, 190, 155], [158, 209, 173], [104, 189, 154]]

replacement_color = [0, 0, 0]

marker_color = [0, 0, 255]

look_ahead = 10

hit_end = False

vector = [-2, -5]

for y in range(len(image)):
    for x in range(len(image[y])):
        for c in invalid_colors:
            if all(image[y][x] == c):
                image[y][x] = replacement_color

image[start[0]][start[1]] = replacement_color

# while(not hit_end):


cv.imshow('Converted Image', image)

cv.waitKey(0)

cv.destroyAllWindows()